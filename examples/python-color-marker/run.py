"""Run the standalone ColorMarkerSensor and generate reproducible demo output."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

import cv2
import numpy as np

from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import ColorMarkerSensor


HERE = Path(__file__).resolve().parent
DEFAULT_SAMPLE = HERE / "sample" / "representative-input.png"
DEFAULT_OUTPUT = HERE / "output"
RUN_ID = "color-marker-standalone-demo"


def synthetic_scene(center: tuple[int, int] | None) -> np.ndarray:
    """Create a clearly labelled synthetic apparatus-like scene."""
    frame = np.full((320, 480, 3), (242, 242, 238), dtype=np.uint8)
    cv2.rectangle(frame, (35, 68), (445, 255), (210, 210, 205), 2)
    cv2.line(frame, (60, 190), (420, 190), (80, 80, 80), 3)
    for x in range(60, 421, 40):
        cv2.line(frame, (x, 185), (x, 197), (80, 80, 80), 1)
    cv2.putText(frame, "SYNTHETIC COLOR-MARKER INPUT", (36, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.66, (45, 45, 45), 2)
    cv2.putText(frame, "pixel ruler (not a physical calibration)", (62, 224), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (75, 75, 75), 1)
    if center is not None:
        cv2.circle(frame, center, 24, (0, 225, 255), -1, cv2.LINE_AA)
        cv2.circle(frame, center, 24, (30, 80, 100), 2, cv2.LINE_AA)
    return frame


def packet(frame: np.ndarray, sequence: int) -> dict:
    frame_id = str(uuid5(NAMESPACE_URL, f"{RUN_ID}:{sequence}"))
    return {
        "schema_version": "1.0.0",
        "frame_id": frame_id,
        "run_id": RUN_ID,
        "source_sensor_id": "camera.capture",
        "sequence": sequence,
        "observed_at": f"2026-08-16T09:00:0{sequence}.000Z",
        "monotonic_ns": 1_000_000_000 + sequence * 1_000_000,
        "source_timestamp": float(sequence),
        "media": {
            "kind": "image-frame",
            "media_type": "image/raw-bgr",
            "width": frame.shape[1],
            "height": frame.shape[0],
            "color_space": "BGR",
            "orientation": "0",
            "mirrored": False,
        },
        "artifact": {
            "uri": f"file://synthetic/color-marker/{sequence}.png",
            "media_type": "image/png",
            "sha256": "0" * 64,
            "bytes": int(frame.nbytes),
        },
        "quality": {"dropped_since_last": 0, "flags": ["synthetic-fixture"]},
    }


def add_title(image: np.ndarray, title: str) -> np.ndarray:
    titled = cv2.copyMakeBorder(image, 42, 0, 0, 0, cv2.BORDER_CONSTANT, value=(250, 250, 250))
    cv2.putText(titled, title, (14, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.64, (35, 35, 35), 2, cv2.LINE_AA)
    return titled


def annotate(frame: np.ndarray, event: dict) -> np.ndarray:
    output = frame.copy()
    source = event["payload"]["source_raw"]
    status = str(event["status"])
    color = (20, 145, 30) if status == "ok" else (20, 20, 210)
    if source["ok"]:
        center = (int(round(source["center_x"])), int(round(source["center_y"])))
        radius = int(round(source["marker_radius"]))
        cv2.circle(output, center, radius, color, 3, cv2.LINE_AA)
        cv2.drawMarker(output, center, color, cv2.MARKER_CROSS, 24, 2)
        cv2.putText(
            output,
            f"center=({source['center_x']:.1f}, {source['center_y']:.1f}) px",
            (center[0] + 30, center[1] - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            color,
            2,
            cv2.LINE_AA,
        )
    cv2.rectangle(output, (0, 278), (480, 320), (245, 245, 245), -1)
    cv2.putText(output, f"ColorMarkerSensor status: {status}", (18, 305), cv2.FONT_HERSHEY_SIMPLEX, 0.64, color, 2)
    return output


async def execute(output_dir: Path, sample_path: Path) -> list[dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    frames = [synthetic_scene((165, 160)), synthetic_scene(None), synthetic_scene((315, 160))]
    cv2.imwrite(str(sample_path), frames[0])

    sensor = ColorMarkerSensor()
    sensor.configure({"hsv_lower": [20, 90, 90], "hsv_upper": [45, 255, 255], "min_area": 200})
    await sensor.start(SensorContext.minimal(RUN_ID))
    events: list[dict] = []
    masks: list[np.ndarray] = []
    annotated: list[np.ndarray] = []
    for sequence, frame in enumerate(frames):
        event = sensor.process_frame(RuntimeFrame(metadata=packet(frame, sequence), pixels=frame))
        events.append(event)
        masks.append(sensor.tracker.last_mask.copy())
        annotated.append(annotate(frame, event))
    await sensor.stop()

    cv2.imwrite(str(output_dir / "overview.png"), annotated[0])
    mask_bgr = cv2.cvtColor(masks[0], cv2.COLOR_GRAY2BGR)
    panels = [add_title(frames[0], "1  Original synthetic frame"), add_title(mask_bgr, "2  HSV mask"), add_title(annotated[0], "3  Sensor detection")]
    cv2.imwrite(str(output_dir / "processing.png"), cv2.hconcat(panels))
    state_panels = [
        add_title(annotated[0], "Frame 0: tracking"),
        add_title(annotated[1], "Frame 1: lost"),
        add_title(annotated[2], "Frame 2: reacquired"),
    ]
    cv2.imwrite(str(output_dir / "lost-reacquire.png"), cv2.hconcat(state_panels))
    (output_dir / "events.json").write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    args = parser.parse_args()
    events = asyncio.run(execute(args.output, args.sample))
    print(f"wrote {len(events)} SensorEvents and demo images to {args.output}")
    print("statuses:", ", ".join(str(event["status"]) for event in events))


if __name__ == "__main__":
    main()
