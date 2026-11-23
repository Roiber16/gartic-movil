#!/usr/bin/env python3
"""Variante D del ícono de Gartic Móvil — «Logo oficial».

Roi pidió una variante con las vibras del logo oficial de Gartic Phone
(VERIFICACION/v2.4/revision-final/pinterest/logo-oficial.jpg): el
teléfono y la tipografía gruesa con contorno. La C1 sigue siendo el
ícono instalado y aprobado; esta variante es SOLO una alternativa para
comparar, no se instala.

Dos intentos:
- D1 «Móvil logo»: móvil moderno grande, cuerpo violeta oscuro con
  contorno blanco estilo pegatina (como el teléfono del logo oficial),
  pantalla lavanda con grieta, lápiz pequeño como garabato en la
  esquina, «Gartic» blanco arriba y «MÓVIL» blanco en grande abajo,
  en Baloo 2 ExtraBold con contorno oscuro grueso.
- D2 «Teléfono clásico»: el teléfono de disco del logo oficial —
  auricular curvado arriba, «Gartic» debajo, «MÓVIL» en grande con el
  disco giratorio como la «Ó» (con su tilde amarilla encima) y la base
  del teléfono abajo. Todo en Baloo 2 ExtraBold con contorno oscuro.

En las dos: degradado violeta a magenta de la app, todo dentro de la
zona segura central (199-823 de 1024 px). Formas planas y simples,
sin aspecto IA. Reutiliza las funciones de scripts/make-icon-C-revisada.py.
"""
import importlib.util
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos")
SCRIPTS = os.path.join(ROOT, "scripts")

_spec = importlib.util.spec_from_file_location(
    "icon_c", os.path.join(SCRIPTS, "make-icon-C-revisada.py"))
_icon_c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_icon_c)

FONT = _icon_c.FONT
DARK = _icon_c.DARK
WHITE = _icon_c.WHITE
YELLOW = _icon_c.YELLOW
LAVENDER = _icon_c.LAVENDER
SAFE_LO, SAFE_HI = _icon_c.SAFE_LO, _icon_c.SAFE_HI
gradient = _icon_c.gradient
centered_text = _icon_c.centered_text
pencil_layer = _icon_c.pencil_layer
sim_miui = _icon_c.sim_miui


