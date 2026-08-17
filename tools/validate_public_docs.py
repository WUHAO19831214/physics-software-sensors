#!/usr/bin/env python3
"""Offline validation for multilingual public-document delivery routes."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
README_FILES = {
    "en": ROOT / "README.md",
    "zh_CN": ROOT / "README.zh-CN.md",
    "ja": ROOT / "README.ja.md",
}
PAGES = {
    "en": DOCS / "index.html",
    "zh_CN": DOCS / "zh-CN/index.html",
    "ja": DOCS / "ja/index.html",
}
NAVIGATION = {
    "en": ('href="zh-CN/"', 'href="ja/"'),
    "zh_CN": ('href="../"', 'href="../ja/"'),
    "ja": ('href="../"', 'href="../zh-CN/"'),
}
SOURCE_NAMES = {"en": "README.md", "zh_CN": "README.zh-CN.md", "ja": "README.ja.md"}
LINK = re.compile(r'(?:href|src)="([^"]+)"')
META = re.compile(r'<meta name="([^"]+)" content="([a-f0-9]{64})">')
CAPABILITIES = {
    "camera.capture",
    "screen.capture",
    "ocr.number",
    "tracker.color-marker",
    "tracker.spot-centroid",
    "tracker.template",
    "tracker.yolo",
    "vector.compose-3d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_public_docs(root: Path = ROOT) -> list[str]:
    docs = root / "docs"
    errors: list[str] = []
    status_path = docs / "project-status.json"
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"docs/project-status.json: {exc}"]
    if (status.get("sensor_count"), status.get("companion_tool_count"), status.get("public_capability_count")) != (7, 1, 8):
        errors.append("project-status.json: expected 7 Sensors, 1 Companion Tool and 8 public capabilities")
    if status.get("public_document_delivery") != {
        "repository_content_integrity": "pass",
        "github_blob_view": "external_error",
        "github_raw": "rate_limited",
        "github_pages": "ready_for_enablement",
        "pages_source": "main /docs",
    }:
        errors.append("project-status.json: public-document delivery state mismatch")
    expected_status_hash = sha256(status_path)

    for language, relative in ((key, path.relative_to(root)) for key, path in README_FILES.items()):
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{relative}: missing or invalid UTF-8: {exc}")
            continue
        for target in ("README.md", "README.zh-CN.md", "README.ja.md"):
            if target not in text and target != path.name:
                errors.append(f"{relative}: missing language source target {target}")
        if "Repository multilingual content integrity: **PASS**" not in text and "仓库三语内容完整性：**PASS**" not in text and "repository の 3 言語コンテンツ完全性：**PASS**" not in text:
            errors.append(f"{relative}: missing language-access integrity statement")

    for language, default_page in PAGES.items():
        page = root / default_page.relative_to(ROOT)
        relative = page.relative_to(root)
        try:
            html = page.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{relative}: missing or invalid UTF-8: {exc}")
            continue
        if '<meta charset="utf-8">' not in html:
            errors.append(f"{relative}: missing UTF-8 declaration")
        for required in NAVIGATION[language]:
            if required not in html:
                errors.append(f"{relative}: missing language route {required}")
        if 'class="language-nav"' not in html:
            errors.append(f"{relative}: missing language navigation")
        if "docs/assets/capability-showcase.png" in html:
            errors.append(f"{relative}: must use a Pages-relative showcase asset route")
        if "capability-showcase.png" not in html:
            errors.append(f"{relative}: missing capability showcase")
        if not CAPABILITIES <= set(re.findall(r"(?:camera\.capture|screen\.capture|ocr\.number|tracker\.(?:color-marker|spot-centroid|template|yolo)|vector\.compose-3d)", html)):
            errors.append(f"{relative}: missing one or more public capabilities")
        meta = dict(META.findall(html))
        source = root / SOURCE_NAMES[language]
        if meta.get("source-readme-sha256") != sha256(source):
            errors.append(f"{relative}: generated page does not match {SOURCE_NAMES[language]}")
        if meta.get("project-status-sha256") != expected_status_hash:
            errors.append(f"{relative}: generated page does not match docs/project-status.json")
        for target in LINK.findall(html):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or target.startswith("#"):
                continue
            local = (page.parent / parts.path).resolve()
            try:
                local.relative_to(root)
            except ValueError:
                errors.append(f"{relative}: route escapes Pages root: {target}")
                continue
            if not local.exists():
                errors.append(f"{relative}: missing local Pages target: {target}")
    return errors


def main() -> int:
    errors = validate_public_docs()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK: public docs 3/3 README sources, 3/3 Pages files, 6/6 language routes, 7 Sensors + 1 Tool")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
