"""Generate synthetic screen-frame PNG fixtures for the standalone OCR example."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample"
ROI = {"x": 0.33, "y": 0.39, "width": 0.34, "height": 0.31}
CASES = [
    ("positive", "+1.25", 1.25, "success"),
    ("negative", "-2.33", -2.33, "success"),
    ("zero", "0.00", 0.0, "success"),
    ("blank", "", None, "parse-failure"),
    ("alphabetic", "READY", None, "parse-failure"),
    ("engine-failure", "9.99", None, "recognition-failure"),
]


def make_frame(display_text: str) -> np.ndarray:
    image = np.full((300, 800, 3), (236, 239, 242), dtype=np.uint8)
    cv2.putText(image, "SYNTHETIC SCREEN FRAME - NOT DEVICE DATA", (32, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (45, 45, 45), 2)
    cv2.rectangle(image, (85, 76), (715, 265), (115, 115, 115), 3)
    cv2.putText(image, "DISPLAY CHANNEL", (112, 112), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (70, 70, 70), 2)
    cv2.rectangle(image, (240, 99), (560, 221), (250, 250, 250), -1)
    cv2.rectangle(image, (240, 99), (560, 221), (65, 65, 65), 2)
    if display_text:
        scale = 2.25 if len(display_text) <= 5 else 1.55
        thickness = 5 if len(display_text) <= 5 else 4
        size, _ = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_DUPLEX, scale, thickness)
        x = 400 - size[0] // 2
        y = 166 + size[1] // 2
        cv2.putText(image, display_text, (x, y), cv2.FONT_HERSHEY_DUPLEX, scale, (15, 15, 15), thickness, cv2.LINE_AA)
    cv2.putText(image, "ROI contains screen pixels only", (263, 247), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 80, 80), 1)
    return image


def main() -> None:
    SAMPLE.mkdir(parents=True, exist_ok=True)
    manifest = {"synthetic": True, "roi": ROI, "cases": []}
    for case_id, display_text, expected_value, expected_outcome in CASES:
        filename = f"{case_id}.png"
        cv2.imwrite(str(SAMPLE / filename), make_frame(display_text))
        manifest["cases"].append(
            {
                "id": case_id,
                "file": filename,
                "displayText": display_text,
                "expectedValue": expected_value,
                "expectedOutcome": expected_outcome,
            }
        )
    (SAMPLE / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {len(CASES)} synthetic OCR frames to {SAMPLE}")


if __name__ == "__main__":
    main()
