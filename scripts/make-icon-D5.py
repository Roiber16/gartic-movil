#!/usr/bin/env python3
"""Variante D5 del ícono de Gartic Móvil — «Teléfono antiguo con detalle».

Roi lo pidió: «Intenta eso» (redibujar con mucho más detalle, a mano).

Contexto: D1 y D2 rechazadas; D3 y D4 rechazadas por Roi («cómo
piensas que eso se parece al original?»). Intentar editar la imagen
del logo original directamente no se pudo. La única vía es un
redibujo propio CON DETALLE.

La lección clave, mirando el logo oficial
(VERIFICACION/v2.4/revision-final/pinterest/logo-oficial-icono.jpg):
en el original NO hay un cuerpo oscuro grande. La palabra PHONE en
blanco ES el cuerpo, enmarcada por el auricular oscuro arriba y la
barra de base oscura abajo, todo envuelto en un contorno blanco
estilo pegatina. La D4 falló justo ahí: puso «MÓVIL» encima de una
losa oscura (trapezoide) y se lee como un bloque, no como el logo.

La D5 copia la estructura REAL del original, con detalle de
ilustración (no pictograma plano):
1. Auricular: barra ancha y baja, borde superior curvado, con
   degradado (más claro arriba, más oscuro abajo), brillo suave
   arriba, bocinas redondas bien marcadas en los extremos (aro
   claro, interior oscuro con rejilla de 3 puntos y brillo) y rayo
   blanco en el centro, como en el original.
2. Debajo del auricular, dos barritas de apoyo (la horquilla donde
   descansa el auricular).
3. «Gartic» en blanco con contorno oscuro, pegado al auricular.
4. «MÓVIL» en grande, letras BLANCAS con contorno oscuro
   directamente sobre el degradado (no sobre una losa oscura), con
   el disco giratorio como la «Ó»: disco blanco GRANDE y detallado
   (10 agujeros para los dedos, números 1-9 y 0 alrededor, centro
   oscuro con punto blanco, brillo) y tilde amarilla encima.
5. Barra de base oscura y ancha debajo, con degradado y brillo en
   el borde superior.
6. Todo envuelto en UN SOLO contorno blanco estilo pegatina (la
   máscara de la unión dilatada), más sombra suave debajo.
Centrado, sin nada a los lados, dentro de la zona segura central
(199-823 de 1024 px), sobre el degradado violeta-magenta de la app.

La C1 sigue siendo el ícono instalado; la D5 es SOLO una
alternativa para que Roi compare y elija. No se instala nada.
"""
import importlib.util
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos")
SCRIPTS = os.path.join(ROOT, "scripts")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_icon_c = _load("icon_c", os.path.join(SCRIPTS, "make-icon-C-revisada.py"))
_icon_d = _load("icon_d", os.path.join(SCRIPTS, "make-icon-D.py"))
_icon_d3 = _load("icon_d3", os.path.join(SCRIPTS, "make-icon-D3.py"))

FONT = _icon_c.FONT
DARK = _icon_c.DARK
WHITE = _icon_c.WHITE
YELLOW = _icon_c.YELLOW
gradient = _icon_c.gradient
sim_miui = _icon_c.sim_miui
bolt = _icon_d3.bolt
sticker_outline = _icon_d3.sticker_outline

