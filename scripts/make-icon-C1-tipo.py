#!/usr/bin/env python3
"""C1 con tipografía nueva — prueba de fuentes legibles a tamaño ícono.

Roi eligió la C1 (lápiz sobre el móvil) pero pide cambiar la tipografía:
debe leerse clara a 96 px y más pequeño. La actual es DejaVu Sans Bold.

Opciones probadas (mismo dibujo, mismos tamaños base, solo cambia la
fuente y el contorno):
- A "Actual": DejaVu Sans Bold (la de la C1 instalada) — referencia.
- B "Baloo 2 ExtraBold": la fuente de la propia app (OFL, empaquetada en
  www/fonts/baloo2-latin.woff2), instanciada a peso 800. Redondeada y
  gruesa, coherente con el juego.
- C "Noto Sans Black": sans limpia y muy gruesa, altura-x grande,
  diseñada para leerse a tamaños pequeños.

Para cada opción: PNG a 1024 px + simulación MIUI a 96 y 48 px, y una
comparativa con las tres a 96 y a 48 px.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "c_rev", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "make-icon-C-revisada.py"))
c_rev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c_rev)

ROOT = c_rev.ROOT
OUT = c_rev.OUT
DARK = c_rev.DARK
WHITE = c_rev.WHITE
YELLOW = c_rev.YELLOW
SAFE_LO, SAFE_HI = c_rev.SAFE_LO, c_rev.SAFE_HI

BALOO_TTF = "/tmp/baloo2-extrabold.ttf"
NOTO_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def make_baloo_extrabold():
    """Instancia Baloo 2 a peso 800 y la guarda como TTF estático."""
    if not os.path.exists(BALOO_TTF):
        font = TTFont(os.path.join(ROOT, "www", "fonts",
                                   "baloo2-latin.woff2"))
        instantiateVariableFont(font, {"wght": 800}, inplace=True)
        font.flavor = None
        font.save(BALOO_TTF)
    return BALOO_TTF


def centered_text(draw, y_top, text, font, fill, stroke_w):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    w = bbox[2] - bbox[0]
    x = (1024 - w) / 2 - bbox[0]
    draw.text((x, y_top - bbox[1]), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=DARK)
    return w


def build_with_font(font_path, size_gartic=76, size_movil=104,
                    stroke_g=5, stroke_m=7):
    """C1 exacta, solo cambia la fuente de los dos textos."""
    img = c_rev.gradient((1024, 1024)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(font_path, size_gartic)
    fm = ImageFont.truetype(font_path, size_movil)
    wg = centered_text(d, 235, "Gartic", fg, WHITE, stroke_w=stroke_g)
    img.alpha_composite(c_rev.modern_phone(1024, 427, 320, 597, 660))
    img.alpha_composite(
        c_rev.pencil_layer(1024, 520, 480, length=300, thick=52,
                           angle=24))
    wm = centered_text(d, 672, "MÓVIL", fm, YELLOW, stroke_w=stroke_m)
    return img.convert("RGB"), wg, wm


def sim(img, px):
    crop = img.crop((SAFE_LO, SAFE_LO, SAFE_HI, SAFE_HI))
    return crop.resize((px, px), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    baloo = make_baloo_extrabold()
    options = [
        ("actual", "DejaVu Bold (actual)", DEJAVU_BOLD, 76, 104, 5, 7),
        ("baloo", "Baloo 2 ExtraBold", baloo, 76, 104, 6, 8),
        ("noto", "Noto Sans Black", NOTO_BLACK, 76, 104, 5, 7),
    ]
    # Zona segura: 199-823 = 624 px de ancho. Medir antes.
    for key, label, path, sg, sm, stg, stm in options:
        img, wg, wm = build_with_font(path, sg, sm, stg, stm)
        print(f"{key}: ancho 'Gartic'={wg}px 'MÓVIL'={wm}px "
              f"(zona segura 624px)")
    for key, label, path, sg, sm, stg, stm in options:
        img, _, _ = build_with_font(path, sg, sm, stg, stm)
        img.save(os.path.join(OUT, f"icono-C1-tipo-{key}.png"))
        sim(img, 96).save(
            os.path.join(OUT, f"icono-C1-tipo-{key}-miui-96.png"))
        sim(img, 48).save(
            os.path.join(OUT, f"icono-C1-tipo-{key}-miui-48.png"))
        print("variante", key, "lista:", label)

    # Comparativa: las tres a 96 y a 48 px, con etiquetas.
    lab = ImageFont.truetype(DEJAVU_BOLD, 26)
    comp = Image.new("RGB", (96 * 3 + 40, 250), (255, 255, 255))
    cd = ImageDraw.Draw(comp)
    for i, (key, label, *_rest) in enumerate(options):
        icon = Image.open(os.path.join(OUT, f"icono-C1-tipo-{key}.png"))
        comp.paste(sim(icon, 96), (10 + i * 106, 10))
        comp.paste(sim(icon, 48), (10 + i * 106 + 24, 120))
        cd.text((10 + i * 106, 176), key.upper(), font=lab,
                fill=(0, 0, 0))
        cd.text((10 + i * 106, 210), "96px / 48px", font=lab,
                fill=(90, 90, 90))
    comp.save(os.path.join(OUT, "comparativa-96-C1-tipo.png"))
    print("comparativa en", OUT)


if __name__ == "__main__":
    main()
