"""ROI-initialized OpenCV single-object tracker with explicit fallback."""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from physics_sensors.core import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    RuntimeFrame,
    SensorContext,
    SensorDescriptor,
    SensorStateError,
    make_sensor_event,
)


TRACKER_FALLBACK_ORDER = ("CSRT", "KCF", "MIL")


def validate_bbox(frame: Any, bbox: Sequence[float]) -> tuple[float, float, float, float]:
    if frame is None or getattr(frame, "ndim", 0) < 2:
        raise ValueError("invalid target initialization frame")
    if bbox is None or len(bbox) != 4:
        raise ValueError("bbox must be (x, y, width, height)")
    try:
        x, y, width, height = (float(value) for value in bbox)
    except (TypeError, ValueError) as exc:
        raise ValueError("bbox values must be numeric") from exc
    frame_height, frame_width = frame.shape[:2]
    if width <= 0 or height <= 0:
        raise ValueError("ROI width and height must be positive")
    if x < 0 or y < 0 or x + width > frame_width or y + height > frame_height:
        raise ValueError(f"ROI exceeds {frame_width}x{frame_height} frame: bbox=({x:g}, {y:g}, {width:g}, {height:g})")
    return x, y, width, height


def scale_bbox_to_frame(bbox: Sequence[float], template_size: Sequence[int], frame: Any) -> tuple[float, float, float, float]:
    if template_size is None or len(template_size) != 2:
        raise ValueError("template_size must be (width, height)")
    template_width, template_height = (float(value) for value in template_size)
    if template_width <= 0 or template_height <= 0:
        raise ValueError("template dimensions must be positive")
    x, y, width, height = (float(value) for value in bbox)
    frame_height, frame_width = frame.shape[:2]
    return validate_bbox(frame, (x * frame_width / template_width, y * frame_height / template_height, width * frame_width / template_width, height * frame_height / template_height))


def create_opencv_tracker(tracker_type: str):
    try:
        import cv2  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("template tracking requires the 'classical-trackers' optional dependency") from exc
    normalized = str(tracker_type).upper()
    if normalized not in TRACKER_FALLBACK_ORDER:
        raise RuntimeError(f"unsupported OpenCV tracker {tracker_type}; choose CSRT, KCF, or MIL")
    factory_name = f"Tracker{normalized}_create"
    factory = getattr(cv2, factory_name, None)
    if callable(factory):
        return factory()
    legacy = getattr(cv2, "legacy", None)
    legacy_factory = getattr(legacy, factory_name, None) if legacy is not None else None
    if callable(legacy_factory):
        return legacy_factory()
    raise RuntimeError(f"OpenCV {cv2.__version__} does not provide {normalized}; install/evaluate opencv-contrib-python-headless")


@dataclass(frozen=True)
class TemplateTrackerResult:
    ok: bool
    bbox_x: float | None = None
    bbox_y: float | None = None
    bbox_width: float | None = None
    bbox_height: float | None = None
    center_x: float | None = None
    center_y: float | None = None
    tracking_status: str = "lost"
    backend: str | None = None
    error: str = ""

    def source_projection(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "bbox_x1": self.bbox_x,
            "bbox_y1": self.bbox_y,
            "bbox_x2": None if self.bbox_x is None or self.bbox_width is None else self.bbox_x + self.bbox_width,
            "bbox_y2": None if self.bbox_y is None or self.bbox_height is None else self.bbox_y + self.bbox_height,
            "bbox_width": self.bbox_width,
            "bbox_height": self.bbox_height,
            "center_x": self.center_x,
            "center_y": self.center_y,
            "confidence": None,
            "class_name": "custom_object",
            "track_id": 1,
            "status": "tracking" if self.ok else "lost",
            "tracking_mode": "custom_object_template",
            "tracking_status": self.tracking_status,
            "error": self.error,
        }


def _lost(error: str = "", backend: str | None = None) -> TemplateTrackerResult:
    return TemplateTrackerResult(False, tracking_status="lost", backend=backend, error=error)


def _tracked(bbox: Sequence[float], backend: str | None) -> TemplateTrackerResult:
    x, y, width, height = (float(value) for value in bbox)
    return TemplateTrackerResult(True, x, y, width, height, x + width / 2.0, y + height / 2.0, "tracking", backend, "")


