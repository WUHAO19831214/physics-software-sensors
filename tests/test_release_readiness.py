from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SENSOR_IDS = {
    "camera.capture",
    "screen.capture",
    "ocr.number",
    "tracker.color-marker",
    "tracker.spot-centroid",
    "tracker.template",
    "tracker.yolo",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_release_manifest_template_has_dry_run_boundaries() -> None:
    template = load(ROOT / "templates" / "RELEASE_MANIFEST.json")
    assert template["release_status"] == "dry-run-not-published"
    assert template["git_sha"] == "FULL_COMMIT_SHA"
    assert template["artifacts"][0]["sha256"] == "64 lowercase hexadecimal characters"


def test_artifact_record_uses_file_hash_and_size(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location(
        "release_builder", ROOT / "tools" / "build_release_artifacts.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    artifact = tmp_path / "candidate.whl"
    artifact.write_bytes(b"deterministic release candidate")
    record = module.artifact_record(artifact, "example", "0.1.0", "python-wheel")
    assert record["bytes"] == artifact.stat().st_size
    assert record["sha256"] == hashlib.sha256(artifact.read_bytes()).hexdigest()


def test_all_sensor_bundles_are_self_describing_without_core_copy(tmp_path: Path) -> None:
    subprocess.run(
        ["python3", str(ROOT / "tools" / "build_sensor_bundle.py"), "--output", str(tmp_path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    index = load(tmp_path / "manifest.json")
    assert index["status"] == "dry-run-not-published"
    assert {entry["sensor_id"] for entry in index["bundles"]} == SENSOR_IDS
    assert len(index["bundles"]) == 7

    for entry in index["bundles"]:
        archive_path = tmp_path / entry["filename"]
        assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == entry["sha256"]
        with zipfile.ZipFile(archive_path) as archive:
            names = set(archive.namelist())
            assert {"README.md", "BUNDLE.json", "DEPENDENCIES.json", "INSTALL.md", "sensor/README.md", "sensor/SOURCE.md", "sensor/benchmarks/README.md", "example/README.md"} <= names
            assert not any(name.startswith(("packages/", "physics_sensors/", "src/core/")) for name in names)
            bundle = json.loads(archive.read("BUNDLE.json"))
            dependencies = json.loads(archive.read("DEPENDENCIES.json"))
        assert bundle["sensor_id"] == entry["sensor_id"]
        assert bundle["git_sha"] == index["git_sha"]
        assert dependencies["bundled_package_code"] is False
