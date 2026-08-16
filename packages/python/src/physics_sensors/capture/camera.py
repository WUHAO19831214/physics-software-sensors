"""Backend-neutral camera capture producing schema-valid runtime FramePackets.

The adapter boundary is derived from the source repositories recorded in
``sensors/camera.capture/SOURCE.md``. Detection, tracking, UI and experiment
state intentionally remain outside this module.
"""

from __future__ import annotations

import asyncio
import hashlib
import time
from collections.abc import AsyncIterator, Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol, runtime_checkable
from uuid import uuid4

from physics_sensors.core import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    RuntimeFrame,
    SensorContext,
    SensorDescriptor,
    SensorStateError,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _pixel_bytes(pixels: Any) -> bytes:
    if hasattr(pixels, "tobytes"):
        return pixels.tobytes()
    if isinstance(pixels, bytes):
        return pixels
    if isinstance(pixels, (bytearray, memoryview)):
        return bytes(pixels)
    raise TypeError("camera pixels must expose tobytes() or be bytes-like")


@dataclass(frozen=True)
class CameraConfig:
    """Requested capture properties; backends report actual values separately."""

    width: int = 1280
    height: int = 720
    requested_fps: float = 30.0
    mirrored: bool = False
    orientation: str = "0"
    artifact_prefix: str = "runtime://camera.capture"


@dataclass(frozen=True)
class BackendFrame:
    """One backend read before it is wrapped in the public FramePacket."""

    pixels: Any
    width: int
    height: int
    color_space: str
    media_type: str
    source_timestamp: float | None = None
    dropped_since_last: int = 0
    observed_at: str | None = None
    monotonic_ns: int | None = None
    artifact_uri: str | None = None
    quality_flags: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class CameraBackend(Protocol):
    """Minimal seam usable by OpenCV, recorded, or future browser adapters."""

    backend_id: str

    def start(self, config: CameraConfig) -> Mapping[str, Any]: ...

    def read(self) -> BackendFrame | None: ...

    def stop(self) -> None: ...


class ImageSequenceCameraBackend:
    """Deterministic finite backend for replay, tests, and L1 benchmarks."""

    backend_id = "image-sequence"

    def __init__(
        self,
        frames: Sequence[BackendFrame],
        *,
        nominal_fps: float | None = None,
        device_name: str = "recorded-image-sequence",
    ) -> None:
        self._frames = tuple(frames)
        self._nominal_fps = nominal_fps
        self._device_name = device_name
        self._index = 0
        self._running = False

    def start(self, config: CameraConfig) -> Mapping[str, Any]:
        self._index = 0
        self._running = True
        first = self._frames[0] if self._frames else None
        return {
            "backend": self.backend_id,
            "device": self._device_name,
            "actual_width": first.width if first else None,
            "actual_height": first.height if first else None,
            "nominal_fps": self._nominal_fps,
            "deterministic_replay": True,
        }

    def read(self) -> BackendFrame | None:
        if not self._running:
            raise RuntimeError("image sequence backend is not running")
        if self._index >= len(self._frames):
            return None
        frame = self._frames[self._index]
        self._index += 1
        return frame

    def stop(self) -> None:
        self._running = False


