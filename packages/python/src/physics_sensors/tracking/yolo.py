"""YOLO detection/tracking adapter with deterministic replay and explicit fallback."""

from __future__ import annotations

import importlib.metadata
import math
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any, Protocol

import numpy as np

from physics_sensors.core import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    ModelArtifact,
    RuntimeFrame,
    SensorContext,
    SensorDescriptor,
    SensorStateError,
    make_sensor_event,
)


SOURCE_COMMIT = "85740d686c67452a057540edb564d713e01ccc51"


@dataclass(frozen=True)
class ClassFilter:
    mode: str = "all"
    values: tuple[int | str, ...] = ()

    def __post_init__(self) -> None:
        if self.mode not in {"all", "ids", "names"}:
            raise ValueError("class_filter mode must be all, ids, or names")
        if self.mode == "all" and self.values:
            raise ValueError("class_filter all must not contain values")
        if self.mode != "all" and not self.values:
            raise ValueError(f"class_filter {self.mode} requires at least one value")
        if self.mode == "ids" and any(not isinstance(value, int) or isinstance(value, bool) for value in self.values):
            raise ValueError("class_filter ids values must be integers")
        if self.mode == "names" and any(not isinstance(value, str) or not value for value in self.values):
            raise ValueError("class_filter names values must be non-empty strings")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "ClassFilter":
        if value is None:
            return cls()
        raw_values = value.get("values", ())
        if not isinstance(raw_values, Sequence) or isinstance(raw_values, (str, bytes)):
            raise ValueError("class_filter values must be an array")
        mode = str(value.get("mode", "all"))
        values: tuple[int | str, ...]
        if mode == "ids":
            values = tuple(int(item) if isinstance(item, int) and not isinstance(item, bool) else item for item in raw_values)
        else:
            values = tuple(str(item) for item in raw_values)
        return cls(mode, values)

    def accepts(self, detection: "YoloDetection") -> bool:
        if self.mode == "all":
            return True
        if self.mode == "ids":
            return detection.class_id in self.values
        return detection.class_name in self.values

    def to_dict(self) -> dict[str, Any]:
        return {"mode": self.mode, "values": list(self.values)}


@dataclass(frozen=True)
class YoloDetection:
    x: float
    y: float
    width: float
    height: float
    detector_confidence: float
    class_id: int
    class_name: str
    track_id: int | None = None
    tracking_id_available: bool = False

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("detection bbox width and height must be positive")
        if not math.isfinite(self.detector_confidence) or self.detector_confidence < 0:
            raise ValueError("detector_confidence must be a non-negative finite backend score")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "YoloDetection":
        bbox = value.get("bbox", {})
        if not isinstance(bbox, Mapping):
            raise ValueError("detection bbox must be an object")
        track_value = value.get("track_id")
        return cls(
            x=float(bbox.get("x", 0)),
            y=float(bbox.get("y", 0)),
            width=float(bbox.get("width", 0)),
            height=float(bbox.get("height", 0)),
            detector_confidence=float(value.get("detector_confidence", 0)),
            class_id=int(value.get("class_id", 0)),
            class_name=str(value.get("class_name", "0")),
            track_id=None if track_value is None else int(track_value),
            tracking_id_available=bool(value.get("tracking_id_available", track_value is not None)),
        )

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2.0

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2.0

    def to_payload(self) -> dict[str, Any]:
        return {
            "track_id": self.track_id,
            "tracking_id_available": self.tracking_id_available,
            "class_id": self.class_id,
            "class_name": self.class_name,
            "bbox": {"x": self.x, "y": self.y, "width": self.width, "height": self.height},
            "center": {"x": self.center_x, "y": self.center_y},
            "detector_confidence": self.detector_confidence,
        }


@dataclass(frozen=True)
class DetectorFrameResult:
    detections: tuple[YoloDetection, ...]
    requested_backend: str
    actual_backend: str
    attempted_backends: tuple[str, ...]
    tracking_mode: str
    fallback_used: bool = False
    fallback_reason: str = ""
    warning: str = ""
    runtime_version: str | None = None
    model_artifact: ModelArtifact | None = None


class DetectorBackend(Protocol):
    def start(self) -> None: ...

    def process(
        self,
        frame_bgr: np.ndarray,
        *,
        tracking: bool,
        confidence_threshold: float,
        class_filter: ClassFilter,
    ) -> DetectorFrameResult: ...

    def stop(self) -> None: ...


