#!/usr/bin/env python3
"""Slice ImageGen-prepared masters, export PNG resources, and build QA previews.

ImageGen performs reconstruction/background extraction. ImageMagick performs
deterministic slicing, sizing and preview composition. Pillow/NumPy read pixels
for bounds and validation only. No game, packer, Jenkins or deployment calls.
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
args = parser.parse_args()
source = Path(__file__).resolve().parent
out = args.export_dir.resolve()
preview = source / 'previews'
out.mkdir(parents=True, exist_ok=True)
preview.mkdir(exist_ok=True)
records = []


def run(*parts):
    subprocess.run(['magick', *map(str, parts)], check=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry(rect):
    x, y, w, h = rect
    return f'{w}x{h}+{x}+{y}'


def bounds(path, rect=None, threshold=16, margin=4):
    with Image.open(path) as im:
        pixels = np.asarray(im)
        x, y, w, h = rect or (0, 0, im.width, im.height)
        alpha = pixels[y:y+h, x:x+w, 3]
        yy, xx = np.where(alpha > threshold)
        if not len(xx):
            raise ValueError(f'Empty asset: {path}, {rect}')
        left = max(x, x + int(xx.min()) - margin)
        top = max(y, y + int(yy.min()) - margin)
        right = min(x+w, x + int(xx.max()) + 1 + margin)
        bottom = min(y+h, y + int(yy.max()) + 1 + margin)
        return [left, top, right-left, bottom-top]


def export(key, resref, master, rect=None, size=None, state='normal',
           padding=None, notes='', reference_rect=None, tight=False,
           icon=False, parent=None):
    path = source / master if not parent else out / master
    if tight:
        rect = bounds(path, rect)
    command = [path]
    if rect:
        command += ['-crop', geometry(rect), '+repage']
    if size:
        command += ['-resize', size]
    if icon:
        command += ['-background', 'none', '-gravity', 'center', '-extent', '64x64']
    target = out / f'{resref}.png'
    run(*command, '-strip', f'PNG32:{target}')
    with Image.open(target) as im:
        pixels = np.asarray(im)
        alpha = pixels[:, :, 3]
        records.append({
            'key': key, 'resref': resref,
            'export_path': f'src/hak/amia_nui/png/{resref}.png',
            'width': im.width, 'height': im.height,
            'state': state, 'content_padding': padding,
            'provenance': {
                'method': 'slice_of_export' if parent else 'slice_of_imagegen_master',
                'master': master, 'master_sha256': sha(path),
                'master_crop_xywh': rect,
                'reference_crop_xywh': reference_rect,
                'reference_crop_is_approximate': reference_rect is not None,
                'resize': size, 'parent_resref': parent,
                'centered_in_64px_cell': icon,
            },
            'alpha_min': int(alpha.min()), 'alpha_max': int(alpha.max()),
            'transparent_pixels': int((alpha == 0).sum()),
            'sha256': sha(target), 'notes': notes,
        })
    return target


export('frame.outer', 'ui_cdx_outer', 'frame-master.png', tight=True,
       size='1248x754!', padding=[42, 38, 42, 38], reference_rect=[20, 89, 1248, 754],
       notes='Reconstructed transparent outer frame; top-right corner repaired. Center is transparent. Use slices for resizing.')


def slices(parent, prefix, key, inset):
    with Image.open(out / f'{parent}.png') as im:
        w, h = im.size
    n = inset
    regions = {
        'tl': [0, 0, n, n], 'tr': [w-n, 0, n, n],
        'bl': [0, h-n, n, n], 'br': [w-n, h-n, n, n],
        'top': [n, 0, w-2*n, n], 'bot': [n, h-n, w-2*n, n],
        'left': [0, n, n, h-2*n], 'right': [w-n, n, n, h-2*n],
    }
    for name, region in regions.items():
        export(f'{key}.{name}', f'{prefix}_{name}', f'{parent}.png', region,
               parent=parent, notes=f'Fixed {n}px corner inset. Stretch edge along its long axis only; no center slice.')


slices('ui_cdx_outer', 'ui_cdx_fr', 'frame.outer.slice', 54)

controls = [
    ('tab.normal', 'ui_cdx_tab_n', [1290, 154, 254, 94], 'normal', [20, 15, 20, 15], [1296, 163, 234, 76]),
    ('tab.selected', 'ui_cdx_tab_s', [1290, 52, 254, 101], 'selected', [20, 20, 20, 20], [1296, 63, 234, 81]),
    ('category.normal', 'ui_cdx_cat_n', [1290, 349, 254, 65], 'normal', [16, 12, 16, 12], [1296, 354, 236, 53]),
    ('category.selected', 'ui_cdx_cat_s', [1286, 275, 264, 73], 'selected', [24, 15, 24, 15], [1293, 283, 246, 62]),
    ('entry.normal', 'ui_cdx_ent_n', [1288, 518, 361, 85], 'normal', [16, 14, 16, 14], [1296, 522, 342, 73]),
    ('entry.selected', 'ui_cdx_ent_s', [1288, 433, 361, 84], 'selected', [16, 14, 16, 14], [1296, 440, 342, 71]),
    ('button.help', 'ui_cdx_help', [1366, 726, 87, 88], 'normal', None, [1375, 732, 70, 71]),
    ('button.close', 'ui_cdx_close', [1481, 724, 89, 91], 'normal', None, [1490, 732, 68, 71]),
    ('ornament.divider.left', 'ui_cdx_div_l', [1289, 824, 154, 65], 'decoration', None, [1296, 833, 132, 43]),
    ('ornament.divider.right', 'ui_cdx_div_r', [1501, 824, 151, 65], 'decoration', None, [1513, 833, 127, 43]),
    ('scrollbar.reference', 'ui_cdx_scroll', [1569, 38, 78, 380], 'decoration', None, [1572, 49, 57, 359]),
    ('panel.compact', 'ui_cdx_panel', [1333, 627, 269, 96], 'normal', [22, 18, 22, 18], [1341, 639, 246, 74]),
]
for key, name, rect, state, padding, reference_rect in controls:
    export(key, name, 'clean-master.png', rect, tight=True, state=state,
           padding=padding, reference_rect=reference_rect,
           notes='Icons removed by ImageGen; label/icon overlays remain separate.' if key.startswith(('tab.', 'category.', 'entry.')) else
                 'Reference artwork only; thumb/track are not a working scrollbar.' if key.startswith('scrollbar.') else '')

slices('ui_cdx_panel', 'ui_cdx_pn', 'frame.panel.slice', 36)

for key, name, rect in [
    ('background.dark', 'ui_cdx_bg', [307, 309, 389, 410]),
    ('background.header', 'ui_cdx_hdrbg', [743, 209, 442, 36]),
    ('background.selected', 'ui_cdx_brown', [1354, 304, 159, 26]),
    ('scrollbar.cap.top', 'ui_cdx_sb_top', [1575, 48, 61, 74]),
    ('scrollbar.cap.bottom', 'ui_cdx_sb_bot', [1575, 346, 61, 65]),
    ('scrollbar.thumb', 'ui_cdx_sb_thumb', [1585, 125, 21, 214]),
    ('scrollbar.rail.sample', 'ui_cdx_sb_rail', [1217, 673, 16, 65]),
]:
    export(key, name, 'clean-master.png', rect, state='decoration' if key.startswith('scrollbar.') else 'normal',
           notes='Source sample; not guaranteed tileable. Custom scrollbar geometry/range remains task 007.' if key.startswith('scrollbar.') else
                 'Uninterrupted source texture; not guaranteed tileable.', reference_rect=rect)

export('background.parchment', 'ui_cdx_paper', 'parchment-master.png', tight=True,
       size='474x546!', padding=[22, 22, 22, 22], reference_rect=[728, 262, 474, 546],
       notes='Parchment isolated/reconstructed by ImageGen; transparent torn edges, no writing.')
export('button.blank', 'ui_cdx_btn', 'button-master.png', tight=True, size='64x64!',
       padding=[9, 9, 9, 9], reference_rect=[1579, 452, 43, 48],
       notes='Reconstructed glyph-free arrow-button housing. Compose with a separate chevron.')

icons = ['book', 'shield', 'scroll', 'people', 'head', 'coins', 'compass', 'gear', 'cave', 'target',
         'temple', 'pin', 'leaf', 'crown', 'sun', 'swirl', 'chat', 'next', 'up', 'down']
cols = [(40, 320), (325, 575), (580, 830), (840, 1090), (1100, 1370)]
rows = [(80, 330), (345, 600), (610, 835), (850, 1080)]
reference_icons = [
    [75, 124, 40, 40], [333, 122, 33, 45], [520, 121, 42, 46], [710, 121, 45, 47], [902, 121, 45, 47],
    [1099, 119, 44, 50], [80, 304, 31, 33], [80, 347, 31, 33], [80, 391, 32, 31], [80, 431, 32, 36],
    [80, 475, 32, 38], [80, 519, 32, 39], [80, 565, 33, 32], [78, 606, 36, 35], [80, 652, 33, 32],
    [80, 696, 33, 34], [79, 742, 34, 36], [1588, 462, 20, 27], [1584, 82, 26, 36], [1584, 349, 26, 36],
]
for i, name in enumerate(icons):
    x1, x2 = cols[i % 5]
    y1, y2 = rows[i // 5]
    export(f'icon.{name}', f'ui_cdx_i_{name}', 'icons-master.png', [x1, y1, x2-x1, y2-y1],
           tight=True, size='56x56', icon=True, reference_rect=reference_icons[i],
           padding=[4, 4, 4, 4], notes='Theme-matched ImageGen reconstruction, not a pixel-exact original crop. 64px transparent cell, glyph fits 56px.')

gaps = [
    'Disabled/hover/pressed variants are not supplied; finalize required states in task 002 after prototype evidence.',
    'Normal and selected backgrounds retain different source bounds; harmonize nine-slice/content padding in task 002.',
    'Texture fill samples are not proven seamless; render as fills initially rather than assuming tiling.',
    'Scrollbar caps/thumb/rail are reference samples. A coherent empty track and synchronized interactive geometry remain task 007.',
    'Category icons for Notes/Traits/Economy filters beyond the reference require a neutral icon or later artwork.',
    'Generated glyphs, parchment boundary and empty frame are theme-matched reconstructions; they are not exact pixel extractions.',
    'No archive has been built and no NUI rendering has been tested; those checks belong to the user.',
]
manifest = {
    'schema_version': 1, 'task': '000 — Extract Assets',
    'reference': {'file': 'reference.png', 'sha256': sha(source / 'reference.png'), 'width': 1671, 'height': 941},
    'asset_root': 'amia_haks', 'bundle_target': 'amia_nui', 'resource_type': 'png',
    'toolchain': 'Built-in image_gen for editing/reconstruction; ImageMagick for deterministic slicing/export/previews.',
    'padding_order': ['left', 'top', 'right', 'bottom'],
    'crop_coordinates': 'XYWH in the named master, not the original reference. Reference rectangles are approximate provenance only.',
    'generation_prompts': 'generation-prompts.json', 'asset_count': len(records),
    'prototype_resrefs': ['ui_cdx_outer', 'ui_cdx_bg', 'ui_cdx_paper', 'ui_cdx_cat_n', 'ui_cdx_cat_s',
                         'ui_cdx_ent_n', 'ui_cdx_btn', 'ui_cdx_i_next', 'ui_cdx_i_book', 'ui_cdx_close'],
    'remaining_work': gaps, 'assets': records,
}
(source / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(source / 'exports.txt').write_text('\n'.join(f"{r['resref']}.png" for r in records) + '\n')

# Labeled review tiles show every exported PNG without altering game resources.
tiles = []
for i, r in enumerate(records):
    tile = preview / f'tile-{i:02}.png'
    run(out / f"{r['resref']}.png", '-resize', '240x125', '-background', '#242930',
        '-gravity', 'center', '-extent', '272x160', '-gravity', 'south', '-splice', '0x40',
        '-font', 'DejaVu-Sans', '-pointsize', '13', '-fill', '#edd5a4',
        '-annotate', '+0+18', r['resref'], '-pointsize', '10', '-fill', '#a7afb8',
        '-annotate', '+0+4', f"{r['width']} x {r['height']} | {r['state']}", tile)
    tiles.append(tile)
run('montage', *tiles, '-tile', '5x', '-geometry', '+6+6', '-background', '#11151a', preview / 'contact-sheet.png')
for tile in tiles:
    tile.unlink()

# Three background checks: transparent edges are visible independently of black.
mask_assets = ['ui_cdx_outer', 'ui_cdx_cat_s', 'ui_cdx_tab_n', 'ui_cdx_paper', 'ui_cdx_close', 'ui_cdx_i_book']
mask_tiles = []
for i, name in enumerate(mask_assets):
    for j, background in enumerate(['#000000', '#64798a', 'pattern:checkerboard']):
        tile = preview / f'mask-{i}-{j}.png'
        run('-size', '390x170', f'xc:{background}' if not background.startswith('pattern:') else background,
            '(', out / f'{name}.png', '-resize', '350x125', ')', '-gravity', 'center', '-compose', 'over', '-composite',
            '-gravity', 'south', '-background', '#151a20', '-splice', '0x28', '-font', 'DejaVu-Sans', '-pointsize', '12',
            '-fill', '#edd5a4', '-annotate', '+0+8', name, tile)
        mask_tiles.append(tile)
run('montage', *mask_tiles, '-tile', '3x', '-geometry', '+4+4', '-background', '#11151a', preview / 'alpha-checks.png')
for tile in mask_tiles:
    tile.unlink()

# Assemble a theme preview strictly from exports. Text below is preview-only.
command = ['-size', '1280x850', 'xc:#090b0e']


def place(name, x, y, width, height):
    command.extend(['(', out / f'{name}.png', '-resize', f'{width}x{height}!', ')',
                    '-geometry', f'+{x}+{y}', '-compose', 'over', '-composite'])


def panel(x, y, width, height):
    n = 36
    place('ui_cdx_bg', x+10, y+10, width-20, height-20)
    for suffix, dx, dy, w, h in [
        ('tl', 0, 0, n, n), ('tr', width-n, 0, n, n),
        ('bl', 0, height-n, n, n), ('br', width-n, height-n, n, n),
        ('top', n, 0, width-2*n, n), ('bot', n, height-n, width-2*n, n),
        ('left', 0, n, n, height-2*n), ('right', width-n, n, n, height-2*n),
    ]:
        place(f'ui_cdx_pn_{suffix}', x+dx, y+dy, w, h)


place('ui_cdx_bg', 40, 85, 1198, 704)
place('ui_cdx_outer', 20, 62, 1240, 754)
tab_names = ['Knowledge', 'Quests', 'Notes', 'Reputation', 'Traits', 'Economy']
for i, (label, icon) in enumerate(zip(tab_names, ['book', 'shield', 'scroll', 'people', 'head', 'coins'])):
    x = 47 + i*194
    place('ui_cdx_tab_s' if i == 0 else 'ui_cdx_tab_n', x, 90, 188, 76)
    place(f'ui_cdx_i_{icon}', x+15, 105, 42, 42)
panel(47, 182, 242, 599)
panel(297, 182, 425, 599)
panel(730, 182, 498, 599)
place('ui_cdx_hdrbg', 752, 201, 454, 45)
place('ui_cdx_paper', 753, 255, 451, 503)
categories = ['All', 'Arcana', 'Engineering', 'Dungeoneering', 'Geography', 'History', 'Local', 'Nature', 'Nobility', 'Religion', 'The Planes', 'OOC']
cat_icons = ['book', 'compass', 'gear', 'cave', 'target', 'temple', 'pin', 'leaf', 'crown', 'sun', 'swirl', 'chat']
for i, icon in enumerate(cat_icons):
    y = 211 + i*44
    place('ui_cdx_cat_s' if i == 0 else 'ui_cdx_cat_n', 66, y, 202, 42)
    place(f'ui_cdx_i_{icon}', 77, y+6, 30, 30)
place('ui_cdx_ent_s', 314, 211, 391, 75)
place('ui_cdx_btn', 650, 226, 44, 44)
place('ui_cdx_i_next', 660, 236, 24, 24)
place('ui_cdx_div_l', 333, 722, 111, 45)
place('ui_cdx_div_r', 572, 722, 111, 45)
place('ui_cdx_help', 1128, 20, 58, 58)
place('ui_cdx_close', 1194, 20, 58, 58)
command.extend(['-font', 'DejaVu-Sans', '-pointsize', '14', '-fill', '#ead19f'])
for i, label in enumerate(tab_names):
    command.extend(['-annotate', f'+{47+i*194+61}+134', label])
for i, label in enumerate(categories):
    command.extend(['-annotate', f'+113+{238+i*44}', label])
command.extend(['-pointsize', '18', '-annotate', '+338+242', 'A guide to Amia',
                '-pointsize', '13', '-fill', '#bdad8d', '-annotate', '+338+265', 'Knowledge entry',
                '-pointsize', '17', '-fill', '#ead19f', '-annotate', '+785+229', 'The Codex',
                '-pointsize', '23', '-fill', '#392716', '-annotate', '+782+307', 'A guide to Amia',
                '-pointsize', '16', '-annotate', '+782+347', 'Lore, discoveries, and stories belong here.',
                '-annotate', '+782+379', 'The artwork is separate from the text.',
                '-annotate', '+782+411', 'Gold frames and parchment follow the mockup.',
                '-pointsize', '13', '-fill', '#d3bd92', '-annotate', '+47+835',
                'OFFLINE ASSET COMPOSITION — preview fonts/text only; NUI rendering remains unverified.',
                preview / 'codex-composition.png'])
run(*command)

# Validate decoded resources, collisions, preserved baseline and manifest hashes.
existing = {}
for path in args.resource_root.rglob('*'):
    if path.is_file():
        existing.setdefault(path.stem.casefold(), []).append(path)
errors = []
seen = set()
for r in records:
    name = r['resref']
    if not re.fullmatch(r'[a-z0-9_]{1,16}', name) or name in seen:
        errors.append(f'Invalid/duplicate resref: {name}')
    seen.add(name)
    path = out / f'{name}.png'
    with Image.open(path) as im:
        im.load()
        if im.mode != 'RGBA' or im.size != (r['width'], r['height']):
            errors.append(f'Wrong mode/dimensions: {name}')
    if sha(path) != r['sha256'] or r['alpha_max'] < 245:
        errors.append(f'Hash/alpha error: {name}')
    for other in existing.get(name.casefold(), []):
        if other.suffix.lower() != '.png' or sha(other) != r['sha256']:
            errors.append(f'Resource collision: {other}')
baseline = json.loads((source / 'existing_resources_before.json').read_text())
changed = [name for name, digest in baseline.items()
           if not (args.resource_root / name).is_file() or sha(args.resource_root / name) != digest]
errors.extend(f'Existing resource changed: {name}' for name in changed)
report = {'status': 'pass' if not errors else 'fail', 'asset_count': len(records),
          'baseline_resources_unchanged': len(baseline)-len(changed),
          'checks': ['PNG decode/RGBA', 'dimensions/hashes', 'resrefs <=16 characters',
                     'case-insensitive cross-format collision scan', 'existing-resource checksums'],
          'errors': errors, 'game_verified': False, 'bundle_built': False}
(source / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if errors:
    raise SystemExit(1)
