#!/usr/bin/env python3
"""Generate a Pages-first trilingual documentation reader from repository facts."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPOSITORY_URL = "https://github.com/WUHAO19831214/physics-software-sensors"
ROUTES = json.loads((DOCS / "site-routes.json").read_text(encoding="utf-8"))
LANGUAGES = {
    "en": ("", "English", "README.md", "Physics Software Sensors"),
    "zh_CN": ("zh-CN", "简体中文", "README.zh-CN.md", "物理实验软件传感器库"),
    "ja": ("ja", "日本語", "README.ja.md", "Physics Software Sensors — 物理実験ソフトウェアセンサーライブラリ"),
}
ATTR_URL = re.compile(r'(?P<attribute>href|src)="(?P<url>[^"]+)"')
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
DOC_PAGES = {
    "installation": ("docs/installation.md", "docs/installation.zh-CN.md", "docs/installation.ja.md"),
    "downloads": ("docs/downloading-sensors.md", "docs/downloading-sensors.zh-CN.md", "docs/downloading-sensors.ja.md"),
    "evidence": ("docs/evidence-and-maturity.md", "docs/evidence-and-maturity.zh-CN.md", "docs/evidence-and-maturity.ja.md"),
    "showcase": ("docs/capability-showcase.md", "docs/capability-showcase.zh-CN.md", "docs/capability-showcase.ja.md"),
    "getting_started": ("docs/getting-started.md", "docs/getting-started.zh-CN.md", "docs/getting-started.ja.md"),
    "sensor_intake": ("docs/sensor-intake.md", "docs/sensor-intake.zh-CN.md", "docs/sensor-intake.ja.md"),
}
EXAMPLES = {
    "camera-capture": ("examples/python-camera-capture/README.md", ("Camera Capture", "摄像头采集", "カメラキャプチャ")),
    "screen-capture": ("examples/web-screen-capture/README.md", ("Screen Capture", "屏幕采集", "画面キャプチャ")),
    "number-ocr": ("examples/web-number-ocr/README.md", ("Number OCR", "数字 OCR", "Number OCR")),
    "screen-to-ocr": ("examples/web-screen-to-ocr/README.md", ("Screen to OCR", "屏幕采集到 OCR", "画面キャプチャから OCR")),
    "color-marker": ("examples/python-color-marker/README.md", ("Color Marker", "颜色标记追踪", "カラーマーカー追跡")),
    "spot-centroid": ("examples/spot-centroid/README.md", ("Spot Centroid", "光斑重心", "光スポット重心")),
    "template-tracker": ("examples/python-template-tracker/README.md", ("Template Tracker", "模板／单目标追踪", "テンプレート／単一物体トラッカー")),
    "yolo-tracker": ("examples/python-yolo-tracker/README.md", ("YOLO Tracker", "YOLO 追踪", "YOLO Tracker")),
    "vector-compose-3d": ("examples/web-vector-compose-3d/README.md", ("3D Vector Composition", "三维矢量合成", "3次元ベクトル合成")),
}


@dataclass(frozen=True)
class Page:
    route: str
    language: str
    title: str
    source: str | None
    body: str


def language_index(language: str) -> int:
    return ("en", "zh_CN", "ja").index(language)


def output_path(route: str, language: str) -> Path:
    prefix = LANGUAGES[language][0]
    pieces = ([prefix] if prefix else []) + ([] if route == "." else route.split("/")) + ["index.html"]
    return DOCS.joinpath(*pieces)


def relative_href(page: Page, route: str, language: str | None = None) -> str:
    target = output_path(route, language or page.language).parent
    return os.path.relpath(target, output_path(page.route, page.language).parent).replace(os.sep, "/") + "/"


def source_text(path: str) -> str:
    return "\n".join(line for line in (ROOT / path).read_text(encoding="utf-8").splitlines() if not line.startswith(("Markdown sources:", "Developer Markdown sources:"))) + "\n"


def title_for(path: str) -> str:
    return next((line.lstrip("# ") for line in source_text(path).splitlines() if line.startswith("# ")), "Physics Software Sensors")


def public_route_for(path: Path) -> str | None:
    relative = path.relative_to(ROOT).as_posix()
    if relative in {item[2] for item in LANGUAGES.values()}:
        return ROUTES["home"]
    for sensor_id, route in ROUTES["sensors"].items():
        if relative.startswith(f"sensors/{sensor_id}/") and path.name.startswith("README"):
            return route
    if relative.startswith("processing/vector.compose-3d/") and path.name.startswith("README"):
        return ROUTES["tools"]["vector.compose-3d"]
    if relative in {"docs/sensor-catalog.md", "docs/sensor-catalog.zh-CN.md", "docs/sensor-catalog.ja.md", "docs/tool-catalog.md", "docs/tool-catalog.zh-CN.md", "docs/tool-catalog.ja.md"}:
        return ROUTES["catalog"]
    for key, paths in DOC_PAGES.items():
        if relative in paths:
            return ROUTES[key]
    for slug, (example, _names) in EXAMPLES.items():
        if relative == example:
            return ROUTES["examples"][slug]
    return None


def site_asset(path: Path) -> Path:
    return DOCS / "site-assets" / path.relative_to(ROOT)


def rewrite_url(url: str, page: Page) -> str:
    parts = urlsplit(html.unescape(url))
    if parts.scheme or parts.netloc or url.startswith(("#", "mailto:")) or not parts.path or not page.source:
        return url
    target = (ROOT / page.source).parent.joinpath(parts.path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return url
    if target.is_file() and target.suffix.lower() in IMAGE_SUFFIXES:
        return os.path.relpath(site_asset(target), output_path(page.route, page.language).parent).replace(os.sep, "/")
    route = public_route_for(target)
    if route:
        return relative_href(page, route)
    return f"{REPOSITORY_URL}/blob/main/{target.relative_to(ROOT).as_posix()}"


def render(page: Page) -> str:
    rendered = markdown.markdown(page.body, extensions=["fenced_code", "tables", "sane_lists"])
    return ATTR_URL.sub(lambda match: f'{match.group("attribute")}="{html.escape(rewrite_url(match.group("url"), page), quote=True)}"', rendered)


def shell(page: Page, body: str, status: dict) -> str:
    language_links = []
    for language, (suffix, label, _source, _title) in LANGUAGES.items():
        language_links.append(f"<strong>{label}</strong>" if language == page.language else f'<a href="{relative_href(page, page.route, language)}">{label}</a>')
    nav_labels = {"en": ("Home", "Catalog", "Installation", "Downloads"), "zh_CN": ("首页", "目录", "安装", "下载"), "ja": ("ホーム", "カタログ", "インストール", "ダウンロード")}[page.language]
    nav = "".join(f'<a href="{relative_href(page, route)}">{label}</a>' for route, label in zip((ROUTES["home"], ROUTES["catalog"], ROUTES["installation"], ROUTES["downloads"]), nav_labels))
    developer = ""
    if page.source:
        heading = {"en": "Developer resources", "zh_CN": "开发者资源", "ja": "開発者向けリソース"}[page.language]
        developer = f'<aside class="developer-resources"><h2>{heading}</h2><a href="{REPOSITORY_URL}/blob/main/{page.source}">Source on GitHub</a> · <a href="{REPOSITORY_URL}/commits/main/{page.source}">Git history</a></aside>'
    css = os.path.relpath(DOCS / "site.css", output_path(page.route, page.language).parent).replace(os.sep, "/")
    source_hash = hashlib.sha256((ROOT / page.source).read_bytes()).hexdigest() if page.source else "generated"
    status_hash = hashlib.sha256((DOCS / "project-status.json").read_bytes()).hexdigest()
    return f'''<!doctype html><html lang="{page.language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="source-sha256" content="{source_hash}"><meta name="project-status-sha256" content="{status_hash}"><title>{html.escape(page.title)}</title><link rel="stylesheet" href="{css}"></head><body><header class="site-header"><a class="repository-link" href="{REPOSITORY_URL}">Physics Software Sensors on GitHub</a><nav class="site-nav">{nav}</nav><nav class="language-nav" aria-label="Language navigation">{" <span>|</span> ".join(language_links)}</nav><p class="status-banner">{status["sensor_count"]} Sensors · {status["companion_tool_count"]} Tool · {status["public_capability_count"]} public capabilities</p></header><main>{body}{developer}</main><footer>Public reader · <a href="{REPOSITORY_URL}">Repository source of truth</a></footer></body></html>\n'''


def pages() -> list[Page]:
    result = []
    for language, (_suffix, _label, source, title) in LANGUAGES.items():
        result.append(Page(ROUTES["home"], language, title, source, source_text(source)))
        sensor_catalog = ("docs/sensor-catalog.md", "docs/sensor-catalog.zh-CN.md", "docs/sensor-catalog.ja.md")[language_index(language)]
        tool_catalog = ("docs/tool-catalog.md", "docs/tool-catalog.zh-CN.md", "docs/tool-catalog.ja.md")[language_index(language)]
        result.append(Page(ROUTES["catalog"], language, "Public Capability Catalog", sensor_catalog, "# Public Capability Catalog\n\n" + source_text(sensor_catalog) + "\n" + source_text(tool_catalog)))
        for sensor_id, route in ROUTES["sensors"].items():
            source = f"sensors/{sensor_id}/" + ("README.md", "README.zh-CN.md", "README.ja.md")[language_index(language)]
            result.append(Page(route, language, title_for(source), source, source_text(source)))
        source = "processing/vector.compose-3d/" + ("README.md", "README.zh-CN.md", "README.ja.md")[language_index(language)]
        result.append(Page(ROUTES["tools"]["vector.compose-3d"], language, title_for(source), source, source_text(source)))
        for key, paths in DOC_PAGES.items():
            source = paths[language_index(language)]
            result.append(Page(ROUTES[key], language, title_for(source), source, source_text(source)))
        for slug, (source, names) in EXAMPLES.items():
            name = names[language_index(language)]
            labels = {"en": ("Example documentation", "This small standalone example demonstrates the capability outside the original experiment application.", "Run source example"), "zh_CN": ("示例文档", "这个小型独立示例在原实验应用之外展示该能力。", "运行源码示例"), "ja": ("Example 文書", "この小さな独立 example は元の実験アプリケーションの外で capability を示します。", "source example を実行")}[language]
            body = f"# {name}\n\n## {labels[0]}\n\n{labels[1]}\n\n## {labels[2]}\n\n```bash\n# Follow the linked repository example instructions\n```\n"
            result.append(Page(ROUTES["examples"][slug], language, name, source, body))
    return result


def copy_assets() -> None:
    target = DOCS / "site-assets"
    if target.exists():
        shutil.rmtree(target)
    for base in (ROOT / "sensors", ROOT / "processing" / "vector.compose-3d", DOCS / "assets"):
        for asset in base.rglob("*"):
            if asset.is_file() and asset.suffix.lower() in IMAGE_SUFFIXES:
                destination = site_asset(asset)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(asset, destination)


def build() -> None:
    status = json.loads((DOCS / "project-status.json").read_text(encoding="utf-8"))
    copy_assets()
    for page in pages():
        destination = output_path(page.route, page.language)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(shell(page, render(page), status), encoding="utf-8")
        print(f"Wrote {destination.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        build()
        return 0
    original = {path: path.read_bytes() for path in DOCS.rglob("index.html")}
    build()
    current = {path: path.read_bytes() for path in DOCS.rglob("index.html")}
    if original != current:
        raise SystemExit("Pages are stale; run tools/build_multilingual_pages.py and commit generated output")
    print(f"PASS: {len(current)} generated Pages files are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
