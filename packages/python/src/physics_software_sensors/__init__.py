"""Compatibility namespace; prefer ``physics_sensors``."""

from .contracts import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    ProcessorSensor,
    SensorContext,
    SensorDescriptor,
    SensorEvent,
    SourceSensor,
)

__all__ = [
    "ConfigResult",
    "HealthSnapshot",
    "LifecycleState",
    "ProcessorSensor",
    "SensorContext",
    "SensorDescriptor",
    "SensorEvent",
    "SourceSensor",
]

__version__ = "0.2.0"
