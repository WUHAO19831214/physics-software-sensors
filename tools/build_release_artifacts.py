#!/usr/bin/env python3
"""Build local wheel/tgz release candidates and write a non-publishing manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def command(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_record(path: Path, package: str, version: str, kind: str) -> dict[str, Any]:
    return {
        "filename": path.name,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "package": package,
        "package_version": version,
        "artifact_type": kind,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    python_metadata = tomllib.loads((ROOT / "packages/python/pyproject.toml").read_text(encoding="utf-8"))["project"]
    typescript_metadata = json.loads((ROOT / "packages/typescript/package.json").read_text(encoding="utf-8"))
    git_sha = command("git", "rev-parse", "HEAD")

    with tempfile.TemporaryDirectory(prefix="physics-sensors-release-dry-run-") as temporary:
        build_dir = Path(temporary)
        wheel_dir = build_dir / "wheel"
        npm_dir = build_dir / "npm"
        wheel_dir.mkdir()
        npm_dir.mkdir()
        subprocess.run(
            (sys.executable, "-m", "pip", "wheel", "packages/python", "--no-deps", "--wheel-dir", str(wheel_dir)),
            cwd=ROOT,
            check=True,
        )
        subprocess.run(("npm", "run", "build"), cwd=ROOT / "packages/typescript", check=True)
        subprocess.run(("npm", "pack", "--pack-destination", str(npm_dir)), cwd=ROOT / "packages/typescript", check=True)
        wheels = sorted(wheel_dir.glob("*.whl"))
        tarballs = sorted(npm_dir.glob("*.tgz"))
        if len(wheels) != 1 or len(tarballs) != 1:
            raise RuntimeError("release dry run must produce exactly one wheel and one npm tgz")
        copied_wheel = Path(shutil.copy2(wheels[0], output / wheels[0].name))
        copied_tgz = Path(shutil.copy2(tarballs[0], output / tarballs[0].name))

    manifest = {
        "schema_version": "1.0.0",
        "release_status": "dry-run-not-published",
        "git_sha": git_sha,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "build_environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "node": command("node", "--version"),
            "npm": command("npm", "--version"),
        },
        "artifacts": [
            artifact_record(copied_wheel, str(python_metadata["name"]), str(python_metadata["version"]), "python-wheel"),
            artifact_record(copied_tgz, str(typescript_metadata["name"]), str(typescript_metadata["version"]), "npm-tarball"),
        ],
        "limitations": [
            "Artifacts were built locally and were not uploaded to PyPI, npm, or GitHub Releases.",
            "The npm package remains private=true and is a release candidate only.",
            "No YOLO model artifact is included or downloaded.",
        ],
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(manifest['artifacts'])} release candidates; manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