class RecordedDetectorBackend:
    """Offline deterministic backend replaying declared detector outputs."""

    def __init__(self, frames: Sequence[Mapping[str, Any]], artifact: ModelArtifact | None = None) -> None:
        self._frames = tuple(dict(frame) for frame in frames)
        self._cursor = 0
        self.artifact = artifact

    def start(self) -> None:
        self._cursor = 0

    def process(
        self,
        frame_bgr: np.ndarray,
        *,
        tracking: bool,
        confidence_threshold: float,
        class_filter: ClassFilter,
    ) -> DetectorFrameResult:
        if self._cursor >= len(self._frames):
            raise RuntimeError("recorded detector fixture is exhausted")
        item = self._frames[self._cursor]
        self._cursor += 1
        detections_value = item.get("detections", ())
        if not isinstance(detections_value, Sequence):
            raise ValueError("recorded detections must be an array")
        detections = tuple(YoloDetection.from_mapping(value) for value in detections_value if isinstance(value, Mapping))
        return DetectorFrameResult(
            detections=detections,
            requested_backend=str(item.get("requested_backend", "recorded-detector")),
            actual_backend=str(item.get("actual_backend", "recorded-detector")),
            attempted_backends=tuple(str(value) for value in item.get("attempted_backends", ("recorded-detector",))),
            tracking_mode=str(item.get("tracking_mode", "recorded-tracks" if tracking else "detection-only")),
            fallback_used=bool(item.get("fallback_used", False)),
            fallback_reason=str(item.get("fallback_reason", "")),
            warning=str(item.get("warning", "")),
            runtime_version=str(item.get("runtime_version", "fixture-1.0.0")),
            model_artifact=self.artifact,
        )

    def stop(self) -> None:
        return None


class OpenCVHogDetectorBackend:
    """Source-compatible person-only HOG fallback; not equivalent to YOLO."""

    def __init__(self) -> None:
        self._hog: Any = None
        self.runtime_version: str | None = None

    def start(self) -> None:
        try:
            import cv2  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("OpenCV HOG fallback requires an OpenCV optional dependency") from exc
        self._hog = cv2.HOGDescriptor()
        self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.runtime_version = cv2.__version__

    def process(
        self,
        frame_bgr: np.ndarray,
        *,
        tracking: bool,
        confidence_threshold: float,
        class_filter: ClassFilter,
    ) -> DetectorFrameResult:
        if self._hog is None:
            self.start()
        if not class_filter.accepts(YoloDetection(0, 0, 1, 1, 0, 0, "person")):
            raw: list[YoloDetection] = []
        else:
            import cv2  # type: ignore[import-not-found]

            height, width = frame_bgr.shape[:2]
            scale = min(1.0, 720.0 / max(width, 1))
            working = cv2.resize(frame_bgr, None, fx=scale, fy=scale) if scale < 1.0 else frame_bgr
            boxes, weights = self._hog.detectMultiScale(working, winStride=(8, 8), padding=(8, 8), scale=1.05)
            raw = []
            for (x, y, box_width, box_height), weight in zip(boxes, weights):
                score = float(weight)
                if score < confidence_threshold:
                    continue
                inverse = 1.0 / scale
                x1, y1 = int(x * inverse), int(y * inverse)
                x2 = min(width - 1, int((x + box_width) * inverse))
                y2 = min(height - 1, int((y + box_height) * inverse))
                raw.append(YoloDetection(x1, y1, x2 - x1, y2 - y1, max(0.0, score), 0, "person"))
            raw.sort(key=lambda item: item.detector_confidence, reverse=True)
            kept: list[YoloDetection] = []
            for candidate in raw:
                if all(_iou(candidate, existing) < 0.45 for existing in kept):
                    kept.append(candidate)
            raw = kept
        return DetectorFrameResult(
            detections=tuple(raw),
            requested_backend="opencv-hog",
            actual_backend="opencv-hog",
            attempted_backends=("opencv-hog",),
            tracking_mode="centroid" if tracking else "detection-only",
            runtime_version=self.runtime_version,
        )

    def stop(self) -> None:
        self._hog = None


