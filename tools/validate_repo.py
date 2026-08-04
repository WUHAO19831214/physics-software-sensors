#!/usr/bin/env python3
"""Dependency-free structural checks for the Phase 1 repository skeleton."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEX40 = re.compile(r"^[a-f0-9]{40}$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
EXPECTED_SENSOR_IDS = {
    "camera.capture",
    "screen.capture",
    "ocr.number",
    "tracker.color-marker",
    "tracker.yolo",
    "tracker.template",
    "tracker.spot-centroid",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def check_json() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
            continue
        try:
            load_json(path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(str(exc))
    return errors


def check_manifests() -> list[str]:
    errors: list[str] = []
    found: set[str] = set()
    for path in sorted((ROOT / "sensors").glob("*/sensor.json")):
        manifest = load_json(path)
        sensor_id = manifest.get("id")
        found.add(str(sensor_id))
        if sensor_id != path.parent.name:
            errors.append(f"{path.relative_to(ROOT)}: id must match directory name")
        if manifest.get("maturity") != "planned":
            errors.append(f"{path.relative_to(ROOT)}: Phase 1 maturity must be planned")
        if manifest.get("implementation_status") != "contract-only":
            errors.append(f"{path.relative_to(ROOT)}: Phase 1 status must be contract-only")
        for source in manifest.get("source_references", []):
            if not HEX40.fullmatch(str(source.get("commit", ""))):
                errors.append(f"{path.relative_to(ROOT)}: source commit must be a full SHA")
            if not str(source.get("repository", "")).startswith("https://github.com/"):
                errors.append(f"{path.relative_to(ROOT)}: source repository must be a GitHub URL")
    if found != EXPECTED_SENSOR_IDS:
        errors.append(f"sensor catalog mismatch: expected {sorted(EXPECTED_SENSOR_IDS)}, found {sorted(found)}")
    return errors


def check_markdown_links() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link target: {raw_target}")
    return errors


def main() -> int:
    errors = check_json() + check_manifests() + check_markdown_links()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    json_count = sum(
        1
        for path in ROOT.rglob("*.json")
        if not any(part in {".git", ".venv", "node_modules"} for part in path.parts)
    )
    print(f"OK: validated {json_count} JSON files, 7 sensor manifests, and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
