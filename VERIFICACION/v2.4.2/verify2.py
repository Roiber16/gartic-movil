#!/usr/bin/env python3
"""Comprobación extra v2.4.2: menús del reproductor de animación y del lienzo.
- album-anim: construye un álbum de Animación y prueba animSpeed/animLoop.
- draw: pantalla de dibujo; el menú de brushSize existe (oculto con su
  contenedor en screen-play, como lo estaba el select original).
Escribe VERIFICACION/v2.4.2/reporte-extra.json y capturas en shots-360/.
"""
import json, os, re, subprocess

PROJ = os.path.expanduser("~/workspace/gartic-movil")
HS = os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/headless_shell")
OUT = os.path.join(PROJ, "VERIFICACION", "v2.4.2")

AUDIT_JS = """
<script>
window.__errs=[];
window.addEventListener("error", function(e){ window.__errs.push(String(e.message)); });
var __ce=console.error; console.error=function(){ window.__errs.push([].join.call(arguments," ")); __ce.apply(console, arguments); };
window.addEventListener("load", function(){
  setTimeout(function(){
    try{
      SCENARIO_ACTIONS
      setTimeout(function(){
        try{
          var active=document.querySelector(".screen.active")||document.body;
          var rep={screen:active.id, errors:window.__errs,
            overflow:document.documentElement.scrollWidth>window.innerWidth,
            scrollW:document.documentElement.scrollWidth, vw:window.innerWidth,
            SCENARIO_REPORT
          };
          document.getElementById("testResult").textContent="AUDIT "+JSON.stringify(rep);
          document.title="AUDIT-DONE";
        }catch(e){ document.title="AUDIT-ERR "+e.message; }
      }, 700);
    }catch(e){ document.title="AUDIT-ERR "+e.message; }
  }, 2200);
});
</script>
</body>"""

ANIM_ACTIONS = """
(function(){
  var players=[{id:0,name:"Ana",avatar:"\\uD83E\\uDD8A"},{id:1,name:"Beto",avatar:"\\uD83D\\uDC3C"},{id:2,name:"Carla",avatar:"\\uD83E\\uDD81"},{id:3,name:"Dan",avatar:"\\uD83D\\uDC38"}];
  S.players=players; S.mode="animation"; S.settings={write:0, draw:0, describe:0};
  var tmp=document.createElement("canvas"); tmp.width=640; tmp.height=440;
  var tc=tmp.getContext("2d"); tc.fillStyle="#fff"; tc.fillRect(0,0,640,440);
  tc.strokeStyle="#1d1933"; tc.lineWidth=6; tc.beginPath(); tc.arc(320,220,90,0,Math.PI*2); tc.stroke();
  var img=tmp.toDataURL("image/png");
  S.engine=new GameEngine(players, S.settings, "animation"); S.engine.start();
  var steps=specFor("animation").steps(4);
  for(var st=0; st<steps; st++){ for(var p=0;p<4;p++){ S.engine.submit(p, st, {type:"draw", image:img, strokes:[]}); } if(st<steps-1) S.engine.step++; }
  S.engine.finished=true; showAlbum();
  var sp=document.querySelector("#animSpeed"); var sb=sp&&sp.nextElementSibling; if(sb) sb.click();
  var pan=document.querySelector(".menu-panel"); var opts=pan?pan.querySelectorAll(".menu-opt"):[];
  var t=null; opts.forEach(function(o){ if(o.textContent.trim()==="2's") t=o; }); if(t) t.click();
  var lp=document.querySelector("#animLoop"); var lb=lp&&lp.nextElementSibling; if(lb) lb.click();
  var pan2=document.querySelector(".menu-panel"); var opts2=pan2?pan2.querySelectorAll(".menu-opt"):[];
  var t2=null; opts2.forEach(function(o){ if(o.textContent.indexOf("Adelante")>=0) t2=o; }); if(t2) t2.click();
})();
"""
ANIM_REPORT = """animPlayer:!!document.querySelector(".anim-player"),
            animSpeedValue:(function(){ var s=document.querySelector("#animSpeed"); return s?s.value:null; })(),
            animSpeedLabel:(function(){ var s=document.querySelector("#animSpeed"); return s&&s.nextElementSibling?s.nextElementSibling.querySelector(".menu-lab").textContent:null; })(),
            animLoopValue:(function(){ var s=document.querySelector("#animLoop"); return s?s.value:null; })(),
            animLoopLabel:(function(){ var s=document.querySelector("#animLoop"); return s&&s.nextElementSibling?s.nextElementSibling.querySelector(".menu-lab").textContent:null; })(),
            visibleSelects:(function(){ var n=0; document.querySelectorAll("select").forEach(function(s){ if(getComputedStyle(s).display!=="none") n++; }); return n; })()"""

DRAW_REPORT = """brushMenu:!!(document.querySelector("#brushSize")&&document.querySelector("#brushSize").nextElementSibling&&document.querySelector("#brushSize").nextElementSibling.classList.contains("menu-btn")),
            brushHidden:getComputedStyle(document.querySelector(".draw-controls")).display==="none",
            visibleSelects:(function(){ var n=0; document.querySelectorAll("select").forEach(function(s){ if(getComputedStyle(s).display!=="none") n++; }); return n; })()"""

def run(name, hashfrag, actions, report):
    src = open(os.path.join(PROJ, "www", "index.html"), encoding="utf-8").read()
    js = AUDIT_JS.replace("SCENARIO_ACTIONS", actions).replace("SCENARIO_REPORT", report)
    tmp = os.path.join(PROJ, "www", "__verify2-%s.html" % name)
    open(tmp, "w", encoding="utf-8").write(src.replace("</body>", js, 1))
    shot = os.path.join(OUT, "shots-360", "shot-%s.png" % name)
    cmd = [HS, "--headless", "--disable-gpu", "--no-sandbox",
           "--window-size=360,800", "--hide-scrollbars",
           "--virtual-time-budget=8000", "--run-all-compositor-stages-before-draw",
           "--screenshot=%s" % shot, "--dump-dom", "file://%s%s" % (tmp, hashfrag)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    m = re.search(r"AUDIT (\{.*?\})</div>", p.stdout, re.S)
    if not m:
        return {"screen": name, "error": "sin AUDIT", "tail": (p.stdout[-300:] if p.stdout else p.stderr[-300:])}
    try:
        r = json.loads(m.group(1))
    except Exception as e:
        return {"screen": name, "error": "JSON malo: %s" % e}
    r["shot"] = "shots-360/shot-%s.png" % name
    return r

def main():
    results = []
    print("album-anim ...", flush=True)
    results.append(run("album-anim", "", ANIM_ACTIONS, ANIM_REPORT))
    print("draw ...", flush=True)
    results.append(run("draw", "#shot=draw", "", DRAW_REPORT))
    with open(os.path.join(OUT, "reporte-extra.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    import glob
    for t in glob.glob(os.path.join(PROJ, "www", "__verify2-*.html")):
        os.remove(t)
    for r in results:
        print(json.dumps(r, ensure_ascii=False))

if __name__ == "__main__":
    main()
