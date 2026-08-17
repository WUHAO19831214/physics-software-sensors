from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_i18n", ROOT / "tools/validate_i18n.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_trilingual_public_document_parity() -> None:
    assert load_validator().validate_i18n(ROOT) == []


def test_validator_detects_sensor_fact_drift(tmp_path: Path) -> None:
    module = load_validator()
    for directory in ("docs", "sensors", "benchmarks", "processing"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    for filename in ("README.md", "README.zh-CN.md", "README.ja.md"):
        shutil.copy2(ROOT / filename, tmp_path / filename)
    path = tmp_path / "sensors/tracker.template/README.ja.md"
    path.write_text(path.read_text(encoding="utf-8").replace("E3", "E2"), encoding="utf-8")
    errors = module.validate_i18n(tmp_path)
    assert any("README.ja.md: missing parity fact E3" in error for error in errors)


def test_validator_detects_tool_fact_drift(tmp_path: Path) -> None:
    module = load_validator()
    for directory in ("docs", "sensors", "benchmarks", "processing"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    for filename in ("README.md", "README.zh-CN.md", "README.ja.md"):
        shutil.copy2(ROOT / filename, tmp_path / filename)
    path = tmp_path / "processing/vector.compose-3d/README.zh-CN.md"
    path.write_text(path.read_text(encoding="utf-8").replace("0.1.0", "0.2.0"), encoding="utf-8")
    errors = module.validate_i18n(tmp_path)
    assert any("README.zh-CN.md: missing tool parity fact 0.1.0" in error for error in errors)
