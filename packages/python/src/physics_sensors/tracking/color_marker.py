"""Experimental HSV color-marker tracker and SensorEvent adapter.

Behavior is anchored to:
WUHAO19831214/audio-visual-soundfield-tracker-stable
commit 85740d686c67452a057540edb564d713e01ccc51
file src/tennis_ball_tracker.py.
"""

from __future__ import annotations

import math
import time
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

from physics_sensors.core import (
    ConfigResult,
    HealthSnapshot,
    InvalidConfigurationError,
    LifecycleState,
    RuntimeFrame,
    SensorContext,
    SensorDescriptor,
    SensorStateError,
    make_sensor_event,
)
from physics_sensors.core.errors import MissingOptionalDependencyError

try:
    import cv2
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - exercised in minimal installs
    cv2 = None
    np = None
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None


DEFAULT_HSV_LOWER = (25, 70, 70)
DEFAULT_HSV_UPPER = (75, 255, 255)


def _require_color_dependencies() -> None:
    if cv2 is None or np is None:
        raise MissingOptionalDependencyError(
            "Color marker tracking requires: pip install 'physics-software-sensors[color-marker]'"
        ) from _IMPORT_ERROR


def _hsv_triplet(values: Sequence[int | float]) -> tuple[int, int, int]:
    _require_color_dependencies()
    if len(values) != 3:
        raise InvalidConfigurationError("HSV thresholds require H, S, and V")
    return (
        int(np.clip(values[0], 0, 179)),
        int(np.clip(values[1], 0, 255)),
        int(np.clip(values[2], 0, 255)),
    )


@dataclass(frozen=True)
class ColorMarkerConfig:
    hsv_lower: tuple[int, int, int] = DEFAULT_HSV_LOWER
    hsv_upper: tuple[int, int, int] = DEFAULT_HSV_UPPER
    min_area: float = 80.0
    max_area: float = 50000.0
    min_circularity: float = 0.45
    smoothing: float = 0.35
    max_lost_frames: int = 30
    class_name: str = "tennis_ball_marker"
    track_id: int = 1
    tracking_mode: str = "tennis_ball_color"

    def __post_init__(self) -> None:
        object.__setattr__(self, "hsv_lower", _hsv_triplet(self.hsv_lower))
        object.__setattr__(self, "hsv_upper", _hsv_triplet(self.hsv_upper))
        if self.min_area < 0 or self.max_area <= self.min_area:
            raise InvalidConfigurationError("marker area thresholds are invalid")
        if not 0 <= self.min_circularity <= 1:
            raise InvalidConfigurationError("min_circularity must be within [0, 1]")
        if not 0 <= self.smoothing <= 1:
            raise InvalidConfigurationError("smoothing must be within [0, 1]")
        if self.max_lost_frames < 1:
            raise InvalidConfigurationError("max_lost_frames must be positive")
        if not self.class_name or not self.tracking_mode:
            raise InvalidConfigurationError("class_name and tracking_mode cannot be empty")

    @classmethod
    def from_mapping(
        cls,
        values: Mapping[str, Any],
        base: "ColorMarkerConfig | None" = None,
    ) -> "ColorMarkerConfig":
        allowed = set(cls.__dataclass_fields__)
        unknown = sorted(set(values) - allowed)
        if unknown:
            raise InvalidConfigurationError(f"unknown color marker settings: {', '.join(unknown)}")
        merged = asdict(base or cls())
        merged.update(values)
        for key in ("hsv_lower", "hsv_upper"):
            if key in merged:
                merged[key] = tuple(merged[key])
        return cls(**merged)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["hsv_lower"] = list(self.hsv_lower)
        value["hsv_upper"] = list(self.hsv_upper)
        return value


@dataclass(frozen=True)
class ColorMarkerResult:
    ok: bool
    bbox_x1: float | None
    bbox_y1: float | None
    bbox_x2: float | None
    bbox_y2: float | None
    bbox_width: float | None
    bbox_height: float | None
    center_x: float | None
    center_y: float | None
    confidence: float | None
    class_name: str
    track_id: int
    status: str
    tracking_status: str
    tracking_mode: str
    marker_radius: float | None
    marker_area: float | None
    marker_circularity: float | None
    lost_frame_count: int
    error: str = ""

    def to_source_dict(self) -> dict[str, Any]:
        """Return the exact public keys used by the source tracker."""
        return asdict(self)


