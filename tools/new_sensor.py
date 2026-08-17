#!/usr/bin/env python3
"""Generate a truthful, contract-only Sensor intake scaffold."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")
SECTIONS = [
    "name", "description", "physics-use", "measurement", "sources", "how-it-works",
    "input", "output", "demo", "example", "distribution", "evidence", "maturity",
    "limitations", "benchmark", "provenance",
]


def page(language: str, sensor_id: str, name: str) -> str:
    labels = {
        "en": ("English", "Name", "Planning scaffold only. Replace every TODO after an ACCEPT decision."),
        "zh_CN": ("简体中文", "名称", "仅为规划骨架。只有 ACCEPT 后才能逐项解决 TODO。"),
        "ja": ("日本語", "名称", "計画用 scaffold のみです。ACCEPT 後に各 TODO を解決してください。"),
    }
    current, name_heading, warning = labels[language]
    switch = {
        "en": "**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)",
        "zh_CN": "[English](README.md) | **简体中文** | [日本語](README.ja.md)",
        "ja": "[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**",
    }[language]
    headings = {
        "en": ["Name", "One-line description", "Typical physics experiment use", "What it actually measures", "Source projects", "How it works", "Input", "Output", "Demo", "Minimal example", "Distribution / Download", "Evidence level", "Maturity", "Known limitations", "Benchmark", "Provenance"],
        "zh_CN": ["名称", "一句话介绍", "典型物理实验用途", "它实际测到什么", "来源项目", "工作原理", "输入", "输出", "Demo", "最小示例", "分发 / 下载", "证据等级", "成熟度", "已知限制", "Benchmark", "来源追溯"],
        "ja": ["名称", "一文での説明", "代表的な物理実験での用途", "実際に観測するもの", "ソースプロジェクト", "動作原理", "入力", "出力", "Demo", "最小 example", "配布 / Download", "エビデンスレベル", "成熟度", "既知の制限", "Benchmark", "来歴"],
    }[language]
    lines = [f"# {name}", "", switch, "", f"Sensor ID: `{sensor_id}` · Implementation version: `0.1.0` · Maturity: `contract-only` · Evidence: `E0` · Release: `unreleased`", "", f"> {warning}", ""]
    for marker, heading in zip(SECTIONS, headings, strict=True):
        lines.extend([f"<!-- section:{marker} -->", f"## {heading}"])
        if marker == "name":
            lines.append(name)
        elif marker == "maturity":
            lines.append("`contract-only` / manifest `planned`; no implementation is claimed.")
        elif marker == "evidence":
            lines.append("`E0` planned contract only; no runtime evidence is claimed.")
        elif marker == "provenance":
            lines.append("TODO: pin repository, full commit SHA, source paths and symbols in SOURCE.md before extraction.")
        elif marker in {"demo", "benchmark"}:
            lines.append("TODO / pending. Do not fabricate evidence or results.")
        else:
            lines.append("TODO: complete from the accepted Sensor Proposal and fixed source evidence.")
        lines.append("")
    return "\n".join(lines)


def manifest(sensor_id: str, name: str, category: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "id": sensor_id,
        "name_zh": f"TODO: {name} Chinese name",
        "name_en": name,
        "category": "source" if category == "capture" else "processor",
        "maturity": "planned",
        "implementation_status": "contract-only",
        "version": "0.1.0",
        "input_kinds": [],
        "output_kinds": ["TODO.pending-output-kind"],
        "capabilities": ["TODO-pending-capability-review"],
        "source_references": [],
        "evidence_level": "documented-prototype",
        "license_review": "pending",
        "known_boundaries": ["Scaffold only; source, implementation, benchmark and evidence are pending."],
        "owners": ["TODO-owner"],
    }


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def update_document_map(root: Path, sensor_id: str) -> None:
    path = root / "docs/i18n/document-map.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": "1.0.0", "languages": ["en", "zh_CN", "ja"], "documents": {}, "sensors": {}, "sensor_sections": SECTIONS}
    data.setdefault("sensors", {})[sensor_id] = {
        "en": f"sensors/{sensor_id}/README.md",
        "zh_CN": f"sensors/{sensor_id}/README.zh-CN.md",
        "ja": f"sensors/{sensor_id}/README.ja.md",
        "version": "0.1.0",
        "maturity": "contract-only",
        "evidence": "E0",
        "release": "unreleased",
    }
    write(path, json.dumps(data, ensure_ascii=False, indent=2))


def generate(root: Path, sensor_id: str, name: str, language: str, category: str) -> Path:
    if not ID_PATTERN.fullmatch(sensor_id):
        raise ValueError("Sensor ID must match <domain>.<capability> using lowercase words and optional hyphens")
    sensor_root = root / "sensors" / sensor_id
    if sensor_root.exists():
        raise FileExistsError(f"refusing to overwrite {sensor_root}")
    write(sensor_root / "README.md", page("en", sensor_id, name))
    write(sensor_root / "README.zh-CN.md", page("zh_CN", sensor_id, f"TODO: {name} 中文名称"))
    write(sensor_root / "README.ja.md", page("ja", sensor_id, f"TODO: {name} 日本語名"))
    write(sensor_root / "sensor.json", json.dumps(manifest(sensor_id, name, category), ensure_ascii=False, indent=2))
    write(sensor_root / "SOURCE.md", f"# {name} provenance\n\nStatus: pending.\n\n- Proposal: `templates/SENSOR_PROPOSAL.md`\n- Source repository: TODO\n- Source commit: TODO — full SHA required; no placeholder SHA is generated.\n- Source paths/symbols: TODO\n- Extraction/algorithm changes: TODO\n- Source-output comparison: TODO\n")
    write(sensor_root / "CHANGELOG.md", f"# Changelog\n\n## 0.1.0 — planned\n\n- Contract-only scaffold generated; no implementation or evidence claimed.\n")
    write(sensor_root / "assets/README.md", "# Assets\n\nDemo asset pending. Do not add fabricated or uncleared assets.\n")
    write(sensor_root / "benchmarks/README.md", "# Benchmark\n\nProtocol, dataset, metrics and result are pending. Do not report zero for unmeasured values.\n")
    write(sensor_root / "examples/README.md", "# Example\n\nRunnable standalone example pending implementation.\n")
    write(sensor_root / "implementation/TODO.md", f"# {language} implementation TODO\n\nCategory hint: `{category}`. Review package placement after ACCEPT; the generator does not create algorithm code or choose a complex module structure.\n")
    update_document_map(root, sensor_id)
    return sensor_root


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--id", required=True, dest="sensor_id")
    value.add_argument("--name", required=True)
    value.add_argument("--language", required=True, choices=("python", "typescript"))
    value.add_argument("--category", choices=("capture", "ocr", "tracking", "other"), default="other")
    value.add_argument("--output-root", type=Path, default=ROOT)
    value.add_argument("--dry-run", action="store_true")
    return value


def main() -> int:
    args = parser().parse_args()
    if not ID_PATTERN.fullmatch(args.sensor_id):
        parser().error("--id must match <domain>.<capability> using lowercase words and optional hyphens")
    target = args.output_root.resolve() / "sensors" / args.sensor_id
    if args.dry_run:
        print(f"DRY RUN: would create contract-only scaffold at {target} and update docs/i18n/document-map.json")
        return 0
    try:
        generated = generate(args.output_root.resolve(), args.sensor_id, args.name, args.language, args.category)
    except (ValueError, FileExistsError) as exc:
        parser().error(str(exc))
    print(f"Created contract-only scaffold: {generated}")
    print("Source, license, implementation, demo and benchmark remain pending TODOs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
