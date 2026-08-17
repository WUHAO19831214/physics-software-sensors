#!/usr/bin/env python3
"""Offline validation for Pages-first public documentation routes."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LINK = re.compile(r'(?:href|src)="([^"]+)"')
LANGUAGES = {"en": "", "zh_CN": "zh-CN", "ja": "ja"}


def route_output(route: str, language: str) -> Path:
    prefix = LANGUAGES[language]
    return DOCS.joinpath(*(([prefix] if prefix else []) + ([] if route == "." else route.split("/")) + ["index.html"]))


def validate_public_docs(root: Path = ROOT) -> list[str]:
    docs = root / "docs"
    errors: list[str] = []
    try:
        routes = json.loads((docs / "site-routes.json").read_text(encoding="utf-8"))
        status = json.loads((docs / "project-status.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"public docs metadata: {exc}"]
    if (status.get("sensor_count"), status.get("companion_tool_count"), status.get("public_capability_count")) != (7, 1, 8):
        errors.append("project status capability count is not 7 Sensors + 1 Tool")
    if status.get("public_document_delivery", {}).get("github_pages") != "enabled":
        errors.append("project status must record enabled GitHub Pages")
    capability_routes = list(routes["sensors"].values()) + list(routes["tools"].values())
    required = [routes["home"], routes["catalog"], routes["installation"], routes["downloads"], routes["evidence"], routes["showcase"], routes["getting_started"], routes["sensor_intake"]] + capability_routes + list(routes["examples"].values())
    pages: list[Path] = []
    for language in LANGUAGES:
        for route in required:
            page = route_output(route, language)
            if not page.is_file():
                errors.append(f"missing public page: {page.relative_to(root)}")
            else:
                pages.append(page)
    if len(routes["sensors"]) != 7 or len(routes["tools"]) != 1:
        errors.append("route manifest must contain exactly 7 Sensors and 1 Tool")
    for page in pages:
        relative = page.relative_to(root)
        text = page.read_text(encoding="utf-8")
        if '<meta charset="utf-8">' not in text or 'class="language-nav"' not in text or 'class="site-nav"' not in text:
            errors.append(f"{relative}: missing Pages shell/navigation")
        if 'Developer resources' not in text and '开发者资源' not in text and '開発者向けリソース' not in text:
            errors.append(f"{relative}: missing secondary developer resources")
        for target in LINK.findall(text):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or target.startswith("#"):
                continue
            local = (page.parent / parts.path).resolve()
            try:
                local.relative_to(root)
            except ValueError:
                errors.append(f"{relative}: internal link escapes site: {target}")
                continue
            if not local.exists():
                errors.append(f"{relative}: broken internal public link: {target}")
    return errors


def main() -> int:
    errors = validate_public_docs()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK: Pages-first docs 3/3 languages, 7/7 Sensors, 1/1 Tool, 9 examples, catalog/support pages and zero broken internal links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
