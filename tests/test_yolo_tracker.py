from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema
import numpy as np
import pytest

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import ModelArtifact, RuntimeFrame, SensorContext
from physics_sensors.tracking import (
    CentroidAssociator,
    ClassFilter,
    RecordedDetectorBackend,
    OpenCVHogDetectorBackend,
    YoloDetection,
    YoloDetectorBackend,
    YoloTrackerSensor,
)


ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = ROOT / "tests/fixtures/yolo_tracker/source-golden.json"
GOLDEN = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
EVENT_SCHEMA = json.loads((ROOT / "contracts/schemas/sensor-event.schema.json").read_text(encoding="utf-8"))


def packet(pixels: np.ndarray, sequence: int = 0, run_id: str = "yolo-replay") -> RuntimeFrame:
    return RuntimeFrame(metadata={
        "schema_version": "1.0.0", "frame_id": f"93000000-0000-4000-8000-{sequence:012d}",
        "run_id": run_id, "source_sensor_id": "camera.capture", "sequence": sequence,
        "observed_at": f"2026-08-16T19:00:{sequence:02d}.000Z", "monotonic_ns": 11_000_000_000 + sequence,
        "source_timestamp": float(sequence),
        "media": {"kind": "camera-frame", "media_type": "application/x-raw-bgr", "width": pixels.shape[1], "height": pixels.shape[0], "color_space": "BGR", "orientation": "0", "mirrored": False},
        "artifact": {"uri": f"recorded://yolo/{sequence}", "media_type": "image/png", "sha256": "7" * 64, "bytes": int(pixels.nbytes)},
        "quality": {"dropped_since_last": 0, "flags": ["synthetic-fixture"]},
    }, pixels=pixels)


def fixture_artifact() -> ModelArtifact:
    return ModelArtifact(
        model_id="source-recorded-yolo-fixture-v1", model_family="recorded-detector-fixture",
        uri="recorded://tests/fixtures/yolo_tracker/source-golden.json",
        sha256=hashlib.sha256(GOLDEN_PATH.read_bytes()).hexdigest(),
        runtime="physics_sensors.recorded", runtime_version="1.0.0",
        class_names=("person", "sports ball"), license_state="repository-generated-mit",
    )


def test_model_artifact_requires_hash_and_refuses_remote_runtime_loading(tmp_path: Path) -> None:
    weight = tmp_path / "model.pt"
    weight.write_bytes(b"explicit-local-test-weight")
    digest = hashlib.sha256(weight.read_bytes()).hexdigest()
    artifact = ModelArtifact("test", "test-family", str(weight), digest, "ultralytics", "not-installed-test", ("person",), "test-only")
    assert artifact.verify_local_file() == weight.resolve()
    with pytest.raises(ValueError, match="remote model URIs"):
        ModelArtifact("remote", "test", "https://example.com/model.pt", "0" * 64, "ultralytics", "8", (), "pending").local_path()
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        ModelArtifact("bad", "test", str(weight), "0" * 64, "ultralytics", "8", (), "pending").verify_local_file()


