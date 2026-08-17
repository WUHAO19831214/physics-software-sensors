from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_public_docs", ROOT / "tools/validate_public_docs.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_document_routes_are_complete_and_offline_valid() -> None:
    assert load_validator().validate_public_docs(ROOT) == []


def test_pages_are_regenerated_from_current_markdown_sources() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tools/build_multilingual_pages.py"), "--check"],
        check=True,
        cwd=ROOT,
    )
