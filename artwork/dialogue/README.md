# Custom dialogue assets — Step 0

42 new RGBA PNG resources reproduce the supplied dialogue window's gold frame,
portrait surround, dark response bars, footer controls and fine divider. Five
existing Codex resources are reused unchanged. All 920 resources recorded before
this work remain unchanged.

This stage prepares assets and an offline composition only. No C# NUI layout or
event implementation, hak packing, deployment, or game operations were performed.
In-game alignment is Step 1; input and dialogue-flow verification are Step 2.

## Deliverables

- Game exports: `../../src/hak/amia_nui/png/ui_dlg_*.png`.
- `reference.png`: retained original user attachment, 1448×1086.
- Six `*-master.png` files: retained built-in ImageGen reconstructions.
- `generation-prompts.json`: complete prompt set, transparency settings, reference
  role, and original generated-output paths.
- `extract_assets.py`: deterministic ImageMagick crop, sizing, slicing, preview,
  manifest and validation workflow. Pillow/NumPy only inspect image pixels.
- `manifest.json`: all new exports, provenance, dimensions, padding and hashes.
- `asset-contract.json`: frame assembly, button end caps, divider assembly, resource
  reuse decisions, offline source-coordinate layout and known visual differences.
- `exports.txt`: the 42 new PNGs. `required-resources.txt`: all 47 resources needed
  for the composition, including the five reused Codex PNGs.
- `existing_resources_before.json`: immutable baseline hashes for 920 NUI files.
- `validation.json`: automated checks, rebuild verification and visual-review record.
- `previews/contact-sheet.png`: core asset families and reused controls.
- `previews/alpha-checks.png`: new artwork on dark, cream and purple backgrounds.
- `previews/dialogue-artwork.png`: assembled artwork with a reference portrait;
  names, dialogue and response labels are absent.
- `previews/dialogue-composition.png`: the same composition with representative
  live content simulated using DejaVu Serif. Text is never in game exports.
- `previews/*-assembled.png`: canonical sliced-frame compositions.
- `previews/*-resized.png`: alternate-size sliced-frame compositions for visual QA.

The reference portrait crop exists only inside offline previews and is not exported
as a game resource. Actual NPC portraits remain dynamic.

## Asset families

| Family | Exports | Canonical source size | Assembly |
| --- | --- | --- | --- |
| Outer frame | 11 | 1180×1016 | Master plus ten slices; fixed corners and fixed central top ornament. |
| Portrait surround | 9 | 335×471 | Master plus eight slices, transparent opening. |
| Dialogue panel | 9 | 746×491 | Master plus eight slices; fill supplied independently. |
| Response bar | 4 | 1088×56 | Master plus left/middle/right; 32px end caps. |
| Footer housing | 4 | 268×60 | Master plus left/middle/right; 40px end caps. |
| Fine divider/rule | 5 | Divider 336×14 | Master, three divider pieces, separate straight hairline. |

The outer frame's top edge is split into `top_l`, `top_m`, and `top_r` so the central
diamond does not stretch. There is no single `ui_dlg_fr_top` resource. Preserve
corner and ornament aspect; stretch straight rails only along their long axis.

Button masters were first scaled uniformly to the chosen height, then only their
middle strip was resized horizontally. This preserves end-cap proportions despite
the generated masters' differing aspect ratios. For variable control widths, use
the three pieces and preserve the caps at the chosen height. A whole-button
`NuiImage` should retain the canonical aspect. The NUI input surface and live
overlays are future Step 1/2 work.

Names, response labels, page counters and footer labels stay live. There are no
selected or pressed variants for these momentary actions. Hover is tooltip-only;
disabled images, muted live overlays and presenter activation guards follow the
Codex pattern and still require client verification.

## Reuse decisions and visual differences

- `ui_cdx_bg`: reused subdued interlaced dark fill; seamless tiling is not claimed.
- `ui_cdx_close`: reused red/gold X.
- `ui_cdx_btn`: reused blank pagination housing.
- `ui_cdx_i_prev` and `ui_cdx_i_next`: reused gold navigation chevrons. Their shape
  differs from the reference's triangles; this is visible in the composition.
- Existing Codex divider and frame families were rejected because their ornamentation
  differs. The new fine divider supplies header, speaker and pagination decorations.

ImageGen reconstructions are close visual adaptations, not pixel-exact extraction.
The native NUI font and layout are not represented by the offline DejaVu Serif
preview. The header/panel decorations use the new reusable three-diamond motif.
Final logical NUI dimensions, GUI scaling and text overflow remain Step 1 checks.

## Rebuild

Requires Python with Pillow/NumPy, ImageMagick `magick`, and DejaVu fonts. From the
`amia_haks` repository root:

```sh
python3 artwork/dialogue/extract_assets.py \
  --export-dir src/hak/amia_nui/png \
  --resource-root src/hak/amia_nui
```

No API key or new ImageGen call is needed: the masters are retained. The script
checks the immutable baseline and refuses to replace unrecognized or modified
exports. It validates lowercase resrefs of at most 16 characters, cross-format
collisions, RGBA dimensions/hashes, frame-opening alpha, opaque button content,
exact frame-slice pixels, and canonical frame reassembly. PNG over-compositing
rounds some alpha values by one; visible premultiplied RGB is unchanged.

The script rewrites the automated `validation.json`, leaving human visual review
and deterministic-repeat confirmation pending for the operator to record after
review. It does not pack or deploy a hak.

## Packaging handoff

The existing Nasher `amia_nui` target includes `src/hak/amia_nui/**/*`. Use the
established bundling workflow and verify the built archive against
`required-resources.txt` before Step 1's in-game layout review. Neither bundling nor
client installation was performed during Step 0.
