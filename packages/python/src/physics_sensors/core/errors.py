"""Stable errors raised by software sensor adapters."""


class PhysicsSensorError(Exception):
    """Base class for public package errors."""


class InvalidConfigurationError(PhysicsSensorError, ValueError):
    """A sensor configuration is invalid or unsupported."""


class InvalidFrameError(PhysicsSensorError, ValueError):
    """A runtime frame or its FramePacket metadata is invalid."""


class SensorStateError(PhysicsSensorError, RuntimeError):
    """An operation is incompatible with the sensor lifecycle state."""


class MissingOptionalDependencyError(PhysicsSensorError, ImportError):
    """An implementation extra was not installed."""
