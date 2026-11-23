#!/usr/bin/env python3
"""Verificación de los 6 cambios de Roi (23 nov 2026 10:48) en Gartic Móvil.

Carga copias de www/index.html con un script de auditoría añadido, en
Chromium headless (headless_shell 1161), a 360x800 y 320x568:
- errores de consola, desbordamiento horizontal
- punto 1: sin pestañas ANÓNIMO/VERIFICADO, sin texto de verificación
- punto 2: rejilla de avatares con 22 (12 animales + 10 personas), grupos
- punto 3: sin «Jugable en» ni etiquetas .tag en las tarjetas de modo
- punto 4: logo D5 (img assets/icon-1024.png) en la cabecera, visible en
  inicio, configurar, modos, crear sala y unirse
- punto 5: flecha del menú a >=12 px del borde derecho del botón
- punto 6: menús propios funcionando: abrir, elegir, valor del <select>
  oculto actualizado, evento change disparado (filas de jugadores,
  avatar humano, modosMaxPlayers, wifiModeSelect)
Uso: python3 verify.py
Escribe VERIFICACION/v2.4.2/reporte.json y capturas en shots-360/ y shots-320/
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
          var lg=document.querySelector("img.logo");
          var tb=document.querySelector("#topbar");
          var np=document.querySelector("#numPlayers");
          var npBtn=np&&np.nextElementSibling;
          var chev=npBtn?npBtn.querySelector(".chev"):null;
          var chevGap=(npBtn&&chev)?Math.round(npBtn.getBoundingClientRect().right-chev.getBoundingClientRect().right):-1;
          var visTxt=(function(){ var b=document.body.cloneNode(true); b.querySelectorAll("script,style").forEach(function(s){ s.remove(); }); return b.textContent; })();
          var rep={screen:active.id, errors:window.__errs,
            overflow:document.documentElement.scrollWidth>window.innerWidth,
            scrollW:document.documentElement.scrollWidth, vw:window.innerWidth,
            topbarVisible:!!tb&&!tb.classList.contains("hidden"),
            logo:lg?{src:lg.getAttribute("src"), ok:lg.complete&&lg.naturalWidth>0}:{missing:true},
            tabAnon:!!document.getElementById("tabAnon"), tabVerif:!!document.getElementById("tabVerif"),
            jugable:visTxt.indexOf("Jugable en")>=0,
            verificado:visTxt.indexOf("VERIFICADO")>=0,
            verificacionTxt:visTxt.indexOf("necesita internet")>=0,
            modeTags:document.querySelectorAll("#modesList .tag").length,
            menuBtns:document.querySelectorAll(".menu-btn").length,
            visibleSelects:(function(){ var n=0; document.querySelectorAll("select").forEach(function(s){ if(getComputedStyle(s).display!=="none") n++; }); return n; })(),
            avatars:document.querySelectorAll("#avatarGrid .avatar-btn").length,
            avatarGroups:Array.prototype.map.call(document.querySelectorAll(".avatar-group-label"), function(e){ return e.textContent; }),
            menuOpen:!!document.querySelector(".menu-panel"),
            chevGap:chevGap,
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

# Acciones y reporte extra por escenario (JS que corre dentro del timeout)
SCEN = {
 "home": ("", "homeAvatars:document.querySelectorAll('#avatarGrid .avatar-btn').length, profileBoxRadius:getComputedStyle(document.querySelector('.profile-box')).borderRadius"),
 "modes": ("""
   var mm=document.querySelector('#modesMaxPlayers');
   var mb=mm&&mm.nextElementSibling; if(mb) mb.click();
   var p=document.querySelector('.menu-panel'); var opts=p?p.querySelectorAll('.menu-opt'):[];
   var t=null; opts.forEach(function(o){ if(o.textContent.trim()==='8') t=o; }); if(t) t.click();
 """, "modesMaxLabel:(function(){ var b=document.querySelector('#modesMaxPlayers'); return b&&b.nextElementSibling?b.nextElementSibling.querySelector('.menu-lab').textContent:null; })(), modesSlots:document.querySelectorAll('#modesAvatarRow .avatar-slot').length"),
 "setup": ("""
   var np=document.querySelector('#numPlayers');
   var nb=np&&np.nextElementSibling; if(nb) nb.click();
   var p=document.querySelector('.menu-panel'); var opts=p?p.querySelectorAll('.menu-opt'):[];
   var t=null; opts.forEach(function(o){ if(o.textContent.trim()==='5 jugadores') t=o; }); if(t) t.click();
   var avSel=document.querySelector('#playersList .player-row select');
   var ab=avSel&&avSel.nextElementSibling; if(ab) ab.click();
   var ap=document.querySelector('.menu-panel.avatars'); var aopts=ap?ap.querySelectorAll('.menu-opt'):[];
   var h=null; aopts.forEach(function(o){ if(o.textContent==='\\uD83D\\uDC69\\uD83C\\uDFFC') h=o; }); if(h) h.click();
 """, "numPlayersValue:document.querySelector('#numPlayers').value, numRows:document.querySelectorAll('#playersList .player-row').length, numLabel:(function(){ var b=document.querySelector('#numPlayers'); return b&&b.nextElementSibling?b.nextElementSibling.querySelector('.menu-lab').textContent:null; })(), avatarValue:(function(){ var s=document.querySelector('#playersList .player-row select'); return s?s.value:null; })()"),
 "setup-menu": ("""
   var np=document.querySelector('#numPlayers');
   var nb=np&&np.nextElementSibling; if(nb) nb.click();
 """, "menuOpts:(function(){ var p=document.querySelector('.menu-panel'); return p?p.querySelectorAll('.menu-opt').length:0; })(), menuPanelRect:(function(){ var p=document.querySelector('.menu-panel'); if(!p) return null; var r=p.getBoundingClientRect(); return {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)}; })()"),
 "create": ("""
   if(window.syncWifiModeButtons) syncWifiModeButtons();
 """, "wifiModeLabel:(function(){ var b=document.querySelector('#wifiModeSelect'); return b&&b.nextElementSibling?b.nextElementSibling.querySelector('.menu-lab').textContent:null; })(), wifiModeOpts:document.querySelector('#wifiModeSelect').options.length"),
 "join": ("", "joinTopbar:!!document.querySelector('#topbar')&&!document.querySelector('#topbar').classList.contains('hidden')"),
}

SHOTS_360 = [("home", ""), ("modes", "#shot=modes"), ("setup", "#shot=setup"),
             ("setup-menu", "#shot=setup"), ("create", "#shot=create"), ("join", "#shot=join")]
SHOTS_320 = [("home", ""), ("setup", "#shot=setup"), ("modes", "#shot=modes")]

def run(name, hashfrag, w, h, folder):
    actions, report = SCEN[name]
    src = open(os.path.join(PROJ, "www", "index.html"), encoding="utf-8").read()
    js = AUDIT_JS.replace("SCENARIO_ACTIONS", actions).replace("SCENARIO_REPORT", report)
    # La copia va dentro de www/ para que las rutas relativas (assets/,
    # fonts/) resuelvan como en la app real; se borra al terminar.
    tmp = os.path.join(PROJ, "www", "__verify-%s-%dx%d.html" % (name, w, h))
    open(tmp, "w", encoding="utf-8").write(src.replace("</body>", js, 1))
    shot = os.path.join(OUT, folder, "shot-%s.png" % name)
    cmd = [HS, "--headless", "--disable-gpu", "--no-sandbox",
           "--window-size=%d,%d" % (w, h), "--hide-scrollbars",
           "--virtual-time-budget=8000", "--run-all-compositor-stages-before-draw",
           "--screenshot=%s" % shot, "--dump-dom", "file://%s%s" % (tmp, hashfrag)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    m = re.search(r"AUDIT (\{.*?\})</div>", p.stdout, re.S)
    if not m:
        return {"screen": name, "size": "%dx%d" % (w, h), "error": "sin AUDIT",
                "tail": (p.stdout[-300:] if p.stdout else p.stderr[-300:])}
    try:
        r = json.loads(m.group(1))
    except Exception as e:
        return {"screen": name, "size": "%dx%d" % (w, h), "error": "JSON malo: %s" % e}
    r["size"] = "%dx%d" % (w, h)
    r["shot"] = "shots-%s/shot-%s.png" % (folder.split("-")[1], name)
    return r

def main():
    os.makedirs(os.path.join(OUT, "shots-360"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "shots-320"), exist_ok=True)
    results = []
    for name, frag in SHOTS_360:
        print("360", name, "...", flush=True)
        results.append(run(name, frag, 360, 800, "shots-360"))
    for name, frag in SHOTS_320:
        print("320", name, "...", flush=True)
        results.append(run(name, frag, 320, 568, "shots-320"))
    with open(os.path.join(OUT, "reporte.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    # Limpieza: borrar las copias temporales de www/
    import glob
    for t in glob.glob(os.path.join(PROJ, "www", "__verify-*.html")):
        os.remove(t)
    for r in results:
        print(json.dumps(r, ensure_ascii=False))

if __name__ == "__main__":
    main()
