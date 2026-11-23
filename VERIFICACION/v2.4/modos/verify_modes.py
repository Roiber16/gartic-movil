#!/usr/bin/env python3
"""Verificación de los 14 modos nuevos de Gartic Móvil (v2.4).

Para cada modo:
- #auto=mode:<id> juega una partida completa de 4 jugadores y escribe el
  resultado en #testResult (errores de consola, desbordamiento, nº de
  álbumes y de eslabones). La captura queda en el álbum del modo.
- #shot=play-<id> captura la pantalla de juego en mitad de la partida
  (paso 1), con la vista previa / piel de cebolla / fondo acumulado /
  censura que toque a cada modo.
Además: regresión de #auto=normal y #auto=guess, y #shot=draw-memory y
#shot=modes (la lista ya muestra los 15 modos jugables).
Uso: python3 verify_modes.py
Escribe VERIFICACION/v2.4/modos/modos-verificacion.json y las capturas.
"""
import json, os, re, subprocess, sys

PROJ = os.path.expanduser("~/workspace/gartic-movil")
HS = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/headless_shell")
OUT = os.path.join(PROJ, "VERIFICACION", "v2.4", "modos")
os.makedirs(OUT, exist_ok=True)

MODES = ["story", "masterpiece", "secret", "sandwich", "score", "icebreaker",
         "knockoff", "complement", "missing", "corpse", "coop",
         "animation", "background", "solo"]

def run(url_hash, shot_name):
    src = os.path.join(PROJ, "www", "index.html")
    tmp = f"/tmp/modos-{shot_name}.html"
    html = open(src, encoding="utf-8").read()
    open(tmp, "w", encoding="utf-8").write(html)
    shot = os.path.join(OUT, f"{shot_name}.png")
    cmd = [HS, "--headless", "--disable-gpu", "--no-sandbox",
           "--window-size=360,800", "--hide-scrollbars",
           "--virtual-time-budget=8000", "--run-all-compositor-stages-before-draw",
           f"--screenshot={shot}", "--dump-dom",
           f"file://{tmp}#{url_hash}"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    dom = p.stdout or ""
    m = re.search(r"TEST (\{.*?\})</div>", dom, re.S)
    if not m:
        return {"hash": url_hash, "error": "sin TEST", "tail": (dom[-300:] or p.stderr[-300:])}
    try:
        return json.loads(m.group(1))
    except Exception as e:
        return {"hash": url_hash, "error": f"json: {e}", "raw": m.group(1)[:300]}

def main():
    results = {}
    for mode in MODES:
        r = run(f"auto=mode:{mode}", f"auto-{mode}")
        results[f"auto:{mode}"] = r
        ok = (not r.get("errors")) and r.get("auto") == f"mode:{mode}" and not r.get("fatal")
        print(f"auto {mode:11s} errors={r.get('errors')} overflow={r.get('overflow')} "
              f"albums={r.get('albums')} links={r.get('linksPerAlbum')} steps={r.get('steps')} "
              f"fatal={r.get('fatal')} -> {'OK' if ok else 'FALLO'}")
        s = run(f"shot=play-{mode}", f"play-{mode}")
        results[f"shot:play-{mode}"] = s
        ok2 = (not s.get("errors")) and not s.get("overflow")
        print(f"shot play-{mode:11s} errors={s.get('errors')} overflow={s.get('overflow')} -> {'OK' if ok2 else 'FALLO'}")
    for name, h in [("auto-normal", "auto=normal"), ("auto-guess", "auto=guess"),
                    ("auto-distrib", "auto=distrib"),
                    ("shot-draw-memory", "shot=draw-memory"), ("shot-secret-write", "shot=secret-write"),
                    ("shot-modes", "shot=modes")]:
        r = run(h, name)
        results[name] = r
        print(f"{name:18s} errors={r.get('errors')} overflow={r.get('overflow')} "
              f"auto={r.get('auto')} shot={r.get('shot')} fatal={r.get('fatal')} "
              f"validPerm={r.get('validPermutation')} random={r.get('randomOrder')} "
              f"fallbackBad={r.get('fallbackBad')} checks={r.get('fallbackChecks')} games={r.get('games')}")
    with open(os.path.join(OUT, "modos-verificacion.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("OK ->", os.path.join(OUT, "modos-verificacion.json"))

if __name__ == "__main__":
    main()
