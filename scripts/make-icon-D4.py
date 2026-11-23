#!/usr/bin/env python3
"""Variante D4 del ícono de Gartic Móvil — «Teléfono antiguo completo».

Roi vio la D3 en su teléfono y dijo: «Pero en qué momento se parece a
la original?» — y tiene razón. La D3 NO se parece lo suficiente.

Lo que falla en la D3: el auricular quedó como un arco grande y alto,
tipo arcoíris, que ocupa media imagen y flota arriba; las letras
flotan sobre el fondo; la base es solo una barrita fina. Se lee como
«arco + texto», no como un teléfono.

Cómo es el original de verdad (zoom en /tmp/logo-telefono-zoom.png):
el teléfono es UNA SOLA PIEZA — arriba el auricular apoyado, en el
centro el cuerpo con el disco, y las palabras integradas con el
teléfono. El auricular es una pieza HORIZONTAL y compacta: una curva
suave y ancha con las dos orejeras en los extremos, apoyada
DIRECTAMENTE sobre el cuerpo (no flotando alto). El cuerpo es la forma
principal: un trapezoide ancho y grande que ocupa la mitad inferior,
violeta oscuro con contorno blanco grueso estilo pegatina, y la palabra
grande va ENCIMA del cuerpo, en letras blancas gruesas con contorno,
con el disco giratorio como la «O». «Gartic» va más pequeño encima del
cuerpo, entre el auricular y la palabra grande. Abajo, una barra de
base. Todo dentro de un contorno blanco continuo estilo pegatina.

D4 copia ESA composición con nuestro nombre:
1. Auricular horizontal y compacto (barra casi plana con los
   extremos redondeados + orejeras como bloques en los extremos),
   apoyado sobre el cuerpo: las orejeras se solapan con las esquinas
   superiores del cuerpo, así auricular y cuerpo son UN SOLO teléfono.
2. Cuerpo ancho y grande (trapezoide redondeado) ocupando la mitad
   inferior, con «MÓVIL» en grande ENCIMA del cuerpo y el disco
   giratorio como la «Ó» (con su tilde amarilla).
3. «Gartic» más pequeño entre el auricular y «MÓVIL», encajado en el
   hueco del auricular y rozando el borde superior del cuerpo.
4. Barra de base abajo, separada del cuerpo por una banda blanca
   (como en el original).
Todo centrado, sin nada a los lados (sin lápiz, libreta, bocadillo ni
estrellas), dentro de la zona segura central (199-823 de 1024 px),
sobre el degradado violeta-magenta de la app, letras Baloo 2
ExtraBold con contorno oscuro grueso.

La silueta completa (auricular + orejeras + cuerpo + base) se dibuja
como UNA SOLA capa oscura y el contorno blanco estilo pegatina sale
por dilatación de su máscara: así el teléfono se lee como un único
objeto, no como piezas sueltas.

La C1 sigue siendo el ícono instalado; la D4 es SOLO una alternativa
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

_spec_d3 = importlib.util.spec_from_file_location(
    "icon_d3", os.path.join(SCRIPTS, "make-icon-D3.py"))
_icon_d3 = importlib.util.module_from_spec(_spec_d3)
_spec_d3.loader.exec_module(_icon_d3)

FONT = _icon_c.FONT
DARK = _icon_c.DARK
WHITE = _icon_c.WHITE
YELLOW = _icon_c.YELLOW
gradient = _icon_c.gradient
centered_text = _icon_c.centered_text
sim_miui = _icon_c.sim_miui
rotary_dial = _icon_d.rotary_dial
handset_polygon = _icon_d.handset_polygon
bolt = _icon_d3.bolt
sticker_outline = _icon_d3.sticker_outline


def phone_silhouette(size=1024):
    """El teléfono antiguo completo como UNA SOLA silueta oscura:
    auricular horizontal + orejeras + cuerpo trapezoide + base.
    El auricular se apoya sobre el cuerpo (las orejeras se solapan
    con las esquinas superiores del cuerpo), así todo es un único
    teléfono reconocible."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # --- auricular: BARRA HORIZONTAL casi plana (no un arco): en el
    # original el auricular es una pieza ancha y baja, con el borde
    # superior apenas curvado y el inferior casi recto. Rectángulo
    # redondeado de 484x100 + orejeras como bloques redondos en los
    # extremos, que bajan hasta apoyar en el cuerpo. ---
    d.rounded_rectangle([270, 265, 754, 365], radius=42,
                        fill=DARK + (255,))
    # orejeras en los extremos del auricular, fundidas con él y
    # apoyadas en las esquinas superiores del cuerpo
    for ex, ey in ((318, 378), (706, 378)):
        d.ellipse([ex - 60, ey - 60, ex + 60, ey + 60],
                  fill=DARK + (255,))
    # --- cuerpo: trapezoide ancho, más ancho arriba que abajo.
    # Borde superior a y=420 (las orejeras, que bajan hasta 438, se
    # solapan con las esquinas superiores: auricular y cuerpo son
    # una sola pieza). Las esquinas las redondea la dilatación del
    # contorno blanco. ---
    body = [(255, 420), (769, 420), (734, 715), (290, 715)]
    d.polygon(body, fill=DARK + (255,))
    # --- base: barra ancha debajo del cuerpo, separada por 13 px
    # (el contorno blanco de ambos se funde en una banda blanca,
    # como en el original). ---
    d.rounded_rectangle([300, 728, 724, 770], radius=14,
                        fill=DARK + (255,))
    return layer


