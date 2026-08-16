from __future__ import annotations

import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]


def test_reviewed_ocr_demo_contains_a_schema_valid_real_tesseract_event() -> None:
    schema = json.loads((ROOT / "contracts" / "schemas" / "sensor-event.schema.json").read_text(encoding="utf-8"))
    result = json.loads((ROOT / "sensors" / "ocr.number" / "assets" / "demo-result.json").read_text(encoding="utf-8"))
    event = result["event"]
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(event)
    assert result["fixture"]["id"] == "negative"
    assert result["fixture"]["expectedValue"] == -2.33
    assert event["payload"]["raw_text"] == "-2.33"
    assert event["measurements"][0]["value"] == -2.33
    assert event["quality"]["flags"] == []
