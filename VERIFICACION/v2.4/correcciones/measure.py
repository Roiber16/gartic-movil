#!/usr/bin/env python3
"""Medición rápida de alturas (docH) y posición de ¡HECHO! por pantalla, a 360x800."""
import json, os, re, subprocess, sys
PROJ = os.path.expanduser("~/workspace/gartic-movil")
HS = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/headless_shell")
OUT = os.path.join(PROJ, "VERIFICACION", "v2.4", "correcciones")
os.makedirs(OUT, exist_ok=True)
SHOTS = sys.argv[1:] or ["home", "modes", "create", "countdown", "play-normal", "play-icebreaker",
                          "play-missing", "play-corpse", "play-knockoff", "play-sandwich",
                          "play-animation", "album", "guess-live", "draw-memory"]
for name in SHOTS:
    src = os.path.join(PROJ, "www", "index.html")
    tmp = f"/tmp/corr-{name}.html"
    html = open(src, encoding="utf-8").read()
    # gancho de medida: tras runShot, escribir docH y posición de ¡HECHO! en #testResult
    hook = """
<script>
setTimeout(function(){
  var r={docH:document.documentElement.scrollHeight, innerH:window.innerHeight, overflow:document.documentElement.scrollWidth>window.innerWidth, hechoTop:-1, hechoBottom:-1, hechoVisible:false, palTop:-1, palBottom:-1, palVisible:false};
  var b=document.querySelector("#btnSendDraw");
  if(b){ var rc=b.getBoundingClientRect(); r.hechoTop=Math.round(rc.top); r.hechoBottom=Math.round(rc.bottom); r.hechoVisible= rc.top>=0 && rc.bottom<=window.innerHeight; }
  var pal=document.querySelector("#barPalette");
  if(pal){ var pr=pal.getBoundingClientRect(); r.palTop=Math.round(pr.top); r.palBottom=Math.round(pr.bottom); r.palVisible= pr.top>=0 && pr.bottom<=window.innerHeight; }
  var el=document.getElementById("testResult"); if(el) el.textContent="MEASURE "+JSON.stringify(r);
}, 1500);
</script>
"""
    if name=="home":
        html = html.replace("<script>", '<script>try{localStorage.setItem("gartic-movil-perfil", JSON.stringify({nick:"Roi",avatar:"🦊"}));}catch(e){}</script><script>', 1)
    html = html.replace("</body>", hook + "</body>")
    open(tmp, "w", encoding="utf-8").write(html)
    shot = os.path.join(OUT, f"med-{name}.png")
    cmd = [HS, "--headless", "--disable-gpu", "--no-sandbox",
           "--window-size=360,800", "--hide-scrollbars",
           "--virtual-time-budget=9000", "--run-all-compositor-stages-before-draw",
           f"--screenshot={shot}", "--dump-dom", f"file://{tmp}#shot={name}"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    dom = p.stdout or ""
    m = re.search(r"MEASURE (\{.*?\})", dom, re.S)
    print(f"{name:18s} {m.group(1) if m else 'SIN MEDIDA ' + (p.stderr[-200:] if p.stderr else '')}")