def test_recorded_backend_maps_multi_target_tracking_lost_and_reappear_events() -> None:
    frames = GOLDEN["recorded_frames"][1:6]
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)

    async def run():
        sensor = YoloTrackerSensor(RecordedDetectorBackend(frames, fixture_artifact()))
        await sensor.start(SensorContext.minimal("yolo-replay"))
        events = [sensor.process_frame(packet(pixels, index)) for index in range(len(frames))]
        await sensor.stop()
        return events

    events = asyncio.run(run())
    assert [event["status"] for event in events] == ["ok", "ok", "ok", "lost", "ok"]
    assert [item["track_id"] for item in events[2]["payload"]["detections"]] == [7, 12]
    assert events[4]["payload"]["detections"][0]["track_id"] == 7
    assert events[3]["payload"]["detections"] == []
    assert events[3]["measurements"][0]["value"] == 0
    assert all(event["quality"]["confidence"] is None for event in events)
    assert events[0]["payload"]["confidence_semantics"].startswith("per-detection")
    jsonschema.Draft202012Validator(EVENT_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(events[2])


def test_recorded_adapter_preserves_all_source_detection_fields() -> None:
    frames = GOLDEN["recorded_frames"]
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)

    async def run():
        sensor = YoloTrackerSensor(RecordedDetectorBackend(frames, fixture_artifact()))
        await sensor.start(SensorContext.minimal("yolo-replay"))
        events = [sensor.process_frame(packet(pixels, index)) for index in range(len(frames))]
        await sensor.stop()
        return events

    for frame, event in zip(frames, asyncio.run(run()), strict=True):
        actual = event["payload"]["detections"]
        assert len(actual) == len(frame["detections"])
        for output, source in zip(actual, frame["detections"], strict=True):
            assert {key: output[key] for key in source} == source
            bbox = source["bbox"]
            assert output["center"] == {
                "x": bbox["x"] + bbox["width"] / 2,
                "y": bbox["y"] + bbox["height"] / 2,
            }
        jsonschema.Draft202012Validator(EVENT_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(event)


def test_source_golden_is_commit_pinned_and_records_call_arguments() -> None:
    assert GOLDEN["source"]["commit"] == "85740d686c67452a057540edb564d713e01ccc51"
    arguments = GOLDEN["source_call_arguments"]
    assert len(arguments["predict"]) == 3 and len(arguments["track"]) == 6
    assert all(call["classes"] is None and call["conf"] == 0.25 and call["verbose"] is False for call in arguments["predict"])
    assert all(
        call["persist"] is True
        and call["tracker"] == "bytetrack.yaml"
        and call["classes"] is None
        and call["conf"] == 0.25
        and call["verbose"] is False
        for call in arguments["track"]
    )


@pytest.mark.parametrize(
    ("class_filter", "expected"),
    [
        ({"mode": "all", "values": []}, ["person", "sports ball"]),
        ({"mode": "ids", "values": [1]}, ["sports ball"]),
        ({"mode": "names", "values": ["person"]}, ["person"]),
    ],
)
def test_class_filter_supports_all_ids_and_names(class_filter: dict[str, Any], expected: list[str]) -> None:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    frame = GOLDEN["recorded_frames"][3]

    async def run():
        sensor = YoloTrackerSensor(RecordedDetectorBackend([frame]))
        sensor.configure({"class_filter": class_filter})
        await sensor.start(SensorContext.minimal("yolo-replay"))
        return sensor.process_frame(packet(pixels))

    event = asyncio.run(run())
    assert [item["class_name"] for item in event["payload"]["detections"]] == expected
    assert event["payload"]["class_filter"] == class_filter


def test_centroid_associator_matches_source_track_id_lifecycle() -> None:
    associator = CentroidAssociator(max_missed=2, max_distance_ratio=0.18)
    inputs = [
        [YoloDetection(10, 20, 100, 200, 0.91, 0, "person")],
        [YoloDetection(20, 20, 100, 200, 0.90, 0, "person")],
        [YoloDetection(30, 20, 100, 200, 0.89, 0, "person"), YoloDetection(220, 100, 50, 50, 0.82, 1, "sports ball")],
        [],
        [YoloDetection(36, 20, 100, 200, 0.88, 0, "person")],
    ]
    for detections, source_case in zip(inputs, GOLDEN["source_centroid_cases"][:5], strict=True):
        actual = associator.update(detections, (260, 360, 3))
        assert [item.track_id for item in actual] == [item["track_id"] for item in source_case["tracks"]]
        assert [(item.x, item.y, item.width, item.height) for item in actual] == [
            (item["x1"], item["y1"], item["bbox_width"], item["bbox_height"]) for item in source_case["tracks"]
        ]
    associator.reset()
    reset = associator.update(inputs[0], (260, 360, 3))
    assert [item.track_id for item in reset] == [1]


def test_recorded_fallback_metadata_is_explicit() -> None:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)

    async def run():
        sensor = YoloTrackerSensor(RecordedDetectorBackend([GOLDEN["recorded_frames"][-1]]))
        await sensor.start(SensorContext.minimal("yolo-replay"))
        return sensor.process_frame(packet(pixels))

    event = asyncio.run(run())
    assert event["payload"]["requested_backend"] == "ultralytics-yolo-bytetrack"
    assert event["payload"]["actual_backend"] == "opencv-hog"
    assert event["payload"]["attempted_backends"] == ["ultralytics-yolo-bytetrack", "opencv-hog"]
    assert "detector-backend-fallback" in event["quality"]["flags"]


class FakeBox:
    def __init__(self, xyxy, confidence=0.9, class_id=0, track_id=7) -> None:
        self.xyxy = np.asarray([xyxy], dtype=float)
        self.conf = np.asarray([confidence], dtype=float)
        self.cls = np.asarray([class_id], dtype=float)
        self.id = None if track_id is None else np.asarray([track_id], dtype=float)


class FakeResult:
    names = {0: "person", 1: "sports ball"}

    def __init__(self, boxes) -> None:
        self.boxes = boxes


class FakeYolo:
    names = FakeResult.names

    def __init__(self, *, fail_track: bool = False, track_id: int | None = 7) -> None:
        self.fail_track = fail_track
        self.track_id = track_id
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def track(self, **kwargs):
        self.calls.append(("track", kwargs))
        if self.fail_track:
            raise RuntimeError("scripted ByteTrack failure")
        return [FakeResult([FakeBox((10, 20, 110, 220), track_id=self.track_id)])]

    def predict(self, **kwargs):
        self.calls.append(("predict", kwargs))
        return [FakeResult([FakeBox((12, 20, 112, 220), track_id=None)])]


def local_artifact(tmp_path: Path) -> ModelArtifact:
    weight = tmp_path / "explicit-test.pt"
    weight.write_bytes(b"not-a-real-model")
    return ModelArtifact("test-yolov8n", "YOLOv8", str(weight), hashlib.sha256(weight.read_bytes()).hexdigest(), "ultralytics", "injected-test-runtime", ("person",), "test-only-not-redistributable")


