#!/usr/bin/env python3
"""Dependency-free structural checks for the Phase 1 repository skeleton."""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

from validate_i18n import validate_i18n


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
EXPECTED_COMPOSITIONS = {
    ("camera.capture", "tracker.color-marker"),
    ("camera.capture", "tracker.spot-centroid"),
    ("camera.capture", "tracker.template"),
    ("camera.capture", "tracker.yolo"),
    ("screen.capture", "ocr.number"),
}
EXPECTED_SOURCE_REPOSITORIES = {
    "WUHAO19831214/audio-visual-soundfield-tracker-stable",
    "WUHAO19831214/spot-vibration-tracking-system-20260508-171952",
    "WUHAO19831214/forced-vibration-af-analyzer-20260502-122715",
    "WUHAO19831214/physics-experiment-bridge-mvp",
    "WUHAO19831214/ampere-force-visualizer-teacher-yanan",
}
EXPECTED_IMPLEMENTATION_STATUS = {
    "camera.capture": ("incubating", "adapter-present", "0.3.0"),
    "screen.capture": ("incubating", "adapter-present", "0.3.0"),
    "ocr.number": ("incubating", "adapter-present", "0.2.0"),
    "tracker.color-marker": ("incubating", "adapter-present", "0.2.0"),
    "tracker.spot-centroid": ("incubating", "adapter-present", "0.4.0"),
    "tracker.template": ("incubating", "adapter-present", "0.4.0"),
    "tracker.yolo": ("incubating", "adapter-present", "0.5.0"),
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
    "tracker.yolo": ("overview.png", "multi-target.png", "tracking.png", "fallback.png", "events.json"),
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
        if "## Distribution" not in (path.parent / "README.md").read_text(encoding="utf-8"):
            errors.append(f"{path.parent.relative_to(ROOT)}: missing Distribution section")
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


def check_evidence_registry() -> list[str]:
    errors: list[str] = []
    registry = load_json(ROOT / "benchmarks/results/index.json")
    entries = registry.get("entries", [])
    if not isinstance(entries, list):
        return ["benchmarks/results/index.json: entries must be an array"]
    ids = {entry.get("sensor_id") for entry in entries if isinstance(entry, dict)}
    if len(entries) != 7 or ids != EXPECTED_SENSOR_IDS:
        errors.append("benchmarks/results/index.json: exactly one entry per known sensor is required")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"benchmarks/results/index.json: entry {index} must be an object")
            continue
        if entry.get("evidence_level") not in {f"E{level}" for level in range(6)}:
            errors.append(f"benchmarks/results/index.json: invalid evidence level at entry {index}")
        for field in ("implementation_version", "benchmark_type", "environment", "dataset", "source_report", "metrics", "limitations"):
            if field not in entry:
                errors.append(f"benchmarks/results/index.json: entry {index} missing {field}")
    return errors


def check_composition_matrix() -> list[str]:
    errors: list[str] = []
    matrix = load_json(ROOT / "tests/composition/matrix.json")
    compositions = matrix.get("compositions", [])
    if not isinstance(compositions, list):
        return ["tests/composition/matrix.json: compositions must be an array"]
    actual = {
        (entry.get("source"), entry.get("processor"))
        for entry in compositions
        if isinstance(entry, dict)
    }
    if len(compositions) != 5 or actual != EXPECTED_COMPOSITIONS:
        errors.append("tests/composition/matrix.json: the five purposeful source/processor paths are required")
    for index, entry in enumerate(compositions):
        if not isinstance(entry, dict) or entry.get("tested") is not True or entry.get("result") != "passed":
            errors.append(f"tests/composition/matrix.json: composition {index} must record a passed test")
        elif not all(entry.get(field) for field in ("fixture", "test")):
            errors.append(f"tests/composition/matrix.json: composition {index} lacks fixture/test evidence")
    return errors


def check_release_candidate() -> list[str]:
    errors: list[str] = []
    manifest_path = ROOT / "release/release-manifest.json"
    manifest = load_json(manifest_path)
    if manifest.get("release_version") != "v0.6.0" or manifest.get("release_status") != "release-candidate-not-published":
        errors.append("release/release-manifest.json: expected v0.6.0 unpublished release candidate")
    if manifest.get("contracts") != {"sensor_event": "1.0.0", "frame_packet": "1.0.0"}:
        errors.append("release/release-manifest.json: contract versions must remain 1.0.0")
    if manifest.get("packages") != {"python": "0.5.0", "typescript": "0.3.0"}:
        errors.append("release/release-manifest.json: package versions mismatch")
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list) or len(artifacts) != 9:
        return errors + ["release/release-manifest.json: exactly nine artifacts are required"]
    bundle_ids = {
        item.get("sensor_id") for item in artifacts
        if isinstance(item, dict) and item.get("type") == "sensor-bundle"
    }
    if bundle_ids != EXPECTED_SENSOR_IDS:
        errors.append("release/release-manifest.json: exactly seven known sensor bundles are required")
    types = [item.get("type") for item in artifacts if isinstance(item, dict)]
    if types.count("python-wheel") != 1 or types.count("typescript-tgz") != 1:
        errors.append("release/release-manifest.json: one wheel and one tgz are required")
    for index, item in enumerate(artifacts):
        if not isinstance(item, dict):
            errors.append(f"release/release-manifest.json: artifact {index} must be an object")
            continue
        if not re.fullmatch(r"[a-f0-9]{64}", str(item.get("sha256", ""))):
            errors.append(f"release/release-manifest.json: artifact {index} has invalid SHA-256")
        if not isinstance(item.get("bytes"), int) or item["bytes"] <= 0:
            errors.append(f"release/release-manifest.json: artifact {index} has invalid size")
        if Path(str(item.get("filename", ""))).suffix.lower() in {".pt", ".onnx", ".engine"}:
            errors.append("release/release-manifest.json: model weights are prohibited")
    sums: dict[str, str] = {}
    for line in (ROOT / "release/SHA256SUMS").read_text(encoding="utf-8").splitlines():
        try:
            digest, filename = line.split("  ", 1)
        except ValueError:
            errors.append("release/SHA256SUMS: invalid line format")
            continue
        sums[filename] = digest
    artifact_names = {str(item.get("filename")) for item in artifacts if isinstance(item, dict)}
    if set(sums) != artifact_names | {"release-manifest.json"}:
        errors.append("release/SHA256SUMS: must cover nine artifacts and release-manifest.json")
    for item in artifacts:
        if isinstance(item, dict) and sums.get(str(item.get("filename"))) != item.get("sha256"):
            errors.append(f"release/SHA256SUMS: hash mismatch for {item.get('filename')}")
    actual_manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if sums.get("release-manifest.json") != actual_manifest_hash:
        errors.append("release/SHA256SUMS: release-manifest.json hash mismatch")
    return errors