class YoloDetectorBackend:
    """Explicit local Ultralytics backend; never downloads a model automatically."""

    def __init__(
        self,
        model_artifact: ModelArtifact | None,
        *,
        tracker: str = "bytetrack.yaml",
        fallback_backend: DetectorBackend | None = None,
        yolo_factory: Callable[[str], Any] | None = None,
    ) -> None:
        self.model_artifact = model_artifact
        self.tracker = tracker
        self.fallback_backend = fallback_backend or OpenCVHogDetectorBackend()
        self.yolo_factory = yolo_factory
        self._model: Any = None
        self._runtime_version: str | None = None
        self._load_error = ""

    def start(self) -> None:
        self._model = None
        self._runtime_version = None
        self._load_error = ""
        try:
            if self.model_artifact is None:
                raise ValueError("no explicit local ModelArtifact was supplied")
            if self.model_artifact.runtime != "ultralytics":
                raise ValueError("YOLO backend requires ModelArtifact runtime='ultralytics'")
            path = self.model_artifact.verify_local_file()
            factory = self.yolo_factory
            if factory is None:
                from ultralytics import YOLO  # type: ignore[import-not-found]

                factory = YOLO
            try:
                self._runtime_version = importlib.metadata.version("ultralytics")
            except importlib.metadata.PackageNotFoundError:
                self._runtime_version = "injected-test-runtime" if self.yolo_factory else None
            self._model = factory(str(path))
        except Exception as exc:
            self._load_error = str(exc)
            self.fallback_backend.start()

    def process(
        self,
        frame_bgr: np.ndarray,
        *,
        tracking: bool,
        confidence_threshold: float,
        class_filter: ClassFilter,
    ) -> DetectorFrameResult:
        requested = "ultralytics-yolo-bytetrack" if tracking else "ultralytics-yolo-detect"
        attempts = [requested]
        if self._model is None:
            return self._fallback(frame_bgr, tracking, confidence_threshold, class_filter, attempts, self._load_error)
        classes = list(class_filter.values) if class_filter.mode == "ids" else None
        kwargs = {"source": frame_bgr, "classes": classes, "conf": confidence_threshold, "verbose": False}
        if tracking:
            try:
                results = self._model.track(**kwargs, persist=True, tracker=self.tracker)
                detections, warning = self._parse_result(results[0], use_track_ids=True)
                return DetectorFrameResult(
                    detections=tuple(detections), requested_backend=requested,
                    actual_backend="ultralytics-yolo-bytetrack", attempted_backends=tuple(attempts),
                    tracking_mode="bytetrack", warning=warning, runtime_version=self._runtime_version,
                    model_artifact=self.model_artifact,
                )
            except Exception as exc:
                track_error = f"ByteTrack failed: {exc}"
                attempts.append("ultralytics-yolo-detect")
                try:
                    results = self._model.predict(**kwargs)
                    detections, _ = self._parse_result(results[0], use_track_ids=False)
                    return DetectorFrameResult(
                        detections=tuple(detections), requested_backend=requested,
                        actual_backend="ultralytics-yolo-detect", attempted_backends=tuple(attempts),
                        tracking_mode="centroid", fallback_used=True, fallback_reason=track_error,
                        warning="ByteTrack unavailable; centroid association is used", runtime_version=self._runtime_version,
                        model_artifact=self.model_artifact,
                    )
                except Exception as detect_exc:
                    attempts.append("opencv-hog")
                    return self._fallback(frame_bgr, tracking, confidence_threshold, class_filter, attempts, f"{track_error}; YOLO detection failed: {detect_exc}")
        try:
            results = self._model.predict(**kwargs)
            detections, _ = self._parse_result(results[0], use_track_ids=False)
            return DetectorFrameResult(
                detections=tuple(detections), requested_backend=requested,
                actual_backend="ultralytics-yolo-detect", attempted_backends=tuple(attempts),
                tracking_mode="detection-only", runtime_version=self._runtime_version,
                model_artifact=self.model_artifact,
            )
        except Exception as exc:
            attempts.append("opencv-hog")
            return self._fallback(frame_bgr, tracking, confidence_threshold, class_filter, attempts, f"YOLO detection failed: {exc}")

    def _fallback(
        self,
        frame_bgr: np.ndarray,
        tracking: bool,
        confidence_threshold: float,
        class_filter: ClassFilter,
        attempts: list[str],
        reason: str,
    ) -> DetectorFrameResult:
        fallback = self.fallback_backend.process(
            frame_bgr, tracking=tracking, confidence_threshold=confidence_threshold, class_filter=class_filter
        )
        combined_attempts = tuple(dict.fromkeys((*attempts, *fallback.attempted_backends)))
        return replace(
            fallback,
            requested_backend=attempts[0],
            attempted_backends=combined_attempts,
            fallback_used=True,
            fallback_reason=reason,
            model_artifact=self.model_artifact,
        )

    def _parse_result(self, result: Any, use_track_ids: bool) -> tuple[list[YoloDetection], str]:
        names = getattr(result, "names", None) or getattr(self._model, "names", {})
        boxes = getattr(result, "boxes", None)
        if boxes is None:
            return [], ""
        detections: list[YoloDetection] = []
        substituted = False
        for index, box in enumerate(boxes):
            coordinates = _coordinates(box.xyxy[0])
            x1, y1, x2, y2 = coordinates
            class_id = int(_scalar(getattr(box, "cls", None), 0))
            class_name = _class_name(names, class_id)
            track_value = getattr(box, "id", None) if use_track_ids else None
            available = track_value is not None
            track_id = int(_scalar(track_value)) if available else None
            if use_track_ids and track_id is None:
                track_id = index + 1
                substituted = True
            detections.append(
                YoloDetection(
                    float(x1), float(y1), float(x2 - x1), float(y2 - y1),
                    min(1.0, max(0.0, _scalar(getattr(box, "conf", None)))),
                    class_id, class_name, track_id, available,
                )
            )
        warning = "ByteTrack did not return some track IDs; current-frame indices were substituted" if substituted else ""
        return detections, warning

    def stop(self) -> None:
        self._model = None
        self.fallback_backend.stop()


