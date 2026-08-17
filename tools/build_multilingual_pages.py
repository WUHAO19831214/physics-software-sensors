#!/usr/bin/env python3
"""Render the trilingual repository READMEs as GitHub Pages-ready static HTML.

The generated pages are a reading fallback only. README Markdown and the
machine-readable repository files remain the canonical source of facts.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

try:
    import markdown
except ImportError as exc:  # pragma: no cover - incomplete dev environments only
    raise SystemExit(
        "Markdown is required to build public pages. Install the Python dev extra: "
        "python -m pip install -e './packages/python[dev]'"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPOSITORY_URL = "https://github.com/WUHAO19831214/physics-software-sensors"
LANGUAGES = {
    "en": {"source": "README.md", "output": "index.html", "label": "English", "title": "Physics Software Sensors"},
    "zh_CN": {"source": "README.zh-CN.md", "output": "zh-CN/index.html", "label": "简体中文", "title": "物理实验软件传感器库"},
    "ja": {"source": "README.ja.md", "output": "ja/index.html", "label": "日本語", "title": "Physics Software Sensors — 物理実験ソフトウェアセンサーライブラリ"},
}
LANGUAGE_ROUTES = {
    "en": {"en": "./", "zh_CN": "zh-CN/", "ja": "ja/"},
    "zh_CN": {"en": "../", "zh_CN": "./", "ja": "../ja/"},
    "ja": {"en": "../", "zh_CN": "../zh-CN/", "ja": "./"},
}
SOURCE_ROUTES = {
    "README.md": "en",
    "README.zh-CN.md": "zh_CN",
    "README.ja.md": "ja",
}
ATTR_URL = re.compile(r'(?P<attribute>href|src)="(?P<url>[^"]+)"')


def source_text(language: str) -> str:
    text = (ROOT / LANGUAGES[language]["source"]).read_text(encoding="utf-8")
    lines = text.splitlines()
    if len(lines) >= 3 and "English" in lines[2] and "日本語" in lines[2]:
        del lines[2]
    return "\n".join(lines) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_path_url(path: str) -> str:
    fragment = ""
    if "#" in path:
        path, fragment = path.split("#", 1)
        fragment = f"#{fragment}"
    return f"{REPOSITORY_URL}/blob/main/{path}{fragment}"


def rewrite_url(url: str, language: str) -> str:
    parts = urlsplit(html.unescape(url))
    if parts.scheme or parts.netloc or url.startswith(("#", "mailto:")):
        return url
    path = parts.path
    if not path:
        return url
    if path in SOURCE_ROUTES:
        rewritten = LANGUAGE_ROUTES[language][SOURCE_ROUTES[path]]
    elif path.startswith("docs/assets/"):
        prefix = "" if language == "en" else "../"
        rewritten = f"{prefix}{path.removeprefix('docs/')}"
    elif path.startswith("assets/"):
        prefix = "" if language == "en" else "../"
        rewritten = f"{prefix}{path}"
    else:
        rewritten = repository_path_url(path)
    return urlunsplit(("", "", rewritten, parts.query, parts.fragment))


def rewrite_attributes(rendered: str, language: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return f'{match.group("attribute")}="{html.escape(rewrite_url(match.group("url"), language), quote=True)}"'

    return ATTR_URL.sub(replace, rendered)


def navigation(language: str) -> str:
    links = []
    for key, spec in LANGUAGES.items():
        label = spec["label"]
        if key == language:
            links.append(f"<strong lang=\"{key}\">{label}</strong>")
        else:
            links.append(f'<a lang="{key}" href="{LANGUAGE_ROUTES[language][key]}">{label}</a>')
    return "<nav class=\"language-nav\" aria-label=\"Language navigation\">" + " <span>|</span> ".join(links) + "</nav>"


def status_banner(language: str, status: dict) -> str:
    sensors = status["sensor_count"]
    tools = status["companion_tool_count"]
    capabilities = status["public_capability_count"]
    text = {
        "en": f"{sensors} Software Sensors · {tools} Companion Processing Tool · {capabilities} reusable public capabilities",
        "zh_CN": f"{sensors} 个软件传感器 · {tools} 个配套处理工具 · 共 {capabilities} 项可复用公开能力",
        "ja": f"{sensors} Software Sensor · {tools} Companion Processing Tool · 再利用可能な公開 capability 全 {capabilities} 項",
    }[language]
    return f"<p class=\"status-banner\">{html.escape(text)}</p>"


def page_html(language: str, status: dict) -> str:
    body = markdown.markdown(source_text(language), extensions=["fenced_code", "tables", "sane_lists"])
    body = rewrite_attributes(body, language)
    title = LANGUAGES[language]["title"]
    source = LANGUAGES[language]["source"]
    source_url = f"{REPOSITORY_URL}/blob/main/{source}"
    source_hash = sha256(ROOT / source)
    status_hash = sha256(DOCS / "project-status.json")
    return f"""<!doctype html>
<html lang=\"{language}\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <meta name=\"source-readme-sha256\" content=\"{source_hash}\">
  <meta name=\"project-status-sha256\" content=\"{status_hash}\">
  <title>{html.escape(title)}</title>
  <link rel=\"stylesheet\" href=\"{'site.css' if language == 'en' else '../site.css'}\">
</head>
<body>
  <header class=\"site-header\">
    <a class=\"repository-link\" href=\"{REPOSITORY_URL}\">Physics Software Sensors on GitHub</a>
    {navigation(language)}
    {status_banner(language, status)}
    <p class=\"source-link\">Markdown source: <a href=\"{source_url}\">{source}</a></p>
  </header>
  <main>
{body}
  </main>
  <footer>Repository source of truth: <a href=\"{REPOSITORY_URL}\">WUHAO19831214/physics-software-sensors</a></footer>
</body>
</html>
"""


def build() -> None:
    status = json.loads((DOCS / "project-status.json").read_text(encoding="utf-8"))
    for language, spec in LANGUAGES.items():
        output = DOCS / spec["output"]
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(page_html(language, status), encoding="utf-8")
        print(f"Wrote {output.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when committed pages differ from regenerated output")
    args = parser.parse_args()
    if not args.check:
        build()
        return 0
    status = json.loads((DOCS / "project-status.json").read_text(encoding="utf-8"))
    stale = []
    for language, spec in LANGUAGES.items():
        output = DOCS / spec["output"]
        if not output.is_file() or output.read_text(encoding="utf-8") != page_html(language, status):
            stale.append(str(output.relative_to(ROOT)))
    if stale:
        raise SystemExit("Pages are missing or stale; run tools/build_multilingual_pages.py: " + ", ".join(stale))
    print("PASS: 3/3 multilingual Pages files match README and project-status sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
