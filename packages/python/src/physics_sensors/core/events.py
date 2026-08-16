"""SensorEvent construction without algorithm dependencies."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any, TypeAlias
from uuid import uuid4


SensorEvent: TypeAlias = dict[str, Any]
FramePacket: TypeAlias = Mapping[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def make_sensor_event(
    *,
    run_id: str,
    sensor_id: str,
    instance_id: str,
    sensor_version: str,
    category: str,
    sequence: int,
    observed_at: str,
    monotonic_ns: int,
    status: str,
    measurements: Sequence[Mapping[str, Any]],
    confidence: float | None,
    latency_ms: float | None,
    quality_flags: Sequence[str] = (),
    dropped_since_last: int = 0,
    source_timestamp: float | None = None,
    clock_domain: str = "camera-source",
    clock_sync_status: str = "unknown",
    coordinate_frame: Mapping[str, Any] | None = None,
    parent_event_ids: Sequence[str] = (),
    payload: Mapping[str, Any] | None = None,
    error: Mapping[str, Any] | None = None,
) -> SensorEvent:
    event: SensorEvent = {
        "schema_version": "1.0.0",
        "event_id": str(uuid4()),
        "run_id": run_id,
        "sensor": {
            "id": sensor_id,
            "instance_id": instance_id,
            "version": sensor_version,
            "category": category,
        },
        "sequence": sequence,
        "time": {
            "observed_at": observed_at,
            "emitted_at": utc_now(),
            "source_timestamp": source_timestamp,
            "monotonic_ns": monotonic_ns,
            "clock": {
                "domain": clock_domain,
                "sync_status": clock_sync_status,
                "uncertainty_ms": None,
            },
        },
        "status": status,
        "quality": {
            "confidence": confidence,
            "latency_ms": latency_ms,
            "flags": list(dict.fromkeys(quality_flags)),
            "dropped_since_last": dropped_since_last,
        },
        "measurements": [dict(item) for item in measurements],
    }
    if coordinate_frame is not None:
        event["coordinate_frame"] = dict(coordinate_frame)
    if parent_event_ids:
        event["parent_event_ids"] = list(parent_event_ids)
    if payload is not None:
        event["payload"] = dict(payload)
    if error is not None:
        event["error"] = dict(error)
    return event
