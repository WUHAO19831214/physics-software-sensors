#!/usr/bin/env python3
"""Build the complete, non-publishing experimental GitHub Release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = re.compile(r"^v0\.[0-9]+\.[0-9]+$")
SENSOR_IDS = {
    "camera.capture",
    "screen.capture",
    "ocr.number",
    "tracker.color-marker",
    "tracker.spot-centroid",
    "tracker.template",
    "tracker.yolo",
}


def command(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True).stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, artifact_type: str, **extra: Any) -> dict[str, Any]:
    return {
        "filename": path.name,
        "type": artifact_type,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        **extra,
    }


def validate_output(output: Path) -> dict[str, Any]:
    manifest = json.loads((output / "release-manifest.json").read_text(encoding="utf-8"))
    artifacts = manifest["artifacts"]
    if len(artifacts) != 9:
        raise RuntimeError("release candidate must contain one wheel, one tgz and seven sensor bundles")
    if {item.get("sensor_id") for item in artifacts if item["type"] == "sensor-bundle"} != SENSOR_IDS:
        raise RuntimeError("release candidate must contain exactly the seven known sensor bundles")
    for item in artifacts:
        path = output / item["filename"]
        if not path.is_file() or sha256(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise RuntimeError(f"artifact integrity mismatch: {item['filename']}")
    sums = {}
    for line in (output / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, filename = line.split("  ", 1)
        sums[filename] = digest
    expected = {item["filename"] for item in artifacts} | {"release-manifest.json"}
    if set(sums) != expected:
        raise RuntimeError("SHA256SUMS must cover all artifacts and release-manifest.json")
    for filename, digest in sums.items():
        if sha256(output / filename) != digest:
            raise RuntimeError(f"SHA256SUMS mismatch: {filename}")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-version", default="v0.6.0")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not RELEASE_VERSION.fullmatch(args.release_version):
        raise SystemExit("release version must be a pre-stable tag such as v0.6.0")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise SystemExit(f"output directory must be empty: {output}")

    git_sha = command("git", "rev-parse", "HEAD")
    commit_epoch = int(command("git", "show", "-s", "--format=%ct", git_sha))
    generated_at = datetime.fromtimestamp(commit_epoch, timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    deterministic_env = os.environ.copy()
    deterministic_env.update({"SOURCE_DATE_EPOCH": str(commit_epoch), "PYTHONHASHSEED": "0"})

    with tempfile.TemporaryDirectory(prefix="physics-sensors-experimental-release-") as temporary:
        work = Path(temporary)
        package_dir = work / "packages"
        bundle_dir = work / "bundles"
        subprocess.run(
            [sys.executable, str(ROOT / "tools/build_release_artifacts.py"), "--output", str(package_dir)],
            cwd=ROOT,
            env=deterministic_env,
            check=True,
        )
        subprocess.run(
            [sys.executable, str(ROOT / "tools/build_sensor_bundle.py"), "--output", str(bundle_dir)],
            cwd=ROOT,
            env=deterministic_env,
            check=True,
        )
        package_manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8"))
        bundle_manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
        if package_manifest["git_sha"] != git_sha or bundle_manifest["git_sha"] != git_sha:
            raise RuntimeError("child artifact manifests do not match release candidate SHA")

        artifacts: list[dict[str, Any]] = []
        for item in package_manifest["artifacts"]:
            source = package_dir / item["filename"]
            target = Path(shutil.copy2(source, output / source.name))
            kind = "python-wheel" if item["artifact_type"] == "python-wheel" else "typescript-tgz"
            artifacts.append(record(target, kind, package=item["package"], package_version=item["package_version"]))
        for item in bundle_manifest["bundles"]:
            source = bundle_dir / item["filename"]
            target = Path(shutil.copy2(source, output / source.name))
            artifacts.append(record(
                target,
                "sensor-bundle",
                sensor_id=item["sensor_id"],
                sensor_version=item["sensor_version"],
                evidence_level=item["evidence_level"],
            ))

    artifacts.sort(key=lambda item: (item["type"], item["filename"]))
    manifest = {
        "schema_version": "1.0.0",
        "release_status": "release-candidate-not-published",
        "release_version": args.release_version,
        "release_title": f"Physics Software Sensors {args.release_version} — Experimental",
        "git_sha": git_sha,
        "contracts": {"sensor_event": "1.0.0", "frame_packet": "1.0.0"},
        "packages": {"python": "0.5.0", "typescript": "0.3.0"},
        "build_environment": {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python": platform.python_version(),
            "node": command("node", "--version"),
            "npm": command("npm", "--version"),
            "source_date_epoch": commit_epoch,
        },
        "build_timestamp": generated_at,
        "release_evidence_note": "Experimental E1-E3 evidence only; no E4 real-device validation, E5 downstream validation or metrology claim.",
        "artifacts": artifacts,
        "limitations": [
            "Release candidate only: no tag, GitHub Release, PyPI publication or npm registry publication was created.",
            "All seven sensors remain experimental.",
            "No YOLO model weight is included or downloaded; real inference requires a separately reviewed local ModelArtifact.",
            "Historical source repository license state remains pending/NOASSERTION where documented.",
        ],
    }
    manifest_path = output / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksum_paths = sorted((output / item["filename"] for item in artifacts), key=lambda path: path.name) + [manifest_path]
    (output / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in checksum_paths),
        encoding="utf-8",
    )
    validate_output(output)
    print(f"built experimental release candidate {args.release_version}: {output}")
    print(f"artifacts: {len(artifacts)}; manifest and SHA256SUMS verified; nothing published")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
