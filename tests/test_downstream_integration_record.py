from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_spot_downstream_record_is_pinned_comparable_and_reversible() -> None:
    record = json.loads((ROOT / "integrations/spot-vibration/integration.json").read_text(encoding="utf-8"))
    assert record["downstream_base_sha"] == "7f0d91cc73afafaecc54acc46b2b9d69375d994a"
    assert len(record["downstream_integration_sha"]) == 40
    assert record["downstream_pull_request_state"] == "MERGED"
    assert record["downstream_merge_sha"] == "172429fae463274ee354e54d56400096c2c6d375"
    assert record["library_release"] == "v0.6.0"
    assert record["package_version"] == "0.5.0"
    assert record["artifact"]["sha256"] == "191258d71e036d5f7b9b2ef3b43c2a70d6a6058af984ce65ea39ddb23db573c9"
    assert record["feature_flag_values"] == ["legacy", "library", "compare"]
    assert record["default_backend"] == "legacy"
    assert record["comparison"]["case_matches"] == "7/7"
    assert record["comparison"]["maximum_absolute_delta"] <= record["comparison"]["tolerance_px"]
    assert record["downstream_regression"]["passed"] is True
    assert record["rollback_tested"] is True
    assert record["legacy_implementation_retained"] is True
    assert record["evidence_level"] == "E5"
    assert record["maturity"] == "experimental"


def test_spot_evidence_registry_matches_integration_record() -> None:
    registry = json.loads((ROOT / "benchmarks/results/index.json").read_text(encoding="utf-8"))
    spot = next(entry for entry in registry["entries"] if entry["sensor_id"] == "tracker.spot-centroid")
    assert spot["evidence_level"] == "E5"
    assert spot["downstream_integration"]["rollback_tested"] is True
    assert spot["downstream_integration"]["integration_sha"] == "6d2a1b8c79bd6b0400c596db9b989235f3637ba3"
    assert spot["downstream_integration"]["merge_sha"] == "172429fae463274ee354e54d56400096c2c6d375"
    assert spot["downstream_integration"]["post_merge_main_verified"] is True
