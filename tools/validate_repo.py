#!/usr/bin/env python3
"""Dependency-free structural checks for the Phase 1 repository skeleton."""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import struct
import sys
import zlib
from pathlib import Path

from validate_i18n import validate_i18n
from validate_public_docs import validate_public_docs


ROOT = Path(__file__).resolve().parents[1]
HEX40 = re.compile(r"^[a-f0-9]{40}$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LINKED_IMAGE = re.compile(r"\[!\[[^\]]*\]\(([^)]+)\)\]\(([^)]+)\)")
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
HOMEPAGE_FILES = {
    "en": ROOT / "README.md",
    "zh_CN": ROOT / "README.zh-CN.md",
    "ja": ROOT / "README.ja.md",
}
DETAILED_DEMO_IMAGES = {
    "sensors/camera.capture/assets/captured-frame.png",
    "sensors/screen.capture/assets/captured-screen-frame.png",
    "sensors/ocr.number/assets/overview.png",
    "sensors/tracker.color-marker/assets/overview.png",
    "sensors/tracker.spot-centroid/assets/overview.png",
    "sensors/tracker.template/assets/overview.png",
    "sensors/tracker.yolo/assets/overview.png",
    "processing/vector.compose-3d/assets/overview.png",
}
HOMEPAGE_SHOWCASE_IMAGE = "docs/assets/capability-showcase.png"
HOMEPAGE_SHOWCASE_PAGES = {
    "en": "docs/capability-showcase.md",
    "zh_CN": "docs/capability-showcase.zh-CN.md",
    "ja": "docs/capability-showcase.ja.md",
}
HOMEPAGE_CAPABILITY_LINKS = {
    "en": {
        "sensors/camera.capture/README.md",
        "sensors/screen.capture/README.md",
        "sensors/ocr.number/README.md",
        "sensors/tracker.color-marker/README.md",
        "sensors/tracker.spot-centroid/README.md",
        "sensors/tracker.template/README.md",
        "sensors/tracker.yolo/README.md",
        "processing/vector.compose-3d/README.md",
    },
    "zh_CN": {
        "sensors/camera.capture/README.zh-CN.md",
        "sensors/screen.capture/README.zh-CN.md",
        "sensors/ocr.number/README.zh-CN.md",
        "sensors/tracker.color-marker/README.zh-CN.md",
        "sensors/tracker.spot-centroid/README.zh-CN.md",
        "sensors/tracker.template/README.zh-CN.md",
        "sensors/tracker.yolo/README.zh-CN.md",
        "processing/vector.compose-3d/README.zh-CN.md",
    },
    "ja": {
        "sensors/camera.capture/README.ja.md",
        "sensors/screen.capture/README.ja.md",
        "sensors/ocr.number/README.ja.md",
        "sensors/tracker.color-marker/README.ja.md",
        "sensors/tracker.spot-centroid/README.ja.md",
        "sensors/tracker.template/README.ja.md",
        "sensors/tracker.yolo/README.ja.md",
        "processing/vector.compose-3d/README.ja.md",
    },
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


def check_tool_manifests() -> list[str]:
    errors: list[str] = []
    paths = sorted((ROOT / "processing").glob("*/tool.json"))
    if len(paths) != 1:
        return [f"processing: expected exactly one Companion Tool, found {len(paths)}"]
    path = paths[0]
    manifest = load_json(path)
    if manifest.get("id") != path.parent.name or manifest.get("id") != "vector.compose-3d":
        errors.append(f"{path.relative_to(ROOT)}: expected id vector.compose-3d matching directory")
    expected = {
        "type": "companion-processing-tool",
        "status": "experimental",
        "version": "0.1.0",
        "language": "typescript",
    }
    for field, value in expected.items():
        if manifest.get(field) != value:
            errors.append(f"{path.relative_to(ROOT)}: {field} must be {value!r}")
    for relative in ("README.md", "README.zh-CN.md", "README.ja.md", "SOURCE.md", "CHANGELOG.md", "benchmarks/README.md", "examples/README.md"):
        if not (path.parent / relative).is_file():
            errors.append(f"{path.parent.relative_to(ROOT)}: missing Tool Page file {relative}")
    for source in manifest.get("source_references", []):
        if not HEX40.fullmatch(str(source.get("commit", ""))):
            errors.append(f"{path.relative_to(ROOT)}: source commit must be a full SHA")
        if not str(source.get("repository", "")).startswith("https://github.com/"):
            errors.append(f"{path.relative_to(ROOT)}: source repository must be a GitHub URL")
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


def check_homepage_showcase() -> list[str]:
    errors: list[str] = []
    status = load_json(ROOT / "docs/project-status.json")
    if status.get("sensor_count") != 7:
        errors.append("docs/project-status.json: sensor_count must remain 7")
    if status.get("companion_tool_count") != 1:
        errors.append("docs/project-status.json: companion_tool_count must be 1")
    if status.get("public_capability_count") != 8:
        errors.append("docs/project-status.json: public_capability_count must be 8")
    sensor_manifests = list((ROOT / "sensors").glob("*/sensor.json"))
    tool_manifests = list((ROOT / "processing").glob("*/tool.json"))
    if len(sensor_manifests) != 7 or len(tool_manifests) != 1:
        errors.append("homepage inventory must resolve to exactly 7 Sensors and 1 Companion Tool")
    showcase_path = ROOT / HOMEPAGE_SHOWCASE_IMAGE
    if not showcase_path.is_file():
        errors.append(f"missing homepage aggregate image {HOMEPAGE_SHOWCASE_IMAGE}")
    else:
        errors.extend(validate_png(showcase_path, expected_size=(1200, 1458)))
        if showcase_path.stat().st_size >= 1_500_000:
            errors.append(f"{HOMEPAGE_SHOWCASE_IMAGE}: must remain below 1.5 MB")
    for asset in sorted(DETAILED_DEMO_IMAGES):
        asset_path = ROOT / asset
        if not asset_path.is_file() or asset_path.stat().st_size <= 0:
            errors.append(f"missing or empty detailed demo asset {asset}")
        else:
            errors.extend(validate_png(asset_path))
    for language, raw_path in HOMEPAGE_SHOWCASE_PAGES.items():
        detail_path = ROOT / raw_path
        detail_text = detail_path.read_text(encoding="utf-8")
        detail_images = {
            str((detail_path.parent / image).resolve().relative_to(ROOT))
            for image, _target in LINKED_IMAGE.findall(detail_text)
            if image != "assets/capability-showcase.png"
        }
        if detail_images != DETAILED_DEMO_IMAGES:
            errors.append(f"{raw_path}: detailed demo image coverage must be exactly 8/8")
    expected_pages = set(EXPECTED_SENSOR_IDS) | {"vector.compose-3d"}
    for language, path in HOMEPAGE_FILES.items():
        text = path.read_text(encoding="utf-8")
        try:
            gallery = text.split("<!-- section:capability-showcase -->", 1)[1].split("<!-- section:principles -->", 1)[0]
        except IndexError:
            errors.append(f"{path.name}: missing capability-showcase/principles section boundary")
            continue
        linked_images = LINKED_IMAGE.findall(gallery)
        pages_root = "https://wuhao19831214.github.io/physics-software-sensors/"
        prefix = {"en": "", "zh_CN": "zh-CN/", "ja": "ja/"}[language]
        expected_linked_image = [(HOMEPAGE_SHOWCASE_IMAGE, pages_root + prefix + "capability-showcase/")]
        if linked_images != expected_linked_image:
            errors.append(f"{path.name}: homepage must contain exactly one linked aggregate image")
        for image, target in linked_images:
            if not (ROOT / image).is_file():
                errors.append(f"{path.name}: missing homepage image {image}")
        if "/sensors/" not in gallery:
            errors.append(f"{path.name}: missing Pages-first Sensor navigation")
        if "/tools/vector-compose-3d/" not in gallery:
            errors.append(f"{path.name}: missing Pages-first Tool navigation")
        if "Companion Processing Tools" not in text and "配套处理工具" not in text:
            errors.append(f"{path.name}: missing separate Companion Processing Tools section")
        for capability_id in expected_pages:
            if capability_id not in text:
                errors.append(f"{path.name}: missing homepage capability {capability_id}")
        if "8/8" not in gallery:
            errors.append(f"{path.name}: missing 8/8 capability coverage statement")
        if "recorded detector replay" not in gallery.lower():
            errors.append(f"{path.name}: missing recorded detector replay boundary")
    return errors


def validate_png(path: Path, expected_size: tuple[int, int] | None = None) -> list[str]:
    """Validate and decompress a non-interlaced 8-bit RGB/RGBA PNG offline."""

    errors: list[str] = []
    relative = path.relative_to(ROOT)
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return [f"{relative}: invalid PNG signature"]
    offset = 8
    idat = bytearray()
    width = height = channels = None
    saw_iend = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        payload_start = offset + 8
        payload_end = payload_start + length
        crc_end = payload_end + 4
        if crc_end > len(data):
            return [f"{relative}: truncated PNG chunk"]
        payload = data[payload_start:payload_end]
        expected_crc = struct.unpack(">I", data[payload_end:crc_end])[0]
        actual_crc = zlib.crc32(chunk_type + payload) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            errors.append(f"{relative}: invalid CRC in {chunk_type.decode('ascii', 'replace')} chunk")
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, _compression, _filter, interlace = struct.unpack(">IIBBBBB", payload)
            channels = {2: 3, 6: 4}.get(color_type)
            if bit_depth != 8 or channels is None or interlace != 0:
                errors.append(f"{relative}: expected non-interlaced 8-bit RGB/RGBA PNG")
        elif chunk_type == b"IDAT":
            idat.extend(payload)
        elif chunk_type == b"IEND":
            saw_iend = True
            break
        offset = crc_end
    if not saw_iend or width is None or height is None or channels is None or not idat:
        return errors + [f"{relative}: incomplete PNG structure"]
    if expected_size is not None and (width, height) != expected_size:
        errors.append(f"{relative}: dimensions {(width, height)} != {expected_size}")
    try:
        decoded = zlib.decompress(bytes(idat))
    except zlib.error as exc:
        errors.append(f"{relative}: PNG image data cannot be decompressed: {exc}")
    else:
        expected_length = height * (1 + width * channels)
        if len(decoded) != expected_length:
            errors.append(f"{relative}: decoded scanline length {len(decoded)} != {expected_length}")
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
        + check_tool_manifests()
        + check_markdown_links()
        + check_homepage_showcase()
        + check_evidence_registry()
        + check_composition_matrix()
        + check_release_candidate()
        + check_handoff()
        + validate_i18n(ROOT)
        + validate_public_docs(ROOT)
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
    print(f"OK: validated {json_count} JSON files, 7 trilingual Sensor Pages/manifests, 1 trilingual Companion Tool, 1 decoded homepage aggregate with 8/8 capability links, i18n parity, pilot demos, and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
