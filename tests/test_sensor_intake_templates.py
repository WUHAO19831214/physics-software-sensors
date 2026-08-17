from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_sensor_proposal_has_required_decision_and_physics_boundaries() -> None:
    text = (ROOT / "templates/SENSOR_PROPOSAL.md").read_text(encoding="utf-8")
    for phrase in ("Source commit", "Source files", "Directly observed", "Derived downstream quantities", "License status", "ACCEPT", "DEFER", "REJECT"):
        assert phrase in text


def test_add_sensor_prompt_has_required_variables_and_commit_rule() -> None:
    text = (ROOT / "templates/ADD_SENSOR_PROMPT.md").read_text(encoding="utf-8")
    for variable in ("SOURCE_REPOSITORY", "SOURCE_COMMIT", "CAPABILITY", "EXPECTED_SENSOR_ID", "PHYSICS_USE"):
        assert variable in text
    assert "pin the current reviewed commit" in text