class OpenCVCameraBackend:
    """Optional local-device backend; importing the package does not require OpenCV."""

    backend_id = "opencv"

    def __init__(
        self,
        device_index: int = 0,
        *,
        api_preference: int | None = None,
        max_consecutive_failures: int = 20,
        retry_delay_s: float = 0.02,
        capture_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.device_index = device_index
        self.api_preference = api_preference
        self.max_consecutive_failures = max_consecutive_failures
        self.retry_delay_s = retry_delay_s
        self.capture_factory = capture_factory
        self._capture: Any = None
        self._cv2: Any = None
        self._failed_reads = 0
        self._actual: dict[str, Any] = {}

    def start(self, config: CameraConfig) -> Mapping[str, Any]:
        try:
            import cv2  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover - exercised in clean consumer without extra
            raise RuntimeError(
                "OpenCVCameraBackend requires the 'camera-opencv' optional dependency"
            ) from exc
        factory = self.capture_factory or cv2.VideoCapture
        capture = (
            factory(self.device_index, self.api_preference)
            if self.api_preference is not None
            else factory(self.device_index)
        )
        if not capture.isOpened():
            capture.release()
            raise RuntimeError(f"unable to open camera device index={self.device_index}")
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        capture.set(cv2.CAP_PROP_FPS, config.requested_fps)
        self._capture = capture
        self._cv2 = cv2
        self._failed_reads = 0
        backend_name = (
            capture.getBackendName() if hasattr(capture, "getBackendName") else "unknown"
        )
        self._actual = {
            "backend": self.backend_id,
            "backend_name": backend_name,
            "device": f"camera-index-{self.device_index}",
            "device_index": self.device_index,
            "actual_width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) or None,
            "actual_height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) or None,
            "nominal_fps": float(capture.get(cv2.CAP_PROP_FPS)) or None,
            "deterministic_replay": False,
        }
        return dict(self._actual)

    def read(self) -> BackendFrame:
        if self._capture is None or self._cv2 is None:
            raise RuntimeError("OpenCV camera backend is not running")
        while True:
            ok, pixels = self._capture.read()
            if ok and pixels is not None:
                break
            self._failed_reads += 1
            if self._failed_reads >= self.max_consecutive_failures:
                raise RuntimeError(
                    f"camera read failed (consecutive failures={self._failed_reads})"
                )
            time.sleep(max(0.0, self.retry_delay_s))
        dropped = self._failed_reads
        self._failed_reads = 0
        height, width = pixels.shape[:2]
        source_ms = float(self._capture.get(self._cv2.CAP_PROP_POS_MSEC))
        return BackendFrame(
            pixels=pixels,
            width=int(width),
            height=int(height),
            color_space="BGR",
            media_type="application/x-raw-bgr",
            source_timestamp=source_ms / 1000.0 if source_ms > 0 else None,
            dropped_since_last=dropped,
            metadata={"backend_name": self._actual.get("backend_name", "unknown")},
        )

    def stop(self) -> None:
        if self._capture is not None:
            self._capture.release()
        self._capture = None


class CameraSource:
    """SourceSensor that turns backend reads into RuntimeFrame packets."""

    def __init__(
        self,
        backend: CameraBackend,
        *,
        instance_id: str = "camera-source-01",
        wall_clock: Callable[[], str] = _utc_now,
        monotonic_clock: Callable[[], int] = time.monotonic_ns,
        frame_id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.backend = backend
        self.instance_id = instance_id
        self._wall_clock = wall_clock
        self._monotonic_clock = monotonic_clock
        self._frame_id_factory = frame_id_factory or (lambda: str(uuid4()))
        self._state = LifecycleState.CREATED
        self._config = CameraConfig()
        self._context: SensorContext | None = None
        self._backend_info: Mapping[str, Any] = {}
        self._sequence = 0
        self._processed = 0
        self._dropped = 0
        self._errors = 0
        self._last_monotonic_ns: int | None = None
        self._measured_fps: float | None = None
        self._last_error: Mapping[str, Any] | None = None

    def describe(self) -> SensorDescriptor:
        return SensorDescriptor(
            sensor_id="camera.capture",
            version="0.3.0",
            category="source",
            input_kinds=(),
            output_kinds=("frame-packet.camera-frame",),
            capabilities=(
                "backend-neutral-source",
                "opencv-local-camera",
                "image-sequence-replay",
                "requested-vs-measured-rate",
                "runtime-pixel-binding",
            ),
            evidence_level="replay-benchmarked",
        )

    def configure(self, config: Mapping[str, Any]) -> ConfigResult:
        if self._state is LifecycleState.RUNNING:
            raise SensorStateError("stop the camera before reconfiguring it")
        allowed = {"width", "height", "requested_fps", "mirrored", "orientation", "artifact_prefix"}
        unknown = sorted(set(config) - allowed)
        if unknown:
            raise ValueError(f"unknown camera settings: {', '.join(unknown)}")
        effective = CameraConfig(
            width=int(config.get("width", self._config.width)),
            height=int(config.get("height", self._config.height)),
            requested_fps=float(config.get("requested_fps", self._config.requested_fps)),
            mirrored=bool(config.get("mirrored", self._config.mirrored)),
            orientation=str(config.get("orientation", self._config.orientation)),
            artifact_prefix=str(config.get("artifact_prefix", self._config.artifact_prefix)),
        )
        if effective.width < 1 or effective.height < 1 or effective.requested_fps <= 0:
            raise ValueError("camera width, height, and requested_fps must be positive")
        if effective.orientation not in {"0", "90", "180", "270"}:
            raise ValueError("camera orientation must be 0, 90, 180, or 270")
        self._config = effective
        self._state = LifecycleState.CONFIGURED
        return ConfigResult(
            accepted=True,
            effective_config={
                "width": effective.width,
                "height": effective.height,
                "requested_fps": effective.requested_fps,
                "mirrored": effective.mirrored,
                "orientation": effective.orientation,
                "artifact_prefix": effective.artifact_prefix,
            },
        )

    async def start(self, context: SensorContext) -> None:
        if self._state is LifecycleState.RUNNING:
            return
        self._context = context
        try:
            self._backend_info = await asyncio.to_thread(self.backend.start, self._config)
        except Exception as exc:
            self._state = LifecycleState.ERROR
            self._errors += 1
            self._last_error = {"code": "CAMERA_START_FAILED", "message": str(exc)}
            raise
        self._sequence = 0
        self._processed = 0
        self._dropped = 0
        self._last_monotonic_ns = None
        self._measured_fps = None
        self._state = LifecycleState.RUNNING

    async def read(self) -> AsyncIterator[RuntimeFrame]:
        if self._state is not LifecycleState.RUNNING or self._context is None:
            raise SensorStateError("camera source must be running")
        while self._state is LifecycleState.RUNNING:
            try:
                backend_frame = await asyncio.to_thread(self.backend.read)
            except Exception as exc:
                self._errors += 1
                self._last_error = {"code": "CAMERA_READ_FAILED", "message": str(exc)}
                self._state = LifecycleState.ERROR
                raise
            if backend_frame is None:
                break
            yield self._wrap_frame(backend_frame)

    def _wrap_frame(self, frame: BackendFrame) -> RuntimeFrame:
        if self._context is None:
            raise SensorStateError("camera source has no active context")
        observed_at = frame.observed_at or self._wall_clock()
        monotonic_ns = frame.monotonic_ns if frame.monotonic_ns is not None else self._monotonic_clock()
        if self._last_monotonic_ns is not None and monotonic_ns > self._last_monotonic_ns:
            self._measured_fps = 1_000_000_000.0 / (monotonic_ns - self._last_monotonic_ns)
        self._last_monotonic_ns = monotonic_ns
        raw = _pixel_bytes(frame.pixels)
        frame_id = self._frame_id_factory()
        flags = list(dict.fromkeys(frame.quality_flags))
        if frame.dropped_since_last:
            flags.append("frame-dropped")
        metadata = {
            "schema_version": "1.0.0",
            "frame_id": frame_id,
            "run_id": self._context.run_id,
            "source_sensor_id": "camera.capture",
            "sequence": self._sequence,
            "observed_at": observed_at,
            "monotonic_ns": monotonic_ns,
            "source_timestamp": frame.source_timestamp,
            "media": {
                "kind": "camera-frame",
                "media_type": frame.media_type,
                "width": frame.width,
                "height": frame.height,
                "color_space": frame.color_space,
                "orientation": self._config.orientation,
                "mirrored": self._config.mirrored,
            },
            "artifact": {
                "uri": frame.artifact_uri or f"{self._config.artifact_prefix}/{frame_id}",
                "media_type": frame.media_type,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            },
            "quality": {
                "dropped_since_last": frame.dropped_since_last,
                "flags": list(dict.fromkeys(flags)),
            },
            "payload": {
                "capture": {
                    "backend": self.backend.backend_id,
                    "instance_id": self.instance_id,
                    "device": dict(self._backend_info),
                    "requested": {
                        "width": self._config.width,
                        "height": self._config.height,
                        "fps": self._config.requested_fps,
                    },
                    "actual": {
                        "width": frame.width,
                        "height": frame.height,
                        "nominal_fps": self._backend_info.get("nominal_fps"),
                        "measured_fps": self._measured_fps,
                    },
                    "frame": dict(frame.metadata),
                }
            },
        }
        self._sequence += 1
        self._processed += 1
        self._dropped += frame.dropped_since_last
        return RuntimeFrame(metadata=metadata, pixels=frame.pixels)

    def health(self) -> HealthSnapshot:
        return HealthSnapshot(
            state=self._state,
            processed_count=self._processed,
            dropped_count=self._dropped,
            error_count=self._errors,
            actual_rate_hz=self._measured_fps,
            last_error=self._last_error,
        )

    async def stop(self) -> None:
        if self._state in {LifecycleState.STOPPED, LifecycleState.CREATED}:
            self._state = LifecycleState.STOPPED
            return
        self._state = LifecycleState.STOPPING
        await asyncio.to_thread(self.backend.stop)
        self._state = LifecycleState.STOPPED