@dataclass
class _AssociationTrack:
    detection: YoloDetection
    missed: int = 0


class CentroidAssociator:
    """Source-compatible nearest-centroid IDs for backends without native tracking."""

    def __init__(self, max_missed: int = 12, max_distance_ratio: float = 0.18) -> None:
        self.max_missed = max_missed
        self.max_distance_ratio = max_distance_ratio
        self._tracks: dict[int, _AssociationTrack] = {}
        self._next_id = 1

    def update(self, detections: Sequence[YoloDetection], frame_shape: tuple[int, ...]) -> list[YoloDetection]:
        height, width = frame_shape[:2]
        maximum_distance = math.hypot(width, height) * self.max_distance_ratio
        unmatched_tracks = set(self._tracks)
        unmatched_detections = set(range(len(detections)))
        pairs: list[tuple[float, int, int]] = []
        for track_id, state in self._tracks.items():
            for index, detection in enumerate(detections):
                pairs.append((math.hypot(state.detection.center_x - detection.center_x, state.detection.center_y - detection.center_y), track_id, index))
        assigned: dict[int, int] = {}
        for distance, track_id, detection_index in sorted(pairs):
            if distance > maximum_distance:
                break
            if track_id not in unmatched_tracks or detection_index not in unmatched_detections:
                continue
            self._tracks[track_id].detection = detections[detection_index]
            self._tracks[track_id].missed = 0
            assigned[detection_index] = track_id
            unmatched_tracks.remove(track_id)
            unmatched_detections.remove(detection_index)
        for track_id in unmatched_tracks:
            self._tracks[track_id].missed += 1
        for detection_index in sorted(unmatched_detections):
            assigned[detection_index] = self._next_id
            self._tracks[self._next_id] = _AssociationTrack(detections[detection_index])
            self._next_id += 1
        for track_id in [key for key, state in self._tracks.items() if state.missed > self.max_missed]:
            del self._tracks[track_id]
        return [replace(detection, track_id=assigned[index], tracking_id_available=False) for index, detection in enumerate(detections)]

    def reset(self) -> None:
        self._tracks.clear()
        self._next_id = 1


