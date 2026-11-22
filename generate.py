#!/usr/bin/env python3
"""Golden honeycomb with thick dripping honey — one hero ingredient, macro close-up.

Deterministic: fixed seed, no clock, no network. Renders 1024x1024 PNG.
The picture is built from layered Pillow drawing only: a warm amber radial
backdrop, a full-frame honeycomb whose cells are filled with glossy honey,
thick honey drips falling from the top edge, and a glossy honey pool along
the bottom. No text anywhere.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
OUT = "entry.png"
rng = random.Random(20261122)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def radial_backdrop():
    """Warm amber glow: bright golden centre, deep burnt-honey edges."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    cx, cy = 512, 430
    for y in range(H):
        for x in range(W):
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2) / 760.0
            d = min(d, 1.0)
            # centre honey-gold -> mid amber -> dark caramel edge
            if d < 0.55:
                c = lerp((255, 196, 66), (232, 148, 32), d / 0.55)
            else:
                c = lerp((232, 148, 32), (96, 48, 8), (d - 0.55) / 0.45)
            px[x, y] = c
    return img


def hex_points(cx, cy, r):
    return [(cx + r * math.cos(math.radians(60 * i - 30)),
             cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]


def draw_honeycomb(base):
    """Full-frame honeycomb: each cell a glossy pool of honey."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = 118  # hex radius: big cells read clearly even at 300 px
    w_step = int(r * math.sqrt(3))
    h_step = int(r * 1.5)
    rows = 0
    for row, cy in enumerate(range(-40, H + 120, h_step)):
        offset = (w_step // 2) if row % 2 else 0
        for cx in range(-60 + offset, W + 120, w_step):
            depth = rng.uniform(0.0, 1.0)
            # honey fill: bright gold top, deep amber bottom
            top = lerp((255, 205, 80), (255, 222, 130), depth)
            bot = lerp((214, 128, 18), (178, 96, 8), depth)
            cell = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            cd = ImageDraw.Draw(cell)
            pts = hex_points(cx, cy, r)
            cd.polygon(pts, fill=top + (255,))
            # vertical honey shading inside the cell
            for yy in range(int(cy - r), int(cy + r) + 1):
                t = (yy - (cy - r)) / (2 * r)
                col = lerp(top, bot, t)
                cd.line([(cx - r, yy), (cx + r, yy)], fill=col + (255,))
            # clip shading to the hexagon
            mask = Image.new("L", (W, H), 0)
            md = ImageDraw.Draw(mask)
            md.polygon(pts, fill=255)
            cell.putalpha(Image.composite(cell.split()[3], Image.new("L", (W, H), 0), mask))
            layer.alpha_composite(cell)
            # thick beeswax wall
            d.polygon(pts, outline=(122, 62, 6, 255), width=14)
            d.line([pts[0], pts[1]], fill=(255, 226, 150, 255), width=5)
            # glossy highlight: bright crescent on the upper-left wall
            hx, hy = cx - r * 0.45, cy - r * 0.55
            d.ellipse([hx - 26, hy - 14, hx + 26, hy + 14], fill=(255, 240, 190, 150))
            rows += 1
    # soften the wax walls slightly so they read as real comb, not vector art
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    base.alpha_composite(layer)
    return base


def draw_drips(base):
    """Thick glossy honey streams falling from the top edge."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    streams = [
        (150, 46, 430), (330, 60, 610), (560, 52, 380),
        (740, 66, 560), (905, 44, 330),
    ]
    for x, wdt, length in streams:
        # main stream with rounded bottom
        d.rounded_rectangle([x - wdt // 2, -10, x + wdt // 2, length],
                            radius=wdt // 2, fill=(246, 166, 34, 255))
        # darker edge on the right side of the stream
        d.rounded_rectangle([x + wdt // 2 - 12, -10, x + wdt // 2, length],
                            radius=6, fill=(196, 106, 12, 255))
        # bright glossy stripe on the left side
        d.rounded_rectangle([x - wdt // 2 + 8, 0, x - wdt // 2 + 22, length - 30],
                            radius=7, fill=(255, 232, 160, 255))
        # droplet hanging at the end
        dy = length + 26
        d.ellipse([x - wdt // 2 - 6, dy - 34, x + wdt // 2 + 6, dy + 34],
                  fill=(246, 166, 34, 255))
        d.ellipse([x - wdt // 2 + 4, dy - 26, x - wdt // 2 + 20, dy + 6],
                  fill=(255, 236, 170, 255))
        # thin thread below the droplet
        d.line([(x, dy + 30), (x, dy + 78)], fill=(246, 166, 34, 255), width=7)
        d.ellipse([x - 9, dy + 76, x + 9, dy + 94], fill=(246, 166, 34, 255))
    layer = layer.filter(ImageFilter.GaussianBlur(0.8))
    base.alpha_composite(layer)
    return base


def draw_pool(base):
    """Glossy honey pool along the bottom with slow swirls."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([-120, 830, 1144, 1180], fill=(238, 152, 26, 255))
    d.ellipse([-40, 880, 1064, 1120], fill=(252, 186, 58, 255))
    # swirl arcs in the pool
    for cx, cy, rx, ry, wd in [(300, 960, 210, 46, 10), (700, 990, 260, 52, 12),
                               (520, 930, 150, 34, 8)]:
        d.arc([cx - rx, cy - ry, cx + rx, cy + ry], start=200, end=340,
              fill=(255, 226, 140, 220), width=wd)
        d.arc([cx - rx, cy - ry, cx + rx, cy + ry], start=20, end=160,
              fill=(190, 100, 10, 200), width=wd)
    # bright specular blobs on the pool
    d.ellipse([180, 905, 330, 945], fill=(255, 240, 190, 200))
    d.ellipse([760, 930, 880, 962], fill=(255, 240, 190, 180))
    layer = layer.filter(ImageFilter.GaussianBlur(1.0))
    base.alpha_composite(layer)
    return base


def finish(img):
    """Warm vignette + a whisper of grain so the picture feels photographic."""
    img = img.convert("RGB")
    overlay = Image.new("L", (W, H), 0)
    od = ImageDraw.Draw(overlay)
    od.ellipse([-260, -260, W + 260, H + 260], fill=255)
    overlay = overlay.filter(ImageFilter.GaussianBlur(180))
    dark = Image.new("RGB", (W, H), (52, 24, 2))
    img = Image.composite(img, dark, overlay)
    # deterministic grain
    px = img.load()
    for _ in range(9000):
        x = rng.randrange(W)
        y = rng.randrange(H)
        v = rng.randint(-9, 9)
        r, g, b = px[x, y]
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)),
                    max(0, min(255, b + v)))
    return img


def main():
    img = radial_backdrop().convert("RGBA")
    img = draw_honeycomb(img)
    img = draw_drips(img)
    img = draw_pool(img)
    img = finish(img)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
