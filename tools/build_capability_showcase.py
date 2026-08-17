#!/usr/bin/env python3
"""Build the repository homepage capability showcase from reviewed demo assets.

The builder is deliberately offline and deterministic for a fixed Pillow version.
It never downloads images and never replaces the detailed per-capability assets.
"""

from __future__ import annotations

import argparse
import io
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - exercised only in incomplete dev environments
    raise SystemExit(
        "Pillow is required to build the showcase. Install the Python dev extra: "
        "python -m pip install -e './packages/python[dev]'"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/assets/capability-showcase.png"
CANVAS_SIZE = (1200, 1458)
TILE_SIZE = (564, 294)

CAPABILITIES = (
    {
        "name": "Camera Capture",
        "caption": "Camera -> FramePacket",
        "asset": "sensors/camera.capture/assets/captured-frame.png",
    },
    {
        "name": "Screen Capture",
        "caption": "Screen -> FramePacket",
        "asset": "sensors/screen.capture/assets/captured-screen-frame.png",
    },
    {
        "name": "Number OCR",
        "caption": "ROI -> Number",
        "asset": "sensors/ocr.number/assets/overview.png",
    },
    {
        "name": "Color Marker",
        "caption": "HSV -> Position",
        "asset": "sensors/tracker.color-marker/assets/overview.png",
    },
    {
        "name": "Spot Centroid",
        "caption": "Spot -> Centroid",
        "asset": "sensors/tracker.spot-centroid/assets/overview.png",
    },
    {
        "name": "Template Tracker",
        "caption": "ROI -> Track",
        "asset": "sensors/tracker.template/assets/overview.png",
    },
    {
        "name": "YOLO Tracker",
        "caption": "Detection -> Track (recorded replay)",
        "asset": "sensors/tracker.yolo/assets/overview.png",
    },
    {
        "name": "3D Vector Composition",
        "caption": "XYZ -> Resultant",
        "asset": "processing/vector.compose-3d/assets/overview.png",
    },
)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def font(size: int) -> ImageFont.ImageFont:
    """Use Pillow's bundled font so the build has no host-font dependency."""

    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10 compatibility
        return ImageFont.load_default()


def load_reviewed_asset(relative_path: str) -> Image.Image:
    path = ROOT / relative_path
    if not path.is_file() or path.stat().st_size <= 0:
        raise FileNotFoundError(f"missing or empty showcase source: {relative_path}")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return image.convert("RGB")


def build_showcase() -> Image.Image:
    canvas = Image.new("RGB", CANVAS_SIZE, "#0d1117")
    draw = ImageDraw.Draw(canvas)
    title_font = font(38)
    tile_title_font = font(25)
    caption_font = font(18)
    footer_font = font(17)

    draw.text((36, 28), "Physics Software Sensors", fill="#f0f6fc", font=title_font)
    draw.text(
        (36, 76),
        "7 Software Sensors + 1 Companion Processing Tool",
        fill="#8c959f",
        font=caption_font,
    )

    left = 24
    top = 122
    gap_x = 24
    gap_y = 18
    tile_width, tile_height = TILE_SIZE
    for index, capability in enumerate(CAPABILITIES):
        row, column = divmod(index, 2)
        x = left + column * (tile_width + gap_x)
        y = top + row * (tile_height + gap_y)
        draw.rounded_rectangle(
            (x, y, x + tile_width, y + tile_height),
            radius=13,
            fill="#161b22",
            outline="#30363d",
            width=2,
        )
        draw.text((x + 18, y + 13), capability["name"], fill="#f0f6fc", font=tile_title_font)

        source = load_reviewed_asset(capability["asset"])
        image_box = (tile_width - 36, 198)
        preview = ImageOps.contain(source, image_box, Image.Resampling.LANCZOS)
        preview_x = x + (tile_width - preview.width) // 2
        preview_y = y + 56 + (image_box[1] - preview.height) // 2
        canvas.paste(preview, (preview_x, preview_y))

        draw.text(
            (x + 18, y + tile_height - 29),
            capability["caption"],
            fill="#8c959f",
            font=caption_font,
        )

    footer_y = 1376
    draw.line((24, footer_y, 1176, footer_y), fill="#30363d", width=2)
    draw.text(
        (36, footer_y + 18),
        "Representative standalone / synthetic / replay demonstrations.",
        fill="#c9d1d9",
        font=footer_font,
    )
    draw.text(
        (36, footer_y + 43),
        "Evidence level varies by capability. Images are enhancements; text links remain canonical.",
        fill="#8c959f",
        font=footer_font,
    )
    return canvas


def encoded_png(image: Image.Image) -> bytes:
    output = io.BytesIO()
    image.save(output, format="PNG", optimize=True, compress_level=9)
    return output.getvalue()


def check_sources() -> None:
    for capability in CAPABILITIES:
        load_reviewed_asset(capability["asset"])


def check_output(path: Path) -> None:
    check_sources()
    if not path.is_file() or path.stat().st_size <= 0:
        raise FileNotFoundError(f"missing or empty showcase output: {display_path(path)}")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        if image.size != CANVAS_SIZE or image.format != "PNG":
            raise ValueError(
                f"unexpected showcase image: format={image.format!r}, size={image.size!r}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="validate source assets and existing output")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output

    if args.check:
        check_output(output)
        print(f"PASS: 8/8 sources and {display_path(output)} decode as PNG")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded_png(build_showcase()))
    check_output(output)
    print(f"Wrote {display_path(output)} ({output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