def dial_small(draw, cx, cy, r):
    """Disco giratorio con los agujeros y el centro escalados al
    tamaño del disco (en el original el disco mide lo mismo que la
    altura de las letras, no más)."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=WHITE + (255,), outline=DARK + (255,), width=5)
    hole_r = max(6, int(r * 0.16))
    for k in range(9):
        a = math.radians(-90 + k * 40)
        hx = cx + int(0.58 * r * math.cos(a))
        hy = cy + int(0.58 * r * math.sin(a))
        draw.ellipse([hx - hole_r, hy - hole_r, hx + hole_r,
                      hy + hole_r], fill=DARK + (255,))
    cr = max(10, int(r * 0.25))
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                 fill=DARK + (255,))


def movil_width(draw, font, dial_r, gap=12):
    b_m = draw.textbbox((0, 0), "M", font=font, stroke_width=9)
    b_vil = draw.textbbox((0, 0), "VIL", font=font, stroke_width=9)
    return ((b_m[2] - b_m[0]) + gap + 2 * dial_r + gap
            + (b_vil[2] - b_vil[0]))


def build_d4(size=1024):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)

    # --- el teléfono entero como una sola silueta + contorno blanco
    # estilo pegatina por dilatación ---
    shape = phone_silhouette(size)
    img.alpha_composite(sticker_outline(shape, 12))
    img.alpha_composite(shape)

    # --- rayo blanco en el centro del auricular (barra entre y=265
    # y y=365 en el centro) ---
    bolt(d, 512, 315, w=26, h=48)

    # --- «Gartic» encajado entre el auricular y el cuerpo: justo
    # debajo del borde inferior de la barra (y=365), rozando el
    # borde superior del cuerpo (y=420). ---
    fg = ImageFont.truetype(FONT, 78)
    centered_text(d, 372, "Gartic", fg, WHITE, stroke_w=7)

    # --- «MÓVIL» en grande ENCIMA del cuerpo, con el disco como
    # la Ó. Se ajusta el tamaño para que quepa en el cuerpo
    # (ancho útil 470 px): teléfono y letras lo más grandes posible.
    # El disco mide lo mismo que la altura de las letras, como en
    # el original (no más grande que ellas). ---
    font = None
    dial_r = None
    for size_try in range(160, 99, -5):
        f_try = ImageFont.truetype(FONT, size_try)
        r_try = int(size_try * 0.37)
        if movil_width(d, f_try, r_try) <= 470:
            font, dial_r = f_try, r_try
            break
    b_m = d.textbbox((0, 0), "M", font=font, stroke_width=9)
    b_vil = d.textbbox((0, 0), "VIL", font=font, stroke_width=9)
    w_m = b_m[2] - b_m[0]
    w_vil = b_vil[2] - b_vil[0]
    gap = 12
    total = w_m + gap + 2 * dial_r + gap + w_vil
    x = (1024 - total) / 2
    # centrado vertical en el cuerpo (420-715, centro 567)
    cap_h = b_m[3] - b_m[1]
    y_top = 567 - cap_h // 2
    d.text((x - b_m[0], y_top - b_m[1]), "M", font=font, fill=WHITE,
           stroke_width=9, stroke_fill=DARK)
    dial_cx = x + w_m + gap + dial_r
    dial_cy = y_top + cap_h // 2
    dial_small(d, int(dial_cx), dial_cy, dial_r)
    # tilde amarilla sobre el disco
    d.ellipse([dial_cx - 10, y_top - 26, dial_cx + 10, y_top - 6],
              fill=YELLOW + (255,), outline=DARK + (255,), width=3)
    x_vil = x + w_m + gap + 2 * dial_r + gap
    d.text((x_vil - b_vil[0], y_top - b_vil[1]), "VIL", font=font,
           fill=WHITE, stroke_width=9, stroke_fill=DARK)
    print("MÓVIL: fuente", font.size, "ancho total", round(total),
          "dial r", dial_r)
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    icon = build_d4()
    icon.save(os.path.join(OUT, "icono-D4.png"))
    sim_miui(icon, 96).save(os.path.join(OUT, "icono-D4-miui-96.png"))
    sim_miui(icon, 192).save(os.path.join(OUT, "icono-D4-miui-192.png"))
    print("variante D4 lista")

    # comparativa a 96 y 48 px: logo oficial / D4 / C1
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
            ("D4", sim_miui(icon, 96), sim_miui(icon, 48)),
            ("C1", sim_miui(c1, 96), sim_miui(c1, 48)))):
        x = 12 + i * 118
        comp.paste(big, (x, 12 if name != "ORIGINAL" else 26))
        cd.text((x + 8, 116), name, font=lab, fill=(0, 0, 0))
        comp.paste(small, (x + 24, 152 if name != "ORIGINAL" else 168))
        cd.text((x + 28, 206), "48 px", font=lab_s, fill=(90, 90, 90))
    comp.save(os.path.join(OUT, "comparativa-96-D4-original.png"))
    print("comparativa en", OUT)


if __name__ == "__main__":
    main()
