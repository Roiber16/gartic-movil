#!/usr/bin/env python3
"""Icono v2 de Gartic Móvil — teléfono roto + nombre.

Diseno: fondo degradado vertical violeta -> magenta; arriba "Gartic" en
blanco; en el centro un auricular clasico de telefono partido en dos
(mitad izquierda y mitad derecha separadas, con un rayo amarillo en la
rotura); abajo "MÓVIL" en grande en amarillo. Colores planos, bordes
gruesos, sin aspecto IA. Fuente DejaVu Sans Bold (del sistema).
Genera assets/icon-1024.png y todos los mipmap-* (launcher, round y
foreground) en android/... y assets/res/...
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.expanduser("~/workspace/gartic-movil")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

VIOLET_TOP = (91, 31, 166)      # #5b1fa6
VIOLET_MID = (106, 31, 181)     # #6a1fb5
MAGENTA = (214, 51, 132)        # #d63384
DARK = (42, 26, 94)             # #2a1a5e
WHITE = (255, 255, 255)
YELLOW = (255, 197, 49)         # #ffc531
GREEN = (46, 230, 168)          # #2ee6a8


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


def handset_layer(size):
    """Auricular clasico completo (arco grueso + dos copas) en capa aparte."""
    s = size
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = s // 2, int(s * 0.50)
    rx, ry = int(s * 0.34), int(s * 0.23)
    # Arco superior (el mango del auricular): de 180 a 360 grados.
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 180, 360,
          fill=WHITE + (255,), width=int(s * 0.10))
    # Copas en los extremos del arco.
    for ex in (cx - rx, cx + rx):
        r = int(s * 0.125)
        d.ellipse([ex - r, cy - r, ex + r, cy + r], fill=WHITE + (255,))
        r2 = int(s * 0.06)
        d.ellipse([ex - r2, cy - r2, ex + r2, cy + r2], fill=DARK + (255,))
    return layer


def broken_handset(size):
    """Parte el auricular en dos mitades separadas con un hueco en medio."""
    s = size
    full = handset_layer(s)
    left = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    right = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    # Mitad izquierda: todo lo que queda a la izquierda del centro - hueco.
    gap = int(s * 0.045)
    lm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(lm).rectangle([0, 0, s // 2 - gap, s], fill=255)
    left.paste(full, (0, 0), lm)
    rm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(rm).rectangle([s // 2 + gap, 0, s, s], fill=255)
    right.paste(full, (0, 0), rm)
    # Separar y girar un poco cada mitad: izquierda sube, derecha baja.
    left = left.rotate(6, resample=Image.BICUBIC, center=(s // 2, s // 2))
    right = right.rotate(-7, resample=Image.BICUBIC, center=(s // 2, s // 2))
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.alpha_composite(left, (0, -int(s * 0.02)))
    out.alpha_composite(right, (int(s * 0.03), int(s * 0.045)))
    # Rayo amarillo en la rotura.
    d = ImageDraw.Draw(out)
    cx, cy = s // 2, int(s * 0.52)
    bolt = [(cx - int(s * 0.02), cy - int(s * 0.16)),
            (cx + int(s * 0.05), cy - int(s * 0.10)),
            (cx + int(s * 0.01), cy - int(s * 0.03)),
            (cx + int(s * 0.06), cy + int(s * 0.04)),
            (cx - int(s * 0.03), cy + int(s * 0.15)),
            (cx + int(s * 0.005), cy + int(s * 0.05)),
            (cx - int(s * 0.05), cy - int(s * 0.02))]
    d.polygon(bolt, fill=YELLOW + (255,), outline=DARK + (255,))
    return out


def centered_text(draw, y, text, font, fill, stroke=DARK, stroke_w=0):
    w = draw.textlength(text, font=font)
    x = (1024 - w) / 2
    draw.text((x, y), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=stroke)
    return w


def build(size=1024):
    img = gradient((size, size)).convert("RGBA")
    scale = size / 1024
    f_gartic = ImageFont.truetype(FONT, int(118 * scale))
    f_movil = ImageFont.truetype(FONT, int(185 * scale))
    d = ImageDraw.Draw(img)
    centered_text(d, int(72 * scale), "Gartic", f_gartic, WHITE,
                  stroke_w=int(6 * scale))
    handset = broken_handset(size)
    img.alpha_composite(handset)
    centered_text(d, int(790 * scale), "MÓVIL", f_movil, YELLOW,
                  stroke_w=int(10 * scale))
    return img.convert("RGB")


def circle_crop(img):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, img.size[0], img.size[1]], fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def main():
    icon = build(1024)
    icon.save(os.path.join(ROOT, "assets", "icon-1024.png"))
    sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    for base in (os.path.join(ROOT, "android", "app", "src", "main", "res"),
                 os.path.join(ROOT, "assets", "res")):
        for dpi, px in sizes.items():
            small = icon.resize((px, px), Image.LANCZOS)
            folder = os.path.join(base, "mipmap-" + dpi)
            small.save(os.path.join(folder, "ic_launcher.png"))
            circle_crop(small.convert("RGBA")).save(
                os.path.join(folder, "ic_launcher_round.png"))
            small.save(os.path.join(folder, "ic_launcher_foreground.png"))
    # Vistas en pequeno para revisar legibilidad.
    prev = os.path.join(ROOT, "VERIFICACION", "v2")
    os.makedirs(prev, exist_ok=True)
    icon.resize((48, 48), Image.LANCZOS).save(
        os.path.join(prev, "icono-48.png"))
    icon.resize((96, 96), Image.LANCZOS).save(
        os.path.join(prev, "icono-96.png"))
    icon.resize((192, 192), Image.LANCZOS).save(
        os.path.join(prev, "icono-192.png"))
    print("icono 1024 + mipmaps actualizados")


if __name__ == "__main__":
    main()
