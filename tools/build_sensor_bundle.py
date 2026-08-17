#!/usr/bin/env python3
"""Build documentation/example sensor bundles without copying package core code."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "WUHAO19831214/physics-software-sensors"
CONFIG = {
    "camera.capture": {"language": "python", "entrypoint": "physics_sensors.capture.CameraSource", "example": "examples/python-camera-capture", "requires": ["physics-software-sensors==0.5.0"], "install": "physics-software-sensors[camera-opencv]==0.5.0"},
    "screen.capture": {"language": "typescript", "entrypoint": "@physics-software-sensors/core.ScreenCaptureSource", "example": "examples/web-screen-capture", "requires": ["@physics-software-sensors/core==0.3.0"], "install": "physics-software-sensors-core-0.3.0.tgz"},
    "ocr.number": {"language": "typescript", "entrypoint": "@physics-software-sensors/core.NumberOCRSensor", "example": "examples/web-number-ocr", "requires": ["@physics-software-sensors/core==0.3.0"], "install": "physics-software-sensors-core-0.3.0.tgz"},
    "tracker.color-marker": {"language": "python", "entrypoint": "physics_sensors.tracking.ColorMarkerSensor", "example": "examples/python-color-marker", "requires": ["physics-software-sensors==0.5.0"], "install": "physics-software-sensors[color-marker]==0.5.0"},
    "tracker.spot-centroid": {"language": "python", "entrypoint": "physics_sensors.tracking.SpotCentroidSensor", "example": "examples/spot-centroid", "requires": ["physics-software-sensors==0.5.0"], "install": "physics-software-sensors[classical-trackers]==0.5.0"},
    "tracker.template": {"language": "python", "entrypoint": "physics_sensors.tracking.TemplateTrackerSensor", "example": "examples/python-template-tracker", "requires": ["physics-software-sensors==0.5.0"], "install": "physics-software-sensors[classical-trackers]==0.5.0"},
    "tracker.yolo": {"language": "python", "entrypoint": "physics_sensors.tracking.YoloTrackerSensor", "example": "examples/python-yolo-tracker", "requires": ["physics-software-sensors[yolo-recorded]==0.5.0"], "install": "physics-software-sensors[yolo-recorded]==0.5.0 (recorded); physics-software-sensors[yolo-runtime]==0.5.0 only with reviewed local artifact"},
}


def git(*args: str) -> str:
    return subprocess.run(("git", *args), cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def tracked_files(prefix: str) -> list[Path]:
    output = git("ls-files", prefix)
    return [ROOT / line for line in output.splitlines() if line and (ROOT / line).is_file()]


def write_bytes(archive: zipfile.ZipFile, name: str, value: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, value)


def build_bundle(sensor_id: str, output: Path, git_sha: str, evidence: str) -> dict[str, Any]:
    manifest = json.loads((ROOT / f"sensors/{sensor_id}/sensor.json").read_text(encoding="utf-8"))
    config = CONFIG[sensor_id]
    bundle = {
        "schema_version": "1.0.0",
        "sensor_id": sensor_id,
        "sensor_version": manifest["version"],
        "contract_version": "1.0.0",
        "implementation_language": config["language"],
        "requires": config["requires"],
        "entrypoint": config["entrypoint"],
        "source_page": f"https://github.com/{REPOSITORY}/tree/{git_sha}/sensors/{sensor_id}",
        "license": "MIT for this repository; historical source and third-party terms remain separate",
        "evidence_level": evidence,
        "git_sha": git_sha,
        "contents": "Sensor Page, manifest, provenance, curated assets, example and install/dependency metadata; package core is not copied",
    }
    install = (
        f"# Install {sensor_id}\n\n"
        "This bundle is a documentation/example snapshot, not a forked implementation package. "
        f"It requires `{config['install']}`. Install the wheel/tgz produced by the same release dry run, "
        "then follow `example/README.md`. Public core code is intentionally not copied into this bundle.\n"
    ).encode()
    dependencies = json.dumps({
        "sensor_id": sensor_id,
        "required_packages": config["requires"],
        "install_spec": config["install"],
        "bundled_package_code": False,
        "runtime_download_boundary": "No YOLO weight is included or downloaded. Tesseract.js may fetch/cache language data when its real runtime is used." if sensor_id in {"ocr.number", "tracker.yolo"} else "No runtime model download is initiated by this bundle.",
    }, ensure_ascii=False, indent=2).encode() + b"\n"
    manifest_bytes = json.dumps(bundle, ensure_ascii=False, indent=2).encode() + b"\n"
    filename = f"{sensor_id}-{manifest['version']}.zip"
    target = output / filename
    sensor_root = ROOT / "sensors" / sensor_id
    example_root = ROOT / str(config["example"])
    with zipfile.ZipFile(target, "w") as archive:
        for path in tracked_files(f"sensors/{sensor_id}"):
            write_bytes(archive, f"sensor/{path.relative_to(sensor_root).as_posix()}", path.read_bytes())
        for path in tracked_files(str(config["example"])):
            write_bytes(archive, f"example/{path.relative_to(example_root).as_posix()}", path.read_bytes())
        write_bytes(archive, "INSTALL.md", install)
        write_bytes(archive, "DEPENDENCIES.json", dependencies)
        write_bytes(archive, "BUNDLE.json", manifest_bytes)
    data = target.read_bytes()
    return {"sensor_id": sensor_id, "sensor_version": manifest["version"], "filename": filename, "sha256": sha256_bytes(data), "bytes": len(data), "evidence_level": evidence}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "sensor-bundles")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    git_sha = git("rev-parse", "HEAD")
    registry = json.loads((ROOT / "benchmarks/results/index.json").read_text(encoding="utf-8"))
    evidence = {entry["sensor_id"]: entry["evidence_level"] for entry in registry["entries"]}
    bundles = [build_bundle(sensor_id, output, git_sha, evidence[sensor_id]) for sensor_id in sorted(CONFIG)]
    index = {"schema_version": "1.0.0", "status": "dry-run-not-published", "git_sha": git_sha, "bundles": bundles}
    (output / "manifest.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"built {len(bundles)} sensor bundles; manifest: {output / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
