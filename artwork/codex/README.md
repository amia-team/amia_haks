# Codex assets — tasks 000 and 002

65 RGBA PNG resources follow the supplied gold, dark-panel and parchment Codex theme. Task 000 supplied 58 resources. Task 002 adds seven and preserves every existing PNG. All resources use unique `ui_cdx_*` names; base-game and shared Amia textures remain unchanged.

Task 001's r5 prototype passed the user's in-game checks on 2026-10-03 at GUI viewport 3440×1382 and 100% scale. The seven new exports require user bundling and client review with the full shell. Client/server versions were not supplied; other display settings remain task 007.

## Deliverables

- Game exports: `../../src/hak/amia_nui/png/ui_cdx_*.png`.
- `manifest.json`: complete 65-resource manifest, provenance, dimensions, hashes and final asset contract.
- `exports.txt`: complete export list; `exports-002.txt`: only the seven new PNGs.
- `asset-contract.json`: state families, source-pixel padding, fixed frame corners, verified logical NUI geometry, glyph/action mapping and disabled treatment.
- `manifest-000.json`: unchanged 58-resource baseline manifest.
- `reference.png`, five original `*-master.png` images and `generation-prompts.json`: retained 000 sources.
- `prev-master.png` and `generation-prompts-002.json`: retained built-in ImageGen left-chevron master, exact prompt and settings.
- `extract_assets.py`: original deterministic 000 export workflow.
- `finalize_assets.py`: deterministic 002 canvas normalization, chevron extraction, combined manifest and validation workflow.
- `validation.json` and `validation-002.json`: local results.
- `existing_resources_before.json`: checksums of the 855 resources preceding 000.
- `existing_resources_before_002.json`: checksums of all 913 resources preceding 002.
- `previews/contact-sheet.png`, `alpha-checks.png`, `codex-composition.png`: original offline previews.
- `previews/contact-sheet-002.png`: the seven new exports.
- `previews/alpha-and-states-002.png`: controls on black, parchment-colored and contrasting backgrounds. Disabled rows are grayscale illustrations, not a simulation of the client's exact native disabled appearance.

## New control canvases

| Family | Normal | Selected | Common source canvas | Content padding L/T/R/B |
| --- | --- | --- | --- | --- |
| Tab | `ui_cdx_tab_n_v2` | `ui_cdx_tab_s_v2` | 245×96 | 21/20/21/20 |
| Category | `ui_cdx_cat_n_v2` | `ui_cdx_cat_s_v2` | 262×72 | 24/16/24/16 |
| Entry/action | `ui_cdx_ent_n_v2` | `ui_cdx_ent_s_v2` | 352×84 | 16/15/16/15 |

These exports add transparent margins without resizing or altering the original artwork pixels. Use the same widget bounds, glyph placement and live-text placement across states. Keep the original six controls available for the r5 prototype; the full shell should consume the normalized `*_v2` backgrounds.

The seventh resource, `ui_cdx_i_prev`, is a transparent 64×64 cell with a left chevron fitted within 56×56, matching the existing next-arrow theme. It is reconstructed from a built-in ImageGen direction edit, not a pixel-exact mirror.

Disabled controls retain their current normal/selected background, use native disabled NuiImage rendering, explicitly mute independent labels/glyphs to RGB(110,100,80), and reject activation in the presenter. Task 001 verified this approach. No extra disabled textures are required. Momentary actions do not need selected artwork. Hover is tooltip-only; pressed has no visual variant.

## Retained asset families

| Family | Count | Contract |
| --- | --- | --- |
| Outer frame and eight slices | 9 | Source corners 54px; verified logical corners 28. Separate fill inset 8 from control inset 24. |
| Original control states | 6 | Retained unchanged; use six normalized v2 variants for the full shell. |
| Help/close buttons | 2 | Close follows existing draft protection. Help stays unused until a useful action exists. |
| Divider ornaments | 2 | Independent decorations. |
| Scrollbar reference and parts | 5 | Native scrolling is verified; custom scrolling remains task 007. |
| Compact panel and eight slices | 9 | Source corners 36px; logical corners 18. Fill independently; content inset 12. |
| Dark, header and brown fills | 3 | Stretch sampled fills as verified; seamless tiling is not guaranteed. |
| Parchment | 1 | Transparent ragged perimeter; source 474×546, verified logical pane 458×450, content inset 26. |
| Blank button housing | 1 | 64×64; overlay separate direction glyph. |
| Original navigation/category/direction icons | 20 | 64×64 transparent cells, glyphs fitted within 56px. |

Use direct textures. Source-pixel image subregions also passed 001, but there is no demonstrated reason to introduce an atlas. Scale frame corners uniformly, stretch straight edges along their long axis, and keep live labels/content independent of bitmaps. The full six-tab header sizing belongs to 003; the verified 940×650 prototype is its starting point.

## Provenance

Built-in `image_gen.imagegen` prepared the original working masters and the new left-chevron master. Original icon removal, boundaries and isolated shapes include reconstructed artwork; they are not pixel-exact copies of the user mockup. Exact prompts and tool settings are retained in the two generation logs.

ImageMagick performs deterministic crops, resizing, canvas extension, frame slicing and offline preview assembly. Pillow/NumPy read pixels only for bounds and validation. Source rectangles identify the retained working master; approximate reference rectangles are not instructions to crop the original mockup.

## Rebuild locally

Requires Python with Pillow/NumPy, ImageMagick `magick`, and DejaVu Sans. From the `amia_haks` root, rebuild 002 from the existing 000 exports:

```sh
python3 artwork/codex/finalize_assets.py \
  --export-dir src/hak/amia_nui/png \
  --resource-root src/hak/amia_nui
```

To rebuild everything from retained masters, first run the original extraction, then finalization:

```sh
python3 artwork/codex/extract_assets.py \
  --export-dir src/hak/amia_nui/png \
  --resource-root src/hak/amia_nui
python3 artwork/codex/finalize_assets.py \
  --export-dir src/hak/amia_nui/png \
  --resource-root src/hak/amia_nui
```

The original extraction writes a 58-resource manifest; finalization restores the combined 65-resource manifest. Do not overwrite the retained `manifest-000.json` baseline. Finalization checks the original resource hashes and refuses changed sources. Neither script calls ImageGen, packs a hak, runs Jenkins, deploys content or launches NWN.

## Local verification and handoff

All seven new exports decode as RGBA, match recorded dimensions/hashes, and have unique lowercase resrefs of at most 16 characters with no cross-format collisions. All six normalized controls preserve their original pixels exactly and contain no unintended transparent content-area holes. The chevron has clear transparent cell margins. A repeated rebuild produced identical SHA-256 values for all seven PNGs. Contact and alpha previews were visually inspected.

All 58 original Codex exports and all 913 pre-existing NUI resources remain byte-for-byte unchanged. The existing Nasher `amia_nui` target includes `src/hak/amia_nui/**/*`; use the established bundling workflow and check the built archive against `exports.txt`. The new subset is `exports-002.txt`. No Jenkins, packing, deployment or game operations were performed for 002.

Task 001 uses the manifest's 27 `prototype_resrefs`, all from 000. Its r5 client checks passed. Task 003 can consume the finalized controls and contract; review the seven new exports in-game as part of the complete browsing handoff, without a separate asset-only game session.