def dark_phone(size, x0, y0, x1, y1, crack_w=9):
    """Móvil moderno con cuerpo violeta oscuro y contorno blanco estilo
    pegatina (como el teléfono del logo oficial), pantalla lavanda con
    grieta, altavoz y barra de inicio en blanco."""
    s = size
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([x0, y0, x1, y1], radius=30,
                        fill=DARK + (255,), outline=WHITE + (255,),
                        width=10)
    sx0, sy0, sx1, sy1 = x0 + 16, y0 + 36, x1 - 16, y1 - 30
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=10,
                        fill=LAVENDER + (255,))
    d.rounded_rectangle([(x0 + x1) // 2 - 22, y0 + 13,
                         (x0 + x1) // 2 + 22, y0 + 21], radius=4,
                        fill=WHITE + (255,))
    d.rounded_rectangle([(x0 + x1) // 2 - 26, y1 - 20,
                         (x0 + x1) // 2 + 26, y1 - 12], radius=4,
                        fill=WHITE + (255,))
    cx = (sx0 + sx1) // 2
    crack = [(sx0 + 18, sy0 + 12), (cx + 6, sy0 + 70),
             (cx - 22, sy0 + 130), (cx + 14, sy0 + 190),
             (cx - 8, sy1 - 14)]
    d.line(crack, fill=DARK + (255,), width=crack_w, joint="curve")
    d.line([(cx - 22, sy0 + 130), (sx0 + 30, sy0 + 168)],
           fill=DARK + (255,), width=7)
    ex, ey = crack[-1]
    for dx, dy in ((0, -18), (0, 18), (-18, 0), (18, 0)):
        d.line([ex, ey, ex + dx, ey + dy], fill=YELLOW + (255,), width=7)
    return out


def star4(draw, cx, cy, r, color):
    for dx, dy in ((0, -r), (0, r), (-r, 0), (r, 0)):
        draw.line([cx, cy, cx + dx, cy + dy], fill=color + (255,),
                  width=max(4, r // 3))


def build_d1(size=1024):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, 88)
    fm = ImageFont.truetype(FONT, 120)
    # garabato estrella arriba a la izquierda, como los del logo oficial
    star4(d, 300, 290, 16, YELLOW)
    centered_text(d, 235, "Gartic", fg, WHITE, stroke_w=7)
    # móvil oscuro grande con contorno blanco
    img.alpha_composite(dark_phone(size, 400, 315, 624, 655))
    # lápiz pequeño como garabato en la esquina del móvil
    img.alpha_composite(
        pencil_layer(size, 668, 565, length=220, thick=44, angle=24))
    centered_text(d, 672, "MÓVIL", fm, WHITE, stroke_w=9)
    return img.convert("RGB")


def rotary_dial(draw, cx, cy, r):
    """Disco giratorio de teléfono clásico: círculo blanco con
    contorno oscuro, agujeros oscuros en anillo y centro oscuro."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=WHITE + (255,), outline=DARK + (255,), width=6)
    import math
    for k in range(9):
        a = math.radians(-90 + k * 40)
        hx = cx + int(0.58 * r * math.cos(a))
        hy = cy + int(0.58 * r * math.sin(a))
        draw.ellipse([hx - 9, hy - 9, hx + 9, hy + 9],
                     fill=DARK + (255,))
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14],
                 fill=DARK + (255,))


def handset_polygon(cx, cy, r, half, a0, a1, step=2):
    """Auricular como una sola silueta tipo plátano: puntos del arco
    exterior (a0→a1) y del interior (a1→a0). Así el contorno blanco
    queda solo por fuera, sin la franja blanca interior que dejaba el
    arco con ancho."""
    pts = []
    a = a0
    while a <= a1:
        rad = math.radians(a)
        pts.append((cx + (r + half) * math.cos(rad),
                    cy + (r + half) * math.sin(rad)))
        a += step
    a = a1
    while a >= a0:
        rad = math.radians(a)
        pts.append((cx + (r - half) * math.cos(rad),
                    cy + (r - half) * math.sin(rad)))
        a -= step
    return pts


def build_d2(size=1024):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, 80)
    fm = ImageFont.truetype(FONT, 130)
    # auricular curvado arriba: una sola silueta con contorno blanco
    # (arco más cerrado para que se lea como auricular y no como arco)
    cx, cy, r = 512, 560, 320
    d.polygon(handset_polygon(cx, cy, r, 61, 220, 320), fill=WHITE)
    d.polygon(handset_polygon(cx, cy, r, 52, 220, 320), fill=DARK)
    # orejeras en los extremos del arco, fundidas con él
    for ex, ey in ((267, 354), (757, 354)):
        d.ellipse([ex - 62, ey - 62, ex + 62, ey + 62],
                  fill=WHITE + (255,))
        d.ellipse([ex - 54, ey - 54, ex + 54, ey + 54],
                  fill=DARK + (255,))
    # base del teléfono justo debajo de «MÓVIL», como en el logo oficial
    d.rounded_rectangle([350, 580, 674, 655], radius=20,
                        fill=DARK + (255,), outline=WHITE + (255,),
                        width=8)
    d.line([390, 618, 634, 618], fill=WHITE + (255,), width=6)
    centered_text(d, 375, "Gartic", fg, WHITE, stroke_w=6)
    # «MÓVIL» con el disco como la Ó (y su tilde amarilla encima)
    y_top = 465
    b_m = d.textbbox((0, 0), "M", font=fm, stroke_width=9)
    b_vil = d.textbbox((0, 0), "VIL", font=fm, stroke_width=9)
    w_m = b_m[2] - b_m[0]
    w_vil = b_vil[2] - b_vil[0]
    dial_r = 59
    gap = 14
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
    # lápiz pequeño como garabato abajo a la izquierda
    img.alpha_composite(
        pencil_layer(size, 300, 770, length=180, thick=36, angle=30))
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    variants = {"D1": build_d1(), "D2": build_d2()}
    for name, icon in variants.items():
        icon.save(os.path.join(OUT, f"icono-{name}.png"))
        sim_miui(icon, 96).save(
            os.path.join(OUT, f"icono-{name}-miui-96.png"))
        sim_miui(icon, 192).save(
            os.path.join(OUT, f"icono-{name}-miui-192.png"))
        print("variante", name, "lista")
    # comparativa C1 / D1 / D2 a 96 y 48 px
    c1 = Image.open(os.path.join(OUT, "icono-C1.png"))
    comp = Image.new("RGB", (350, 225), (255, 255, 255))
    cd = ImageDraw.Draw(comp)
    lab = ImageFont.truetype(FONT, 26)
    lab_s = ImageFont.truetype(FONT, 20)
    for i, (name, icon) in enumerate((("C1", c1), ("D1", variants["D1"]),
                                      ("D2", variants["D2"]))):
        x = 10 + i * 116
        comp.paste(sim_miui(icon, 96), (x, 8))
        cd.text((x + 35, 108), name, font=lab, fill=(0, 0, 0))
        comp.paste(sim_miui(icon, 48), (x + 24, 142))
        cd.text((x + 28, 194), "48 px", font=lab_s, fill=(90, 90, 90))
    comp.save(os.path.join(OUT, "comparativa-96-D-C1.png"))
    print("comparativa en", OUT)


if __name__ == "__main__":
    main()