# --- geometría de la D5 (lienzo 1024, centro x=512) ---
# Auricular: barra de x=272 a 752; borde superior con arco que sube
# 60 px en el centro; grosor 60. Bocinas en los extremos.
HS_X0, HS_X1 = 272, 752
HS_TOP_END, HS_RISE, HS_THICK = 402, 60, 60
EAR_R = 52
EAR_C = [(HS_X0, HS_TOP_END + HS_THICK // 2),
         (HS_X1, HS_TOP_END + HS_THICK // 2)]
REST_BARS = [(240, 460, 320, 482), (704, 460, 784, 482)]
BASE_BAR = (300, 634, 724, 688)
GARTIC_Y = 405
MOVIL_Y = 508

# Colores de detalle (derivados del violeta oscuro de la app).
HS_TOP = (78, 54, 152)      # auricular, borde superior (más claro)
HS_BOT = (36, 22, 84)       # auricular, borde inferior (más oscuro)
CUP_RING = (118, 86, 196)   # aro claro de la bocina
CUP_IN = (26, 16, 62)       # interior oscuro de la bocina
BASE_TOP = (62, 40, 134)    # base, borde superior
BASE_BOT = (34, 20, 80)     # base, borde inferior
SHADOW = (18, 8, 48)


def vertical_gradient(size, top, bottom):
    """Degradado vertical RGB entre dos colores."""
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t)
                  for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def handset_points():
    """Polígono del auricular: borde superior en arco, borde
    inferior paralelo (grosor uniforme)."""
    n = 48
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        x = HS_X0 + (HS_X1 - HS_X0) * t
        y = HS_TOP_END - HS_RISE * math.sin(math.pi * t)
        top.append((x, y))
        bot.append((x, y + HS_THICK))
    return top + bot[::-1]


def handset_mask():
    """Máscara L del auricular completo: barra + bocinas + apoyos."""
    m = Image.new("L", (1024, 1024), 0)
    d = ImageDraw.Draw(m)
    d.polygon(handset_points(), fill=255)
    for ex, ey in EAR_C:
        d.ellipse([ex - EAR_R, ey - EAR_R, ex + EAR_R, ey + EAR_R],
                  fill=255)
    for x0, y0, x1, y1 in REST_BARS:
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=255)
    return m


def base_mask():
    m = Image.new("L", (1024, 1024), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle(list(BASE_BAR), radius=16, fill=255)
    return m


def tilde_points(cx, cy, hw=13, hh=4, angle=-25):
    """Tilde como barrita inclinada (acento), no como punto: se lee
    como la tilde de la Ó y no como un lunar bajo «Gartic»."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)):
        pts.append((cx + dx * ca - dy * sa, cy + dx * sa + dy * ca))
    return pts


def movil_layout(draw, font, dial_r, gap=12):
    """Ancho y posiciones de «M» + disco + «VIL» con esa fuente."""
    sw = 9
    b_m = draw.textbbox((0, 0), "M", font=font, stroke_width=sw)
    b_vil = draw.textbbox((0, 0), "VIL", font=font, stroke_width=sw)
    w_m = b_m[2] - b_m[0]
    w_vil = b_vil[2] - b_vil[0]
    total = w_m + gap + 2 * dial_r + gap + w_vil
    return total, b_m, b_vil


def draw_dial(d, cx, cy, r):
    """Disco giratorio GRANDE y detallado: disco blanco, 10 agujeros
    para los dedos, números 1-9 y 0 alrededor, centro oscuro con
    punto blanco y brillo."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r],
              fill=WHITE + (255,), outline=DARK + (255,), width=5)
    # 10 agujeros para los dedos
    hole_r = max(7, int(r * 0.16))
    for k in range(10):
        a = math.radians(-90 + k * 36)
        hx = cx + int(0.58 * r * math.cos(a))
        hy = cy + int(0.58 * r * math.sin(a))
        d.ellipse([hx - hole_r, hy - hole_r, hx + hole_r,
                   hy + hole_r], fill=DARK + (255,))
    # números 1-9, 0 alrededor de los agujeros
    num_f = ImageFont.truetype(FONT, max(12, int(r * 0.26)))
    for k, num in enumerate("1234567890"):
        a = math.radians(-90 + k * 36)
        nx = cx + int(0.80 * r * math.cos(a))
        ny = cy + int(0.80 * r * math.sin(a))
        d.text((nx, ny), num, font=num_f, fill=DARK + (255,),
               anchor="mm")
    # centro oscuro con punto blanco
    cr = max(11, int(r * 0.27))
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
              fill=DARK + (255,),
              outline=(120, 92, 200, 255), width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4],
              fill=WHITE + (255,))
    # brillo arriba a la izquierda del disco
    d.arc([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
          start=175, end=265, fill=(255, 255, 255, 150), width=4)


def build_d5(size=1024):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)

    # --- fuentes y medidas de «MÓVIL» ---
    font = None
    dial_r = None
    for size_try in range(160, 99, -4):
        f_try = ImageFont.truetype(FONT, size_try)
        r_try = int(size_try * 0.37)
        total, _, _ = movil_layout(d, f_try, r_try)
        if total <= 560:
            font, dial_r = f_try, r_try
            break
    total, b_m, b_vil = movil_layout(d, font, dial_r)
    gap = 12
    w_m = b_m[2] - b_m[0]
    w_vil = b_vil[2] - b_vil[0]
    x_mov = (1024 - total) / 2
    cap_h = b_m[3] - b_m[1]
    y_top = MOVIL_Y
    dial_cx = x_mov + w_m + gap + dial_r
    dial_cy = y_top + cap_h // 2
    x_vil = x_mov + w_m + gap + 2 * dial_r + gap

    fg = ImageFont.truetype(FONT, 80)

    # --- máscara de la unión (auricular + apoyos + base + letras +
    # disco + tilde): el contorno blanco estilo pegatina envuelve
    # TODO como una sola pieza, como en el original. ---
    union = Image.new("L", (1024, 1024), 0)
    ud = ImageDraw.Draw(union)
    ud.polygon(handset_points(), fill=255)
    for ex, ey in EAR_C:
        ud.ellipse([ex - EAR_R, ey - EAR_R, ex + EAR_R, ey + EAR_R],
                   fill=255)
    for x0, y0, x1, y1 in REST_BARS:
        ud.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=255)
    ud.rounded_rectangle(list(BASE_BAR), radius=16, fill=255)
    # «Gartic» y «MÓVIL» en la máscara (con su trazo, como en el
    # dibujo final) para que la pegatina las envuelva también.
    gb = ud.textbbox((0, 0), "Gartic", font=fg, stroke_width=7)
    gw = gb[2] - gb[0]
    gx = (1024 - gw) / 2 - gb[0]
    ud.text((gx, GARTIC_Y - gb[1]), "Gartic", font=fg, fill=255,
            stroke_width=7)
    ud.text((x_mov - b_m[0], y_top - b_m[1]), "M", font=font,
            fill=255, stroke_width=9)
    ud.text((x_vil - b_vil[0], y_top - b_vil[1]), "VIL", font=font,
            fill=255, stroke_width=9)
    ud.ellipse([dial_cx - dial_r, dial_cy - dial_r,
                dial_cx + dial_r, dial_cy + dial_r], fill=255)
    ud.polygon(tilde_points(dial_cx, y_top - 14), fill=255)

    # --- sombra suave debajo de toda la pegatina ---
    shadow_mask = union.filter(ImageFilter.MaxFilter(3)).filter(
        ImageFilter.GaussianBlur(10))
    shadow = Image.new("RGBA", (1024, 1024), SHADOW + (110,))
    shadow.putalpha(shadow_mask)
    img.alpha_composite(shadow, (0, 14))

    # --- contorno blanco estilo pegatina ---
    shape = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    shape.putalpha(union)
    img.alpha_composite(sticker_outline(shape, 12))

    # --- auricular con degradado (claro arriba, oscuro abajo) ---
    hs_m = handset_mask()
    grad = vertical_gradient((1024, 1024), HS_TOP, HS_BOT).convert(
        "RGBA")
    layer = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    layer.paste(grad, (0, 0), hs_m)
    img.alpha_composite(layer)

    # brillo suave en el borde superior del auricular
    hl = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.ellipse([300, 330, 724, 372], fill=(255, 255, 255, 70))
    hl = hl.filter(ImageFilter.GaussianBlur(8))
    hl.putalpha(Image.composite(hl.split()[3], Image.new(
        "L", (1024, 1024), 0), hs_m))
    img.alpha_composite(hl)

    # --- bocinas: aro claro, interior oscuro con rejilla y brillo ---
    d = ImageDraw.Draw(img)
    for ex, ey in EAR_C:
        d.ellipse([ex - 40, ey - 40, ex + 40, ey + 40],
                  outline=CUP_RING + (255,), width=4)
        d.ellipse([ex - 34, ey - 34, ex + 34, ey + 34],
                  fill=CUP_IN + (255,))
        for dx, dy in ((-10, -6), (10, -6), (0, 10)):
            d.ellipse([ex + dx - 4, ey + dy - 4, ex + dx + 4,
                       ey + dy + 4], fill=(16, 9, 40, 255))
        d.arc([ex - 40, ey - 40, ex + 40, ey + 40], start=190,
              end=320, fill=(255, 255, 255, 170), width=5)

    # --- rayo blanco en el centro del auricular ---
    bolt(d, 512, 372, w=30, h=46)

    # --- barra de base con degradado y brillo superior ---
    bm = base_mask()
    grad_b = vertical_gradient((1024, 1024), BASE_TOP,
                               BASE_BOT).convert("RGBA")
    layer_b = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    layer_b.paste(grad_b, (0, 0), bm)
    img.alpha_composite(layer_b)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([BASE_BAR[0] + 14, BASE_BAR[1] + 6,
                         BASE_BAR[2] - 14, BASE_BAR[1] + 14],
                        radius=4, fill=(255, 255, 255, 80))

    # --- «Gartic» blanco con contorno oscuro ---
    d.text((gx, GARTIC_Y - gb[1]), "Gartic", font=fg,
           fill=WHITE, stroke_width=7, stroke_fill=DARK)

    # --- «MÓVIL»: M + disco + VIL, letras blancas con contorno ---
    d.text((x_mov - b_m[0], y_top - b_m[1]), "M", font=font,
           fill=WHITE, stroke_width=9, stroke_fill=DARK)
    draw_dial(d, int(dial_cx), dial_cy, dial_r)
    # tilde amarilla inclinada sobre el disco (justo encima de la Ó)
    tp = tilde_points(dial_cx, y_top - 14)
    tp_big = tilde_points(dial_cx, y_top - 14, hw=16, hh=7)
    d.polygon(tp_big, fill=DARK + (255,))
    d.polygon(tp, fill=YELLOW + (255,))
    d.text((x_vil - b_vil[0], y_top - b_vil[1]), "VIL", font=font,
           fill=WHITE, stroke_width=9, stroke_fill=DARK)
    print("MÓVIL: fuente", font.size, "ancho total", round(total),
          "dial r", dial_r)
    return img.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    icon = build_d5()
    icon.save(os.path.join(OUT, "icono-D5.png"))
    sim_miui(icon, 96).save(os.path.join(OUT, "icono-D5-miui-96.png"))
    sim_miui(icon, 192).save(os.path.join(OUT, "icono-D5-miui-192.png"))
    print("variante D5 lista")

    # comparativa a 96 y 48 px: logo oficial / D5 / C1
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
            ("D5", sim_miui(icon, 96), sim_miui(icon, 48)),
            ("C1", sim_miui(c1, 96), sim_miui(c1, 48)))):
        x = 12 + i * 118
        comp.paste(big, (x, 12 if name != "ORIGINAL" else 26))
        cd.text((x + 8, 116), name, font=lab, fill=(0, 0, 0))
        comp.paste(small, (x + 24, 152 if name != "ORIGINAL" else 168))
        cd.text((x + 28, 206), "48 px", font=lab_s, fill=(90, 90, 90))
    comp.save(os.path.join(OUT, "comparativa-96-D5-original.png"))
    print("comparativa en", OUT)


if __name__ == "__main__":
    main()