class TemplateTracker:
    """Source-compatible ROI tracker; this is not static template matching."""

    def __init__(self, tracker_type: str = "CSRT", tracker_factory: Callable[[str], Any] = create_opencv_tracker) -> None:
        self.requested_tracker_type = str(tracker_type).upper()
        self.tracker_factory = tracker_factory
        self.actual_tracker_type: str | None = None
        self.attempted_backends: list[str] = []
        self.tracker: Any = None
        self.initialized = False
        self.last_error = ""
        self.last_result = _lost("target has not been initialized")
        self.lost_frame_count = 0
        self.consecutive_lost_frames = 0
        self.total_frame_count = 0
        self.tracked_frame_count = 0

    def candidate_types(self) -> list[str]:
        if self.requested_tracker_type in TRACKER_FALLBACK_ORDER:
            return list(TRACKER_FALLBACK_ORDER[TRACKER_FALLBACK_ORDER.index(self.requested_tracker_type):])
        return list(TRACKER_FALLBACK_ORDER)

    @property
    def fallback_used(self) -> bool:
        return self.actual_tracker_type is not None and self.actual_tracker_type != self.requested_tracker_type

    def initialize(self, frame: Any, bbox: Sequence[float]) -> bool:
        self.reset()
        try:
            normalized = validate_bbox(frame, bbox)
        except ValueError as exc:
            self.last_error = str(exc)
            self.last_result = _lost(self.last_error)
            return False
        opencv_bbox = tuple(int(round(value)) for value in normalized)
        errors: list[str] = []
        for candidate in self.candidate_types():
            self.attempted_backends.append(candidate)
            try:
                tracker = self.tracker_factory(candidate)
                initialized = tracker.init(frame, opencv_bbox)
                if initialized is False:
                    errors.append(f"{candidate} initialization returned False")
                    continue
                self.tracker = tracker
                self.actual_tracker_type = candidate
                self.initialized = True
                self.last_result = _tracked(opencv_bbox, candidate)
                return True
            except Exception as exc:
                errors.append(f"{candidate}: {exc}")
        self.last_error = "; ".join(errors) or "no OpenCV tracker is available"
        self.last_result = _lost(self.last_error)
        return False

    def update(self, frame: Any) -> TemplateTrackerResult:
        if not self.initialized or self.tracker is None:
            return _lost(self.last_error or "target has not been initialized", self.actual_tracker_type)
        self.total_frame_count += 1
        try:
            ok, bbox = self.tracker.update(frame)
        except Exception as exc:
            ok, bbox = False, None
            self.last_error = str(exc)
        if not ok or bbox is None:
            self.lost_frame_count += 1
            self.consecutive_lost_frames += 1
            self.last_result = _lost(self.last_error, self.actual_tracker_type)
            return self.last_result
        try:
            validate_bbox(frame, bbox)
        except ValueError as exc:
            self.lost_frame_count += 1
            self.consecutive_lost_frames += 1
            self.last_error = str(exc)
            self.last_result = _lost(self.last_error, self.actual_tracker_type)
            return self.last_result
        self.tracked_frame_count += 1
        self.consecutive_lost_frames = 0
        self.last_result = _tracked(bbox, self.actual_tracker_type)
        return self.last_result

    @property
    def tracking_success_rate(self) -> float:
        if self.total_frame_count <= 0:
            return 1.0 if self.initialized else 0.0
        return self.tracked_frame_count / self.total_frame_count

    def reset(self) -> None:
        self.tracker = None
        self.actual_tracker_type = None
        self.attempted_backends = []
        self.initialized = False
        self.last_error = ""
        self.last_result = _lost("target has not been initialized")
        self.lost_frame_count = self.consecutive_lost_frames = self.total_frame_count = self.tracked_frame_count = 0


def _measurement(name: str, value: float, unit: str, role: str) -> dict[str, Any]:
    return {"name": name, "value": float(value), "value_type": "number", "unit": unit, "role": role, "uncertainty": None}


