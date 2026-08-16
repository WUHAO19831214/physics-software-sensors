"""Compose Sensor Page PNGs from the actual OCR example results and pixel stages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent


def title(image: np.ndarray, text: str, width: int = 420) -> np.ndarray:
    height = 220
    canvas = np.full((height, width, 3), 250, dtype=np.uint8)
    scale = min((width - 20) / image.shape[1], (height - 55) / image.shape[0])
    resized = cv2.resize(image, (max(1, int(image.shape[1] * scale)), max(1, int(image.shape[0] * scale))), interpolation=cv2.INTER_NEAREST)
    x = (width - resized.shape[1]) // 2
    y = 48 + (height - 48 - resized.shape[0]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    cv2.putText(canvas, text, (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (35, 35, 35), 2, cv2.LINE_AA)
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=HERE.parents[1] / "sensors" / "ocr.number" / "assets")
    args = parser.parse_args()
    args.assets.mkdir(parents=True, exist_ok=True)
    results = json.loads((HERE / "output" / "results.json").read_text(encoding="utf-8"))
    negative = next(item for item in results if item["fixture"]["id"] == "negative")
    event = negative["event"]
    original = cv2.imread(str(HERE / "sample" / "negative.png"))
    roi = cv2.imread(str(HERE / "output" / "negative-roi.png"))
    processed = cv2.imread(str(HERE / "output" / "negative-preprocessed.png"))
    rect = negative["pixelRoi"]

    annotated = original.copy()
    cv2.rectangle(
        annotated,
        (rect["x"], rect["y"]),
        (rect["x"] + rect["width"], rect["y"] + rect["height"]),
        (30, 70, 220),
        4,
    )
    raw = event["payload"]["raw_text"].replace("\n", " ")
    value = event["measurements"][0]["value"]
    cv2.rectangle(annotated, (0, 258), (800, 300), (248, 248, 248), -1)
    cv2.putText(
        annotated,
        f"Tesseract rawText={raw!r}  parsed value={value}",
        (22, 286),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.66,
        (25, 120, 25),
        2,
        cv2.LINE_AA,
    )
    cv2.imwrite(str(args.assets / "overview.png"), annotated)

    panels = [title(original, "1  Original synthetic screen frame"), title(roi, "2  Pixel ROI crop"), title(processed, "3  Preprocessed ROI")]
    processing = cv2.hconcat(panels)
    footer = np.full((70, processing.shape[1], 3), 250, dtype=np.uint8)
    cv2.putText(footer, f"4  Tesseract.js rawText={raw!r}    5  parsed value={value}", (22, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 120, 25), 2, cv2.LINE_AA)
    cv2.imwrite(str(args.assets / "processing.png"), cv2.vconcat([processing, footer]))
    (args.assets / "demo-result.json").write_text(json.dumps(negative, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote OCR demo assets to {args.assets}")


if __name__ == "__main__":
    main()
