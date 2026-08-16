"""Language-level sensor lifecycle shared by implementations."""

from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from .events import FramePacket, SensorEvent


JsonObject = Mapping[str, Any]


class LifecycleState(StrEnum):
    CREATED = "created"
    CONFIGURED = "configured"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass(frozen=True)
class SensorDescriptor:
    sensor_id: str
    version: str
    category: str
    input_kinds: tuple[str, ...]
    output_kinds: tuple[str, ...]
    capabilities: tuple[str, ...] = ()
    config_schema_version: str = "1.0.0"
    evidence_level: str = "documented-prototype"


@dataclass(frozen=True)
class ConfigResult:
    accepted: bool
    effective_config: JsonObject
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class SensorContext:
    run_id: str
    clock: Any = None
    artifact_store: Any = None
    logger: Any = None
    cancellation: Any = None

    @classmethod
    def minimal(cls, run_id: str) -> "SensorContext":
        return cls(run_id=run_id)


@dataclass(frozen=True)
class HealthSnapshot:
    state: LifecycleState
    processed_count: int = 0
    dropped_count: int = 0
    lost_count: int = 0
    error_count: int = 0
    actual_rate_hz: float | None = None
    latency_ms: Mapping[str, float] = field(default_factory=dict)
    last_error: JsonObject | None = None


@runtime_checkable
class SensorLifecycle(Protocol):
    def describe(self) -> SensorDescriptor: ...

    def configure(self, config: JsonObject) -> ConfigResult: ...

    async def start(self, context: SensorContext) -> None: ...

    def health(self) -> HealthSnapshot: ...

    async def stop(self) -> None: ...


@runtime_checkable
class SourceSensor(SensorLifecycle, Protocol):
    def read(self) -> AsyncIterator[FramePacket | SensorEvent]: ...


@runtime_checkable
class ProcessorSensor(SensorLifecycle, Protocol):
    def process(self, input_packet: Any) -> AsyncIterator[SensorEvent]: ...