class TemplateTrackerSensor:
    SENSOR_ID = "tracker.template"
    VERSION = "0.4.0"

    def __init__(self, instance_id: str = "template-tracker-01", tracker_factory: Callable[[str], Any] = create_opencv_tracker) -> None:
        self.instance_id = instance_id
        self.tracker_factory = tracker_factory
        self.requested_backend = "CSRT"
        self.tracker = TemplateTracker(self.requested_backend, self.tracker_factory)
        self.state = LifecycleState.CREATED
        self.context: SensorContext | None = None
        self.initialization_frame_id: str | None = None
        self.template_asset_uri: str | None = None
        self._sequence = self._processed = self._lost = self._errors = 0
        self._last_latency_ms: float | None = None
        self._started_at: float | None = None

    def describe(self) -> SensorDescriptor:
        return SensorDescriptor(self.SENSOR_ID, self.VERSION, "processor", ("frame-packet.camera-frame", "frame-packet.image-frame", "initialization-roi"), ("sensor-event.tracking",), ("roi-initialized-single-object", "opencv-csrt", "opencv-kcf", "opencv-mil", "backend-fallback", "reinitialize", "lost-state"), evidence_level="replay-benchmarked")

    def configure(self, config: Mapping[str, Any]) -> ConfigResult:
        if self.state == LifecycleState.RUNNING:
            raise SensorStateError("stop the sensor before reconfiguring it")
        allowed = {"tracker_type", "template_asset_uri"}
        unknown = sorted(set(config) - allowed)
        if unknown:
            raise ValueError(f"unknown template tracker settings: {', '.join(unknown)}")
        self.requested_backend = str(config.get("tracker_type", self.requested_backend)).upper()
        self.template_asset_uri = None if config.get("template_asset_uri") is None else str(config["template_asset_uri"])
        self.tracker = TemplateTracker(self.requested_backend, self.tracker_factory)
        self.state = LifecycleState.CONFIGURED
        warnings = ("template_asset_uri is provenance metadata; the OpenCV ROI-tracker profile does not perform static template matching",) if self.template_asset_uri else ()
        return ConfigResult(True, {"tracker_type": self.requested_backend, "template_asset_uri": self.template_asset_uri}, warnings)

    async def start(self, context: SensorContext) -> None:
        self.context = context
        self.tracker.reset()
        self.initialization_frame_id = None
        self._sequence = self._processed = self._lost = self._errors = 0
        self._started_at = time.perf_counter()
        self.state = LifecycleState.RUNNING

    def initialize_target(self, frame: RuntimeFrame, roi: Sequence[float]) -> bool:
        if self.state != LifecycleState.RUNNING or self.context is None:
            raise SensorStateError("sensor must be started before target initialization")
        if frame.run_id != self.context.run_id:
            raise SensorStateError("FramePacket run_id does not match SensorContext run_id")
        initialized = self.tracker.initialize(frame.pixels, roi)
        self.initialization_frame_id = frame.frame_id
        if not initialized:
            self._errors += 1
        return initialized

    def process_frame(self, frame: RuntimeFrame) -> dict[str, Any]:
        if self.state != LifecycleState.RUNNING or self.context is None:
            raise SensorStateError("sensor must be started before processing frames")
        if frame.run_id != self.context.run_id:
            raise SensorStateError("FramePacket run_id does not match SensorContext run_id")
        started = time.perf_counter()
        result = self.tracker.update(frame.pixels)
        latency_ms = (time.perf_counter() - started) * 1000.0
        self._last_latency_ms = latency_ms
        self._processed += 1
        if not result.ok:
            self._lost += 1
        if result.error:
            self._errors += 1
        measurements: list[dict[str, Any]] = []
        if result.ok:
            assert None not in (result.bbox_x, result.bbox_y, result.bbox_width, result.bbox_height, result.center_x, result.center_y)
            measurements = [
                _measurement("center_x", result.center_x, "px", "raw"), _measurement("center_y", result.center_y, "px", "raw"),
                _measurement("bbox_x", result.bbox_x, "px", "raw"), _measurement("bbox_y", result.bbox_y, "px", "raw"),
                _measurement("bbox_width", result.bbox_width, "px", "raw"), _measurement("bbox_height", result.bbox_height, "px", "raw"),
            ]
        flags = [] if result.ok else ["target-lost"]
        if self.tracker.fallback_used:
            flags.append("tracker-backend-fallback")
        frame_quality = frame.metadata.get("quality", {})
        dropped = int(frame_quality.get("dropped_since_last", 0)) if isinstance(frame_quality, Mapping) else 0
        event = make_sensor_event(
            run_id=frame.run_id, sensor_id=self.SENSOR_ID, instance_id=self.instance_id, sensor_version=self.VERSION,
            category="processor", sequence=self._sequence, observed_at=str(frame.metadata["observed_at"]), monotonic_ns=int(frame.metadata["monotonic_ns"]), source_timestamp=frame.metadata.get("source_timestamp"),
            status="ok" if result.ok else "lost", measurements=measurements, confidence=None, latency_ms=latency_ms,
            quality_flags=flags, dropped_since_last=dropped,
            coordinate_frame={"id": f"{frame.frame_id}:image-pixel", "space": "image-pixel", "origin": "top-left", "x_direction": "right", "y_direction": "down", "unit": "px", "width": frame.width, "height": frame.height, "calibration_id": None},
            parent_event_ids=tuple(dict.fromkeys(item for item in (self.initialization_frame_id, frame.frame_id) if item)),
            payload={"profile": "opencv-roi-single-object-tracker", "requested_backend": self.requested_backend, "tracker_backend": self.tracker.actual_tracker_type, "attempted_backends": self.tracker.attempted_backends, "fallback_used": self.tracker.fallback_used, "tracking_status": result.tracking_status, "lost_frame_count": self.tracker.lost_frame_count, "consecutive_lost_frames": self.tracker.consecutive_lost_frames, "template_asset_uri": self.template_asset_uri, "source_projection": result.source_projection(), "confidence_available": False},
        )
        self._sequence += 1
        return event

    async def process(self, input_packet: RuntimeFrame):
        yield self.process_frame(input_packet)

    def health(self) -> HealthSnapshot:
        rate = None if self._started_at is None else self._processed / max(time.perf_counter() - self._started_at, 1e-9)
        return HealthSnapshot(self.state, self._processed, 0, self._lost, self._errors, rate, {"last": self._last_latency_ms} if self._last_latency_ms is not None else {})

    async def stop(self) -> None:
        if self.state == LifecycleState.STOPPED:
            return
        self.state = LifecycleState.STOPPING
        self.context = None
        self.state = LifecycleState.STOPPED
