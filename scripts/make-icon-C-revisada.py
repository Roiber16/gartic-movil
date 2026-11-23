#!/usr/bin/env python3
"""Ícono C revisado de Gartic Móvil — lápiz + TELÉFONO MÓVIL de verdad.

Roi eligió la C (el lápiz dibujando) pero pidió que haya también un
teléfono, para que juegue con el nombre "Gartic Móvil". Y dejó claro que
la A "no es un teléfono en ningún lugar del mundo, parece unas gafas o
un bigote": el auricular abstracto NO vale. El teléfono de aquí es un
MÓVIL MODERNO reconocible de verdad: rectángulo vertical, pantalla con
la grieta dibujada dentro, altavoz arriba, barra de inicio abajo, borde
oscuro. Que cualquiera lo vea y diga "eso es un móvil".

Dos composiciones:
- C1 (recomendada): móvil grande en el centro, lápiz más pequeño en
  diagonal dibujando SOBRE su pantalla (la punta toca la grieta).
- C2: móvil a la izquierda y lápiz a la derecha, del mismo tamaño,
  dibujando una línea quebrada en el aire.

En las dos: "Gartic" blanco arriba, "MÓVIL" amarillo en grande abajo,
degradado violeta a magenta, todo dentro de la zona segura central
(199-823 de 1024 px). Formas planas y simples, sin aspecto IA.
Fuente Baloo 2 ExtraBold (la fuente de la propia app, OFL, instanciada
a peso 800 desde www/fonts/baloo2-latin.woff2; ver
scripts/make-icon-C1-tipo.py): a 96 px se lee mejor que la DejaVu Sans
Bold anterior — trazo más grueso, formas redondeadas y coherente con
el juego. Tamaños 88/120 con contorno 6/8.

La elegida se instala con install(): assets/icon-1024.png y todos los
mipmap-* en android/... y assets/res/... (igual que make-icon-v2.1.py).
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.expanduser("~/workspace/gartic-movil")
OUT = os.path.join(ROOT, "VERIFICACION", "v2.3", "iconos-nuevos")
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "baloo2-extrabold.ttf")

VIOLET_TOP = (91, 31, 166)
VIOLET_MID = (106, 31, 181)
MAGENTA = (214, 51, 132)
DARK = (42, 26, 94)
WHITE = (255, 255, 255)
YELLOW = (255, 197, 49)
LAVENDER = (232, 222, 255)
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


def centered_text(draw, y_top, text, font, fill, stroke_w=5):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    w = bbox[2] - bbox[0]
    x = (1024 - w) / 2 - bbox[0]
    draw.text((x, y_top - bbox[1]), text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=DARK)


def modern_phone(size, x0, y0, x1, y1, crack=True, crack_w=9):
    """Móvil moderno reconocible: cuerpo blanco, pantalla lavanda con
    la grieta, altavoz arriba y barra de inicio abajo."""
    s = size
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    # cuerpo blanco con borde oscuro
    d.rounded_rectangle([x0, y0, x1, y1], radius=26,
                        fill=WHITE + (255,), outline=DARK + (255,), width=6)
    # pantalla lavanda (margen para altavoz arriba y barra abajo)
    sx0, sy0, sx1, sy1 = x0 + 16, y0 + 36, x1 - 16, y1 - 30
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=10,
                        fill=LAVENDER + (255,))
    # altavoz (ranura arriba, centrada)
    d.rounded_rectangle([(x0 + x1) // 2 - 22, y0 + 13,
                         (x0 + x1) // 2 + 22, y0 + 21], radius=4,
                        fill=DARK + (255,))
    # barra de inicio abajo
    d.rounded_rectangle([(x0 + x1) // 2 - 26, y1 - 20,
                         (x0 + x1) // 2 + 26, y1 - 12], radius=4,
                        fill=DARK + (255,))
    # grieta en la pantalla: zigzag oscuro de arriba a abajo + ramita
    if crack:
        cx = (sx0 + sx1) // 2
        crack = [(sx0 + 18, sy0 + 12), (cx + 6, sy0 + 70),
                 (cx - 22, sy0 + 130), (cx + 14, sy0 + 190),
                 (cx - 8, sy1 - 14)]
        d.line(crack, fill=DARK + (255,), width=crack_w, joint="curve")
        d.line([(cx - 22, sy0 + 130), (sx0 + 30, sy0 + 168)],
               fill=DARK + (255,), width=7)
        # estrellita amarilla al final de la grieta
        ex, ey = crack[-1]
        for dx, dy in ((0, -18), (0, 18), (-18, 0), (18, 0)):
            d.line([ex, ey, ex + dx, ey + dy], fill=YELLOW + (255,),
                   width=7)
    return out


def pencil_layer(size, tip_x, tip_y, length=300, thick=52, angle=24):
    """Lápiz amarillo en una capa, con la punta en (tip_x, tip_y)
    apuntando a la derecha; se gira 'angle' grados (antihorario) sobre
    la punta, así el cuerpo queda arriba a la izquierda."""
    s = size
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0 = tip_x - length
    y0 = tip_y - thick // 2
    y1 = tip_y + thick // 2
    # goma rosa + casquillo
    d.rounded_rectangle([x0, y0, x0 + 40, y1], radius=10,
                        fill=(255, 120, 150, 255), outline=DARK + (255,),
                        width=4)
    d.rectangle([x0 + 40, y0, x0 + 56, y1], fill=(200, 200, 200, 255),
                outline=DARK + (255,), width=4)
    # cuerpo amarillo
    d.rounded_rectangle([x0 + 56, y0, tip_x - 62, y1], radius=12,
                        fill=YELLOW + (255,), outline=DARK + (255,), width=5)
    d.line([x0 + 66, y0 + 8, tip_x - 72, y0 + 8], fill=DARK + (255,),
           width=3)
    d.line([x0 + 66, y1 - 8, tip_x - 72, y1 - 8], fill=DARK + (255,),
           width=3)
    # punta de madera + mina
    d.polygon([(tip_x - 62, y0), (tip_x, tip_y), (tip_x - 62, y1)],
              fill=(255, 220, 170, 255), outline=DARK + (255,))
    d.polygon([(tip_x - 26, tip_y - 9), (tip_x, tip_y),
               (tip_x - 26, tip_y + 9)], fill=DARK + (255,))
    layer = layer.rotate(angle, resample=Image.BICUBIC,
                         center=(tip_x, tip_y))
    return layer


def zigzag(size, points, width=16, color=WHITE):
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(out).line(points, fill=color + (255,), width=width,
                             joint="curve")
    return out


def build(size=1024, variant="C1"):
    img = gradient((size, size)).convert("RGBA")
    d = ImageDraw.Draw(img)
    fg = ImageFont.truetype(FONT, 88)
    fm = ImageFont.truetype(FONT, 120)
    centered_text(d, 235, "Gartic", fg, WHITE, stroke_w=6)
    if variant == "C1":
        # Móvil grande centrado; lápiz pequeño en diagonal con la punta
        # sobre la grieta de la pantalla.
        img.alpha_composite(modern_phone(size, 427, 320, 597, 660))
        img.alpha_composite(
            pencil_layer(size, 520, 480, length=300, thick=52, angle=24))
    else:  # C2
        # Móvil a la izquierda; lápiz a la derecha dibujando en el aire.
        img.alpha_composite(modern_phone(size, 250, 330, 400, 650))
        tip = (455, 555)
        # lápiz apuntando a la izquierda-abajo: se dibuja apuntando a
        # la derecha y se gira 180-28 grados sobre la punta
        layer = pencil_layer(size, tip[0], tip[1], length=330, thick=52,
                             angle=0)
        layer = layer.rotate(152, resample=Image.BICUBIC, center=tip)
        img.alpha_composite(layer)
        zig = [(tip[0] + 8, tip[1] - 6), (tip[0] + 70, tip[1] - 70),
               (tip[0] + 125, tip[1] - 25), (tip[0] + 185, tip[1] - 80),
               (tip[0] + 245, tip[1] - 35)]
        img.alpha_composite(zigzag(size, zig, width=14))
        ex, ey = zig[-1]
        star = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        sd = ImageDraw.Draw(star)
        for dx, dy in ((0, -22), (0, 22), (-22, 0), (22, 0)):
            sd.line([ex, ey, ex + dx, ey + dy], fill=YELLOW + (255,),
                    width=9)
        img.alpha_composite(star)
    centered_text(d, 672, "MÓVIL", fm, YELLOW, stroke_w=8)
    return img.convert("RGB")


def sim_miui(icon, px=96):
    crop = icon.crop((SAFE_LO, SAFE_LO, SAFE_HI, SAFE_HI))
    return crop.resize((px, px), Image.LANCZOS)


def circle_crop(img):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, img.size[0], img.size[1]], fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def install(icon):
    """Instala el ícono elegido: assets/icon-1024.png y mipmaps."""
    icon.save(os.path.join(ROOT, "assets", "icon-1024.png"))
    sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144,
             "xxxhdpi": 192}
    for base in (os.path.join(ROOT, "android", "app", "src", "main", "res"),
                 os.path.join(ROOT, "assets", "res")):
        for dpi, px in sizes.items():
            small = icon.resize((px, px), Image.LANCZOS)
            folder = os.path.join(base, "mipmap-" + dpi)
            small.save(os.path.join(folder, "ic_launcher.png"))
            circle_crop(small.convert("RGBA")).save(
                os.path.join(folder, "ic_launcher_round.png"))
            small.save(os.path.join(folder, "ic_launcher_foreground.png"))
    print("icono instalado en assets/icon-1024.png y mipmaps")


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in ("C1", "C2"):
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
    for i, name in enumerate(("C1", "C2")):
        sim = sim_miui(build(1024, name), 96)
        comp.paste(sim, (10 + i * 106, 10))
        cd.text((10 + i * 106 + 26, 112), name, font=lab, fill=(0, 0, 0))
    comp.save(os.path.join(OUT, "comparativa-96-C.png"))
    print("comparativa en", OUT)


if __name__ == "__main__":
    main()
