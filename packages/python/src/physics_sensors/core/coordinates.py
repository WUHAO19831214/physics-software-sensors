"""Coordinate and ROI value objects."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import InvalidConfigurationError


@dataclass(frozen=True)
class NormalizedRect:
    x: float
    y: float
    width: float
    height: float

    def __post_init__(self) -> None:
        values = (self.x, self.y, self.width, self.height)
        if not all(isinstance(value, (int, float)) for value in values):
            raise InvalidConfigurationError("ROI values must be numeric")
        if self.width <= 0 or self.height <= 0:
            raise InvalidConfigurationError("ROI width and height must be positive")
        if self.x < 0 or self.y < 0 or self.x + self.width > 1 or self.y + self.height > 1:
            raise InvalidConfigurationError("normalized ROI must stay within [0, 1]")

    @classmethod
    def from_mapping(cls, value: dict) -> "NormalizedRect":
        try:
            return cls(float(value["x"]), float(value["y"]), float(value["width"]), float(value["height"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidConfigurationError("ROI requires numeric x, y, width, and height") from exc

    def to_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}
