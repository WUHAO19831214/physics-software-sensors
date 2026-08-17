from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "experimental_release_builder", ROOT / "tools" / "build_experimental_release.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_release_builder_declares_exact_sensor_set() -> None:
    module = load_builder()
    assert module.SENSOR_IDS == {
        "camera.capture",
        "screen.capture",
        "ocr.number",
        "tracker.color-marker",
        "tracker.spot-centroid",
        "tracker.template",
        "tracker.yolo",
    }


def test_committed_release_manifest_and_checksums_match() -> None:
    release = ROOT / "release"
    manifest = json.loads((release / "release-manifest.json").read_text(encoding="utf-8"))
    assert manifest["release_version"] == "v0.6.0"
    assert manifest["release_status"] == "release-candidate-not-published"
    assert len(manifest["artifacts"]) == 9
    sums = (release / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert len(sums) == 10
    assert any(line.endswith("  release-manifest.json") for line in sums)


def test_release_notes_keep_experimental_boundary() -> None:
    notes = (ROOT / "release" / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    required = [
        "experimental pre-stable release",
        "no metrology",
        "No YOLO model",
        "GitHub Actions",
        "rollback",
    ]
    for phrase in required:
        assert phrase.lower() in notes.lower()
