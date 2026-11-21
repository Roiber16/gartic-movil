#!/usr/bin/env python3
"""Icono v2.1 de Gartic Móvil — corrección del recorte en el launcher.

Problema (Roi, Redmi 10, 21 nov 2026): el ícono v2 se veía bien a 1024 px
pero en el launcher de MIUI solo se veía el teléfono: "Gartic" y "MÓVIL"
quedaban fuera porque el diseño estaba pegado a los bordes y el launcher
muestra solo la zona segura central del ícono adaptativo (108 dp -> el
launcher enseña el cuadro central de 66 dp, es decir, el 61% del lienzo).

Corrección: TODO el contenido (textos y auricular) cabe dentro del cuadro
central de 626 px (de 199 a 823 en un lienzo de 1024), con márgenes de
~28-30% por cada lado. Además se comprueba que el nombre sobrevive a la
máscara circular (radio 295 px, test de estrés) y a la squircle de MIUI.

Diseño: igual que v2 — degradado violeta -> magenta, "Gartic" blanco
arriba, auricular clásico partido con rayo amarillo en el centro,
"MÓVIL" amarillo en grande abajo. Colores planos, sin aspecto IA.
Fuente DejaVu Sans Bold (del sistema).
Genera assets/icon-1024.png y todos los mipmap-* (launcher, round y
foreground) en android/... y assets/res/..., más las pruebas con máscara
en VERIFICACION/v2.1/.
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

# Zona segura: cuadro central 626x626 (x/y de 199 a 823). Todo el contenido
# va dentro, con margen extra. Círculo de estrés: centro (512,512), r=295.
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


def broken_handset(size):
    """Auricular partido, compacto, centrado en la zona segura.

    Centro (512, 505), arco rx=200/ry=120, copas r=72. Ocupa x 240-784,
    y ~360-580: bien dentro del cuadro seguro.
    """
    s = size
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = s // 2, 505
    rx, ry = 200, 120
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 180, 360,
          fill=WHITE + (255,), width=52)
    for ex in (cx - rx, cx + rx):
        r = 72
        d.ellipse([ex - r, cy - r, ex + r, cy + r], fill=WHITE + (255,))
        r2 = 38
        d.ellipse([ex - r2, cy - r2, ex + r2, cy + r2], fill=DARK + (255,))
    # Partir en dos mitades con hueco en el centro.
    left = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    right = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gap = 46
    lm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(lm).rectangle([0, 0, s // 2 - gap, s], fill=255)
    left.paste(layer, (0, 0), lm)
    rm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(rm).rectangle([s // 2 + gap, 0, s, s], fill=255)
    right.paste(layer, (0, 0), rm)
    left = left.rotate(5, resample=Image.BICUBIC, center=(s // 2, s // 2))
    right = right.rotate(-6, resample=Image.BICUBIC, center=(s // 2, s // 2))
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.alpha_composite(left, (0, -10))
    out.alpha_composite(right, (16, 24))
    # Rayo amarillo en la rotura.
    d = ImageDraw.Draw(out)
    cx, cy = s // 2, 510
    bolt = [(cx - 20, cy - 82), (cx + 48, cy - 52), (cx + 10, cy - 16),
            (cx + 58, cy + 20), (cx - 28, cy + 78), (cx + 4, cy + 26),
            (cx - 48, cy - 10)]
    d.polygon(bolt, fill=YELLOW + (255,), outline=DARK + (255,))
    return out


def centered_text(draw, y_top, text, font, fill, stroke_w=5):
    """Dibuja el texto centrado con su borde superior en y_top."""
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    w = bbox[2] - bbox[0]
    x = (1024 - w) / 2 - bbox[0]
    draw.text((x, y_top - bbox[1]), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=DARK)
    return (x + bbox[0], y_top, x + bbox[2], y_top + (bbox[3] - bbox[1]))


def build(size=1024):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    f_gartic = ImageFont.truetype(FONT, 84)
    f_movil = ImageFont.truetype(FONT, 110)
    # "Gartic": centro vertical ~330, ocupa y 288-372.
    centered_text(d, 288, "Gartic", f_gartic, WHITE, stroke_w=5)
    handset = broken_handset(size)
    img.alpha_composite(handset)
    # "MÓVIL": ocupa y ~635-720.
    centered_text(d, 635, "MÓVIL", f_movil, YELLOW, stroke_w=7)
    return img.convert("RGB")


def circle_crop(img):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, img.size[0], img.size[1]], fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def squircle_crop(img, radius):
    """Máscara squircle (rectángulo redondeado) estilo MIUI."""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius, fill=255)
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

    # --- Verificación con máscaras, en VERIFICACION/v2.1/ ---
    prev = os.path.join(ROOT, "VERIFICACION", "v2.1")
    os.makedirs(prev, exist_ok=True)
    icon.resize((192, 192), Image.LANCZOS).save(
        os.path.join(prev, "icono-192.png"))
    # Simulación MIUI: el launcher enseña solo el cuadro central de 626 px.
    crop = icon.crop((SAFE_LO, SAFE_LO, SAFE_HI, SAFE_HI))  # 624x624
    for px in (48, 96, 192):
        crop.resize((px, px), Image.LANCZOS).save(
            os.path.join(prev, f"sim-miui-{px}.png"))
        squircle_crop(crop, radius=int(624 * 0.28)).resize(
            (px, px), Image.LANCZOS).save(
            os.path.join(prev, f"sim-squircle-{px}.png"))
        circle_crop(icon.convert("RGBA")).resize(
            (px, px), Image.LANCZOS).save(
            os.path.join(prev, f"sim-circulo-{px}.png"))
    # Test de estrés: círculo de radio 295 (zona segura circular).
    stress = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    mask = Image.new("L", (1024, 1024), 0)
    ImageDraw.Draw(mask).ellipse(
        [512 - 295, 512 - 295, 512 + 295, 512 + 295], fill=255)
    stress.paste(icon.convert("RGBA"), (0, 0), mask)
    stress.resize((192, 192), Image.LANCZOS).save(
        os.path.join(prev, "sim-circulo-seguro-192.png"))
    print("icono v2.1 + mipmaps + verificación actualizados")


if __name__ == "__main__":
    main()
