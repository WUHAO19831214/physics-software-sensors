from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    tools_path = str(ROOT / "tools")
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)
    spec = importlib.util.spec_from_file_location("validate_repo_homepage", ROOT / "tools/validate_repo.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_homepage_showcase_has_seven_sensors_and_one_tool() -> None:
    assert load_validator().check_homepage_showcase() == []


def test_public_capability_counts_do_not_turn_tool_into_sensor() -> None:
    status = json.loads((ROOT / "docs/project-status.json").read_text(encoding="utf-8"))
    assert status["sensor_count"] == 7
    assert status["companion_tool_count"] == 1
    assert status["public_capability_count"] == 8
    assert status["homepage_visual_coverage"] == {
        "sensors": "7/7",
        "companion_tools": "1/1",
        "total": "8/8",
        "broken_demo_links": 0,
    }
