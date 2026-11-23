#!/usr/bin/env python3
"""Instala la D5 como ícono final de Gartic Móvil v2.4.

Roi confirmó el 23 nov 2026 01:50: «El nuevo ícono» — la D5 sustituye
a la C1. Procedimiento idéntico al install() de
scripts/make-icon-C-revisada.py (el que instaló la C1): assets/icon-1024.png
y todos los mipmap-* (launcher, round y foreground) en android/... y
assets/res/..., tamaños mdpi 48, hdpi 72, xhdpi 96, xxhdpi 144,
xxxhdpi 192, redimensionado LANCZOS, round con recorte circular.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.expanduser("~/workspace/gartic-movil")
SRC = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos",
                   "icono-D5.png")


def circle_crop(img):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, img.size[0], img.size[1]], fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def main():
    icon = Image.open(SRC).convert("RGB")
    assert icon.size == (1024, 1024), icon.size
    icon.save(os.path.join(ROOT, "assets", "icon-1024.png"))
    sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144,
             "xxxhdpi": 192}
    for base in (os.path.join(ROOT, "android", "app", "src", "main", "res"),
                 os.path.join(ROOT, "assets", "res")):
        for dpi, px in sizes.items():
            small = icon.resize((px, px), Image.LANCZOS)
            folder = os.path.join(base, "mipmap-" + dpi)
            os.makedirs(folder, exist_ok=True)
            small.save(os.path.join(folder, "ic_launcher.png"))
            circle_crop(small.convert("RGBA")).save(
                os.path.join(folder, "ic_launcher_round.png"))
            small.save(os.path.join(folder, "ic_launcher_foreground.png"))
    print("D5 instalada en assets/icon-1024.png y mipmaps")


if __name__ == "__main__":
    main()
