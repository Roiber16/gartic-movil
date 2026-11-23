#!/usr/bin/env python3
"""Medición B1/B2: clip de «Deshacer» y solape de la barra roja con la fila
Deshacer/Rehacer/Limpiar/✕ Salir en las pantallas de dibujo, a 360x800 y 390x844.
Uso: python3 measure_b1b2.py [360|390] [shot...]
Escribe JSON en VERIFICACION/v2.4/revision-final/fix-b1b2/measure-<w>-<antes|despues>.json
y capturas med-<shot>-<w>.png en el mismo directorio (solo si se pasa --shots)."""
import json, os, re, subprocess, sys

PROJ = os.path.expanduser("~/workspace/gartic-movil")
HS = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/headless_shell")
OUT = os.path.join(PROJ, "VERIFICACION", "v2.4", "revision-final", "fix-b1b2")
os.makedirs(OUT, exist_ok=True)

W = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 360
H = 844 if W == 390 else 800
REST = [a for a in sys.argv[2:] if not a.startswith("--")]
TAG = "despues" if "--despues" in sys.argv else "antes"
SHOTS = REST or ["play-normal", "play-icebreaker", "play-missing", "play-corpse",
                 "play-knockoff", "play-sandwich", "play-animation", "play-story",
                 "play-masterpiece", "play-secret", "play-score", "play-complement",
                 "play-coop", "play-background", "play-solo",
                 "draw", "draw-memory", "draw-tools", "guess-draw", "guess-live"]

HOOK = """
<script>
setTimeout(function(){
  var r={docH:document.documentElement.scrollHeight, innerH:window.innerHeight,
    overflowX:document.documentElement.scrollWidth>window.innerWidth, undo:null, row:null, bar:null, hecho:null, pal:null};
  function m(el){ if(!el) return null; var rc=el.getBoundingClientRect();
    return {x:Math.round(rc.x), y:Math.round(rc.y), w:Math.round(rc.width), h:Math.round(rc.height),
      top:Math.round(rc.top), bottom:Math.round(rc.bottom),
      sw:el.scrollWidth, cw:el.clientWidth, clip: el.scrollWidth>el.clientWidth+1,
      visible: rc.top>=0 && rc.bottom<=window.innerHeight}; }
  var u=document.querySelector("#btnUndo");
  if(u){ var row=u.parentElement; r.undo={btn:m(u), redo:m(document.querySelector("#btnRedo")),
    clear:m(document.querySelector("#btnClear")), leave:m(document.querySelector("#btnLeaveDraw")),
    row:m(row)}; }
  var bar=document.querySelector(".draw-bar");
  if(bar) r.bar=m(bar);
  if(r.undo && r.bar){
    var a=r.undo.row, b=r.bar;
    var oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
    var ox=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x);
    r.overlapRowBar = (oy>0 && ox>0) ? {oy:oy, ox:ox} : null;
  }
  var hd=document.querySelector("#btnSendDraw");
  if(hd) r.hecho=m(hd);
  var pal=document.querySelector("#barPalette");
  if(pal) r.pal=m(pal);
  var el=document.getElementById("testResult"); if(el) el.textContent="MEASURE "+JSON.stringify(r)+" ENDMEASURE";
}, 1500);
</script>
"""

results = {}
for name in SHOTS:
    src = os.path.join(PROJ, "www", "index.html")
    tmp = f"/tmp/b1b2-{W}-{name}.html"
    html = open(src, encoding="utf-8").read()
    if name == "play-normal":
        pass
    html = html.replace("</body>", HOOK + "</body>")
    open(tmp, "w", encoding="utf-8").write(html)
    shot = os.path.join(OUT, f"med-{name}-{W}.png")
    cmd = [HS, "--headless", "--disable-gpu", "--no-sandbox",
           f"--window-size={W},{H}", "--hide-scrollbars",
           "--virtual-time-budget=9000", "--run-all-compositor-stages-before-draw",
           f"--screenshot={shot}", "--dump-dom", f"file://{tmp}#shot={name}"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        print(f"{name:18s} TIMEOUT"); results[name] = {"error": "timeout"}; continue
    dom = p.stdout or ""
    m = re.search(r"MEASURE (\{.*?\}) ENDMEASURE", dom, re.S)
    if m:
        try:
            results[name] = json.loads(m.group(1))
        except Exception as e:
            results[name] = {"error": "parse", "raw": m.group(1)[:300]}
    else:
        results[name] = {"error": "sin medida", "stderr": (p.stderr or "")[-200:]}

out = os.path.join(OUT, f"measure-{W}-{TAG}.json")
json.dump(results, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for name, r in results.items():
    if "error" in r:
        print(f"{name:18s} ERROR {r['error']}")
        continue
    u = r.get("undo")
    if not u:
        print(f"{name:18s} docH={r['docH']} (sin lienzo)")
        continue
    b = u["btn"]
    ov = r.get("overlapRowBar")
    print(f"{name:18s} docH={r['docH']:4d} undo {b['sw']}v{b['cw']} clip={b['clip']} "
          f"row y={u['row']['top']}-{u['row']['bottom']} vis={u['row']['visible']} "
          f"bar y={r['bar']['top']}-{r['bar']['bottom']} solape={ov} "
          f"hecho vis={r['hecho']['visible'] if r.get('hecho') else '-'} pal vis={r['pal']['visible'] if r.get('pal') else '-'}")
print("->", out)
