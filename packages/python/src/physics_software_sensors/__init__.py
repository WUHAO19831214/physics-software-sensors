"""Contract-only Python skeleton for physics software sensors."""

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

__version__ = "0.1.0"
