#!/usr/bin/env python3
"""Variante D3 del ícono de Gartic Móvil — «Como el original».

Roi vio D1 y D2 y dijo: «No, quiero que sea más parecido al icono
original de gartic phone». Ni D1 ni D2 le convencen.

Modelo directo: VERIFICACION/v2.4/revision-final/pinterest/logo-oficial.jpg
— el logo oficial es un teléfono de disco visto de frente: auricular
curvado arriba (tubo grueso con dos orejeras redondas en los extremos,
contorno blanco grueso estilo pegatina, cuerpo violeta oscuro, rayo
blanco en el centro), «Gartic» en letras gruesas con contorno en el
medio, «PHONE» en grande abajo con el disco giratorio como la «O», y
la base del teléfono como barra oscura con contorno blanco. Todo sobre
degradado violeta-magenta.

D3 copia esa composición con nuestro nombre: «Gartic» arriba y
«MÓVIL» en grande abajo (el disco giratorio como la «Ó», con su
tilde). Correcciones respecto a la D2:
- La barra del auricular es MUCHO más gruesa (mitad 70 en vez de
  52-61): un tubo gordo, no un arco fino.
- Las orejeras son solo un poco más grandes que la barra (r 78 frente
  a mitad 70) y, sobre todo, el auricular se dibuja como UNA SOLA
  silueta (tubo + orejeras) con el contorno blanco sacado por
  dilatación de la máscara: en la D2 cada orejera tenía su propio
  anillo blanco y se leía como una bola suelta; aquí el contorno
  blanco es continuo alrededor de todo el auricular, como en el logo
  oficial, y las orejeras se leen como los extremos redondos del tubo.
- El arco es más cerrado (195°-345°, 150° de apertura en vez de
  220°-320°): baja más en los extremos, como un auricular ∩ de verdad.
- Rayo blanco en el centro del auricular, como en el original.
- La base es una barra ancha con contorno blanco y esquinas
  redondeadas (en la D2 era una barra oscura estrecha que se leía como
  una barra cualquiera).

Todo dentro de la zona segura central (199-823 de 1024 px), en Baloo 2
ExtraBold con contorno oscuro grueso, sobre el degradado
violeta-magenta de la app. Formas planas y simples, sin aspecto IA.
ACLARACIÓN DE ROI: el ícono va CENTRADO y SIN las cosas de los lados
— solo el logo del teléfono centrado (auricular, «Gartic», base con
disco como «Ó» de «MÓVIL»), sin lápiz, libreta, auricular suelto ni
bocadillo que decoran los lados del logo oficial. Nada de decoración
lateral.
La C1 sigue siendo el ícono instalado; la D3 es SOLO una alternativa
para que Roi compare y elija. No se instala nada.
"""
import importlib.util
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos")
SCRIPTS = os.path.join(ROOT, "scripts")

_spec = importlib.util.spec_from_file_location(
    "icon_c", os.path.join(SCRIPTS, "make-icon-C-revisada.py"))
_icon_c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_icon_c)

_spec_d = importlib.util.spec_from_file_location(
    "icon_d", os.path.join(SCRIPTS, "make-icon-D.py"))
_icon_d = importlib.util.module_from_spec(_spec_d)
_spec_d.loader.exec_module(_icon_d)

FONT = _icon_c.FONT
DARK = _icon_c.DARK
WHITE = _icon_c.WHITE
YELLOW = _icon_c.YELLOW
SAFE_LO, SAFE_HI = _icon_c.SAFE_LO, _icon_c.SAFE_HI
gradient = _icon_c.gradient
centered_text = _icon_c.centered_text
sim_miui = _icon_c.sim_miui
rotary_dial = _icon_d.rotary_dial
handset_polygon = _icon_d.handset_polygon
star4 = _icon_d.star4


