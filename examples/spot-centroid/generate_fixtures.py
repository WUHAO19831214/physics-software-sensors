"""Generate deterministic synthetic spot frames; not physical experiment data."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample"
CASES = [
    ("bright", (80, 60), (20, 20, 245), 10),
    ("horizontal", (112, 60), (20, 20, 245), 10),
    ("vertical", (80, 88), (20, 20, 245), 10),
    ("dim", (80, 60), (35, 35, 155), 10),
    ("blank", None, (0, 0, 0), 0),
    ("roi-edge", (12, 60), (20, 20, 245), 10),
]


def frame(center, bgr, radius) -> np.ndarray:
    image = np.full((120, 160, 3), (18, 18, 18), dtype=np.uint8)
    if center is not None:
        cv2.circle(image, center, radius, bgr, -1, cv2.LINE_8)
    return image


def main() -> None:
    SAMPLE.mkdir(parents=True, exist_ok=True)
    manifest = {"synthetic": True, "color_order": "PNG/RGBA", "cases": []}
    for case_id, center, bgr, radius in CASES:
        filename = f"{case_id}.png"
        cv2.imwrite(str(SAMPLE / filename), frame(center, bgr, radius))
        manifest["cases"].append({"id": case_id, "file": filename, "center": center, "radius": radius})
    (SAMPLE / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {len(CASES)} synthetic spot frames")


if __name__ == "__main__":
    main()
