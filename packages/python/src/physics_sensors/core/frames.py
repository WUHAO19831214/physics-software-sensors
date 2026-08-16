"""Runtime binding between a serializable FramePacket and in-memory pixels."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .errors import InvalidFrameError


@dataclass(frozen=True)
class RuntimeFrame:
    """FramePacket metadata plus pixels kept out of the JSON event envelope."""

    metadata: Mapping[str, Any]
    pixels: Any

    def __post_init__(self) -> None:
        required = (
            "schema_version",
            "frame_id",
            "run_id",
            "source_sensor_id",
            "sequence",
            "observed_at",
            "monotonic_ns",
            "media",
            "artifact",
            "quality",
        )
        missing = [key for key in required if key not in self.metadata]
        if missing:
            raise InvalidFrameError(f"FramePacket is missing: {', '.join(missing)}")
        media = self.metadata.get("media")
        if not isinstance(media, Mapping) or int(media.get("width", 0)) < 1 or int(media.get("height", 0)) < 1:
            raise InvalidFrameError("FramePacket media width and height must be positive")
        if not isinstance(self.metadata.get("artifact"), Mapping):
            raise InvalidFrameError("FramePacket artifact must be an object")
        shape = getattr(self.pixels, "shape", None)
        if shape is not None and len(shape) >= 2:
            if int(shape[1]) != int(media["width"]) or int(shape[0]) != int(media["height"]):
                raise InvalidFrameError("pixel dimensions do not match FramePacket media")

    @property
    def frame_id(self) -> str:
        return str(self.metadata["frame_id"])

    @property
    def run_id(self) -> str:
        return str(self.metadata["run_id"])

    @property
    def width(self) -> int:
        return int(self.metadata["media"]["width"])

    @property
    def height(self) -> int:
        return int(self.metadata["media"]["height"])