class YoloTrackerSensor:
    SENSOR_ID = "tracker.yolo"
    VERSION = "0.5.0"

    def __init__(self, backend: DetectorBackend | None = None, instance_id: str = "yolo-tracker-01") -> None:
        self.backend = backend or RecordedDetectorBackend([])
        self.instance_id = instance_id
        self.state = LifecycleState.CREATED
        self.context: SensorContext | None = None
        self.confidence_threshold = 0.25
        self.tracking = True
        self.class_filter = ClassFilter()
        self.max_missed = 12
        self.max_distance_ratio = 0.18
        self.associator = CentroidAssociator(self.max_missed, self.max_distance_ratio)
        self._sequence = self._processed = self._lost = self._errors = 0
        self._started_at: float | None = None
        self._last_latency_ms: float | None = None

    def describe(self) -> SensorDescriptor:
        return SensorDescriptor(
            self.SENSOR_ID, self.VERSION, "processor",
            ("frame-packet.camera-frame", "frame-packet.image-frame"),
            ("sensor-event.detection", "sensor-event.tracking"),
            ("multi-target", "model-artifact", "recorded-backend", "ultralytics-yolo", "bytetrack", "class-filter", "opencv-hog-fallback", "centroid-association"),
            evidence_level="replay-benchmarked",
        )

    def configure(self, config: Mapping[str, Any]) -> ConfigResult:
        if self.state == LifecycleState.RUNNING:
            raise SensorStateError("stop the sensor before reconfiguring it")
        allowed = {"confidence_threshold", "tracking", "class_filter", "max_missed", "max_distance_ratio"}
        unknown = sorted(set(config) - allowed)
        if unknown:
            raise ValueError(f"unknown YOLO tracker settings: {', '.join(unknown)}")
        threshold = float(config.get("confidence_threshold", self.confidence_threshold))
        if not 0 <= threshold <= 1:
            raise ValueError("confidence_threshold must be within [0, 1]")
        max_missed = int(config.get("max_missed", self.max_missed))
        distance_ratio = float(config.get("max_distance_ratio", self.max_distance_ratio))
        if max_missed < 0 or distance_ratio <= 0:
            raise ValueError("max_missed must be non-negative and max_distance_ratio must be positive")
        class_filter_value = config.get("class_filter")
        if class_filter_value is not None and not isinstance(class_filter_value, Mapping):
            raise ValueError("class_filter must be an object")
        self.confidence_threshold = threshold
        self.tracking = bool(config.get("tracking", self.tracking))
        self.class_filter = ClassFilter.from_mapping(class_filter_value) if class_filter_value is not None else self.class_filter
        self.max_missed = max_missed
        self.max_distance_ratio = distance_ratio
        self.associator = CentroidAssociator(max_missed, distance_ratio)
        self.state = LifecycleState.CONFIGURED
        return ConfigResult(True, {
            "confidence_threshold": self.confidence_threshold,
            "tracking": self.tracking,
            "class_filter": self.class_filter.to_dict(),
            "max_missed": self.max_missed,
            "max_distance_ratio": self.max_distance_ratio,
        })

    async def start(self, context: SensorContext) -> None:
        self.context = context
        self.associator.reset()
        self.backend.start()
        self._sequence = self._processed = self._lost = self._errors = 0
        self._started_at = time.perf_counter()
        self.state = LifecycleState.RUNNING

    def process_frame(self, frame: RuntimeFrame) -> dict[str, Any]:
        if self.state != LifecycleState.RUNNING or self.context is None:
            raise SensorStateError("sensor must be started before processing frames")
        if frame.run_id != self.context.run_id:
            raise SensorStateError("FramePacket run_id does not match SensorContext run_id")
        started = time.perf_counter()
        error_payload: dict[str, Any] | None = None
        try:
            backend_result = self.backend.process(
                frame.pixels, tracking=self.tracking,
                confidence_threshold=self.confidence_threshold, class_filter=self.class_filter,
            )
            detections = [item for item in backend_result.detections if item.detector_confidence >= self.confidence_threshold and self.class_filter.accepts(item)]
            if self.tracking and (not detections or all(item.track_id is None for item in detections)):
                detections = self.associator.update(detections, frame.pixels.shape)
            status = "degraded" if detections and (backend_result.fallback_used or backend_result.warning) else ("ok" if detections else "lost")
        except Exception as exc:
            self._errors += 1
            backend_result = DetectorFrameResult((), "unknown", "error", (), "none", warning=str(exc))
            detections = []
            status = "error"
            error_payload = {
                "code": "DETECTOR_BACKEND_ERROR",
                "message": str(exc),
                "retryable": True,
                "cause": type(exc).__name__,
            }
        latency_ms = (time.perf_counter() - started) * 1000.0
        self._last_latency_ms = latency_ms
        self._processed += 1
        if not detections:
            self._lost += 1
        flags: list[str] = []
        if not detections and status != "error":
            flags.append("no-target")
        if backend_result.fallback_used:
            flags.append("detector-backend-fallback")
        if any(not item.tracking_id_available for item in detections) and self.tracking:
            flags.append("tracking-id-not-native")
        if backend_result.warning:
            flags.append("detector-warning")
        tracked_count = sum(item.track_id is not None for item in detections)
        measurements = [
            _measurement("detection_count", len(detections), "1", "raw"),
            _measurement("tracked_count", tracked_count, "1", "derived"),
        ]
        frame_quality = frame.metadata.get("quality", {})
        dropped = int(frame_quality.get("dropped_since_last", 0)) if isinstance(frame_quality, Mapping) else 0
        event = make_sensor_event(
            run_id=frame.run_id, sensor_id=self.SENSOR_ID, instance_id=self.instance_id,
            sensor_version=self.VERSION, category="processor", sequence=self._sequence,
            observed_at=str(frame.metadata["observed_at"]), monotonic_ns=int(frame.metadata["monotonic_ns"]),
            source_timestamp=frame.metadata.get("source_timestamp"), status=status,
            measurements=measurements, confidence=None, latency_ms=latency_ms,
            quality_flags=flags, dropped_since_last=dropped,
            coordinate_frame={"id": f"{frame.frame_id}:image-pixel", "space": "image-pixel", "origin": "top-left", "x_direction": "right", "y_direction": "down", "unit": "px", "width": frame.width, "height": frame.height, "calibration_id": None},
            parent_event_ids=(frame.frame_id,),
            payload={
                "detections": [item.to_payload() for item in detections],
                "detection_count": len(detections), "tracking_enabled": self.tracking,
                "tracking_mode": backend_result.tracking_mode,
                "requested_backend": backend_result.requested_backend,
                "actual_backend": backend_result.actual_backend,
                "attempted_backends": list(backend_result.attempted_backends),
                "fallback_used": backend_result.fallback_used,
                "fallback_reason": backend_result.fallback_reason,
                "warning": backend_result.warning,
                "class_filter": self.class_filter.to_dict(),
                "confidence_semantics": "per-detection detector score; not tracking confidence, uncertainty, or physical accuracy",
                "runtime_version": backend_result.runtime_version,
                "model_artifact": backend_result.model_artifact.to_dict() if backend_result.model_artifact else None,
                "source_commit": SOURCE_COMMIT,
            },
            error=error_payload,
        )
        self._sequence += 1
        return event

    async def process(self, input_packet: RuntimeFrame):
        yield self.process_frame(input_packet)

    def health(self) -> HealthSnapshot:
        rate = None if self._started_at is None else self._processed / max(time.perf_counter() - self._started_at, 1e-9)
        latency = {"last": self._last_latency_ms} if self._last_latency_ms is not None else {}
        return HealthSnapshot(self.state, self._processed, 0, self._lost, self._errors, rate, latency)

    async def stop(self) -> None:
        if self.state == LifecycleState.STOPPED:
            return
        self.state = LifecycleState.STOPPING
        self.backend.stop()
        self.context = None
        self.state = LifecycleState.STOPPED


