#!/usr/bin/env python3
"""Finalize 002 exports from retained 000 resources and one ImageGen master.

ImageMagick preserves control pixels while adding transparent canvas margins.
Pillow/NumPy only read images for bounds and validation. No packing or deployment.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--export-dir', type=Path, required=True)
parser.add_argument('--resource-root', type=Path, required=True)
parser.add_argument('--base-export-dir', type=Path)
args = parser.parse_args()
source = Path(__file__).resolve().parent
out = args.export_dir.resolve()
resource_root = args.resource_root.resolve()
base_dir = (args.base_export_dir or resource_root / 'png').resolve()
preview = source / 'previews'
out.mkdir(parents=True, exist_ok=True)
preview.mkdir(exist_ok=True)
base = json.loads((source / 'manifest-000.json').read_text())
records = list(base['assets'])
new_records = []

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(*parts):
    subprocess.run(['magick', *map(str, parts)], check=True)

def rgba(path):
    with Image.open(path) as image:
        if image.mode != 'RGBA':
            raise ValueError(f'Not RGBA: {path}: {image.mode}')
        return np.asarray(image)

families = {
    'tab': {'canvas': [245, 96], 'content_padding': [21, 20, 21, 20]},
    'category': {'canvas': [262, 72], 'content_padding': [24, 16, 24, 16]},
    'entry': {'canvas': [352, 84], 'content_padding': [16, 15, 16, 15]},
}
prefixes = {'tab': 'tab', 'category': 'cat', 'entry': 'ent'}
for family, spec in families.items():
    spec['states'] = {}
    for state, suffix in [('normal', 'n'), ('selected', 's')]:
        parent_ref = f'ui_cdx_{prefixes[family]}_{suffix}'
        parent_record = next(a for a in base['assets'] if a['resref'] == parent_ref)
        parent = base_dir / (parent_ref + '.png')
        assert sha(parent) == parent_record['sha256'], f'Changed source: {parent}'
        width, height = spec['canvas']
        pixels = rgba(parent)
        ph, pw = pixels.shape[:2]
        left, top = (width - pw) // 2, (height - ph) // 2
        ref = parent_ref + '_v2'
        target = out / (ref + '.png')
        run('-size', f'{width}x{height}', 'canvas:none', parent, '-geometry', f'+{left}+{top}',
            '-compose', 'Copy', '-composite', '-strip', f'PNG32:{target}')
        normalized = rgba(target)
        assert np.array_equal(normalized[top:top+ph, left:left+pw], pixels), f'Pixels changed: {ref}'
        l, t, r, b = spec['content_padding']
        assert (normalized[t:height-b, l:width-r, 3] > 16).all(), f'Interior alpha hole: {ref}'
        record = {
            'key': f'control.{family}.{state}', 'resref': ref,
            'export_path': f'src/hak/amia_nui/png/{ref}.png',
            'width': width, 'height': height, 'state': state,
            'content_padding': spec['content_padding'], 'atlas_region': None,
            'provenance': {'method': 'pixel_preserving_canvas_export',
                'parent_resref': parent_ref, 'parent_sha256': sha(parent),
                'source_placement_xy': [left, top], 'source_dimensions': [pw, ph],
                'pixel_preserving': True, 'resize': None},
            'alpha_min': int(normalized[:, :, 3].min()), 'alpha_max': int(normalized[:, :, 3].max()),
            'transparent_pixels': int((normalized[:, :, 3] == 0).sum()),
            'sha256': sha(target),
            'notes': 'Normal and selected states share one canvas and content inset; original art pixels are unchanged.',
        }
        new_records.append(record)
        spec['states'][state] = ref
    spec['disabled'] = {'resref': 'retain_current_normal_or_selected',
        'widget_enabled': False, 'overlay_color_rgb': [110, 100, 80],
        'activation_allowed': False,
        'treatment': 'Native NuiImage disabled appearance; explicitly dim draw-list glyphs/live labels. Verified in 001.'}

master = source / 'prev-master.png'
pixels = rgba(master)
yy, xx = np.where(pixels[:, :, 3] > 8)
assert len(xx), 'Empty previous glyph master'
x, y = max(0, int(xx.min()) - 4), max(0, int(yy.min()) - 4)
x2, y2 = min(pixels.shape[1], int(xx.max()) + 5), min(pixels.shape[0], int(yy.max()) + 5)
rect = [x, y, x2-x, y2-y]
ref = 'ui_cdx_i_prev'
target = out / (ref + '.png')
run(master, '-crop', f'{rect[2]}x{rect[3]}+{rect[0]}+{rect[1]}', '+repage',
    '-resize', '56x56', '-background', 'none', '-gravity', 'center', '-extent', '64x64',
    '-strip', f'PNG32:{target}')
pixels = rgba(target)
yy, xx = np.where(pixels[:, :, 3] > 16)
assert xx.max()-xx.min()+1 <= 56 and yy.max()-yy.min()+1 <= 56
assert (pixels[0, :, 3] == 0).all() and (pixels[-1, :, 3] == 0).all()
assert (pixels[:, 0, 3] == 0).all() and (pixels[:, -1, 3] == 0).all()
new_records.append({'key': 'icon.previous', 'resref': ref,
    'export_path': f'src/hak/amia_nui/png/{ref}.png',
    'width': 64, 'height': 64, 'state': 'normal', 'content_padding': [4, 4, 4, 4],
    'atlas_region': None,
    'provenance': {'method': 'slice_of_imagegen_master', 'master': 'prev-master.png',
        'master_sha256': sha(master), 'master_crop_xywh': rect, 'resize': '56x56',
        'centered_in_64px_cell': True, 'style_reference_resref': 'ui_cdx_i_next',
        'generation_prompt': 'generation-prompts-002.json'},
    'alpha_min': int(pixels[:, :, 3].min()), 'alpha_max': int(pixels[:, :, 3].max()),
    'transparent_pixels': int((pixels[:, :, 3] == 0).sum()), 'sha256': sha(target),
    'notes': 'ImageGen direction variant matched to the supplied next glyph; reconstructed, not a pixel-exact mirror.'})
records += new_records

contract = {
    'schema_version': 1, 'task': '002', 'units': 'source pixels unless explicitly logical_nui',
    'textures': 'Direct PNG resrefs. No production atlas; source-pixel subregions were verified in 001.',
    'control_families': families,
    'legacy_control_resrefs': [f'ui_cdx_{p}_{s}' for p in prefixes.values() for s in ['n', 's']],
    'frames': {
        'outer': {'source_resref': 'ui_cdx_outer', 'slice_prefix': 'ui_cdx_fr',
            'source_corner_pixels': 54, 'logical_nui_corner': 28,
            'fill_resref': 'ui_cdx_bg', 'logical_nui_fill_inset': 8, 'logical_nui_content_inset': 24},
        'panel': {'source_resref': 'ui_cdx_panel', 'slice_prefix': 'ui_cdx_pn',
            'source_corner_pixels': 36, 'logical_nui_corner': 18,
            'fill_resref': 'ui_cdx_bg', 'logical_nui_content_inset': 12},
        'assembly': 'Eight independent slices: scale corners uniformly, stretch each straight edge only along its long axis. Fill separately.'},
    'reading_pane': {'resref': 'ui_cdx_paper', 'logical_nui_size': [458, 450],
        'logical_nui_content_inset': 26, 'title_and_body_color_rgb': [48, 29, 15],
        'scrolling': 'Native body Y scrollbar; no shell scrollbar; frame and title remain fixed.'},
    'glyphs': {'canvas_pixels': [64, 64], 'maximum_glyph_pixels': [56, 56],
        'logical_nui_category_size': 24, 'logical_nui_entry_arrow_size': 28,
        'fit': 'NuiAspect.Fit; render independently of the control background.'},
    'tabs': {'tab_knowledge': 'ui_cdx_i_book', 'tab_quests': 'ui_cdx_i_shield',
        'tab_notes': 'ui_cdx_i_scroll', 'tab_reputation': 'ui_cdx_i_people',
        'tab_traits': 'ui_cdx_i_head', 'tab_economy': 'ui_cdx_i_coins'},
    'category_fallbacks': {'Knowledge': 'ui_cdx_i_book', 'Quests': 'ui_cdx_i_shield',
        'Notes': 'ui_cdx_i_scroll', 'Reputation': 'ui_cdx_i_people',
        'Traits': 'ui_cdx_i_head', 'Economy': 'ui_cdx_i_coins'},
    'actions': {
        'entry': {'family': 'entry', 'glyph': 'ui_cdx_i_next', 'selected': 'reflect_current_detail_selection'},
        'pagination_previous': {'background': 'ui_cdx_btn', 'glyph': 'ui_cdx_i_prev', 'selected': 'not_applicable_momentary'},
        'pagination_next': {'background': 'ui_cdx_btn', 'glyph': 'ui_cdx_i_next', 'selected': 'not_applicable_momentary'},
        'close': {'background': 'ui_cdx_close', 'glyph': 'baked_X', 'selected': 'not_applicable_momentary',
            'routing': 'Existing close/draft-protection path; never unconditional token.Close in production.'},
        'note_and_confirmation_actions': {'family': 'entry', 'glyph': 'none',
            'labels': ['New Note', 'Find', 'Clear', 'Edit', 'Delete', 'Save', 'Cancel', 'Keep', 'Discard', 'Confirm'],
            'selected': 'not_applicable_momentary', 'text': 'Live labels; preserve existing action IDs and behavior.'},
        'select_traits': {'family': 'entry', 'glyph': 'ui_cdx_i_head', 'text': 'Live Select Traits label'},
        'disabled_momentary_actions': {'widget_enabled': False, 'overlay_color_rgb': [110, 100, 80], 'activation_allowed': False},
        'editor_fields_dropdowns': 'Native controls and existing binds; do not replace with bitmap text.',
        'help': 'No implemented useful help action; ui_cdx_help is retained source artwork, not an active control.'},
    'states': {'normal': 'Canonical *_n_v2 texture', 'selected': 'Canonical *_s_v2, static glow',
        'disabled': 'Native disabled background plus explicit muted overlays and presenter guard.',
        'hover': 'Tooltip only; no new texture or dependency on hover events.',
        'pressed': 'No visual variant; matching left press/release gates activation.'},
    'colors_rgb': {'gold': [242, 196, 113], 'ink': [48, 29, 15], 'disabled_overlay': [110, 100, 80]},
    'verified_logical_nui_shell': {'size': [940, 650], 'gui_viewport': [3440, 1382], 'gui_scale_percent': 100,
        'client_server_versions': 'not supplied', 'evidence': 'User confirmed all 001 checks green on 2026-10-03.'},
    'layout_rules': ['Root group: padding 0, margin 0, border false, scrollbars None.',
        'Put fill/frame draw list on a child group, not the root group.',
        'Use explicit spacers for content insets; separate artwork inset from control inset.',
        'Native font and live content; let NWN apply GUI scaling once. Other scales remain task 007.',
        'Use normalized v2 backgrounds at fixed hit bounds; background/label/icon state changes do not move controls.',
        'No assumed seamless tiling; stretch fill samples as in the verified prototype.'],
    'deferred': ['Custom scrollbar geometry/interaction: 007.', 'Compact/high-scale layout verification: 007.',
        'Additional specialized category glyphs: use semantic tab fallback until needed.'],
}
manifest = dict(base)
manifest.update({'schema_version': 2, 'task': '002 — Finalize artwork states and asset contract',
    'asset_count': len(records), 'assets': records, 'base_manifest': 'manifest-000.json',
    'new_export_count': len(new_records), 'contract': contract,
    'generation_prompts_002': 'generation-prompts-002.json',
    'prototype_resrefs': sorted(['ui_cdx_bg', 'ui_cdx_outer', 'ui_cdx_paper', 'ui_cdx_close', 'ui_cdx_i_book',
        'ui_cdx_i_next', 'ui_cdx_cat_n', 'ui_cdx_cat_s', 'ui_cdx_ent_n', 'ui_cdx_ent_s', 'ui_cdx_tab_s'] +
        [f'ui_cdx_{p}_{s}' for p in ['fr','pn'] for s in ['tl','tr','bl','br','top','bot','left','right']]),
    'remaining_work': contract['deferred'] + ['Seven 002 exports require user bundling/deployment; verify them in the full shell milestone.']})
(source / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(source / 'asset-contract.json').write_text(json.dumps(contract, indent=2) + '\n')
(source / 'exports.txt').write_text(''.join(a['resref'] + '.png\n' for a in records))
(source / 'exports-002.txt').write_text(''.join(a['resref'] + '.png\n' for a in new_records))

# Contact sheet and disabled-treatment illustration (preview images are not game exports).
tiles = []
for i, a in enumerate(new_records):
    tile = preview / f'002-tile-{i}.png'
    run(out / (a['resref']+'.png'), '-resize', '352x100', '-background', '#171b20',
        '-gravity', 'center', '-extent', '380x130', '-gravity', 'south', '-splice', '0x42',
        '-font', 'DejaVu-Sans', '-pointsize', '14', '-fill', '#edcf94', '-annotate', '+0+20', a['resref'],
        '-pointsize', '11', '-fill', '#adb4bd', '-annotate', '+0+4', f"{a['width']} x {a['height']} | {a['state']}", tile)
    tiles.append(tile)
run('montage', *tiles, '-tile', '2x', '-geometry', '+6+6', '-background', '#11151a', preview / 'contact-sheet-002.png')
for tile in tiles: tile.unlink()

panels = []
for family, spec in families.items():
    for state in ['normal', 'selected', 'disabled']:
        ref = spec['states']['normal' if state == 'disabled' else state]
        for background in ['#000000', '#dbc69b', '#547a8e']:
            target = preview / f'002-check-{len(panels)}.png'
            ops = ['-colorspace', 'Gray', '-colorspace', 'sRGB'] if state == 'disabled' else []
            run(out/(ref+'.png'), *ops, '-background', background, '-gravity', 'center', '-extent', '380x112',
                '-gravity', 'south', '-splice', '0x28', '-font', 'DejaVu-Sans', '-pointsize', '12',
                '-fill', '#ffffcc' if background=='#000000' else '#17212a',
                '-annotate', '+0+7', f'{family} / {state}', target)
            panels.append(target)
run('montage', *panels, '-tile', '3x', '-geometry', '+3+3', '-background', '#1b2028', preview/'alpha-and-states-002.png')
for target in panels: target.unlink()

# Cross-format collision checks and immutable-resource baseline verification.
refs = [a['resref'] for a in records]
assert len(set(r.lower() for r in refs)) == len(refs)
assert all(re.fullmatch('[a-z0-9_]{1,16}', r) for r in refs)
current = {}
for path in resource_root.rglob('*'):
    if path.is_file(): current.setdefault(path.stem.lower(), []).append(path)
for ref in refs:
    matches = current.get(ref.lower(), [])
    assert len(matches) <= 1 and all(p.suffix.lower()=='.png' and p.name==ref+'.png' for p in matches), f'Collision: {ref}: {matches}'
for a in base['assets']:
    assert sha(base_dir/(a['resref']+'.png'))==a['sha256'], f'Changed 000 export: {a["resref"]}'
baseline = json.loads((source/'existing_resources_before_002.json').read_text())
for relative, digest in baseline.items():
    assert sha(resource_root/relative)==digest, f'Changed existing resource: {relative}'
for a in new_records:
    pixels = rgba(out/(a['resref']+'.png'))
    assert pixels.shape[:2] == (a['height'],a['width']) and sha(out/(a['resref']+'.png'))==a['sha256']
validation = {'status': 'pass', 'base_exports_unchanged': len(base['assets']),
    'existing_resources_unchanged': len(baseline), 'new_exports': len(new_records),
    'total_manifest_exports': len(records), 'normalized_controls_pixel_preserving': 6,
    'resref_length_max': max(map(len,refs)), 'cross_format_collisions': [],
    'new_png_rgba_dimensions_and_hashes': 'pass', 'canonical_control_interior_alpha': 'pass',
    'previous_glyph_bounds_and_transparent_margins': 'pass',
    'game_verification': '001 all green; seven 002 PNGs await user bundling and in-game review.'}
(source/'validation-002.json').write_text(json.dumps(validation, indent=2)+'\n')
print(json.dumps(validation))
