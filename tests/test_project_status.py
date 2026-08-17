from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_project_status_matches_sensor_registry_and_maintenance_baseline() -> None:
    status = load("docs/project-status.json")
    benchmark = load("benchmarks/results/index.json")
    document_map = load("docs/i18n/document-map.json")
    assert status["project_state"] == "maintenance"
    assert status["phase_5_library_merge_sha"] == "2c3e91ed3c36f23b82c76cfd70076807adc1f891"
    assert status["baseline_release"]["tag"] == "v0.6.0"
    assert status["baseline_release"]["immutable"] is True
    assert status["sensor_count"] == status["implemented_adapter_count"] == 7
    assert status["companion_tool_count"] == 1
    assert status["public_capability_count"] == 8
    assert status["languages"] == ["en", "zh-CN", "ja"]
    assert set(status["sensors"]) == set(document_map["sensors"])
    assert set(status["companion_tools"]) == set(document_map["tools"]) == {"vector.compose-3d"}
    assert status["companion_tools"]["vector.compose-3d"]["released"] is False
    evidence = {entry["sensor_id"]: entry["evidence_level"] for entry in benchmark["entries"]}
    for sensor_id, sensor in status["sensors"].items():
        assert sensor["maturity"] == "experimental"
        assert sensor["evidence"] == evidence[sensor_id]
        assert sensor["evidence"] == document_map["sensors"][sensor_id]["evidence"]
    assert status["sensors"]["tracker.spot-centroid"]["evidence"] == "E5"
    assert status["sensors"]["tracker.spot-centroid"]["e4_real_device"] is False


def test_maintenance_workflows_and_merged_reuse_are_recorded() -> None:
    status = load("docs/project-status.json")
    assert status["workflows"] == {
        "sensor_intake": "ready",
        "companion_tool_intake": "ready",
        "sensor_upgrade": "ready",
        "downstream_reuse": "ready",
        "release": "ready",
    }
    integration = status["downstream_integrations"][0]
    assert integration["sensor_id"] == "tracker.spot-centroid"
    assert integration["status"] == "merged"
    assert integration["merge_sha"] == "172429fae463274ee354e54d56400096c2c6d375"
    assert integration["default_backend"] == "legacy"
    assert integration["realtime_bridge"] is False
