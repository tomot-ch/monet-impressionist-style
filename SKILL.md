---
name: monet-impressionist-style
description: Generate or restyle recognizable, luminous Monet-inspired Impressionist scenes using observed light and curated painting references. Use for landscapes, bright water lilies, and figures in their environment; not for generic oil filters or dark blue-dominant abstraction.
---

# Monet Impressionist Style

Make an observed scene read through light, large color relationships and varied paint handling. Visible marks serve those relationships; their density is not the measure of style strength.

## Mode and strength

- **Generate:** choose an informal, controlled composition; default to 4:3 PNG.
- **Restyle:** inspect the photograph; preserve its aspect ratio, framing, viewpoint, major silhouettes, object positions and actual light event. Default to PNG. Simplify incidental detail without inventing objects.
- Accept light (25), balanced (55, default), strong (80), or 0–100. These are prompt semantics, not numerical tool controls. Light changes surface handling modestly; balanced actively reinterprets paint and color while preserving recognition and tonal organization; strong simplifies and repaints more assertively without drifting into abstraction. Increasing strength does not require more contrast or more strokes everywhere.

## Read and select evidence

Read [style-profile.md](references/style-profile.md) and [technique-reading.md](references/technique-reading.md). Use the `techniques` lookup in `assets/reference-slices/index.json` to select 2–4 individually analyzed crop IDs for the actual problem. Read only their entries in [technique-atlas.json](references/technique-atlas.json), then inspect those images. `unreviewed` crops are not analyzed evidence. Consult [reference-routing.md](references/reference-routing.md) for a subject board only when it adds a missing relationship.

The photograph governs content and light; the crops govern specific handling techniques. Do not import their objects, palette wholesale, viewing distance or composition. Use the selected crops as image references when supported; giant TIFF originals are for inspection, not upload. Report reference failures rather than claiming visual grounding when only text reached the generator.

## Build the brief

1. State the subject, framing and at most three recognition anchors.
2. Describe the observed light event and the largest light/midtone/dark masses. Keep shadow areas and their relative darkness; luminosity comes from relationships, not a global exposure lift.
3. Set strength, then assign a distinct handling to each major material: broad related-color passages, local dragged/scumbled transitions, and selective broken accents. Indicate where the painting should remain quiet.
4. Name each reference's crop ID, technique and limit of transfer. Keep a few firm contours; let other edges merge where light or distance warrants it.
5. Include only the exclusions relevant to the observed risk, and the requested output format/aspect ratio. Avoid stacking synonymous texture commands.

For repetitive dabs, fluorescent ribbons or uniform relief, use [feedback-calibration.md](references/feedback-calibration.md). The correction is selective contrast, varied coverage and edges—not extra simulated paint thickness.

## Generate, inspect, revise

Use an available reference-capable image generator, preferring the native tool. Generate separate outputs for separate photographs. Inspect both the whole picture and representative light, shadow and material transitions:

- Recognizable scene, framing, perspective and important positions.
- Source-consistent light, shadow, reflection and large tonal masses.
- Broad forms read first; varied, material-specific strokes read on closer viewing.
- Quiet passages and accents coexist; no repeated stamp, marker overlay or uniform embossed surface.
- Bright water lilies retain flower/leaf/water separation and supporting dark greens.

If an output fails, identify the region and mechanism, compare the relevant original/crop, and change the smallest responsible instruction. For repeated calibration, regenerate from the original photograph to avoid cumulative drift. Keep inputs, prompts, outputs, reviews and skill snapshots outside the installed skill. Stop after the user's requested rounds and report residual defects; do not label an untested final patch as validated.

## Extend references

For supplied TIFFs, preserve originals and follow [reference-curation.md](references/reference-curation.md). Record source and crop boxes, add observed technique entries, then run `scripts/build_reference_sets.py`. Keep only derived crops, boards and their index in the skill; uncertain artwork attribution stays uncertain.
