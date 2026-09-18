# Reference routing

Reference boards live under `assets/reference-slices/<group>/boards/`. Use the generated `index.json` to see which works and crops contribute to each board. This is the **secondary subject router**: first choose individually analyzed crops by the `techniques` index and `references/technique-reading.md`. A scene-matching board does not by itself prove the right brushwork or light behavior.

| Group | Use when the scene contains | Borrow from the references |
| --- | --- | --- |
| `sky-atmosphere` | sky, clouds, mist, open air | airy stroke scale, temperature shifts, atmospheric spacing |
| `water-reflections` | rivers, sea, ponds, wet surfaces | horizontal broken marks, vertical reflection cues, sparkle |
| `vegetation` | trees, grass, flowers, gardens | clustered strokes, massing, warm/cool leaf variation |
| `architecture` | buildings, bridges, stations | readable geometry softened by light, chromatic masonry |
| `distance-transition` | distant shore, haze, layered depth | edge hierarchy, reduced contrast, limited soft transition |
| `sun-shadow` | strong daylight, backlight, cast shadows | chromatic highlights and colored shadows |
| `stroke-color-juxtaposition` | every generated or restyled image | separated marks, optical mixing, local contrast |
| `light-brush-relationship` | photograph restyling or any scene driven by observed light | how stroke direction, density, hue, and edge behavior encode a specific light event |
| `snow-special-light` | snow, frost, dawn, sunset | reflected color in pale surfaces and unusual light |
| `bright-water-lilies` | lily pond, Japanese bridge, aquatic garden | luminous water palette, readable pads/blossoms, bright reflections |
| `figures` | people are present or central | silhouette, gesture, clothing marks, integration with atmosphere |
| `composition-viewpoint` | a new composition is generated or reframing is allowed | asymmetry, cropping, high/low viewpoint, stabilizing anchors |
| `modern-life-motion` | ports, bridges, stations, railways, steam, leisure or moving boats | geometric framework interrupted by air, light, smoke, steam, and movement |

Do not automatically include any whole board. Select 2–4 crop IDs by the technical problem first. Add a subject group only if it supplies a missing material or scene relationship. For text-to-image generation, `composition-viewpoint` may help; for strict restyling, the user's source composition remains authoritative, so use that board only if reframing is allowed. Use `bright-water-lilies` for water-lily scenes and do not substitute a dark or blue-dominant board.

For an image with a person in a garden beside water, a possible selection—after inspecting the actual source light—is:

1. `parasol-skirt-sky-light` for cloth form and reflected environment color.
2. `river-autumn-foliage` for clustered vegetation with structural dark gaps.
3. `sunset-water-orange` only if the source has low-angle colored reflection; otherwise choose another water crop.

The user's source image remains the authority for content and composition. Reference boards are authorities only for mark-making, color relationships, light, and atmosphere.
