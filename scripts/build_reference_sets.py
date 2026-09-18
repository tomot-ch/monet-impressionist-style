#!/usr/bin/env python3
"""Build curated reference crops and clean contact boards from a JSON manifest."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps


ALLOWED_GROUPS = {
    "sky-atmosphere",
    "water-reflections",
    "vegetation",
    "architecture",
    "distance-transition",
    "sun-shadow",
    "stroke-color-juxtaposition",
    "light-brush-relationship",
    "snow-special-light",
    "bright-water-lilies",
    "figures",
    "composition-viewpoint",
    "modern-life-motion",
}

TECHNIQUE_FIELDS = (
    "stroke_geometry",
    "surface_evidence",
    "color_light",
    "realism_anchor",
    "transfer_rule",
    "failure_mode",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export lossless crops and reference boards without changing source images."
    )
    parser.add_argument("manifest", type=Path, help="UTF-8 JSON crop manifest")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--crop-max", type=int, default=1024, help="Maximum edge of an exported crop"
    )
    parser.add_argument("--tile", type=int, default=512, help="Square tile size in pixels")
    parser.add_argument("--columns", type=int, default=3, help="Board column count")
    parser.add_argument("--max-per-board", type=int, default=9, help="Maximum tiles per board")
    parser.add_argument("--gutter", type=int, default=16, help="Neutral gutter in pixels")
    return parser.parse_args()


def fail(message: str) -> None:
    raise ValueError(message)


def safe_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value):
        fail(f"{field} must contain lowercase letters, digits, and hyphens: {value!r}")
    return value


def crop_box(spec: dict[str, Any], width: int, height: int) -> tuple[int, int, int, int]:
    unit = spec.get("unit")
    values = [spec.get(key) for key in ("x", "y", "width", "height")]
    if not all(isinstance(value, (int, float)) for value in values):
        fail(f"Crop box values must be numeric: {spec!r}")
    x, y, box_width, box_height = (float(value) for value in values)
    if unit == "normalized":
        if not (0 <= x < 1 and 0 <= y < 1 and box_width > 0 and box_height > 0):
            fail(f"Invalid normalized crop: {spec!r}")
        left, top = round(x * width), round(y * height)
        right, bottom = round((x + box_width) * width), round((y + box_height) * height)
    elif unit == "pixels":
        left, top = round(x), round(y)
        right, bottom = round(x + box_width), round(y + box_height)
    else:
        fail(f"Crop unit must be 'normalized' or 'pixels': {unit!r}")

    left, top = max(0, left), max(0, top)
    right, bottom = min(width, right), min(height, bottom)
    if right <= left or bottom <= top:
        fail(f"Crop is empty or outside the image: {spec!r}")
    return left, top, right, bottom


def open_rgb(path: Path) -> Image.Image:
    with Image.open(path) as source:
        source.seek(0)
        return ImageOps.exif_transpose(source).convert("RGB")


def load_technique_atlas(path: Path, crop_ids: set[str]) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        fail(f"Technique atlas not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("examples"), list):
        fail("Technique atlas must contain version 1 and an examples array")
    examples: dict[str, dict[str, Any]] = {}
    for item in data["examples"]:
        if not isinstance(item, dict):
            fail(f"Technique example must be an object: {item!r}")
        crop_id = safe_id(item.get("crop_id"), "technique crop id")
        if crop_id not in crop_ids:
            fail(f"Technique atlas references unknown crop id: {crop_id}")
        if crop_id in examples:
            fail(f"Duplicate technique analysis for crop id: {crop_id}")
        tags = item.get("tags")
        if not isinstance(tags, list) or not tags or len(tags) != len(set(tags)):
            fail(f"Technique tags must be a nonempty unique list for {crop_id}")
        for tag in tags:
            safe_id(tag, f"technique tag for {crop_id}")
        for field in TECHNIQUE_FIELDS:
            if not isinstance(item.get(field), str) or not item[field].strip():
                fail(f"Missing {field} for technique crop {crop_id}")
        examples[crop_id] = item
    return examples


def square_tile(image: Image.Image, size: int) -> Image.Image:
    return ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS)


def build_board(tiles: list[Image.Image], tile_size: int, columns: int, gutter: int) -> Image.Image:
    rows = math.ceil(len(tiles) / columns)
    width = columns * tile_size + (columns + 1) * gutter
    height = rows * tile_size + (rows + 1) * gutter
    board = Image.new("RGB", (width, height), (226, 222, 211))
    for index, tile in enumerate(tiles):
        row, column = divmod(index, columns)
        x = gutter + column * (tile_size + gutter)
        y = gutter + row * (tile_size + gutter)
        board.paste(tile, (x, y))
    return board


def main() -> int:
    args = parse_args()
    if (
        args.crop_max < 256
        or args.tile < 64
        or args.columns < 1
        or args.max_per_board < 1
        or args.gutter < 0
    ):
        fail("Crop, tile, columns, max-per-board, and gutter values are out of range")

    manifest_path = args.manifest.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("crops"), list):
        fail("Manifest must contain version 1 and a crops array")

    manifest_ids = {
        safe_id(item.get("id"), "crop id")
        for item in data["crops"]
        if isinstance(item, dict)
    }
    atlas_path = manifest_path.parent / "technique-atlas.json"
    atlas = load_technique_atlas(atlas_path, manifest_ids)

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    seen_ids: set[str] = set()
    grouped: dict[str, list[tuple[dict[str, Any], Path]]] = defaultdict(list)
    index: dict[str, Any] = {
        "version": 2,
        "manifest": str(manifest_path),
        "technique_atlas": str(atlas_path),
        "groups": {},
        "techniques": {},
        "analysis_coverage": {"detailed": len(atlas), "unreviewed": len(data["crops"]) - len(atlas)},
    }

    for item in data["crops"]:
        if not isinstance(item, dict):
            fail(f"Each crop must be an object: {item!r}")
        crop_id = safe_id(item.get("id"), "crop id")
        if crop_id in seen_ids:
            fail(f"Duplicate crop id: {crop_id}")
        seen_ids.add(crop_id)
        group = safe_id(item.get("group"), "group")
        if group not in ALLOWED_GROUPS:
            fail(f"Unknown group {group!r}; allowed groups: {sorted(ALLOWED_GROUPS)}")
        source_value = item.get("source")
        if not isinstance(source_value, str) or not source_value:
            fail(f"Crop {crop_id} has no source path")
        source_path = (manifest_path.parent / source_value).resolve()
        if not source_path.is_file():
            fail(f"Source image not found for {crop_id}: {source_path}")

        image = open_rgb(source_path)
        region = image.crop(crop_box(item.get("box", {}), *image.size))
        region.thumbnail((args.crop_max, args.crop_max), Image.Resampling.LANCZOS)
        group_crops = output / group / "crops"
        group_crops.mkdir(parents=True, exist_ok=True)
        crop_path = group_crops / f"{crop_id}.png"
        region.save(crop_path, "PNG", optimize=True)
        grouped[group].append((item, crop_path))

    for group, entries in sorted(grouped.items()):
        board_dir = output / group / "boards"
        board_dir.mkdir(parents=True, exist_ok=True)
        group_index: dict[str, Any] = {"crops": [], "boards": []}
        for item, crop_path in entries:
            crop_entry = {
                "id": item["id"],
                "file": str(crop_path.relative_to(output)),
                "source": item["source"],
                "work": item.get("work"),
                "year": item.get("year"),
                "reason": item.get("reason"),
                "box": item.get("box"),
                "analysis_status": "detailed" if item["id"] in atlas else "unreviewed",
            }
            if item["id"] in atlas:
                crop_entry["analysis"] = atlas[item["id"]]
                for tag in atlas[item["id"]]["tags"]:
                    index["techniques"].setdefault(tag, []).append(item["id"])
            group_index["crops"].append(crop_entry)

        board_count = math.ceil(len(entries) / args.max_per_board)
        entries_per_board = math.ceil(len(entries) / board_count)
        for board_number, start in enumerate(range(0, len(entries), entries_per_board), 1):
            batch = entries[start : start + entries_per_board]
            tiles = [square_tile(open_rgb(path), args.tile) for _, path in batch]
            board = build_board(tiles, args.tile, args.columns, args.gutter)
            board_path = board_dir / f"{group}-{board_number:02d}.png"
            board.save(board_path, "PNG", optimize=True)
            group_index["boards"].append(
                {
                    "file": str(board_path.relative_to(output)),
                    "crop_ids": [item["id"] for item, _ in batch],
                }
            )
        index["groups"][group] = group_index

    index["techniques"] = dict(sorted(index["techniques"].items()))

    (output / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {len(seen_ids)} crops across {len(grouped)} groups in {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
