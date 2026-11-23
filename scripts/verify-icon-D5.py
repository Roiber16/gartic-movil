#!/usr/bin/env python3
"""Verifica que todos los mipmap de Gartic Móvil vengan de la D5 y no de la C1."""
import os
from PIL import Image, ImageDraw, ImageChops

ROOT = os.path.expanduser("~/workspace/gartic-movil")
D5 = Image.open(os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos",
                              "icono-D5.png")).convert("RGB")
C1 = Image.open(os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos",
                              "icono-C1.png")).convert("RGB")
assert D5.size == (1024, 1024) and C1.size == (1024, 1024)


def circle_crop(img):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, img.size[0], img.size[1]], fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def meandiff(a, b):
    a = a.convert("RGB")
    b = b.convert("RGB")
    diff = ImageChops.difference(a, b)
    px = list(diff.getdata())
    return sum(sum(p) for p in px) / (len(px) * 3)


SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
BASES = [os.path.join(ROOT, "android", "app", "src", "main", "res"),
         os.path.join(ROOT, "assets", "res")]
bad = []
for base in BASES:
    for dpi, px in SIZES.items():
        d5_small = D5.resize((px, px), Image.LANCZOS)
        c1_small = C1.resize((px, px), Image.LANCZOS)
        for name, expected in (
                ("ic_launcher.png", d5_small),
                ("ic_launcher_foreground.png", d5_small),
                ("ic_launcher_round.png",
                 circle_crop(d5_small.convert("RGBA")))):
            path = os.path.join(base, "mipmap-" + dpi, name)
            rel = os.path.relpath(path, ROOT)
            if not os.path.exists(path):
                print("FALTA", rel)
                bad.append(rel)
                continue
            got = Image.open(path)
            d_d5 = meandiff(got, expected)
            d_c1 = meandiff(got, c1_small if "round" not in name
                            else circle_crop(c1_small.convert("RGBA")))
            status = "OK  " if d_d5 < 0.5 else "MAL "
            print(f"{status} {rel} ({got.size[0]}px) "
                  f"dif-vs-D5={d_d5:.2f} dif-vs-C1={d_c1:.2f}")
            if d_d5 >= 0.5:
                bad.append(rel)
print()
print("FALLOS:", len(bad), bad if bad else "(ninguno)")
