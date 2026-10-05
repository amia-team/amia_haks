#!/usr/bin/env python3
"""Export retained ImageGen masters; validate assets and build offline previews.

ImageGen reconstructs artwork. ImageMagick performs deterministic cropping,
slicing, resizing and composition. Pillow/NumPy only inspect pixels. This script
does not call ImageGen, pack a hak, deploy content, launch NWN or change C# code.
"""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


def run(*parts):
    subprocess.run(['magick', *map(str, parts)], check=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixels(path):
    with Image.open(path) as image:
        assert image.mode == 'RGBA', f'Expected RGBA: {path}'
        return np.asarray(image)


def geometry(rect):
    x, y, width, height = rect
    return f'{width}x{height}+{x}+{y}'


def bounds(path, region=None, margin=4):
    data = pixels(path)
    x, y, width, height = region or [0, 0, data.shape[1], data.shape[0]]
    yy, xx = np.where(data[y:y+height, x:x+width, 3] > 16)
    assert len(xx), f'Empty artwork: {path}'
    left, top = max(x, x+int(xx.min())-margin), max(y, y+int(yy.min())-margin)
    right = min(x+width, x+int(xx.max())+1+margin)
    bottom = min(y+height, y+int(yy.max())+1+margin)
    return [left, top, right-left, bottom-top]


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--export-dir', type=Path, required=True)
    parser.add_argument('--resource-root', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out, resource_root = args.export_dir.resolve(), args.resource_root.resolve()
    preview = source/'previews'
    out.mkdir(parents=True, exist_ok=True)
    preview.mkdir(exist_ok=True)
    baseline = json.loads((source/'existing_resources_before.json').read_text())
    # Detect unrelated changes before exporting into a real resource directory.
    for relative, digest in baseline.items():
        assert sha(resource_root/relative) == digest, f'Changed existing resource: {relative}'
    records = []
    previously_exported = {}
    if (source/'manifest.json').exists():
        previously_exported = {a['resref']: a['sha256']
                               for a in json.loads((source/'manifest.json').read_text())['assets']}

    def export(key, ref, input_path, rect=None, size=None, padding=None,
               notes='', reference_rect=None, parent=None, extra=None):
        command = [input_path]
        if rect:
            command += ['-crop', geometry(rect), '+repage']
        if size:
            command += ['-resize', size]
        target = out/f'{ref}.png'
        # Never silently replace an unrelated file, including an untracked PNG.
        if target.exists():
            assert ref in previously_exported and sha(target) == previously_exported[ref], \
                f'Refusing to replace unrecognized or modified export: {target}'
        run(*command, '-strip', f'PNG32:{target}')
        data = pixels(target)
        records.append({
            'key': key, 'resref': ref, 'export_path': f'src/hak/amia_nui/png/{ref}.png',
            'width': data.shape[1], 'height': data.shape[0], 'state': 'normal',
            'content_padding_ltrb': padding, 'sha256': sha(target),
            'alpha_min': int(data[:,:,3].min()), 'alpha_max': int(data[:,:,3].max()),
            'transparent_pixels': int((data[:,:,3] == 0).sum()),
            'provenance': {
                'method': 'slice_of_export' if parent else 'processed_imagegen_master',
                'source': str(input_path.name), 'source_sha256': sha(input_path),
                'source_crop_xywh': rect, 'resize': size, 'parent_resref': parent,
                'reference_crop_xywh': reference_rect,
                'reference_crop_is_approximate': reference_rect is not None,
                **(extra or {})},
            'notes': notes})
        return target

    def frame(parent, prefix, key, corner, top_center=0):
        data = pixels(parent)
        height, width = data.shape[:2]
        n = corner
        regions = {'tl': [0,0,n,n], 'tr': [width-n,0,n,n],
                   'bl': [0,height-n,n,n], 'br': [width-n,height-n,n,n],
                   'bot': [n,height-n,width-2*n,n],
                   'left': [0,n,n,height-2*n], 'right': [width-n,n,n,height-2*n]}
        if top_center:
            left = (width-top_center)//2
            regions.update({'top_l': [n,0,left-n,n], 'top_m': [left,0,top_center,n],
                            'top_r': [left+top_center,0,width-n-left-top_center,n]})
        else:
            regions['top'] = [n,0,width-2*n,n]
        for part, rect in regions.items():
            export(f'{key}.slice.{part}', f'{prefix}_{part}', parent, rect,
                   parent=parent.stem,
                   notes='Preserve corners; stretch straight rails only along their long axis. '
                         + ('Keep top_m ornament at uniform scale.' if top_center else 'No center fill slice.'))

    for key, ref, filename, size, padding, rectangle, corner, prefix, top_center in [
        ('frame.outer','ui_dlg_outer','outer-master.png','1180x1016!', [48,100,48,32],
         [143,56,1180,1016],112,'ui_dlg_fr',144),
        ('frame.portrait','ui_dlg_portrait','portrait-master.png','335x471!', [12,14,12,14],
         [188,161,335,471],48,'ui_dlg_pf',0),
        ('frame.dialogue','ui_dlg_panel','panel-master.png','746x491!', [34,22,34,60],
         [540,164,746,491],48,'ui_dlg_pn',0)]:
        master = source/filename
        target = export(key, ref, master, bounds(master), size, padding,
                        notes='Transparent opening; no fill or live content baked into frame. '
                              'Master artwork is reconstructed, not a pixel-exact extraction.',
                        reference_rect=rectangle)
        frame(target, prefix, key, corner, top_center)

    # Normalize button height uniformly, then resize only the middle strip.
    # This preserves the proportions of the decorative end caps even when the
    # generated master's overall aspect differs from the reference.
    with tempfile.TemporaryDirectory(prefix='dialogue-export-') as task_tmp:
        task_tmp = Path(task_tmp)
        for family, ref, filename, width, height, cap, padding, rectangle, prefix in [
            ('choice','ui_dlg_choice','choice-master.png',1088,56,32,[36,8,36,8],
             [189,670,1088,56],'ui_dlg_ch'),
            ('footer','ui_dlg_footer','footer-master.png',268,60,40,[44,10,44,10],
             [190,981,268,60],'ui_dlg_ft')]:
            master = source/filename
            master_rect = bounds(master)
            scaled = task_tmp/f'{family}-height.png'
            run(master, '-crop', geometry(master_rect), '+repage', '-resize', f'x{height}',
                '-strip', f'PNG32:{scaled}')
            data = pixels(scaled)
            original_width = data.shape[1]
            parts = []
            for name, rect, target_width in [
                ('l',[0,0,cap,height],cap),
                ('m',[cap,0,original_width-2*cap,height],width-2*cap),
                ('r',[original_width-cap,0,cap,height],cap)]:
                part = task_tmp/f'{family}-{name}.png'
                run(scaled, '-crop', geometry(rect), '+repage',
                    '-resize', f'{target_width}x{height}!', '-strip', f'PNG32:{part}')
                parts.append(part)
            normalized = task_tmp/f'{family}-normalized.png'
            run(*parts, '+append', '-strip', f'PNG32:{normalized}')
            target = export(f'control.{family}',ref,normalized,padding=padding,
                            notes='Empty opaque dark interior; fixed end caps and stretchable middle. '
                                  'Live label/glyph supplied by NUI; no pressed/selected artwork.',
                            reference_rect=rectangle,
                            extra={'method':'uniform_height_and_fixed_caps_from_imagegen_master',
                                   'source':filename,'source_sha256':sha(master),
                                   'source_crop_xywh':master_rect,
                                   'retained_master':filename,'retained_master_sha256':sha(master),
                                   'master_crop_xywh':master_rect,
                                   'uniform_height':height,'end_cap_width':cap,
                                   'normalized_from_width':original_width})
            for name, rect in [('l',[0,0,cap,height]),
                               ('m',[cap,0,width-2*cap,height]),
                               ('r',[width-cap,0,cap,height])]:
                export(f'control.{family}.slice.{name}',f'{prefix}_{name}',target,rect,
                       parent=ref,notes='Use equal height for all parts; only middle width may stretch.')

        divider_master = source/'divider-master.png'
        divider = export('decoration.divider','ui_dlg_divider',divider_master,
                         bounds(divider_master),'336x14!',
                         notes='Fine hairline with three hollow diamonds. Keep center ornament at uniform scale.',
                         reference_rect=[744,228,336,14])
        for name, rect in [('l',[0,0,150,14]),('m',[150,0,36,14]),('r',[186,0,150,14])]:
            export(f'decoration.divider.slice.{name}',f'ui_dlg_div_{name}',divider,rect,
                   parent=divider.stem,
                   notes='Center is fixed; stretch tails horizontally. Combine a tail and center for header side dividers.')
        rule_rect = bounds(divider, [12,0,120,14], margin=0)
        export('decoration.rule','ui_dlg_rule',divider,rule_rect,
               parent=divider.stem,notes='Straight gold hairline; stretch horizontally for header separator.')

        reuse = []
        for ref, role, decision in [
            ('ui_cdx_bg','shell and dialogue-panel fill',
             'Reuse: subdued black interlaced texture matches the supplied theme. Stretching is allowed; seamless tiling is not claimed.'),
            ('ui_cdx_close','close control',
             'Reuse: red/gold X fits the theme; rendering proportions must be checked in Step 1.'),
            ('ui_cdx_btn','text-pagination housing',
             'Reuse: blank square gold/dark housing; overlay a separate glyph.'),
            ('ui_cdx_i_prev','previous-text-page glyph',
             'Reuse: gold chevron rather than the reference triangle; accepted asset-stage style difference.'),
            ('ui_cdx_i_next','next-text-page and More glyph',
             'Reuse: gold chevron rather than the reference triangle; accepted asset-stage style difference.')]:
            path = resource_root/'png'/f'{ref}.png'
            data = pixels(path)
            reuse.append({'resref':ref,'role':role,'decision':decision,
                          'width':data.shape[1],'height':data.shape[0],'sha256':sha(path)})

        contract = {
            'schema_version':1,'units':'source pixels; no final logical NUI dimensions verified',
            'textures':'Direct RGBA PNG resrefs; no atlas.',
            'shell_source_size':[1180,1016],
            'frames': {
                'outer':{'master':'ui_dlg_outer','prefix':'ui_dlg_fr','corner':112,
                         'top_center_width':144,'slice_count':10,
                         'assembly':'Four corners, left/right/bottom rails, top_l/top_m/top_r. '
                                    'Uniformly scale corners/top_m; stretch straight rails only along their long axis.',
                         'fill':'ui_cdx_bg','fill_inset':12,'content_padding_ltrb':[48,100,48,32]},
                'portrait':{'master':'ui_dlg_portrait','prefix':'ui_dlg_pf','corner':48,
                            'slice_count':8,'aperture_xywh':[12,14,311,443],
                            'content_padding_ltrb':[12,14,12,14],
                            'assembly':'Eight slices; portrait stays beneath frame filigree, aspect preserved.'},
                'dialogue':{'master':'ui_dlg_panel','prefix':'ui_dlg_pn','corner':48,
                            'slice_count':8,'fill':'ui_cdx_bg','fill_inset':6,
                            'content_padding_ltrb':[34,22,34,60],
                            'assembly':'Eight slices; reserve pagination inside bottom padding.'}},
            'controls': {
                'choice':{'master':'ui_dlg_choice','parts':['ui_dlg_ch_l','ui_dlg_ch_m','ui_dlg_ch_r'],
                          'source_size':[1088,56],'end_cap_width':32,'content_padding_ltrb':[36,8,36,8]},
                'footer':{'master':'ui_dlg_footer','parts':['ui_dlg_ft_l','ui_dlg_ft_m','ui_dlg_ft_r'],
                          'source_size':[268,60],'end_cap_width':40,'content_padding_ltrb':[44,10,44,10]},
                'assembly':'Preserve cap aspect at the chosen height; stretch the middle horizontally. '
                           'If using the whole bitmap in one NuiImage, preserve its canonical aspect.',
                'text':'Live centered labels; More reserves space for a separate arrow.',
                'states':{'normal':'Canonical artwork','selected':'Not applicable to momentary dialogue actions',
                          'pressed':'No texture variant; later matching left press/release gates activation',
                          'hover':'Tooltip only','disabled':'Native disabled image plus muted overlays and presenter guard; verify in Step 1/2'}},
            'divider':{'master':'ui_dlg_divider','parts':['ui_dlg_div_l','ui_dlg_div_m','ui_dlg_div_r'],
                       'center_width':36,'source_height':14,'rule':'ui_dlg_rule',
                       'assembly':'Keep center ornament at uniform scale; stretch tail width only.'},
            'reused_resources':reuse,
            'rejected_reuse':{'ui_cdx_div_l':'Too heavy; use the new fine divider components.',
                              'ui_cdx_div_r':'Too heavy; use the new fine divider components.',
                              'ui_cdx_fr_*':'Different corner ornamentation.',
                              'ui_cdx_pn_*':'Different panel ornamentation.'},
            'offline_reference_layout': {
                'coordinate_origin':'Outer reference crop x143 y56; XYWH in source pixels',
                'shell':[0,0,1180,1016],'close':[1103,28,58,58],
                'portrait':[45,105,335,471],'dialogue_panel':[397,108,746,491],
                'choices':[[46,614+i*60,1088,56] for i in range(5)],
                'goodbye':[46,925,268,60],'more':[862,925,268,60]},
            'live_content':['Both speaker headings','NPC portrait','Dialogue body','Five response labels',
                            'Text-page counter','Goodbye','More-page counter'],
            'scope':'Assets and offline composition only; NUI implementation, packing, deployment and client review remain later stages.',
            'known_deviations':['ImageGen reconstruction is not pixel-exact artwork extraction.',
                                'Reused navigation glyphs are chevrons rather than the reference triangles.',
                                'Preview font is DejaVu Serif and does not predict the native NUI font.']}
        write_json(source/'asset-contract.json',contract)
        write_json(source/'manifest.json',{
            'schema_version':1,'stage':'Step 0','reference':{'file':'reference.png',
            'sha256':sha(source/'reference.png'),'width':1448,'height':1086},
            'toolchain':'Built-in image_gen reconstruction; ImageMagick export/composition; Pillow/NumPy read-only inspection.',
            'generation_prompts':'generation-prompts.json','asset_contract':'asset-contract.json',
            'asset_count':len(records),'assets':records,'reused_resources':reuse})
        (source/'exports.txt').write_text(''.join(a['resref']+'.png\n' for a in records))
        (source/'required-resources.txt').write_text(''.join(ref+'.png\n' for ref in
            sorted([a['resref'] for a in records]+[a['resref'] for a in reuse])))

        # Build previews exclusively with ImageMagick. Each fresh subprocess
        # avoids cumulative raster edits, and retained masters stay untouched.
        tiles = []
        for index, ref in enumerate(['ui_dlg_outer','ui_dlg_portrait','ui_dlg_panel',
                                     'ui_dlg_choice','ui_dlg_footer','ui_dlg_divider',
                                     'ui_cdx_close','ui_cdx_btn','ui_cdx_i_prev','ui_cdx_i_next']):
            path = out/f'{ref}.png' if ref.startswith('ui_dlg_') else resource_root/'png'/f'{ref}.png'
            tile = task_tmp/f'tile-{index}.png'
            run(path,'-resize','350x250','-background','#171b20','-alpha','remove',
                '-gravity','center','-extent','380x310','-gravity','south','-font','DejaVu-Sans',
                '-pointsize','16','-fill','#f2c471','-annotate','+0+8',ref,tile)
            tiles.append(tile)
        run('montage',*tiles,'-tile','2x','-geometry','+6+6','-background','#11151a',preview/'contact-sheet.png')

        checks = []
        for index, ref in enumerate(['ui_dlg_outer','ui_dlg_portrait','ui_dlg_panel',
                                     'ui_dlg_choice','ui_dlg_footer','ui_dlg_divider']):
            for background in ['#15191e','#e7d7b8','#654575']:
                tile = task_tmp/f'alpha-{len(checks)}.png'
                run(out/f'{ref}.png','-resize','340x240','-background',background,'-alpha','remove',
                    '-gravity','center','-extent','370x300','-gravity','south','-font','DejaVu-Sans',
                    '-pointsize','13','-fill','#ffffff' if background != '#e7d7b8' else '#221910',
                    '-annotate','+0+8',ref,tile)
                checks.append(tile)
        run('montage',*checks,'-tile','3x','-geometry','+4+4','-background','#11151a',preview/'alpha-checks.png')

        # Assemble sliced frames at canonical and alternate aspect ratios to
        # expose seam/corner mistakes independently of any future NUI code.
        def frame_layers(prefix,width,height,n,top_center=0):
            placements={'tl':(0,0,n,n),'tr':(width-n,0,n,n),
                        'bl':(0,height-n,n,n),'br':(width-n,height-n,n,n),
                        'bot':(n,height-n,width-2*n,n),
                        'left':(0,n,n,height-2*n),'right':(width-n,n,n,height-2*n)}
            if top_center:
                left=(width-top_center)//2
                placements.update({'top_l':(n,0,left-n,n),'top_m':(left,0,top_center,n),
                                   'top_r':(left+top_center,0,width-n-left-top_center,n)})
            else:
                placements['top']=(n,0,width-2*n,n)
            layers=[]
            for part,(x,y,w,h) in placements.items():
                layers += ['(',out/f'{prefix}_{part}.png','-resize',f'{w}x{h}!',')',
                           '-geometry',f'+{x}+{y}','-compose','Over','-composite']
            return layers

        for prefix,width,height,n,center,name in [
            ('ui_dlg_fr',1180,1016,112,144,'outer-assembled.png'),
            ('ui_dlg_pf',335,471,48,0,'portrait-assembled.png'),
            ('ui_dlg_pn',746,491,48,0,'panel-assembled.png'),
            ('ui_dlg_fr',940,780,90,116,'outer-resized.png'),
            ('ui_dlg_pf',240,340,34,0,'portrait-resized.png'),
            ('ui_dlg_pn',580,380,37,0,'panel-resized.png')]:
            run('-size',f'{width}x{height}','xc:none',*frame_layers(prefix,width,height,n,center),
                '-strip',f'PNG32:{preview/name}')

        composition=['-size','1180x1016','xc:none']
        def layer(path,x,y,width,height):
            composition.extend(['(',path,'-resize',f'{width}x{height}!',')',
                                '-geometry',f'+{x}+{y}','-compose','Over','-composite'])
        def divider_layer(x,y,width,height):
            center=round(36*height/14)
            left=(width-center)//2
            right=width-center-left
            layer(out/'ui_dlg_div_l.png',x,y,left,height)
            layer(out/'ui_dlg_div_m.png',x+left,y,center,height)
            layer(out/'ui_dlg_div_r.png',x+left+center,y,right,height)
        bg = resource_root/'png'/'ui_cdx_bg.png'
        layer(bg,12,12,1156,992)
        layer(preview/'outer-assembled.png',0,0,1180,1016)
        # A crop of the supplied portrait is preview-only, never a game export.
        sample_portrait=task_tmp/'sample-portrait.png'
        run(source/'reference.png','-crop','307x445+201+176','+repage',sample_portrait)
        layer(sample_portrait,57,119,311,443)
        layer(preview/'portrait-assembled.png',45,105,335,471)
        layer(bg,403,114,734,479)
        layer(preview/'panel-assembled.png',397,108,746,491)
        layer(out/'ui_dlg_rule.png',22,83,1136,3)
        layer(resource_root/'png'/'ui_cdx_close.png',1103,28,58,58)
        layer(out/'ui_dlg_div_l.png',235,45,45,14)
        layer(out/'ui_dlg_div_m.png',280,47,25,10)
        layer(out/'ui_dlg_div_m.png',860,47,25,10)
        layer(out/'ui_dlg_div_r.png',885,45,45,14)
        layer(out/'ui_dlg_divider.png',603,169,336,14)
        for x in [474,950]:
            divider_layer(x,144,104,12)
        for x,y,width,height in contract['offline_reference_layout']['choices']:
            layer(out/'ui_dlg_choice.png',x,y,width,height)
        layer(out/'ui_dlg_footer.png',46,925,268,60)
        layer(out/'ui_dlg_footer.png',862,925,268,60)
        for x,ref in [(640,'ui_cdx_i_prev'),(842,'ui_cdx_i_next')]:
            layer(resource_root/'png'/'ui_cdx_btn.png',x,542,64,48)
            layer(resource_root/'png'/f'{ref}.png',x+18,553,28,26)
        for x in [486,932]:
            divider_layer(x,559,112,12)
        layer(resource_root/'png'/'ui_cdx_i_next.png',1088,941,24,26)
        run(*composition,'-strip',f'PNG32:{preview/"dialogue-artwork.png"}')

        # Add representative LIVE content only to a separate offline preview.
        labels=[preview/'dialogue-artwork.png','-font','DejaVu-Serif','-fill','#f4dfa4']
        def centered(text,x,y,width,height,size):
            labels.extend(['(','-background','none','-fill','#f4dfa4','-font','DejaVu-Serif',
                           '-pointsize',str(size),'-gravity','center','-size',f'{width}x{height}',
                           f'caption:{text}',')','-gravity','northwest','-geometry',f'+{x}+{y}','-compose','Over','-composite'])
        centered('Guildhouse Guard Nefzen',315,23,535,58,35)
        centered('Guildhouse Guard Nefzen',477,126,582,46,29)
        body=('Duis commodo felis vitae mauris interdum condimentum. Quisque in pretium quam, '
              'posuere bibendum sem. Vivamus eu nulla cursus, congue velit vel, pharetra est.\n\n'
              'Praesent feugiat ante vitae luctus lobortis. Maecenas ante ante, cursus imperdiet '
              'lorem faucibus, sagittis ullamcorper mi.\n\nInteger nec ligula id ipsum condimentum.')
        labels.extend(['(','-background','none','-fill','#f4dfa4','-font','DejaVu-Serif',
                       '-pointsize','27','-gravity','northwest','-size','678x344',f'caption:{body}',')',
                       '-gravity','northwest','-geometry','+431+190','-compose','Over','-composite'])
        centered('4/8',720,542,104,48,28)
        for index,text in enumerate(['Goodbye','option','weee','egegegég','fefefefef']):
            centered(text,82,614+index*60,1016,56,28)
        centered('Goodbye',90,935,180,40,27)
        centered('More (1/2)',906,935,172,40,25)
        run(*labels,'-strip',f'PNG32:{preview/"dialogue-composition.png"}')

    # Validate actual exports, registry collisions and immutability after export.
    refs=[a['resref'] for a in records]
    assert len(set(refs)) == len(refs)
    assert all(re.fullmatch('[a-z0-9_]{1,16}',ref) for ref in refs)
    registry={}
    for path in resource_root.rglob('*'):
        if path.is_file():
            registry.setdefault(path.stem.lower(),[]).append(path)
    for ref in refs:
        matches=registry.get(ref,[])
        assert not matches or (len(matches)==1 and matches[0].resolve()==(out/f'{ref}.png').resolve()), \
            f'Cross-format or existing resource collision: {ref}: {matches}'
    for relative,digest in baseline.items():
        assert sha(resource_root/relative)==digest, f'Changed existing resource: {relative}'
    for asset in records:
        path=out/f'{asset["resref"]}.png'
        data=pixels(path)
        assert data.shape[:2] == (asset['height'],asset['width']) and sha(path)==asset['sha256']
        assert np.any(data[:,:,3]>16), f'Empty export: {path}'
    openings={}
    for ref,inset in [('ui_dlg_outer',112),('ui_dlg_portrait',48),('ui_dlg_panel',48)]:
        data=pixels(out/f'{ref}.png')
        alpha=data[inset:-inset,inset:-inset,3]
        assert not np.any(alpha>16), f'Opaque contamination in frame opening: {ref}'
        openings[ref]={'interior_alpha_max':int(alpha.max()),'opaque_pixels_over_16':0}
    for ref,padding in [('ui_dlg_choice',[36,8,36,8]),('ui_dlg_footer',[44,10,44,10])]:
        data=pixels(out/f'{ref}.png')
        left,top,right,bottom=padding
        assert np.all(data[top:-bottom,left:-right,3]>240), f'Transparent control interior: {ref}'
    seam_comparisons={}
    for ref,name in [('ui_dlg_outer','outer'),('ui_dlg_portrait','portrait'),('ui_dlg_panel','panel')]:
        canonical=pixels(out/f'{ref}.png')
        assembled=pixels(preview/f'{name}-assembled.png')
        # PNG over-compositing may clear invisible RGB or round alpha by one.
        # Compare visible premultiplied color, and validate raw slice crops below.
        a,b=canonical.astype(float),assembled.astype(float)
        color_delta=np.abs(a[:,:,:3]*a[:,:,3,None]/255-b[:,:,:3]*b[:,:,3,None]/255)
        alpha_delta=np.abs(a[:,:,3]-b[:,:,3])
        assert color_delta.max() <= 2 and alpha_delta.max() <= 1, f'Frame seam/reassembly mismatch: {ref}'
        seam_comparisons[ref]={'visible_color_delta_max':float(color_delta.max()),
                               'alpha_delta_max':int(alpha_delta.max()),
                               'result':'Matches within 8-bit over-compositing rounding.'}
    for asset in records:
        parent=asset['provenance']['parent_resref']
        if parent and asset['key'].startswith('frame.'):
            x,y,width,height=asset['provenance']['source_crop_xywh']
            original=pixels(out/f'{parent}.png')[y:y+height,x:x+width]
            assert np.array_equal(original,pixels(out/f'{asset["resref"]}.png')), f'Altered frame slice: {asset["resref"]}'
    validation={'status':'pass','new_exports':len(records),'reused_resources':len(reuse),
                'existing_resources_unchanged':len(baseline),'resref_length_max':max(map(len,refs)),
                'cross_format_collisions':[],'png_rgba_dimensions_and_hashes':'pass',
                'transparent_frame_openings':openings,'opaque_control_content_areas':'pass',
                'frame_slices_pixel_preserving':26,'frame_slice_reassembly':seam_comparisons,
                'visual_review':'pending','deterministic_rebuild':'pending',
                'game_verification':'Not performed; Step 1 alignment remains pending.',
                'packing_and_deployment':'Not performed.'}
    write_json(source/'validation.json',validation)
    print(json.dumps(validation,indent=2))


if __name__ == '__main__':
    main()
