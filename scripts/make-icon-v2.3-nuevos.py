#!/usr/bin/env python3
"""Iconos NUEVOS v2.3 de Gartic Móvil — 3 conceptos REALMENTE distintos.

Roi tenía razón: las variantes A/B/C de make-icon-v2.3.py eran el mismo
diseño con cambios mínimos. Estas tres son conceptos diferentes:

- A "Teléfono roto clásico": el auricular partido con rayo, pulido
  (auricular más grande y grueso, rotura más ancha, rayo marcado).
- B "Pájaro": mascota pájaro PROPIA (no el logo oficial), de formas
  planas y simples: cuerpo lavanda claro, ala violeta, pico amarillo,
  ojo grande. El pájaro de Gartic Phone es violeta con pico amarillo;
  aquí el cuerpo es claro para que se lea sobre el fondo violeta.
- C "Lápiz dibujando": un lápiz grueso en diagonal dibujando una línea
  quebrada (la grieta del teléfono roto) en blanco.

En las tres: "Gartic" blanco arriba, "MÓVIL" amarillo en grande abajo,
degradado violeta a magenta, todo dentro de la zona segura central
(199-823 de 1024 px). Fuente DejaVu Sans Bold. Sin aspecto IA.

NO instala nada: solo genera las tres opciones en
VERIFICACION/v2.3/iconos-nuevos/ para que Roi elija.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

VIOLET_TOP = (91, 31, 166)
VIOLET_MID = (106, 31, 181)
MAGENTA = (214, 51, 132)
DARK = (42, 26, 94)
WHITE = (255, 255, 255)
YELLOW = (255, 197, 49)
LAVENDER = (232, 222, 255)
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


def centered_text(draw, y_top, text, font, fill, stroke_w=5):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    w = bbox[2] - bbox[0]
    x = (1024 - w) / 2 - bbox[0]
    draw.text((x, y_top - bbox[1]), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=DARK)


def broken_handset(size, cx=512, cy=505, rx=225, ry=135, cup=82,
                   gap=60, bolt_scale=1.25):
    """Auricular clásico partido en dos, con rayo amarillo en medio."""
    s = size
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 180, 360,
          fill=WHITE + (255,), width=58)
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
    left = left.rotate(6, resample=Image.BICUBIC, center=(s // 2, s // 2))
    right = right.rotate(-7, resample=Image.BICUBIC, center=(s // 2, s // 2))
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.alpha_composite(left, (0, -12))
    out.alpha_composite(right, (18, 26))
    d = ImageDraw.Draw(out)
    bs = bolt_scale
    bx, by = s // 2, cy + 5
    bolt = [(bx - 20 * bs, by - 82 * bs), (bx + 48 * bs, by - 52 * bs),
            (bx + 10 * bs, by - 16 * bs), (bx + 58 * bs, by + 20 * bs),
            (bx - 28 * bs, by + 78 * bs), (bx + 4 * bs, by + 26 * bs),
            (bx - 48 * bs, by - 10 * bs)]
    d.polygon(bolt, fill=YELLOW + (255,), outline=DARK + (255,))
    return out


def bird(size, cx=512, cy=512):
    """Pájaro propio, formas planas: cuerpo lavanda, ala violeta,
    pico amarillo grande, ojo grande, mechón en la cabeza."""
    s = size
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    # cola (3 plumas que asoman a la izquierda del cuerpo)
    for dx, dy, w in ((-150, 40, 30), (-128, 58, 30), (-100, 72, 30)):
        d.rounded_rectangle([cx + dx - w // 2, cy + dy - 20,
                             cx + dx + w // 2, cy + dy + 40],
                            radius=15, fill=(106, 31, 181, 255),
                            outline=DARK + (255,), width=4)
    # cuerpo
    d.ellipse([cx - 150, cy - 115, cx + 150, cy + 120],
              fill=LAVENDER + (255,), outline=DARK + (255,), width=6)
    # barriga blanca
    d.ellipse([cx - 105, cy + 5, cx + 105, cy + 118],
              fill=WHITE + (255,))
    # ala violeta: media elipse en el costado izquierdo, con su borde
    d.pieslice([cx - 165, cy - 30, cx + 15, cy + 100], 180, 360,
               fill=(91, 31, 166, 255))
    d.arc([cx - 165, cy - 30, cx + 15, cy + 100], 180, 360,
          fill=DARK + (255,), width=5)
    # mechón de la cabeza (3 plumitas cortas, sin tocar "Gartic")
    for ang in (-30, 0, 30):
        d.line([cx - 8, cy - 104, cx - 8 + ang, cy - 132],
               fill=DARK + (255,), width=11)
    # ojo grande
    d.ellipse([cx + 55, cy - 78, cx + 115, cy - 18],
              fill=WHITE + (255,), outline=DARK + (255,), width=5)
    d.ellipse([cx + 72, cy - 62, cx + 102, cy - 32],
              fill=DARK + (255,))
    d.ellipse([cx + 82, cy - 56, cx + 94, cy - 44],
              fill=WHITE + (255,))
    # pico amarillo grande (dos partes)
    d.polygon([(cx + 128, cy - 55), (cx + 215, cy - 18),
               (cx + 128, cy + 8)], fill=YELLOW + (255,),
              outline=DARK + (255,))
    d.polygon([(cx + 128, cy + 8), (cx + 200, cy + 8),
               (cx + 128, cy + 42)], fill=(255, 170, 20, 255),
              outline=DARK + (255,))
    return out


def pencil_drawing(size, cx=512, cy=500):
    """Lápiz grueso en diagonal dibujando una línea quebrada blanca
    (la grieta del teléfono roto)."""
    s = size
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    # línea quebrada que sale de la punta del lápiz (hacia arriba-derecha)
    zig = [(cx - 30, cy + 55), (cx + 40, cy - 10), (cx + 95, cy - 55),
           (cx + 150, cy - 95), (cx + 205, cy - 55), (cx + 250, cy - 105)]
    d.line(zig, fill=WHITE + (255,), width=16, joint="curve")
    # estrellita al final del trazo
    ex, ey = zig[-1]
    for dx, dy in ((0, -26), (0, 26), (-26, 0), (26, 0)):
        d.line([ex, ey, ex + dx, ey + dy], fill=YELLOW + (255,), width=10)
    # lápiz: cuerpo amarillo en diagonal, de abajo-izquierda a centro
    pencil = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pencil)
    # cuerpo (rectángulo grueso)
    pd.rounded_rectangle([300, 470, 560, 540], radius=18,
                         fill=YELLOW + (255,), outline=DARK + (255,), width=6)
    # líneas del lápiz
    pd.line([330, 478, 530, 478], fill=DARK + (255,), width=4)
    pd.line([330, 532, 530, 532], fill=DARK + (255,), width=4)
    # punta de madera + mina
    pd.polygon([(560, 470), (640, 505), (560, 540)],
               fill=(255, 220, 170, 255), outline=DARK + (255,))
    pd.polygon([(610, 492), (640, 505), (610, 518)],
               fill=DARK + (255,))
    # goma rosa + casquillo
    pd.rounded_rectangle([252, 470, 300, 540], radius=12,
                         fill=(255, 120, 150, 255), outline=DARK + (255,),
                         width=5)
    pd.rectangle([300, 470, 318, 540], fill=(200, 200, 200, 255),
                 outline=DARK + (255,), width=4)
    pencil = pencil.rotate(28, resample=Image.BICUBIC, center=(cx, cy))
    out.alpha_composite(pencil)
    return out


def build(size=1024, art="handset", f_gartic=84, f_movil=110):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, f_gartic)
    fm = ImageFont.truetype(FONT, f_movil)
    centered_text(d, 288, "Gartic", fg, WHITE, stroke_w=5)
    if art == "handset":
        img.alpha_composite(broken_handset(size))
    elif art == "bird":
        img.alpha_composite(bird(size))
    elif art == "pencil":
        img.alpha_composite(pencil_drawing(size))
    centered_text(d, 635, "MÓVIL", fm, YELLOW, stroke_w=7)
    return img.convert("RGB")


def sim_miui(icon, px=96):
    crop = icon.crop((SAFE_LO, SAFE_LO, SAFE_HI, SAFE_HI))
    return crop.resize((px, px), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    variants = {
        "A": dict(art="handset", f_gartic=88, f_movil=116),
        "B": dict(art="bird", f_gartic=88, f_movil=116),
        "C": dict(art="pencil", f_gartic=88, f_movil=116),
    }
    for name, kw in variants.items():
        icon = build(1024, **kw)
        icon.save(os.path.join(OUT, f"icono-{name}.png"))
        sim_miui(icon, 96).save(
            os.path.join(OUT, f"icono-{name}-miui-96.png"))
        sim_miui(icon, 192).save(
            os.path.join(OUT, f"icono-{name}-miui-192.png"))
        print("variante", name, "lista")
    # tira comparativa: las tres a 96 px con etiquetas
    comp = Image.new("RGB", (96 * 3 + 40, 140), (255, 255, 255))
    cd = ImageDraw.Draw(comp)
    lab = ImageFont.truetype(FONT, 28)
    for i, name in enumerate("ABC"):
        sim = sim_miui(build(1024, **variants[name]), 96)
        comp.paste(sim, (10 + i * 106, 10))
        cd.text((10 + i * 106 + 30, 112), name, font=lab, fill=(0, 0, 0))
    comp.save(os.path.join(OUT, "comparativa-96.png"))
    print("iconos nuevos en", OUT)


if __name__ == "__main__":
    main()
