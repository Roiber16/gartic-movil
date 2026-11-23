#!/usr/bin/env python3
"""Auditoría de botones de Gartic Móvil a 360x800.

Para cada pantalla (#shot=...), carga una copia de www/index.html con un
script de auditoría añadido, y vuelca un JSON con todos los botones,
selects e inputs visibles de la pantalla activa:
- rect (x,y,w,h), altura <44 px, texto cortado, fuera de la pantalla
  (horizontal), solapamiento con otros botones.
Uso: python3 audit_buttons.py [pantalla ...]  (por defecto, todas)
Escribe VERIFICACION/v2.4/buttons-audit.json y capturas en VERIFICACION/v2.4/
"""
import json, os, re, subprocess, sys, shutil

PROJ = os.path.expanduser("~/workspace/gartic-movil")
HS = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/headless_shell")
OUT = os.path.join(PROJ, "VERIFICACION", "v2.4")
os.makedirs(OUT, exist_ok=True)

SHOTS = ["splash", "home", "modes", "setup", "settings", "how", "join",
         "create", "countdown", "pass", "write", "describe", "draw",
         "draw-tools", "album", "guess-draw", "guess-live", "podium", "rooms"]

AUDIT_JS = """
<script>
window.addEventListener("load", function(){
  setTimeout(function(){
    try{
      var active=document.querySelector(".screen.active")||document.body;
      var els=active.querySelectorAll("button, select, input, textarea, [role=button]");
      var items=[];
      var rects=[];
      els.forEach(function(el){
        var r=el.getBoundingClientRect();
        var cs=getComputedStyle(el);
        if(cs.display==="none"||cs.visibility==="hidden") return;
        if(r.width===0&&r.height===0) return;
        var txt=(el.textContent||el.value||el.placeholder||el.getAttribute("aria-label")||"").trim().replace(/\\s+/g," ").slice(0,40);
        var clipX=el.scrollWidth>el.clientWidth+1, clipY=el.scrollHeight>el.clientHeight+1;
        items.push({tag:el.tagName.toLowerCase(), id:el.id||"", cls:(el.className||"").toString().slice(0,30),
          text:txt, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height),
          lowH:r.height<44, clipText:clipX||clipY, outH:r.x<-1||r.right>361, outV:r.bottom>801});
        rects.push({id:el.id||txt, x:r.x, y:r.y, r:r.right, b:r.bottom});
      });
      var overlaps=[];
      for(var i=0;i<rects.length;i++) for(var j=i+1;j<rects.length;j++){
        var a=rects[i], b=rects[j];
        var ox=Math.min(a.r,b.r)-Math.max(a.x,b.x), oy=Math.min(a.b,b.b)-Math.max(a.y,b.y);
        if(ox>4&&oy>4) overlaps.push(a.id+" ~ "+b.id);
      }
      var rep={screen:active.id, overflow:document.documentElement.scrollWidth>window.innerWidth,
        scrollW:document.documentElement.scrollWidth, items:items, overlaps:overlaps};
      var el2=document.getElementById("testResult");
      el2.textContent="AUDIT "+JSON.stringify(rep);
      document.title="AUDIT-DONE";
    }catch(e){ document.title="AUDIT-ERR "+e.message; }
  }, 1800);
});
</script>
</body>"""

def run_shot(name):
    src = os.path.join(PROJ, "www", "index.html")
    tmp = f"/tmp/audit-{name}.html"
    html = open(src, encoding="utf-8").read()
    assert "</body>" in html
    open(tmp, "w", encoding="utf-8").write(html.replace("</body>", AUDIT_JS, 1))
    shot = os.path.join(OUT, f"shot-{name}.png")
    cmd = [HS, "--headless", "--disable-gpu", "--no-sandbox",
           f"--window-size=360,800", "--hide-scrollbars",
           "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw",
           f"--screenshot={shot}", "--dump-dom",
           f"file://{tmp}#shot={name}"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    dom = p.stdout
    m = re.search(r"AUDIT (\{.*?\})</div>", dom, re.S)
    if not m:
        m2 = re.search(r"TEST (\{.*?\})</div>", dom, re.S)
        return {"screen": name, "error": "sin AUDIT", "dom_tail": dom[-300:] if dom else p.stderr[-300:]}
    try:
        return json.loads(m.group(1))
    except Exception as e:
        return {"screen": name, "error": f"json: {e}", "raw": m.group(1)[:300]}

def main():
    shots = sys.argv[1:] or SHOTS
    results = {}
    for s in shots:
        try:
            results[s] = run_shot(s)
            it = results[s].get("items", [])
            flags = sum(1 for i in it if i.get("lowH") or i.get("clipText") or i.get("outH"))
            print(f"{s}: {len(it)} controles, {flags} con aviso, "
                  f"solapes={len(results[s].get('overlaps', []))}, "
                  f"overflow={results[s].get('overflow')}")
        except Exception as e:
            results[s] = {"screen": s, "error": str(e)}
            print(f"{s}: ERROR {e}")
    with open(os.path.join(OUT, "buttons-audit.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("OK ->", os.path.join(OUT, "buttons-audit.json"))

if __name__ == "__main__":
    main()
