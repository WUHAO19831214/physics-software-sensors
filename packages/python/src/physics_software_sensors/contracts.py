"""Compatibility re-exports for the Phase 1 import path.

New code should import from :mod:`physics_sensors.core`.
"""

from physics_sensors.core.events import FramePacket, SensorEvent
from physics_sensors.core.sensor import (
    ConfigResult,
    HealthSnapshot,
    LifecycleState,
    ProcessorSensor,
    SensorContext,
    SensorDescriptor,
    SensorLifecycle,
    SourceSensor,
)

__all__ = [
    "ConfigResult",
    "FramePacket",
    "HealthSnapshot",
    "LifecycleState",
    "ProcessorSensor",
    "SensorContext",
    "SensorDescriptor",
    "SensorEvent",
    "SensorLifecycle",
    "SourceSensor",
]