def make_color_mask(
    frame: Any,
    hsv_lower: Sequence[int | float] = DEFAULT_HSV_LOWER,
    hsv_upper: Sequence[int | float] = DEFAULT_HSV_UPPER,
) -> Any:
    """Create the source-compatible HSV mask and morphology result."""
    _require_color_dependencies()
    if frame is None or not hasattr(frame, "ndim") or frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError("frame must be a valid three-channel BGR image")
    lower = _hsv_triplet(hsv_lower)
    upper = _hsv_triplet(hsv_upper)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if lower[0] <= upper[0]:
        mask = cv2.inRange(hsv, np.array(lower, np.uint8), np.array(upper, np.uint8))
    else:
        low_mask = cv2.inRange(
            hsv,
            np.array((0, lower[1], lower[2]), np.uint8),
            np.array(upper, np.uint8),
        )
        high_mask = cv2.inRange(
            hsv,
            np.array(lower, np.uint8),
            np.array((179, upper[1], upper[2]), np.uint8),
        )
        mask = cv2.bitwise_or(low_mask, high_mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


def find_color_candidates(mask: Any) -> list[dict[str, Any]]:
    """Extract source-compatible contour geometry."""
    _require_color_dependencies()
    if mask is None or not hasattr(mask, "ndim") or mask.ndim != 2:
        raise ValueError("mask must be a single-channel image")
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates: list[dict[str, Any]] = []
    for contour in contours:
        area = float(cv2.contourArea(contour))
        perimeter = float(cv2.arcLength(contour, True))
        circularity = float(4.0 * math.pi * area / (perimeter * perimeter)) if perimeter > 0 else 0.0
        (center_x, center_y), radius = cv2.minEnclosingCircle(contour)
        x, y, width, height = cv2.boundingRect(contour)
        candidates.append(
            {
                "center_x": float(center_x),
                "center_y": float(center_y),
                "radius": float(radius),
                "area": area,
                "circularity": circularity,
                "bbox": (float(x), float(y), float(width), float(height)),
                "contour": contour,
            }
        )
    return candidates


def choose_best_candidate(
    candidates: Iterable[Mapping[str, Any]],
    previous_center: Sequence[int | float] | None = None,
) -> Mapping[str, Any] | None:
    options = list(candidates)
    if not options:
        return None
    if previous_center is None:
        return max(
            options,
            key=lambda item: float(item.get("area", 0.0))
            * max(float(item.get("circularity", 0.0)), 0.05),
        )
    previous_x, previous_y = map(float, previous_center[:2])
    return min(
        options,
        key=lambda item: math.hypot(
            float(item.get("center_x", 0.0)) - previous_x,
            float(item.get("center_y", 0.0)) - previous_y,
        )
        / max(0.25 + float(item.get("circularity", 0.0)), 0.25),
    )


def estimate_hsv_range_from_roi(
    frame: Any,
    bbox: Sequence[int | float],
    h_margin: int = 12,
    s_margin: int = 60,
    v_margin: int = 60,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    _require_color_dependencies()
    if frame is None or not hasattr(frame, "ndim") or frame.ndim != 3:
        raise ValueError("frame must be a valid image")
    if len(bbox) != 4:
        raise ValueError("bbox must be (x, y, width, height)")
    x, y, width, height = (int(round(float(value))) for value in bbox)
    frame_height, frame_width = frame.shape[:2]
    if width <= 0 or height <= 0 or x < 0 or y < 0:
        raise ValueError("ROI coordinates and dimensions are invalid")
    if x + width > frame_width or y + height > frame_height:
        raise ValueError("ROI is outside the image")
    roi = frame[y : y + height, x : x + width]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV).reshape(-1, 3)
    useful = hsv[(hsv[:, 1] >= 35) & (hsv[:, 2] >= 35)]
    if useful.size == 0:
        useful = hsv
    center = np.median(useful, axis=0)
    lower = (
        max(0, int(round(center[0])) - int(h_margin)),
        max(0, int(round(center[1])) - int(s_margin)),
        max(0, int(round(center[2])) - int(v_margin)),
    )
    upper = (
        min(179, int(round(center[0])) + int(h_margin)),
        min(255, int(round(center[1])) + int(s_margin)),
        min(255, int(round(center[2])) + int(v_margin)),
    )
    return lower, upper


def _lost_result(config: ColorMarkerConfig, lost_frames: int, error: str = "") -> ColorMarkerResult:
    return ColorMarkerResult(
        ok=False,
        bbox_x1=None,
        bbox_y1=None,
        bbox_x2=None,
        bbox_y2=None,
        bbox_width=None,
        bbox_height=None,
        center_x=None,
        center_y=None,
        confidence=None,
        class_name=config.class_name,
        track_id=config.track_id,
        status="lost",
        tracking_status="lost",
        tracking_mode=config.tracking_mode,
        marker_radius=None,
        marker_area=None,
        marker_circularity=None,
        lost_frame_count=int(lost_frames),
        error=error,
    )


class ColorMarkerTracker:
    """UI-independent, source-compatible HSV contour tracker."""

    def __init__(self, config: ColorMarkerConfig | None = None) -> None:
        _require_color_dependencies()
        self.config = config or ColorMarkerConfig()
        self.reset()

    def reset(self) -> None:
        self.previous_center: tuple[float, float] | None = None
        self.consecutive_lost_frames = 0
        self.total_frames = 0
        self.tracked_frames = 0
        self.last_mask: Any = None
        self.last_result = _lost_result(self.config, 0)

    def update(self, frame: Any) -> ColorMarkerResult:
        self.total_frames += 1
        try:
            mask = make_color_mask(frame, self.config.hsv_lower, self.config.hsv_upper)
            self.last_mask = mask
            candidates = [
                candidate
                for candidate in find_color_candidates(mask)
                if self.config.min_area <= candidate["area"] <= self.config.max_area
                and candidate["circularity"] >= self.config.min_circularity
            ]
            candidate = choose_best_candidate(candidates, self.previous_center)
        except Exception as exc:
            self.consecutive_lost_frames += 1
            self.last_result = _lost_result(self.config, self.consecutive_lost_frames, str(exc))
            return self.last_result
        if candidate is None:
            self.consecutive_lost_frames += 1
            self.last_result = _lost_result(self.config, self.consecutive_lost_frames)
            return self.last_result

        raw_center = (float(candidate["center_x"]), float(candidate["center_y"]))
        if self.previous_center is None:
            center = raw_center
        else:
            alpha = self.config.smoothing
            center = (
                alpha * raw_center[0] + (1.0 - alpha) * self.previous_center[0],
                alpha * raw_center[1] + (1.0 - alpha) * self.previous_center[1],
            )
        self.previous_center = center
        self.consecutive_lost_frames = 0
        self.tracked_frames += 1
        radius = float(candidate["radius"])
        self.last_result = ColorMarkerResult(
            ok=True,
            bbox_x1=center[0] - radius,
            bbox_y1=center[1] - radius,
            bbox_x2=center[0] + radius,
            bbox_y2=center[1] + radius,
            bbox_width=radius * 2.0,
            bbox_height=radius * 2.0,
            center_x=center[0],
            center_y=center[1],
            confidence=float(np.clip(candidate["circularity"], 0.0, 1.0)),
            class_name=self.config.class_name,
            track_id=self.config.track_id,
            status="tracking",
            tracking_status="tracking",
            tracking_mode=self.config.tracking_mode,
            marker_radius=radius,
            marker_area=float(candidate["area"]),
            marker_circularity=float(candidate["circularity"]),
            lost_frame_count=0,
        )
        return self.last_result

    @property
    def tracking_success_rate(self) -> float:
        return self.tracked_frames / self.total_frames if self.total_frames else 0.0


def _measurement(name: str, value: float, unit: str, role: str) -> dict[str, Any]:
    return {
        "name": name,
        "value": float(value),
        "value_type": "number",
        "unit": unit,
        "role": role,
        "uncertainty": None,
    }


class ColorMarkerSensor:
    """Map source-compatible tracker results to the unified SensorEvent."""

    SENSOR_ID = "tracker.color-marker"
    VERSION = "0.2.0"

    def __init__(self, instance_id: str = "color-marker-01") -> None:
        self.instance_id = instance_id
        self.state = LifecycleState.CREATED
        self.config = ColorMarkerConfig()
        self.tracker = ColorMarkerTracker(self.config)
        self.context: SensorContext | None = None
        self._sequence = 0
        self._processed = 0
        self._lost = 0
        self._errors = 0
        self._last_latency_ms: float | None = None
        self._started_at: float | None = None

    def describe(self) -> SensorDescriptor:
        return SensorDescriptor(
            sensor_id=self.SENSOR_ID,
            version=self.VERSION,
            category="processor",
            input_kinds=("frame-packet.camera-frame", "frame-packet.image-frame"),
            output_kinds=("sensor-event.tracking",),
            capabilities=("hsv-mask", "morphology", "contour-ranking", "centroid-smoothing", "lost-state"),
            evidence_level="replay-benchmarked",
        )

    def configure(self, config: Mapping[str, Any]) -> ConfigResult:
        if self.state == LifecycleState.RUNNING:
            raise SensorStateError("stop the sensor before reconfiguring it")
        self.config = ColorMarkerConfig.from_mapping(config, self.config)
        self.tracker = ColorMarkerTracker(self.config)
        self.state = LifecycleState.CONFIGURED
        return ConfigResult(accepted=True, effective_config=self.config.to_dict())

    async def start(self, context: SensorContext) -> None:
        if self.state == LifecycleState.RUNNING:
            return
        if self.state == LifecycleState.ERROR:
            raise SensorStateError("cannot start a sensor in error state")
        self.context = context
        self.tracker.reset()
        self._sequence = 0
        self._processed = 0
        self._lost = 0
        self._errors = 0
        self._started_at = time.perf_counter()
        self.state = LifecycleState.RUNNING

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
            assert result.center_x is not None and result.center_y is not None
            assert result.bbox_width is not None and result.bbox_height is not None
            assert result.marker_radius is not None and result.marker_area is not None
            assert result.marker_circularity is not None
            measurements = [
                _measurement("center_x", result.center_x, "px", "filtered"),
                _measurement("center_y", result.center_y, "px", "filtered"),
                _measurement("bbox_width", result.bbox_width, "px", "derived"),
                _measurement("bbox_height", result.bbox_height, "px", "derived"),
                _measurement("marker_radius", result.marker_radius, "px", "raw"),
                _measurement("marker_area", result.marker_area, "px2", "raw"),
                _measurement("marker_circularity", result.marker_circularity, "1", "derived"),
            ]

        frame_quality = frame.metadata.get("quality", {})
        dropped = int(frame_quality.get("dropped_since_last", 0)) if isinstance(frame_quality, Mapping) else 0
        flags = [] if result.ok else ["target-lost"]
        if result.error:
            flags.append("input-invalid")
        event = make_sensor_event(
            run_id=frame.run_id,
            sensor_id=self.SENSOR_ID,
            instance_id=self.instance_id,
            sensor_version=self.VERSION,
            category="processor",
            sequence=self._sequence,
            observed_at=str(frame.metadata["observed_at"]),
            monotonic_ns=int(frame.metadata["monotonic_ns"]),
            source_timestamp=frame.metadata.get("source_timestamp"),
            status="ok" if result.ok else "lost",
            measurements=measurements,
            confidence=result.confidence,
            latency_ms=latency_ms,
            quality_flags=flags,
            dropped_since_last=dropped,
            coordinate_frame={
                "id": f"{frame.frame_id}:image-pixel",
                "space": "image-pixel",
                "origin": "top-left",
                "x_direction": "right",
                "y_direction": "down",
                "unit": "px",
                "width": frame.width,
                "height": frame.height,
                "calibration_id": None,
            },
            parent_event_ids=(frame.frame_id,),
            payload={
                "algorithm": "hsv-contour-marker",
                "algorithm_version": "source-85740d6",
                "config": self.config.to_dict(),
                "source_raw": result.to_source_dict(),
            },
        )
        self._sequence += 1
        return event

    async def process(self, input_packet: RuntimeFrame):
        yield self.process_frame(input_packet)

    def health(self) -> HealthSnapshot:
        rate = None
        if self._started_at is not None:
            elapsed = max(time.perf_counter() - self._started_at, 1e-9)
            rate = self._processed / elapsed
        latency = {"last": self._last_latency_ms} if self._last_latency_ms is not None else {}
        return HealthSnapshot(
            state=self.state,
            processed_count=self._processed,
            lost_count=self._lost,
            error_count=self._errors,
            actual_rate_hz=rate,
            latency_ms=latency,
        )

    async def stop(self) -> None:
        if self.state == LifecycleState.STOPPED:
            return
        self.state = LifecycleState.STOPPING
        self.context = None
        self.state = LifecycleState.STOPPED
