from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]


def test_standalone_color_marker_example_generates_events_and_visualizations(tmp_path: Path) -> None:
    output = tmp_path / "output"
    sample = tmp_path / "sample.png"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples" / "python-color-marker" / "run.py"),
            "--output",
            str(output),
            "--sample",
            str(sample),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "statuses: ok, lost, ok" in completed.stdout
    for filename in ("overview.png", "processing.png", "lost-reacquire.png", "events.json"):
        assert (output / filename).stat().st_size > 0
    assert sample.stat().st_size > 0

    schema = json.loads((ROOT / "contracts" / "schemas" / "sensor-event.schema.json").read_text(encoding="utf-8"))
    events = json.loads((output / "events.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    assert [event["status"] for event in events] == ["ok", "lost", "ok"]
    for event in events:
        validator.validate(event)