def git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def check_handoff() -> list[str]:
    errors: list[str] = []
    path = ROOT / ".agent-handoff/latest.json"
    try:
        handoff = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"invalid agent handoff: {exc}"]
    if handoff.get("schema_version") != "1.1.0":
        errors.append(".agent-handoff/latest.json: schema_version must be 1.1.0")
    if handoff.get("repository") != "WUHAO19831214/physics-software-sensors":
        errors.append(".agent-handoff/latest.json: repository mismatch")
    if handoff.get("status") not in {"IN_PROGRESS", "BLOCKED", "READY_FOR_REVIEW", "MERGED", "RELEASED", "MAINTENANCE_READY"}:
        errors.append(".agent-handoff/latest.json: invalid status")
    git_value = handoff.get("git", {})
    if not isinstance(git_value, dict):
        return errors + [".agent-handoff/latest.json: git must be an object"]
    actual_head = git("rev-parse", "HEAD")
    actual_branch = git("branch", "--show-current") or os.environ.get("GITHUB_HEAD_REF", "")
    if git_value.get("working_branch") != actual_branch:
        errors.append(f".agent-handoff/latest.json: branch does not match {actual_branch or 'detached HEAD'}")
    tested_sha = git_value.get("tested_sha")
    if not HEX40.fullmatch(str(tested_sha or "")):
        errors.append(".agent-handoff/latest.json: tested_sha must be a full commit SHA")
    elif subprocess.run(("git", "merge-base", "--is-ancestor", tested_sha, actual_head), cwd=ROOT).returncode:
        errors.append(".agent-handoff/latest.json: tested_sha must be an ancestor of current HEAD")
    published = git_value.get("published_head_sha")
    expected_ref = f"refs/heads/{git_value.get('working_branch')}"
    if published != {"resolution": "branch-ref", "ref": expected_ref}:
        errors.append(".agent-handoff/latest.json: published_head_sha must resolve from the working branch ref")
    handoff_commit = git_value.get("handoff_commit_sha")
    if handoff_commit != {"resolution": "containing-commit"}:
        errors.append(".agent-handoff/latest.json: handoff_commit_sha must resolve from the containing commit")
    porcelain = git("status", "--porcelain")
    actual_clean = porcelain == ""
    if git_value.get("working_tree_clean") is not actual_clean:
        errors.append(".agent-handoff/latest.json: working_tree_clean does not match git status")
    sensors = handoff.get("sensors", {})
    if not isinstance(sensors, dict) or set(sensors) != EXPECTED_SENSOR_IDS:
        errors.append(".agent-handoff/latest.json: sensors must contain exactly the seven known IDs")
    pull_request = handoff.get("pull_request", {})
    if not isinstance(pull_request, dict):
        errors.append(".agent-handoff/latest.json: pull_request must be an object")
    else:
        number = pull_request.get("number")
        url = pull_request.get("url")
        if number is not None:
            expected_url = f"https://github.com/WUHAO19831214/physics-software-sensors/pull/{number}"
            if url != expected_url:
                errors.append(".agent-handoff/latest.json: PR URL does not match repository and number")
        elif url:
            errors.append(".agent-handoff/latest.json: PR URL must be empty when number is null")
    tests = handoff.get("tests", {})
    if not isinstance(tests, dict):
        errors.append(".agent-handoff/latest.json: tests must be an object")
    else:
        def walk_numbers(value: object, location: str) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    walk_numbers(child, f"{location}.{key}")
            elif isinstance(value, (int, float)) and not isinstance(value, bool) and value < 0:
                errors.append(f".agent-handoff/latest.json: negative test number at {location}")
        walk_numbers(tests, "tests")
    source_repositories = handoff.get("source_repositories", [])
    if not isinstance(source_repositories, list):
        errors.append(".agent-handoff/latest.json: source_repositories must be an array")
    else:
        actual_repositories = {
            item.get("repository") for item in source_repositories if isinstance(item, dict)
        }
        if not EXPECTED_SOURCE_REPOSITORIES <= actual_repositories:
            errors.append(".agent-handoff/latest.json: five fixed source repositories are required")
    return errors


def main() -> int:
    errors = (
        check_json()
        + check_manifests()
        + check_markdown_links()
        + check_evidence_registry()
        + check_composition_matrix()
        + check_release_candidate()
        + check_handoff()
        + validate_i18n(ROOT)
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    json_count = sum(
        1
        for path in ROOT.rglob("*.json")
        if not skip_generated(path)
    )
    print(f"OK: validated {json_count} JSON files, 7 trilingual Sensor Pages/manifests, i18n parity, pilot demos, and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
