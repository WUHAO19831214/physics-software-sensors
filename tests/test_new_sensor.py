from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/new_sensor.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run((sys.executable, str(TOOL), *args), text=True, capture_output=True)


def test_generator_creates_truthful_trilingual_scaffold(tmp_path: Path) -> None:
    result = run("--id", "vision.angle", "--name", "Angle Tracker", "--language", "python", "--category", "tracking", "--output-root", str(tmp_path))
    assert result.returncode == 0, result.stderr
    root = tmp_path / "sensors/vision.angle"
    expected = {"README.md", "README.zh-CN.md", "README.ja.md", "sensor.json", "SOURCE.md", "CHANGELOG.md", "assets", "benchmarks", "examples", "implementation"}
    assert expected <= {path.name for path in root.iterdir()}
    manifest = json.loads((root / "sensor.json").read_text(encoding="utf-8"))
    assert manifest["id"] == "vision.angle"
    assert manifest["maturity"] == "planned"
    assert manifest["implementation_status"] == "contract-only"
    assert manifest["source_references"] == []
    assert manifest["license_review"] == "pending"
    for page in ("README.md", "README.zh-CN.md", "README.ja.md"):
        text = (root / page).read_text(encoding="utf-8")
        assert text.count("<!-- section:") == 16
        assert "contract-only" in text and "E0" in text
    document_map = json.loads((tmp_path / "docs/i18n/document-map.json").read_text(encoding="utf-8"))
    assert document_map["sensors"]["vision.angle"]["maturity"] == "contract-only"


def test_generator_dry_run_writes_nothing(tmp_path: Path) -> None:
    result = run("--id", "vision.angle", "--name", "Angle Tracker", "--language", "python", "--output-root", str(tmp_path), "--dry-run")
    assert result.returncode == 0
    assert "DRY RUN" in result.stdout
    assert not (tmp_path / "sensors").exists()


def test_generator_rejects_invalid_id_and_overwrite(tmp_path: Path) -> None:
    invalid = run("--id", "AngleTracker", "--name", "Angle Tracker", "--language", "python", "--output-root", str(tmp_path))
    assert invalid.returncode != 0
    first = run("--id", "vision.angle", "--name", "Angle Tracker", "--language", "typescript", "--output-root", str(tmp_path))
    assert first.returncode == 0
    second = run("--id", "vision.angle", "--name", "Angle Tracker", "--language", "typescript", "--output-root", str(tmp_path))
    assert second.returncode != 0
    assert "refusing to overwrite" in second.stderr