def test_yolo_backend_passes_source_compatible_bytetrack_arguments(tmp_path: Path) -> None:
    model = FakeYolo()
    backend = YoloDetectorBackend(local_artifact(tmp_path), yolo_factory=lambda path: model)
    backend.start()
    result = backend.process(np.zeros((260, 360, 3), dtype=np.uint8), tracking=True, confidence_threshold=0.25, class_filter=ClassFilter("ids", (0,)))
    assert result.actual_backend == "ultralytics-yolo-bytetrack"
    assert result.detections[0].track_id == 7
    method, kwargs = model.calls[0]
    assert method == "track"
    assert kwargs["persist"] is True and kwargs["tracker"] == "bytetrack.yaml"
    assert kwargs["classes"] == [0] and kwargs["conf"] == 0.25 and kwargs["verbose"] is False


def test_bytetrack_failure_uses_detection_plus_centroid_and_records_fallback(tmp_path: Path) -> None:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    backend = YoloDetectorBackend(local_artifact(tmp_path), yolo_factory=lambda path: FakeYolo(fail_track=True))

    async def run():
        sensor = YoloTrackerSensor(backend)
        await sensor.start(SensorContext.minimal("yolo-replay"))
        return sensor.process_frame(packet(pixels))

    event = asyncio.run(run())
    assert event["status"] == "degraded"
    assert event["payload"]["actual_backend"] == "ultralytics-yolo-detect"
    assert event["payload"]["tracking_mode"] == "centroid"
    assert event["payload"]["detections"][0]["track_id"] == 1
    assert "detector-backend-fallback" in event["quality"]["flags"]
    assert "tracking-id-not-native" in event["quality"]["flags"]


def test_missing_native_bytetrack_id_preserves_source_substitution_warning(tmp_path: Path) -> None:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    backend = YoloDetectorBackend(local_artifact(tmp_path), yolo_factory=lambda path: FakeYolo(track_id=None))

    async def run():
        sensor = YoloTrackerSensor(backend)
        await sensor.start(SensorContext.minimal("yolo-replay"))
        return sensor.process_frame(packet(pixels))

    event = asyncio.run(run())
    detection = event["payload"]["detections"][0]
    assert event["status"] == "degraded"
    assert detection["track_id"] == 1
    assert detection["tracking_id_available"] is False
    assert "tracking-id-not-native" in event["quality"]["flags"]
    assert "detector-warning" in event["quality"]["flags"]


def test_backend_exception_is_a_schema_valid_error_without_mock_detection() -> None:
    pixels = np.zeros((64, 64, 3), dtype=np.uint8)

    async def run():
        sensor = YoloTrackerSensor(RecordedDetectorBackend([]))
        await sensor.start(SensorContext.minimal("yolo-replay"))
        return sensor.process_frame(packet(pixels))

    event = asyncio.run(run())
    assert event["status"] == "error"
    assert event["payload"]["detections"] == []
    assert event["error"]["code"] == "DETECTOR_BACKEND_ERROR"
    jsonschema.Draft202012Validator(EVENT_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(event)


def test_no_model_artifact_never_downloads_and_uses_declared_fallback() -> None:
    fallback_frame = {
        "requested_backend": "opencv-hog", "actual_backend": "opencv-hog",
        "attempted_backends": ["opencv-hog"], "tracking_mode": "centroid", "detections": [],
    }
    backend = YoloDetectorBackend(None, fallback_backend=RecordedDetectorBackend([fallback_frame]))
    backend.start()
    result = backend.process(np.zeros((64, 64, 3), dtype=np.uint8), tracking=True, confidence_threshold=0.25, class_filter=ClassFilter())
    assert result.fallback_used is True
    assert result.actual_backend == "opencv-hog"
    assert "no explicit local ModelArtifact" in result.fallback_reason
    assert result.attempted_backends == ("ultralytics-yolo-bytetrack", "opencv-hog")


def test_real_opencv_hog_backend_processes_blank_frame_offline() -> None:
    backend = OpenCVHogDetectorBackend()
    backend.start()
    result = backend.process(
        np.zeros((128, 96, 3), dtype=np.uint8),
        tracking=True,
        confidence_threshold=0.25,
        class_filter=ClassFilter(),
    )
    backend.stop()
    assert result.detections == ()
    assert result.actual_backend == "opencv-hog"
    assert result.tracking_mode == "centroid"
    assert result.runtime_version


def test_camera_source_composes_directly_with_yolo_sensor() -> None:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    camera_frame = BackendFrame(pixels, 360, 260, "BGR", "image/png", observed_at="2026-08-16T19:00:00.000Z", monotonic_ns=1, quality_flags=("synthetic-fixture",))

    async def run():
        context = SensorContext.minimal("camera-to-yolo")
        camera = CameraSource(ImageSequenceCameraBackend([camera_frame]))
        sensor = YoloTrackerSensor(RecordedDetectorBackend([GOLDEN["recorded_frames"][1]], fixture_artifact()))
        await camera.start(context)
        frame = await anext(camera.read())
        await sensor.start(context)
        event = sensor.process_frame(frame)
        await sensor.stop(); await camera.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    assert event["sensor"]["id"] == "tracker.yolo"
    assert event["payload"]["detections"][0]["track_id"] == 7
