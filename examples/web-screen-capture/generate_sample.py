"""Generate a clearly labelled synthetic recorded-screen fixture."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


HERE = Path(__file__).resolve().parent


def main() -> None:
    image = np.full((300, 800, 3), (234, 238, 242), dtype=np.uint8)
    cv2.putText(image, "SYNTHETIC SHARED-WINDOW PIXELS", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.78, (35, 35, 35), 2)
    cv2.putText(image, "recorded replay - not a source-project screenshot", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (65, 65, 65), 1)
    cv2.rectangle(image, (85, 82), (715, 264), (105, 105, 105), 3)
    cv2.putText(image, "DISPLAY CHANNEL", (110, 116), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (65, 65, 65), 2)
    cv2.rectangle(image, (240, 118), (560, 211), (250, 250, 250), -1)
    cv2.rectangle(image, (240, 118), (560, 211), (55, 55, 55), 2)
    cv2.putText(image, "-2.33", (287, 188), cv2.FONT_HERSHEY_DUPLEX, 2.2, (12, 12, 12), 5, cv2.LINE_AA)
    cv2.putText(image, "screen.capture outputs pixels; OCR is downstream", (160, 246), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (70, 70, 70), 1)
    target = HERE / "sample" / "recorded-screen.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(target), image)
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
