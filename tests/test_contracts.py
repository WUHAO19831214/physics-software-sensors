from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "contracts" / "schemas"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("schema_path", sorted(SCHEMAS.glob("*.schema.json")))
def test_schema_is_valid(schema_path: Path) -> None:
    jsonschema.Draft202012Validator.check_schema(load(schema_path))


@pytest.mark.parametrize("manifest_path", sorted((ROOT / "sensors").glob("*/sensor.json")))
def test_sensor_manifest(manifest_path: Path) -> None:
    schema = load(SCHEMAS / "sensor-manifest.schema.json")
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(load(manifest_path))


@pytest.mark.parametrize(
    ("example", "schema_name"),
    [
        ("spot-centroid-event.json", "sensor-event.schema.json"),
        ("screen-frame-packet.json", "frame-packet.schema.json"),
        ("benchmark-result.json", "benchmark-result.schema.json"),
    ],
)
def test_contract_example(example: str, schema_name: str) -> None:
    schema = load(SCHEMAS / schema_name)
    instance = load(ROOT / "contracts" / "examples" / example)
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(instance)


def test_benchmark_counts_add_up() -> None:
    result = load(ROOT / "contracts" / "examples" / "benchmark-result.json")
    counts = result["sample_counts"]
    assert counts["total"] == sum(counts[name] for name in ("ok", "degraded", "lost", "error"))
