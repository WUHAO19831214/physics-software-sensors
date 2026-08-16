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
EXPECTED_IMPLEMENTATION_STATUS = {
    "camera.capture": ("incubating", "adapter-present", "0.3.0"),
    "screen.capture": ("incubating", "adapter-present", "0.3.0"),
    "ocr.number": ("incubating", "adapter-present", "0.2.0"),
    "tracker.color-marker": ("incubating", "adapter-present", "0.2.0"),
    "tracker.spot-centroid": ("incubating", "adapter-present", "0.4.0"),
    "tracker.template": ("incubating", "adapter-present", "0.4.0"),
}
SENSOR_PAGE_FILES = (
    "README.md",
    "SOURCE.md",
    "CHANGELOG.md",
    "assets/README.md",
    "examples/README.md",
    "benchmarks/README.md",
)
PILOT_DEMO_ASSETS = {
    "camera.capture": ("captured-frame.png", "frame-packet-metadata.png", "backend-information.png"),
    "screen.capture": ("captured-screen-frame.png", "frame-packet-metadata.png", "permission-boundary.png"),
    "tracker.color-marker": ("overview.png", "processing.png", "lost-reacquire.png"),
    "ocr.number": ("overview.png", "processing.png", "demo-result.json"),
    "tracker.spot-centroid": ("overview.png", "processing.png", "movement.png"),
    "tracker.template": ("overview.png", "initialization.png", "tracking.png", "lost.png"),
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def skip_generated(path: Path) -> bool:
    return any(part in {".git", ".venv", "node_modules"} for part in path.parts) or (
        "examples" in path.parts and "output" in path.parts
    )


def check_json() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if skip_generated(path):
            continue
        try:
            with path.open(encoding="utf-8") as handle:
                json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
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
        expected = EXPECTED_IMPLEMENTATION_STATUS.get(str(sensor_id), ("planned", "contract-only", "0.1.0"))
        actual = (manifest.get("maturity"), manifest.get("implementation_status"), manifest.get("version"))
        if actual != expected:
            errors.append(f"{path.relative_to(ROOT)}: expected maturity/status/version {expected}, found {actual}")
        for relative in SENSOR_PAGE_FILES:
            if not (path.parent / relative).is_file():
                errors.append(f"{path.parent.relative_to(ROOT)}: missing Sensor Page file {relative}")
        for asset in PILOT_DEMO_ASSETS.get(str(sensor_id), ()):
            if not (path.parent / "assets" / asset).is_file():
                errors.append(f"{path.parent.relative_to(ROOT)}: missing reviewed demo asset {asset}")
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
        if skip_generated(path):
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
        if not skip_generated(path)
    )
    print(f"OK: validated {json_count} JSON files, 7 Sensor Pages/manifests, pilot demos, and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