def _scalar(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        if hasattr(value, "cpu"):
            value = value.cpu()
        if hasattr(value, "item"):
            return float(value.item())
        array = np.asarray(value).reshape(-1)
        return float(array[0]) if array.size else default
    except (TypeError, ValueError):
        return default


def _coordinates(value: Any) -> list[int]:
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    coordinates = np.asarray(value).reshape(-1)[:4]
    if coordinates.size != 4:
        raise ValueError("YOLO bbox must have four coordinates")
    return coordinates.astype(int).tolist()


def _class_name(names: Any, class_id: int) -> str:
    if isinstance(names, Mapping):
        return str(names.get(class_id, class_id))
    if isinstance(names, Sequence) and not isinstance(names, (str, bytes)) and class_id < len(names):
        return str(names[class_id])
    return str(class_id)


def _iou(a: YoloDetection, b: YoloDetection) -> float:
    x1, y1 = max(a.x, b.x), max(a.y, b.y)
    x2, y2 = min(a.x + a.width, b.x + b.width), min(a.y + a.height, b.y + b.height)
    intersection = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    union = a.width * a.height + b.width * b.height - intersection
    return intersection / union if union else 0.0


def _measurement(name: str, value: float, unit: str, role: str) -> dict[str, Any]:
    return {"name": name, "value": float(value), "value_type": "number", "unit": unit, "role": role, "uncertainty": None}
