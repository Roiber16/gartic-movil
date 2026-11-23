#!/usr/bin/env python3
"""Icono v2.3 de Gartic Móvil — 3 variantes para que Roi elija.

Idea (la misma de v2/v2.1, pedida por Roi): teléfono roto (auricular
clásico partido en dos) con el nombre escrito en el propio ícono
("Gartic" arriba en blanco, "MÓVIL" en grande abajo en amarillo), sobre
degradado violeta a magenta. Colores planos, sin aspecto IA.
Fuente DejaVu Sans Bold (del sistema).

Zona segura (lección de la v2.1): TODO el contenido cabe dentro del
cuadro central de 626 px (de 199 a 823 en un lienzo de 1024), porque el
launcher de MIUI solo enseña esa zona.

Variantes:
- A "Clásico mejorado": como la v2.1 pero con el auricular más grande,
  la rotura más ancha y el rayo más grande.
- B "Diagonal": el auricular entero inclinado -12°, más dinámico;
  "MÓVIL" aún más grande abajo.
- C "Partido abierto": las dos mitades bien separadas, con chispas
  amarillas en la rotura; el teléfono más pequeño y el nombre manda.

La variante elegida se instala con install.py (o a mano): se copia a
assets/icon-1024.png y a todos los mipmap-* (ver make-icon-v2.1.py).
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

VIOLET_TOP = (91, 31, 166)
VIOLET_MID = (106, 31, 181)
MAGENTA = (214, 51, 132)
DARK = (42, 26, 94)
WHITE = (255, 255, 255)
YELLOW = (255, 197, 49)
SAFE_LO, SAFE_HI = 199, 823


def gradient(size):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        if t < 0.5:
            a, b, f = VIOLET_TOP, VIOLET_MID, t / 0.5
        else:
            a, b, f = VIOLET_MID, MAGENTA, (t - 0.5) / 0.5
        c = tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def broken_handset(size, cx=512, cy=505, rx=200, ry=120, cup=72,
                   gap=46, rot_l=5, rot_r=-6, off_l=(0, -10),
                   off_r=(16, 24), bolt_scale=1.0, tilt=0, sparks=False):
    s = size
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 180, 360,
          fill=WHITE + (255,), width=52)
    for ex in (cx - rx, cx + rx):
        r = cup
        d.ellipse([ex - r, cy - r, ex + r, cy + r], fill=WHITE + (255,))
        r2 = int(cup * 0.53)
        d.ellipse([ex - r2, cy - r2, ex + r2, cy + r2], fill=DARK + (255,))
    left = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    right = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    lm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(lm).rectangle([0, 0, s // 2 - gap, s], fill=255)
    left.paste(layer, (0, 0), lm)
    rm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(rm).rectangle([s // 2 + gap, 0, s, s], fill=255)
    right.paste(layer, (0, 0), rm)
    left = left.rotate(rot_l, resample=Image.BICUBIC, center=(s // 2, s // 2))
    right = right.rotate(rot_r, resample=Image.BICUBIC, center=(s // 2, s // 2))
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.alpha_composite(left, off_l)
    out.alpha_composite(right, off_r)
    d = ImageDraw.Draw(out)
    bs = bolt_scale
    bx, by = s // 2, cy + 5
    bolt = [(bx - 20 * bs, by - 82 * bs), (bx + 48 * bs, by - 52 * bs),
            (bx + 10 * bs, by - 16 * bs), (bx + 58 * bs, by + 20 * bs),
            (bx - 28 * bs, by + 78 * bs), (bx + 4 * bs, by + 26 * bs),
            (bx - 48 * bs, by - 10 * bs)]
    d.polygon(bolt, fill=YELLOW + (255,), outline=DARK + (255,))
    if sparks:
        for (x1, y1, x2, y2) in [
                (bx - 95, by - 60, bx - 120, by - 95),
                (bx - 85, by + 40, bx - 118, by + 62),
                (bx + 95, by - 55, bx + 122, by - 88),
                (bx + 88, by + 45, bx + 120, by + 66)]:
            d.line([x1, y1, x2, y2], fill=YELLOW + (255,), width=9)
            d.line([x1, y1, x2, y2], fill=DARK + (255,), width=13)
            d.line([x1, y1, x2, y2], fill=YELLOW + (255,), width=9)
    if tilt:
        out = out.rotate(tilt, resample=Image.BICUBIC, center=(s // 2, s // 2))
    return out


def centered_text(draw, y_top, text, font, fill, stroke_w=5):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    w = bbox[2] - bbox[0]
    x = (1024 - w) / 2 - bbox[0]
    draw.text((x, y_top - bbox[1]), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=DARK)
    return (x + bbox[0], y_top, x + bbox[2], y_top + (bbox[3] - bbox[1]))


def build(size=1024, f_gartic=84, f_movil=110, handset=None):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, f_gartic)
    fm = ImageFont.truetype(FONT, f_movil)
    centered_text(d, 288, "Gartic", fg, WHITE, stroke_w=5)
    img.alpha_composite(broken_handset(size, **(handset or {})))
    centered_text(d, 635, "MÓVIL", fm, YELLOW, stroke_w=7)
    return img.convert("RGB")


def sim_miui(icon, px=96):
    crop = icon.crop((SAFE_LO, SAFE_LO, SAFE_HI, SAFE_HI))
    return crop.resize((px, px), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    variants = {
        "A": dict(f_gartic=88, f_movil=116, handset=dict(
            rx=215, ry=130, cup=78, gap=56, bolt_scale=1.15)),
        "B": dict(f_gartic=76, f_movil=122, handset=dict(
            cy=495, rx=205, ry=118, cup=72, gap=50, bolt_scale=1.2,
            tilt=-12)),
        "C": dict(f_gartic=80, f_movil=110, handset=dict(
            cy=490, rx=185, ry=108, cup=66, gap=72, rot_l=8, rot_r=-9,
            off_l=(-14, -16), off_r=(26, 30), bolt_scale=1.0,
            sparks=True)),
    }
    for name, kw in variants.items():
        icon = build(1024, **kw)
        icon.save(os.path.join(OUT, f"icon-{name}.png"))
        sim_miui(icon, 96).save(os.path.join(OUT, f"icon-{name}-miui-96.png"))
        sim_miui(icon, 192).save(os.path.join(OUT, f"icon-{name}-miui-192.png"))
        print("variante", name, "lista")
    print("iconos v2.3 en", OUT)


if __name__ == "__main__":
    main()