def bolt(draw, cx, cy, w=26, h=54):
    """Rayo blanco como el del auricular del logo oficial."""
    pts = [(cx + w // 2, cy - h // 2),
           (cx - w // 2 + 4, cy + 2),
           (cx + 2, cy + 2),
           (cx - w // 2, cy + h // 2),
           (cx + w // 2 - 4, cy - 2),
           (cx - 2, cy - 2)]
    draw.polygon(pts, fill=WHITE + (255,))


def handset_layer(size):
    """Auricular como UNA SOLA silueta: tubo grueso (crescente) +
    orejeras redondas en los extremos. Sin contorno aquí: el contorno
    blanco continuo se saca por dilatación de la máscara."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy, r, half = 512, 520, 225, 70
    d.polygon(handset_polygon(cx, cy, r, half, 195, 345),
              fill=DARK + (255,))
    for ex, ey in ((295, 462), (729, 462)):
        d.ellipse([ex - 78, ey - 78, ex + 78, ey + 78],
                  fill=DARK + (255,))
    return layer


def sticker_outline(shape, px=10):
    """Contorno blanco continuo estilo pegatina alrededor de una
    silueta: dilata su máscara alfa `px` píxeles."""
    mask = shape.split()[3].filter(ImageFilter.MaxFilter(2 * px + 1))
    out = Image.new("RGBA", shape.size, WHITE + (255,))
    out.putalpha(mask)
    return out


def build_d3(size=1024):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, 84)
    fm = ImageFont.truetype(FONT, 132)

    # Sin decoración lateral (aclaración de Roi): solo el teléfono
    # centrado, sin lápiz, libreta, auricular suelto ni bocadillo.

    # --- auricular: una sola silueta con contorno blanco continuo ---
    shape = handset_layer(size)
    img.alpha_composite(sticker_outline(shape, 10))
    img.alpha_composite(shape)
    # rayo blanco en el centro del auricular
    bolt(d, 512, 295)

    # --- «Gartic» entre el auricular y «MÓVIL» ---
    centered_text(d, 548, "Gartic", fg, WHITE, stroke_w=7)

    # --- «MÓVIL» en grande, con el disco giratorio como la Ó ---
    y_top = 648
    b_m = d.textbbox((0, 0), "M", font=fm, stroke_width=9)
    b_vil = d.textbbox((0, 0), "VIL", font=fm, stroke_width=9)
    w_m = b_m[2] - b_m[0]
    w_vil = b_vil[2] - b_vil[0]
    dial_r = 59
    gap = 16
    total = w_m + gap + 2 * dial_r + gap + w_vil
    x = (1024 - total) / 2
    d.text((x - b_m[0], y_top - b_m[1]), "M", font=fm, fill=WHITE,
           stroke_width=9, stroke_fill=DARK)
    dial_cx = x + w_m + gap + dial_r
    cap_h = b_m[3] - b_m[1]
    dial_cy = y_top + cap_h // 2
    rotary_dial(d, int(dial_cx), dial_cy, dial_r)
    # tilde amarilla sobre el disco
    d.ellipse([dial_cx - 10, y_top - 26, dial_cx + 10, y_top - 6],
              fill=YELLOW + (255,), outline=DARK + (255,), width=3)
    x_vil = x + w_m + gap + 2 * dial_r + gap
    d.text((x_vil - b_vil[0], y_top - b_vil[1]), "VIL", font=fm,
           fill=WHITE, stroke_width=9, stroke_fill=DARK)

    # --- base del teléfono de disco: barra ancha con contorno blanco,
    # tan ancha como «MÓVIL», como en el logo oficial ---
    d.rounded_rectangle([280, 772, 744, 820], radius=16,
                        fill=DARK + (255,), outline=WHITE + (255,),
                        width=8)
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    icon = build_d3()
    icon.save(os.path.join(OUT, "icono-D3.png"))
    sim_miui(icon, 96).save(os.path.join(OUT, "icono-D3-miui-96.png"))
    sim_miui(icon, 192).save(os.path.join(OUT, "icono-D3-miui-192.png"))
    print("variante D3 lista")

    # comparativa a 96 y 48 px: logo oficial / D3 / C1
    official = Image.open(os.path.join(
        ROOT, "VERIFICACION", "v2.4", "revision-final", "pinterest",
        "logo-oficial.jpg")).convert("RGB")
    c1 = Image.open(os.path.join(OUT, "icono-C1.png"))
    comp = Image.new("RGB", (360, 240), (255, 255, 255))
    cd = ImageDraw.Draw(comp)
    lab = ImageFont.truetype(FONT, 26)
    lab_s = ImageFont.truetype(FONT, 20)
    off96 = official.resize((96, 70), Image.LANCZOS)
    off48 = official.resize((48, 35), Image.LANCZOS)
    for i, (name, big, small) in enumerate((
            ("ORIGINAL", off96, off48),
            ("D3", sim_miui(icon, 96), sim_miui(icon, 48)),
            ("C1", sim_miui(c1, 96), sim_miui(c1, 48)))):
        x = 12 + i * 118
        comp.paste(big, (x, 12 if name != "ORIGINAL" else 26))
        cd.text((x + 8, 116), name, font=lab, fill=(0, 0, 0))
        comp.paste(small, (x + 24, 152 if name != "ORIGINAL" else 168))
        cd.text((x + 28, 206), "48 px", font=lab_s, fill=(90, 90, 90))
    comp.save(os.path.join(OUT, "comparativa-96-D3-original.png"))
    print("comparativa en", OUT)


if __name__ == "__main__":
    main()
