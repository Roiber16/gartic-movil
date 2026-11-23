#!/usr/bin/env python3
"""Ícono A revisado de Gartic Móvil — teléfono roto, pero con un MÓVIL
de verdad.

Roi: la A "no es un teléfono en ningún lugar del mundo, parece unas
gafas o un bigote". El auricular abstracto NO vale. Aquí el teléfono es
un MÓVIL MODERNO reconocible a la primera: rectángulo vertical, pantalla,
altavoz arriba, barra de inicio abajo. Dos composiciones:

- A1 "Partido en dos": el móvil partido verticalmente en dos mitades,
  separadas e inclinadas, con el rayo amarillo en la rotura. Es la idea
  del teléfono roto de siempre, pero con un móvil de verdad.
- A2 "Pantalla agrietada": un solo móvil, entero, con la grieta grande
  en la pantalla y la estrellita amarilla. Simple y directo.

En las dos: "Gartic" blanco arriba, "MÓVIL" amarillo en grande abajo,
degradado violeta a magenta, todo dentro de la zona segura central
(199-823 de 1024 px). Formas planas y simples, sin aspecto IA.
Fuente DejaVu Sans Bold (del sistema).

Reutiliza modern_phone/gradient/centered_text/sim_miui/install de
make-icon-C-revisada.py. La mejor de las dos se compara con la mejor C
(comparativa-96-AC.png) y se instala la ganadora.
"""
import os
import importlib.util
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "make_icon_C_revisada", os.path.join(_HERE, "make-icon-C-revisada.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
gradient = _mod.gradient
centered_text = _mod.centered_text
modern_phone = _mod.modern_phone
sim_miui = _mod.sim_miui
install = _mod.install
DARK = _mod.DARK
WHITE = _mod.WHITE
YELLOW = _mod.YELLOW
FONT = _mod.FONT
SAFE_LO = _mod.SAFE_LO
SAFE_HI = _mod.SAFE_HI

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos")


def split_phone(size, gap=30):
    """Móvil moderno partido POR LA MITAD en horizontal: la mitad de
    arriba y la de abajo separadas, con el rayo amarillo en la rotura.
    Cada mitad conserva el ancho del móvil, así las dos se leen como
    partes de un teléfono (el corte vertical lo dejaba como dos palitos).
    """
    s = size
    layer = modern_phone(s, 427, 320, 597, 660, crack=False)
    cy = 490
    top = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bottom = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    tm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(tm).rectangle([0, 0, s, cy - gap], fill=255)
    top.paste(layer, (0, 0), tm)
    bm = Image.new("L", (s, s), 0)
    ImageDraw.Draw(bm).rectangle([0, cy + gap, s, s], fill=255)
    bottom.paste(layer, (0, 0), bm)
    top = top.rotate(-4, resample=Image.BICUBIC, center=(s // 2, s // 2))
    bottom = bottom.rotate(5, resample=Image.BICUBIC,
                           center=(s // 2, s // 2))
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.alpha_composite(top, (0, -8))
    out.alpha_composite(bottom, (12, 16))
    # rayo amarillo en la rotura (más pequeño, cabe en el hueco)
    d = ImageDraw.Draw(out)
    bx, by = s // 2, cy
    bs = 0.75
    bolt = [(bx - 20 * bs, by - 82 * bs), (bx + 48 * bs, by - 52 * bs),
            (bx + 10 * bs, by - 16 * bs), (bx + 58 * bs, by + 20 * bs),
            (bx - 28 * bs, by + 78 * bs), (bx + 4 * bs, by + 26 * bs),
            (bx - 48 * bs, by - 10 * bs)]
    d.polygon(bolt, fill=YELLOW + (255,), outline=DARK + (255,))
    return out


def build(size=1024, variant="A1"):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, 76)
    fm = ImageFont.truetype(FONT, 104)
    centered_text(d, 235, "Gartic", fg, WHITE, stroke_w=5)
    if variant == "A1":
        img.alpha_composite(split_phone(size))
    else:  # A2: móvil entero con la grieta grande
        img.alpha_composite(
            modern_phone(size, 427, 320, 597, 660, crack=True, crack_w=13))
    centered_text(d, 672, "MÓVIL", fm, YELLOW, stroke_w=7)
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in ("A1", "A2"):
        icon = build(1024, name)
        icon.save(os.path.join(OUT, f"icono-{name}.png"))
        sim_miui(icon, 96).save(
            os.path.join(OUT, f"icono-{name}-miui-96.png"))
        sim_miui(icon, 192).save(
            os.path.join(OUT, f"icono-{name}-miui-192.png"))
        print("variante", name, "lista")
    comp = Image.new("RGB", (96 * 2 + 30, 140), (255, 255, 255))
    cd = ImageDraw.Draw(comp)
    lab = ImageFont.truetype(FONT, 28)
    for i, name in enumerate(("A1", "A2")):
        sim = sim_miui(build(1024, name), 96)
        comp.paste(sim, (10 + i * 106, 10))
        cd.text((10 + i * 106 + 26, 112), name, font=lab, fill=(0, 0, 0))
    comp.save(os.path.join(OUT, "comparativa-96-A.png"))
    print("comparativa A en", OUT)


if __name__ == "__main__":
    main()
