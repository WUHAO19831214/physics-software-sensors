"""Source-compatible red light-spot weighted centroid sensor."""

from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from physics_sensors.core import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    NormalizedRect,
    RuntimeFrame,
    SensorContext,
    SensorDescriptor,
    SensorStateError,
    make_sensor_event,
)


@dataclass(frozen=True)
class SpotCentroidConfig:
    roi: NormalizedRect = NormalizedRect(0.0, 0.0, 1.0, 1.0)
    color_channel: str = "red"
    hue_low_max: float = 18.0
    hue_high_min: float = 340.0
    saturation_min: float = 0.38
    value_min: float = 0.35
    channel_min: int = 135
    channel_green_delta_min: int = 35
    channel_blue_delta_min: int = 20
    brightness_weighting: bool = True
    minimum_candidate_pixels: int = 1
    lost_weight_threshold: float = 900.0
    overexposure_value: float = 0.98
    overexposure_fraction: float = 0.25

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], base: "SpotCentroidConfig" | None = None) -> "SpotCentroidConfig":
        current = base or cls()
        allowed = set(cls.__dataclass_fields__)
        unknown = sorted(set(value) - allowed)
        if unknown:
            raise ValueError(f"unknown spot centroid settings: {', '.join(unknown)}")
        updates = dict(value)
        if "roi" in updates:
            roi = updates["roi"]
            if not isinstance(roi, Mapping):
                raise ValueError("roi must contain normalized x, y, width, and height")
            updates["roi"] = NormalizedRect.from_mapping(dict(roi))
        config = replace(current, **updates)
        if config.color_channel != "red":
            raise ValueError("source-compatible 0.4.0 supports only color_channel='red'")
        if config.minimum_candidate_pixels < 1 or config.lost_weight_threshold < 0:
            raise ValueError("minimum_candidate_pixels must be >= 1 and lost_weight_threshold must be non-negative")
        if not (0 <= config.saturation_min <= 1 and 0 <= config.value_min <= 1):
            raise ValueError("saturation_min and value_min must be within [0, 1]")
        if not (0 <= config.overexposure_fraction <= 1 and 0 <= config.overexposure_value <= 1):
            raise ValueError("overexposure settings must be within [0, 1]")
        return config

    def to_dict(self) -> dict[str, Any]:
        data = {name: getattr(self, name) for name in self.__dataclass_fields__}
        data["roi"] = self.roi.to_dict()
        return data


@dataclass(frozen=True)
class SpotCentroidResult:
    detected: bool
    centroid_x: float | None
    centroid_y: float | None
    spot_area: float
    candidate_pixels: int
    intensity_sum: float
    peak_intensity: float | None
    bbox_x: float | None
    bbox_y: float | None
    bbox_width: float | None
    bbox_height: float | None
    radius: float | None
    overexposed_fraction: float
    roi_edge: bool
    error: str = ""

    def source_projection(self) -> dict[str, Any]:
        return {
            "locked": self.detected,
            "x": self.centroid_x,
            "y": self.centroid_y,
            "radius": self.radius,
            "weight_sum": self.intensity_sum,
        }


