"""Small dependency-free core shared by all Python sensors."""

from .coordinates import NormalizedRect
from .errors import InvalidConfigurationError, InvalidFrameError, SensorStateError
from .events import FramePacket, SensorEvent, make_sensor_event
from .frames import RuntimeFrame
from .model_artifact import ModelArtifact
from .sensor import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    ProcessorSensor,
    SensorContext,
    SensorDescriptor,
    SourceSensor,
)

__all__ = [
    "ConfigResult",
    "FramePacket",
    "HealthSnapshot",
    "InvalidConfigurationError",
    "InvalidFrameError",
    "LifecycleState",
    "NormalizedRect",
    "ProcessorSensor",
    "RuntimeFrame",
    "ModelArtifact",
    "SensorContext",
    "SensorDescriptor",
    "SensorEvent",
    "SensorStateError",
    "SourceSensor",
    "make_sensor_event",
]
