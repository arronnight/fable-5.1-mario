#!/usr/bin/env python3
"""Cut sprite frames out of retro sprite-sheet rips.

Sheets use a solid background color (orange / cyan / teal / white). This tool
flood-fills the background from the image borders (so interior pixels that
share the bg color, e.g. white eyes, survive), finds foreground connected
components for inspection, and cuts manifest-listed boxes into trimmed RGBA
frames with optional palette remapping.

Usage:
  python3 tools/cut_sprites.py preview <sheet.png> <bg hex> <out.png> [minsize]
      numbered-box overview of every foreground component.
  python3 tools/cut_sprites.py cut <manifest.json> [assetsdir]
      cut frames; manifest maps name -> {sheet, bbox, palette?, pad?}.

Manifest bbox is [x0, y0, x1, y1] in sheet pixels (x1/y1 exclusive).
"""
import json
import os
import sys
from collections import deque

from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def hexrgb(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def load_rgb(path):
    return Image.open(path).convert('RGB')


def fg_mask(im, bg, tol=0):
    """Boolean foreground mask; background = flood fill of ~bg from borders."""
    w, h = im.size
    px = im.load()
    br, bgc, bb = bg
    isbg = bytearray(w * h)

    def match(x, y):
        r, g, b = px[x, y]
        return abs(r - br) <= tol and abs(g - bgc) <= tol and abs(b - bb) <= tol

    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if match(x, y) and not isbg[y * w + x]:
                isbg[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if match(x, y) and not isbg[y * w + x]:
                isbg[y * w + x] = 1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h:
                i = ny * w + nx
                if not isbg[i] and match(nx, ny):
                    isbg[i] = 1
                    q.append((nx, ny))
    return isbg  # 1 = background


def components(isbg, w, h, minsize=8):
    """4-connected foreground components -> [(x0,y0,x1,y1,count)], sorted y,x."""
    seen = bytearray(w * h)
    out = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if isbg[i] or seen[i]:
                continue
            q = deque([(x, y)])
            seen[i] = 1
            x0 = x1 = x
            y0 = y1 = y
            n = 0
            while q:
                cx, cy = q.popleft()
                n += 1
                if cx < x0:
                    x0 = cx
                if cx > x1:
                    x1 = cx
                if cy < y0:
                    y0 = cy
                if cy > y1:
                    y1 = cy
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if not isbg[j] and not seen[j]:
                            seen[j] = 1
                            q.append((nx, ny))
            if n >= minsize:
                out.append((x0, y0, x1 + 1, y1 + 1, n))
    out.sort(key=lambda b: (b[1] // 4, b[0]))
    return out


def cmd_preview(sheet, bghex, out, minsize=8):
    im = load_rgb(sheet)
    w, h = im.size
    isbg = fg_mask(im, hexrgb(bghex))
    comps = components(isbg, w, h, minsize)
    ov = im.copy()
    d = ImageDraw.Draw(ov)
    for i, (x0, y0, x1, y1, n) in enumerate(comps):
        d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(255, 0, 0))
        d.text((x0 + 1, max(0, y0 - 10)), str(i), fill=(255, 0, 0))
    ov.save(out)
    print(f'{sheet}: {len(comps)} components -> {out}')
    for i, (x0, y0, x1, y1, n) in enumerate(comps):
        print(f'  {i}: bbox=({x0},{y0},{x1},{y1}) size={x1-x0}x{y1-y0} px={n}')


def cut_frame(im, isbg, w, bbox, bg, palette=None, pad=0):
    x0, y0, x1, y1 = bbox
    # trim to actual foreground inside bbox
    tx0, ty0, tx1, ty1 = x1, y1, x0, y0
    px = im.load()
    for y in range(y0, y1):
        base = y * w
        for x in range(x0, x1):
            if not isbg[base + x] and px[x, y] != bg:
                if x < tx0:
                    tx0 = x
                if x + 1 > tx1:
                    tx1 = x + 1
                if y < ty0:
                    ty0 = y
                if y + 1 > ty1:
                    ty1 = y + 1
    if tx1 <= tx0:
        raise ValueError(f'empty frame bbox {bbox}')
    pal = {}
    if palette:
        pal = {tuple(map(int, k.split(','))): tuple(map(int, v.split(',')))
               for k, v in palette.items()}
    cw, ch = tx1 - tx0 + pad * 2, ty1 - ty0 + pad * 2
    out = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    op = out.load()
    for y in range(ty0, ty1):
        base = y * w
        for x in range(tx0, tx1):
            # A pixel is art only if the flood fill never reached it AND it
            # is not exactly the bg color (kills teal pockets trapped between
            # a sprite outline and the sheet's black grid lines).
            if not isbg[base + x] and px[x, y] != bg:
                c = px[x, y]
                op[x - tx0 + pad, y - ty0 + pad] = pal.get(c, c) + (255,)
    return out, (tx0, ty0, tx1, ty1)


def cmd_cut(manifest_path, assetsdir='assets'):
    with open(manifest_path) as f:
        man = json.load(f)
    sheets = {}
    cutdir = os.path.join(REPO, assetsdir, 'cut')
    os.makedirs(cutdir, exist_ok=True)
    report = {}
    for name, spec in man.items():
        spath = os.path.join(REPO, spec['sheet'])
        key = (spath, spec.get('bg', '#ff8040'))
        if key not in sheets:
            im = load_rgb(spath)
            w, h = im.size
            sheets[key] = (im, fg_mask(im, hexrgb(key[1])), w, h)
        im, isbg, w, h = sheets[key]
        frame, trimmed = cut_frame(im, isbg, w, spec['bbox'], hexrgb(key[1]),
                                   spec.get('palette'), spec.get('pad', 0))
        if spec.get('scale', 1) != 1:
            s = spec['scale']
            frame = frame.resize((frame.width * s, frame.height * s), Image.NEAREST)
        dest = os.path.join(cutdir, name + '.png')
        frame.save(dest)
        report[name] = {'file': os.path.relpath(dest, REPO),
                        'size': list(frame.size), 'trimmed': list(trimmed)}
        print(f"  {name}: {frame.size} trimmed={trimmed} -> {dest}")
    with open(os.path.join(REPO, assetsdir, 'cut', 'manifest.out.json'), 'w') as f:
        json.dump(report, f, indent=1)
    print(f'done: {len(report)} frames')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == 'preview':
        sheet, bghex, out = sys.argv[2:5]
        ms = int(sys.argv[5]) if len(sys.argv) > 5 else 8
        cmd_preview(sheet, bghex, out, ms)
    elif sys.argv[1] == 'cut':
        cmd_cut(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'assets')
    else:
        sys.exit(__doc__)