def _rgb_hsv(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = rgb.astype(np.float64) / 255.0
    r, g, b = values[..., 0], values[..., 1], values[..., 2]
    maximum = values.max(axis=2)
    minimum = values.min(axis=2)
    delta = maximum - minimum
    hue = np.zeros_like(maximum)
    nonzero = delta != 0
    red = nonzero & (maximum == r)
    green = nonzero & (maximum == g)
    blue = nonzero & (maximum == b)
    hue[red] = 60.0 * np.mod((g[red] - b[red]) / delta[red], 6.0)
    hue[green] = 60.0 * ((b[green] - r[green]) / delta[green] + 2.0)
    hue[blue] = 60.0 * ((r[blue] - g[blue]) / delta[blue] + 4.0)
    hue[hue < 0] += 360.0
    saturation = np.divide(delta, maximum, out=np.zeros_like(delta), where=maximum != 0)
    return hue, saturation, maximum


class SpotCentroidTracker:
    """Weighted centroid matching the fixed source threshold behavior by default."""

    def __init__(self, config: SpotCentroidConfig | None = None) -> None:
        self.config = config or SpotCentroidConfig()
        self.last_mask: np.ndarray | None = None
        self.last_weights: np.ndarray | None = None

    def update(self, frame_bgr: np.ndarray) -> SpotCentroidResult:
        if frame_bgr is None or getattr(frame_bgr, "ndim", 0) != 3 or frame_bgr.shape[2] < 3:
            return SpotCentroidResult(False, None, None, 0, 0, 0, None, None, None, None, None, None, 0, False, "invalid BGR frame")
        height, width = frame_bgr.shape[:2]
        roi = self.config.roi
        x0 = int(np.floor(roi.x * width))
        y0 = int(np.floor(roi.y * height))
        x1 = int(np.ceil((roi.x + roi.width) * width))
        y1 = int(np.ceil((roi.y + roi.height) * height))
        step = 2 if width > 1000 else 1
        crop = frame_bgr[y0:y1:step, x0:x1:step, :3]
        rgb = crop[..., ::-1]
        hue, saturation, value = _rgb_hsv(rgb)
        r = rgb[..., 0].astype(np.float64)
        g = rgb[..., 1].astype(np.float64)
        b = rgb[..., 2].astype(np.float64)
        hue_red = (hue <= self.config.hue_low_max) | (hue >= self.config.hue_high_min)
        strong_red = (
            (r > self.config.channel_min)
            & (r - g > self.config.channel_green_delta_min)
            & (r - b > self.config.channel_blue_delta_min)
        )
        mask = hue_red & (saturation > self.config.saturation_min) & (value > self.config.value_min) & strong_red
        source_weights = (saturation * value * 255.0 + np.maximum(0.0, r - np.maximum(g, b))) / 2.0
        weights = np.where(mask, source_weights if self.config.brightness_weighting else 1.0, 0.0)
        self.last_mask = mask.astype(np.uint8) * 255
        self.last_weights = weights
        candidate_y, candidate_x = np.nonzero(mask)
        count = int(candidate_x.size)
        weight_sum = float(weights.sum())
        detected = count >= self.config.minimum_candidate_pixels and weight_sum > self.config.lost_weight_threshold
        if count == 0:
            return SpotCentroidResult(False, None, None, 0.0, 0, weight_sum, None, None, None, None, None, None, 0.0, False)
        global_x = x0 + candidate_x.astype(np.float64) * step
        global_y = y0 + candidate_y.astype(np.float64) * step
        candidate_weights = weights[mask]
        min_x, max_x = float(global_x.min()), float(global_x.max())
        min_y, max_y = float(global_y.min()), float(global_y.max())
        radius = max(7.0, float(np.hypot(max_x - min_x, max_y - min_y) / 2.0))
        overexposed_fraction = float(np.mean(value[mask] >= self.config.overexposure_value))
        roi_edge = bool(min_x <= x0 or min_y <= y0 or max_x >= x1 - step or max_y >= y1 - step)
        if not detected:
            return SpotCentroidResult(False, None, None, float(count * step * step), count, weight_sum, float(r[mask].max()), min_x, min_y, max_x - min_x + step, max_y - min_y + step, radius, overexposed_fraction, roi_edge)
        centroid_x = float(np.sum(global_x * candidate_weights) / weight_sum)
        centroid_y = float(np.sum(global_y * candidate_weights) / weight_sum)
        return SpotCentroidResult(True, centroid_x, centroid_y, float(count * step * step), count, weight_sum, float(r[mask].max()), min_x, min_y, max_x - min_x + step, max_y - min_y + step, radius, overexposed_fraction, roi_edge)


def _measurement(name: str, value: float, unit: str, role: str) -> dict[str, Any]:
    return {"name": name, "value": float(value), "value_type": "number", "unit": unit, "role": role, "uncertainty": None}


class SpotCentroidSensor:
    SENSOR_ID = "tracker.spot-centroid"
    VERSION = "0.4.0"

    def __init__(self, instance_id: str = "spot-centroid-01") -> None:
        self.instance_id = instance_id
        self.state = LifecycleState.CREATED
        self.config = SpotCentroidConfig()
        self.tracker = SpotCentroidTracker(self.config)
        self.context: SensorContext | None = None
        self._sequence = self._processed = self._lost = self._errors = 0
        self._last_latency_ms: float | None = None
        self._started_at: float | None = None

    def describe(self) -> SensorDescriptor:
        return SensorDescriptor(self.SENSOR_ID, self.VERSION, "processor", ("frame-packet.camera-frame", "frame-packet.image-frame"), ("sensor-event.centroid",), ("source-compatible-red-threshold", "brightness-weighted-centroid", "normalized-roi", "lost-state", "overexposure-warning"), evidence_level="replay-benchmarked")

    def configure(self, config: Mapping[str, Any]) -> ConfigResult:
        if self.state == LifecycleState.RUNNING:
            raise SensorStateError("stop the sensor before reconfiguring it")
        self.config = SpotCentroidConfig.from_mapping(config, self.config)
        self.tracker = SpotCentroidTracker(self.config)
        self.state = LifecycleState.CONFIGURED
        return ConfigResult(True, self.config.to_dict())

    async def start(self, context: SensorContext) -> None:
        self.context = context
        self._sequence = self._processed = self._lost = self._errors = 0
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
        if not result.detected:
            self._lost += 1
        if result.error:
            self._errors += 1
        measurements: list[dict[str, Any]] = []
        if result.detected:
            assert result.centroid_x is not None and result.centroid_y is not None
            measurements = [
                _measurement("centroid_x", result.centroid_x, "px", "raw"),
                _measurement("centroid_y", result.centroid_y, "px", "raw"),
                _measurement("spot_area", result.spot_area, "px2", "raw"),
                _measurement("spot_intensity_sum", result.intensity_sum, "1", "raw"),
                _measurement("peak_intensity", result.peak_intensity or 0.0, "1", "raw"),
            ]
            if result.bbox_width is not None and result.bbox_height is not None:
                measurements += [_measurement("bbox_width", result.bbox_width, "px", "derived"), _measurement("bbox_height", result.bbox_height, "px", "derived")]
        flags: list[str] = []
        if not result.detected:
            flags.append("spot-lost")
            if result.candidate_pixels > 0:
                flags.append("low-signal")
        if result.overexposed_fraction >= self.config.overexposure_fraction and result.candidate_pixels > 0:
            flags.append("overexposed")
        if result.roi_edge:
            flags.append("roi-edge")
        frame_quality = frame.metadata.get("quality", {})
        dropped = int(frame_quality.get("dropped_since_last", 0)) if isinstance(frame_quality, Mapping) else 0
        event = make_sensor_event(
            run_id=frame.run_id, sensor_id=self.SENSOR_ID, instance_id=self.instance_id, sensor_version=self.VERSION,
            category="processor", sequence=self._sequence, observed_at=str(frame.metadata["observed_at"]),
            monotonic_ns=int(frame.metadata["monotonic_ns"]), source_timestamp=frame.metadata.get("source_timestamp"),
            status="ok" if result.detected else "lost", measurements=measurements, confidence=None,
            latency_ms=latency_ms, quality_flags=flags, dropped_since_last=dropped,
            coordinate_frame={"id": f"{frame.frame_id}:image-pixel", "space": "image-pixel", "origin": "top-left", "x_direction": "right", "y_direction": "down", "unit": "px", "width": frame.width, "height": frame.height, "calibration_id": None},
            parent_event_ids=(frame.frame_id,), payload={"algorithm": "source-red-weighted-centroid", "algorithm_source_commits": ["7f0d91cc73afafaecc54acc46b2b9d69375d994a", "c3f58175a09ff29cacdfb976a5055758c4eff619"], "config": self.config.to_dict(), "source_projection": result.source_projection(), "candidate_pixels": result.candidate_pixels, "overexposed_fraction": result.overexposed_fraction},
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
