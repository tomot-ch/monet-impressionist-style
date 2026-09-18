# TIFF reference curation

## Goal

Build compact, reusable style evidence from the user's high-resolution TIFF paintings without placing giant originals inside the skill. Group crops by shared visual function across multiple works, but make the primary lookup about mark-making, light, and recognizability rather than scene category.

## Preserve provenance

- Never modify or overwrite a TIFF original.
- Keep originals in the user's source folder outside this skill.
- Record the work title, approximate year when known, source filename, crop box, group, and a short reason for selection.
- Do not include signatures, frames, labels, color bars, damaged margins, or museum backgrounds in crops.

## Choose crops

Select regions that are large enough to reveal both individual marks and their larger visual effect. Prefer crops with a coherent visual function and avoid regions dominated by compression artifacts, glare, restoration damage, or reproductions with obvious color casts.

Before curating, check [source-audit.json](source-audit.json). Do not add excluded, duplicate, misattributed, or palette-incompatible sources unless the user explicitly changes the relevant boundary.

Each group should eventually contain examples from at least three works where the corpus allows it. Avoid filling a board with neighboring crops from the same painting. A useful crop should demonstrate one or more of:

- stroke edge and direction;
- local warm/cool or complementary juxtaposition;
- transition between light and shadow;
- material-specific mark-making;
- relationship between close-up marks and readable form.
- asymmetrical or cropped composition with a clear stabilizing anchor;
- a modern structure or vehicle partially dissolved by light, steam, air, or motion.
- a direct relationship between observed illumination and stroke direction, density, hue, or edge interruption.

Most material and stroke crops should show a close or medium region. `composition-viewpoint` crops may cover most of a painting because viewpoint and spatial organization cannot be learned from a tiny detail. They are still derived, reduced assets rather than the giant TIFF originals.

Water-lily candidates must satisfy the bright-water-lily rule in `style-profile.md`. Exclude dark or blue-dominant late panels from the default board.

## Manifest

Create a UTF-8 JSON file with this structure:

```json
{
  "version": 1,
  "crops": [
    {
      "id": "unique-short-id",
      "source": "../../原图/example.tif",
      "work": "Work title",
      "year": "1891",
      "group": "vegetation",
      "reason": "Warm and cool leaf marks remain separate around a sunlit mass.",
      "box": {"unit": "normalized", "x": 0.10, "y": 0.15, "width": 0.30, "height": 0.30}
    }
  ]
}
```

Paths are resolved relative to the manifest. `box.unit` may be `normalized` with values from 0 to 1, or `pixels` with integer coordinates. Boxes use the image's top-left corner as the origin.

## Build and inspect

Run:

```bash
python3 scripts/build_reference_sets.py path/to/crops.json --output assets/reference-slices
```

Before building, inspect candidate crops individually at normal and close viewing scale. For each crop promoted to detailed technique evidence, add one entry to [technique-atlas.json](technique-atlas.json) keyed by the unchanged crop ID. Fill `stroke_geometry`, `surface_evidence`, `color_light`, `realism_anchor`, `transfer_rule`, and `failure_mode`; assign concrete technique tags. Describe only what is visible in the reproduction and separate any inference about physical process. Leave uncertain crops `unreviewed`, rather than inventing detail.

The script validates atlas references and exports individual PNG crops with a 1024-pixel maximum edge, clean image-only boards, and `index.json`. The index contains technique tags, per-crop analysis, and counts of detailed versus unreviewed examples. Visually inspect every crop and board. Remove weak, redundant, mislabeled, or color-inaccurate crops by editing the manifest and rebuilding. Override the crop limit only when a close analysis genuinely needs more detail, for example with `--crop-max 1600`.

Reference boards intentionally contain no text labels because labels can pollute image-generation style references. Provenance stays in `index.json`.
