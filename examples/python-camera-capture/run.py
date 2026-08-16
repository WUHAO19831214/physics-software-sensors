"""Standalone CameraSource replay, asset generator, and opt-in hardware smoke test."""

from __future__ import annotations

import argparse
import asyncio
import json
import platform
from pathlib import Path

import cv2
import numpy as np

from physics_sensors.capture import (
    BackendFrame,
    CameraSource,
    ImageSequenceCameraBackend,
    OpenCVCameraBackend,
)
from physics_sensors.core import SensorContext


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = HERE / "output"
ASSETS = ROOT / "sensors" / "camera.capture" / "assets"


def scene(sequence: int) -> np.ndarray:
    image = np.full((360, 640, 3), (240, 242, 244), dtype=np.uint8)
    cv2.putText(image, "SYNTHETIC RECORDED CAMERA FRAME", (34, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (34, 34, 34), 2)
    cv2.putText(image, "L1 deterministic replay - not a hardware claim", (34, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (65, 65, 65), 1)
    cv2.rectangle(image, (54, 112), (586, 310), (155, 155, 155), 2)
    for x in range(78, 570, 70):
        cv2.line(image, (x, 270), (x, 286), (80, 80, 80), 2)
    cv2.circle(image, (160 + 100 * sequence, 220), 24, (0, 210, 255), -1, cv2.LINE_AA)
    cv2.putText(image, f"frame {sequence}", (510, 338), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (55, 55, 55), 1)
    return image


def text_panel(title: str, lines: list[str], width: int = 760, height: int = 360) -> np.ndarray:
    panel = np.full((height, width, 3), (248, 248, 248), dtype=np.uint8)
    cv2.putText(panel, title, (28, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (30, 30, 30), 2, cv2.LINE_AA)
    y = 88
    for line in lines:
        cv2.putText(panel, line, (32, y), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (55, 55, 55), 1, cv2.LINE_AA)
        y += 34
    return panel


async def replay(publish_assets: bool) -> None:
    frames = [
        BackendFrame(
            pixels=scene(sequence),
            width=640,
            height=360,
            color_space="BGR",
            media_type="image/png",
            source_timestamp=sequence / 20,
            observed_at=f"2026-08-16T13:00:00.{sequence * 50:03d}Z",
            monotonic_ns=4_000_000_000 + sequence * 50_000_000,
            dropped_since_last=1 if sequence == 2 else 0,
            artifact_uri=f"recorded://camera-demo/{sequence}.png",
            quality_flags=("synthetic-fixture", "recorded-replay"),
        )
        for sequence in range(3)
    ]
    source = CameraSource(ImageSequenceCameraBackend(frames, nominal_fps=20, device_name="synthetic-camera-sequence"))
    source.configure({"width": 1280, "height": 720, "requested_fps": 30})
    await source.start(SensorContext.minimal("camera-capture-standalone-demo"))
    output = [frame async for frame in source.read()]
    await source.stop()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    metadata = [dict(frame.metadata) for frame in output]
    (OUTPUT / "frame-packets.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    captured = output[0].pixels
    cv2.imwrite(str(OUTPUT / "captured-frame.png"), captured)
    second_capture = output[1].metadata["payload"]["capture"]
    metadata_panel = text_panel(
        "FramePacket metadata (actual CameraSource output)",
        [
            f"frame_id: {output[1].frame_id}",
            f"run_id: {output[1].run_id}",
            f"observed_at: {output[1].metadata['observed_at']}",
            f"monotonic_ns: {output[1].metadata['monotonic_ns']}",
            f"source_timestamp: {output[1].metadata['source_timestamp']} s",
            "media: 640 x 360 / BGR / orientation 0 / mirrored false",
            f"measured_fps: {second_capture['actual']['measured_fps']:.1f}",
            "evidence: synthetic recorded replay (L1)",
        ],
    )
    backend_panel = text_panel(
        "Backend/device evidence (requested is not actual)",
        [
            "backend: image-sequence",
            "device: synthetic-camera-sequence",
            "requested: 1280 x 720 @ 30 fps",
            "actual frame: 640 x 360",
            "backend nominal: 20 fps",
            "measured delivery: 20 fps",
            "dropped_since_last on frame 2: 1",
            "real-device compatibility: NOT TESTED by this replay",
        ],
    )
    cv2.imwrite(str(OUTPUT / "frame-packet-metadata.png"), metadata_panel)
    cv2.imwrite(str(OUTPUT / "backend-information.png"), backend_panel)
    if publish_assets:
        ASSETS.mkdir(parents=True, exist_ok=True)
        for filename, image in (
            ("captured-frame.png", captured),
            ("frame-packet-metadata.png", metadata_panel),
            ("backend-information.png", backend_panel),
        ):
            cv2.imwrite(str(ASSETS / filename), image)
        (ASSETS / "replay-frame-packets.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"replayed {len(output)} frames; measured={source.health().actual_rate_hz:.1f} fps; dropped={source.health().dropped_count}")


async def hardware(device: int) -> None:
    source = CameraSource(OpenCVCameraBackend(device))
    source.configure({"width": 1280, "height": 720, "requested_fps": 30})
    await source.start(SensorContext.minimal("camera-hardware-smoke"))
    frame = await anext(source.read())
    await source.stop()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUTPUT / "hardware-frame.png"), frame.pixels)
    report = {
        "evidence": "manual-real-device-smoke",
        "device_index": device,
        "platform": platform.platform(),
        "frame_packet": dict(frame.metadata),
        "claim_boundary": "one-frame smoke test; not a compatibility matrix or timing validation",
    }
    (OUTPUT / "hardware-smoke.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"captured one real-device frame at {frame.width}x{frame.height}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", type=int, help="opt in to a real OpenCV camera device index")
    parser.add_argument("--publish-assets", action="store_true")
    args = parser.parse_args()
    asyncio.run(hardware(args.device) if args.device is not None else replay(args.publish_assets))


if __name__ == "__main__":
    main()
