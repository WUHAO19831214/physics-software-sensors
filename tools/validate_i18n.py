#!/usr/bin/env python3
"""Validate trilingual public-document parity against machine facts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "zh_CN", "ja")
SWITCH_LABELS = ("English", "简体中文", "日本語")
MARKER = re.compile(r"<!-- section:([a-z0-9-]+) -->")
RELEASE_URL = "https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0"


def load_object(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def validate_set(root: Path, key: str, spec: dict, expected_sections: list[str]) -> list[str]:
    errors: list[str] = []
    observed: dict[str, list[str]] = {}
    for language in LANGUAGES:
        raw_path = spec.get(language)
        if not isinstance(raw_path, str):
            errors.append(f"{key}: missing {language} path")
            continue
        path = root / raw_path
        if not path.is_file():
            errors.append(f"{key}: missing {language} file {raw_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for label in SWITCH_LABELS:
            if label not in text:
                errors.append(f"{raw_path}: language switch missing {label}")
        markers = MARKER.findall(text)
        observed[language] = markers
        if markers != expected_sections:
            errors.append(f"{raw_path}: section markers {markers} != {expected_sections}")
    if len(observed) == 3 and len({tuple(value) for value in observed.values()}) != 1:
        errors.append(f"{key}: section order differs between languages")
    return errors


def validate_i18n(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        document_map = load_object(root / "docs/i18n/document-map.json")
        terminology = load_object(root / "docs/i18n/terminology.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    if document_map.get("languages") != list(LANGUAGES):
        errors.append("document-map.json: languages must be en, zh_CN, ja")
    documents = document_map.get("documents")
    if not isinstance(documents, dict):
        return errors + ["document-map.json: documents must be an object"]
    for key, value in documents.items():
        if not isinstance(value, dict) or not isinstance(value.get("sections"), list):
            errors.append(f"document-map.json: invalid document set {key}")
            continue
        errors.extend(validate_set(root, key, value, value["sections"]))

    sensor_sections = document_map.get("sensor_sections")
    sensors = document_map.get("sensors")
    if not isinstance(sensor_sections, list) or not isinstance(sensors, dict):
        return errors + ["document-map.json: sensors/sensor_sections must be present"]
    directory_ids = {path.parent.name for path in (root / "sensors").glob("*/sensor.json")}
    if set(sensors) != directory_ids:
        errors.append(f"document-map.json: sensor IDs do not match directories: {sorted(set(sensors) ^ directory_ids)}")
    registry = load_object(root / "benchmarks/results/index.json")
    evidence_by_id = {
        item["sensor_id"]: item["evidence_level"]
        for item in registry.get("entries", [])
        if isinstance(item, dict) and "sensor_id" in item and "evidence_level" in item
    }
    for sensor_id, spec in sensors.items():
        if not isinstance(spec, dict):
            errors.append(f"document-map.json: invalid sensor {sensor_id}")
            continue
        errors.extend(validate_set(root, sensor_id, spec, sensor_sections))
        manifest = load_object(root / "sensors" / sensor_id / "sensor.json")
        expected = {
            "version": manifest.get("version"),
            "maturity": "experimental",
            "evidence": evidence_by_id.get(sensor_id),
            "release": "v0.6.0",
        }
        for field, value in expected.items():
            if spec.get(field) != value:
                errors.append(f"document-map.json: {sensor_id} {field} {spec.get(field)!r} != {value!r}")
        for language in LANGUAGES:
            raw_path = spec.get(language)
            if not isinstance(raw_path, str) or not (root / raw_path).is_file():
                continue
            text = (root / raw_path).read_text(encoding="utf-8")
            required_literals = (sensor_id, str(expected["version"]), "experimental", str(expected["evidence"]), "v0.6.0")
            for literal in required_literals:
                if literal not in text:
                    errors.append(f"{raw_path}: missing parity fact {literal}")
            if RELEASE_URL not in text and "/releases/download/v0.6.0/" not in text:
                errors.append(f"{raw_path}: missing v0.6.0 release link")

    tool_sections = document_map.get("tool_sections")
    tools = document_map.get("tools")
    if not isinstance(tool_sections, list) or not isinstance(tools, dict):
        return errors + ["document-map.json: tools/tool_sections must be present"]
    directory_ids = {path.parent.name for path in (root / "processing").glob("*/tool.json")}
    if set(tools) != directory_ids:
        errors.append(f"document-map.json: tool IDs do not match directories: {sorted(set(tools) ^ directory_ids)}")
    for tool_id, spec in tools.items():
        if not isinstance(spec, dict):
            errors.append(f"document-map.json: invalid tool {tool_id}")
            continue
        errors.extend(validate_set(root, tool_id, spec, tool_sections))
        manifest = load_object(root / "processing" / tool_id / "tool.json")
        expected = {"version": manifest.get("version"), "status": manifest.get("status")}
        for field, value in expected.items():
            if spec.get(field) != value:
                errors.append(f"document-map.json: {tool_id} {field} {spec.get(field)!r} != {value!r}")
        for language in LANGUAGES:
            raw_path = spec.get(language)
            if not isinstance(raw_path, str) or not (root / raw_path).is_file():
                continue
            text = (root / raw_path).read_text(encoding="utf-8")
            for literal in (tool_id, str(expected["version"]), str(expected["status"])):
                if literal not in text:
                    errors.append(f"{raw_path}: missing tool parity fact {literal}")

    entries = terminology.get("entries")
    if not isinstance(entries, list) or len(entries) < 40:
        errors.append("terminology.json: at least 40 entries are required")
    else:
        keys: set[str] = set()
        for index, item in enumerate(entries):
            if not isinstance(item, dict):
                errors.append(f"terminology.json: entry {index} must be an object")
                continue
            if set(item) != {"key", "en", "zh_CN", "ja", "notes"}:
                errors.append(f"terminology.json: entry {index} fields mismatch")
            key = item.get("key")
            if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
                errors.append(f"terminology.json: invalid key at entry {index}")
            elif key in keys:
                errors.append(f"terminology.json: duplicate key {key}")
            else:
                keys.add(key)
            for language in LANGUAGES:
                if not isinstance(item.get(language), str) or not item[language].strip():
                    errors.append(f"terminology.json: {key} missing {language}")
        required_keys = {"software_sensor", "frame_packet", "sensor_event", "spot_centroid", "template_tracker", "confidence", "uncertainty"}
        if not required_keys <= keys:
            errors.append(f"terminology.json: missing required keys {sorted(required_keys - keys)}")
    return errors


def main() -> int:
    errors = validate_i18n()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    document_map = load_object(ROOT / "docs/i18n/document-map.json")
    terms = load_object(ROOT / "docs/i18n/terminology.json")["entries"]
    print(f"OK: i18n parity {len(document_map['documents'])} public document sets, {len(document_map['sensors'])} Sensor Pages x 3, {len(document_map['tools'])} Tool Page x 3, {len(terms)} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
