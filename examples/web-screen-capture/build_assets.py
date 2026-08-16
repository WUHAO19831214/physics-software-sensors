"""Render capture metadata and permission-boundary evidence panels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def panel(title: str, lines: list[str], height: int = 360) -> np.ndarray:
    image = np.full((height, 820, 3), (248, 248, 248), dtype=np.uint8)
    cv2.putText(image, title, (28, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (28, 28, 28), 2, cv2.LINE_AA)
    for index, line in enumerate(lines):
        cv2.putText(image, line, (34, 88 + index * 34), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (55, 55, 55), 1, cv2.LINE_AA)
    return image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish-assets", action="store_true")
    args = parser.parse_args()
    packet = json.loads((HERE / "output" / "frame-packet.json").read_text(encoding="utf-8"))
    capture = packet["payload"]["capture"]
    metadata = panel(
        "ScreenCaptureSource FramePacket (recorded replay)",
        [
            f"frame_id: {packet['frame_id']}",
            f"run_id: {packet['run_id']}",
            f"observed_at: {packet['observed_at']}",
            f"monotonic_ns: {packet['monotonic_ns']}",
            f"size/color: {packet['media']['width']} x {packet['media']['height']} / RGBA",
            f"requested sampling interval: {capture['requested']['sampling_interval_ms']} ms",
            "actual interval: unavailable from a single frame (null)",
            "evidence: synthetic recorded screen replay (L1)",
        ],
    )
    permission = panel(
        "Browser permission boundary (manual smoke path)",
        [
            "1. User clicks Start screen capture",
            "2. start() calls getDisplayMedia",
            "3. Browser chooser: screen / window / tab",
            "4. User accepts or denies; denial is an explicit error",
            "5. Track 'ended' means user/browser stopped sharing",
            "6. Reload normally requires authorization again",
            "Screen pixels are NOT a device SDK or internal application data",
        ],
    )
    output = HERE / "output"
    cv2.imwrite(str(output / "frame-packet-metadata.png"), metadata)
    cv2.imwrite(str(output / "permission-boundary.png"), permission)
    if args.publish_assets:
        assets = ROOT / "sensors" / "screen.capture" / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        source_image = cv2.imread(str(HERE / "sample" / "recorded-screen.png"))
        cv2.imwrite(str(assets / "captured-screen-frame.png"), source_image)
        cv2.imwrite(str(assets / "frame-packet-metadata.png"), metadata)
        cv2.imwrite(str(assets / "permission-boundary.png"), permission)
        (assets / "replay-frame-packet.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
