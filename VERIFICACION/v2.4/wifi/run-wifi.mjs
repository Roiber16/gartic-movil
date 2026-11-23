#!/usr/bin/env node
/* Simulador de wifi local para Gartic Móvil v2.4.
 *
 * Dos (o más) páginas reales de Chromium (headless, pilotadas por CDP)
 * juegan partidas completas por wifi simulado:
 * - Un servidor Node hace de "red local": sirve la app en varios puertos
 *   (cada página tiene su propio origen -> su propio localStorage, como
 *   dos teléfonos distintos) y reenvía las peticiones /api/* a la página
 *   del anfitrión, igual que el plugin LanServer (onRequest + sendResponse
 *   con espera, aquí con un sondeo del anfitrión cada 120 ms).
 * - Cada página lleva un bot inyectado que juega sus turnos (escribe,
 *   describe, dibuja con PointerEvents reales, elige palabra y adivina).
 *
 * Uso:
 *   node run-wifi.mjs normal|story|secret|animation|guess|dropout|host-leaves|kick|late-join|reconnect [all]
 * Sin dependencias (Node 24: WebSocket global). Chrome: el de Playwright.
 * Escribe el informe en wifi-resultados.json y las capturas en este dir.
 */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { spawn, execSync } from "node:child_process";

const PROJ = path.resolve(os.homedir(), "workspace/gartic-movil");
const OUT = path.resolve(PROJ, "VERIFICACION", "v2.4", "wifi");
fs.mkdirSync(OUT, { recursive: true });
const CHROME = path.join(os.homedir(), ".cache/ms-playwright/chromium-1161/chrome-linux/chrome");
const HOST_PORT = 18081;
const CLIENT_PORTS = [18082, 18083, 18084, 18085, 18086, 18087, 18088, 18089, 18090, 18091, 18092, 18093, 18094];
const CDP_PORT = 9222;
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".woff2": "font/woff2", ".json": "application/json", ".svg": "image/svg+xml" };

/* ---------------- servidor: archivos + red local simulada ---------------- */
let pending = []; // {id, method, path, body, res, timer}
let delivered = new Set();
let shared = { word: "", wordRound: "" };
let reqSeq = 0;
/* Ganchos de pruebas de red (correcciones ChatGPT, punto 1):
   - blackoutUntil: mientras dura, las peticiones /api/* devuelven 503
     (como si el hotspot se hubiera caído) y el anfitrión no ve nada.
   - dropNextSubmit: la próxima respuesta a /api/submit se pierde (el
     anfitrión sí la procesa, pero el cliente no recibe la respuesta). */
let blackoutUntil = 0;
let dropNextSubmit = false;

function cors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Origin, Content-Type, Accept, Authorization");
}
function serveFile(req, res) {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (p === "/") p = "/index.html";
  const file = path.join(PROJ, "www", p);
  if (!file.startsWith(path.join(PROJ, "www")) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    cors(res); res.writeHead(404); res.end("no");
    return;
  }
  cors(res);
  res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
}
function handleReq(req, res) {
  const u = new URL(req.url, "http://x");
  if (req.method === "OPTIONS") { cors(res); res.writeHead(204); res.end(); return; }
  if (u.pathname === "/ping") { cors(res); res.writeHead(200, { "Content-Type": "application/json" }); res.end(JSON.stringify({ ok: true })); return; }
  if (u.pathname === "/__lan/pending") {
    const list = pending.filter((p) => !delivered.has(p.id));
    list.forEach((p) => delivered.add(p.id));
    cors(res); res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(list.map((p) => ({ requestId: p.id, method: p.method, path: p.path, body: p.body }))));
    return;
  }
  if (u.pathname === "/__lan/respond" && req.method === "POST") {
    let b = "";
    req.on("data", (c) => (b += c));
    req.on("end", () => {
      try {
        const j = JSON.parse(b);
        const p = pending.find((x) => x.id === j.requestId);
        if (p) {
          if (dropNextSubmit && p.path === "/api/submit") {
            /* La respuesta de esta entrega se pierde: el anfitrión ya la
               procesó, pero el cliente no la recibe y reintenta; el
               anfitrión debe devolver already:true y no duplicar. */
            dropNextSubmit = false;
            clearTimeout(p.timer);
            pending = pending.filter((x) => x !== p);
            try { cors(p.res); p.res.writeHead(200, { "Content-Type": "application/json" }); p.res.end(JSON.stringify({ error: "timeout" })); } catch (e) {}
          } else {
            clearTimeout(p.timer); cors(p.res); p.res.writeHead(200, { "Content-Type": "application/json" }); p.res.end(j.body || "{}"); pending = pending.filter((x) => x !== p);
          }
        }
      } catch (e) {}
      cors(res); res.writeHead(200); res.end("ok");
    });
    return;
  }
  if (u.pathname === "/__test/share" && req.method === "POST") {
    let b = "";
    req.on("data", (c) => (b += c));
    req.on("end", () => { try { Object.assign(shared, JSON.parse(b)); } catch (e) {} cors(res); res.writeHead(200); res.end("ok"); });
    return;
  }
  if (u.pathname === "/__test/word") { cors(res); res.writeHead(200, { "Content-Type": "application/json" }); res.end(JSON.stringify(shared)); return; }
  if (u.pathname === "/__test/reset") { shared = { word: "", wordRound: "" }; cors(res); res.writeHead(200); res.end("ok"); return; }
  if (u.pathname === "/__test/blackout" && req.method === "POST") {
    let b = "";
    req.on("data", (c) => (b += c));
    req.on("end", () => { try { const j = JSON.parse(b); blackoutUntil = Date.now() + (j.ms || 5000); } catch (e) {} cors(res); res.writeHead(200); res.end("ok"); });
    return;
  }
  if (u.pathname === "/__test/dropNextSubmit" && req.method === "POST") {
    dropNextSubmit = true;
    cors(res); res.writeHead(200); res.end("ok"); return;
  }
  if (u.pathname.startsWith("/api/") && req.method === "POST") {
    if (Date.now() < blackoutUntil) {
      cors(res); res.writeHead(503, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "blackout" }));
      return;
    }
    let b = "";
    req.on("data", (c) => (b += c));
    req.on("end", () => {
      const id = "r" + ++reqSeq + "-" + Date.now().toString(36);
      const item = { id, method: req.method, path: u.pathname, body: b, res };
      item.timer = setTimeout(() => {
        pending = pending.filter((x) => x !== item);
        try { cors(res); res.writeHead(200, { "Content-Type": "application/json" }); res.end(JSON.stringify({ error: "timeout" })); } catch (e) {}
      }, 12000);
      pending.push(item);
    });
    return;
  }
  serveFile(req, res);
}
for (const port of [HOST_PORT, ...CLIENT_PORTS]) http.createServer(handleReq).listen(port, "127.0.0.1");

/* ---------------- bot inyectado en cada página ---------------- */
const BOT_SRC = `
window.__errors = [];
window.addEventListener("error", function(e){ window.__errors.push("JS: " + (e.message || e.error)); });
window.__botName = new URLSearchParams(location.search).get("p") || "Jugador";
window.__botOff = false;
window.__lanOrigin = "http://127.0.0.1:${HOST_PORT}";
if (location.search.indexOf("lan=host") >= 0) {
  /* Stub del plugin LanServer: connect + sondeo de peticiones pendientes. */
  window.Capacitor = { Plugins: { LanServer: {
    connect: function(){ return Promise.resolve({ ip: "127.0.0.1", port: ${HOST_PORT} }); },
    addListener: function(ev, fn){ window.__lanHandler = fn; },
    sendResponse: function(r){
      fetch(window.__lanOrigin + "/__lan/respond", { method: "POST", body: JSON.stringify(r) }).catch(function(){});
    }
  }}};
  setInterval(function(){
    fetch(window.__lanOrigin + "/__lan/pending").then(function(r){ return r.json(); }).then(function(list){
      (list || []).forEach(function(d){ if (window.__lanHandler) { try { window.__lanHandler(d); } catch(e){ window.__errors.push("hostRouter: " + e.message); } } });
    }).catch(function(){});
  }, 120);
}
window.__scribble = function(){
  var cv = document.querySelector("#drawCanvas");
  if (!cv) return false;
  var key = (document.querySelector("#turnLabel") || {}).textContent + "|" + (document.querySelector(".draw-top") || {}).textContent;
  if (window.__drewKey === key) return true;
  var r = cv.getBoundingClientRect();
  function pt(x, y, type){
    var e = new PointerEvent(type, { bubbles: true, cancelable: true, pointerId: 1, clientX: r.left + x * (r.width / 640), clientY: r.top + y * (r.height / 440), isPrimary: true });
    cv.dispatchEvent(e);
  }
  pt(90, 90, "pointerdown");
  for (var i = 1; i <= 24; i++) pt(90 + i * 16, 110 + Math.sin(i * 0.9) * 55, "pointermove");
  pt(480, 110, "pointerup");
  pt(150, 300, "pointerdown");
  for (var j = 1; j <= 12; j++) pt(150 + j * 20, 300 + Math.cos(j) * 30, "pointermove");
  pt(390, 300, "pointerup");
  window.__drewKey = key;
  return true;
};
window.__typeSlow = function(text, perMs){
  /* Escribe el texto letra a letra en #writeInput (como un jugador real
     que teclea despacio) para comprobar que ningún sondeo borra letras. */
  window.__typeSlowDone = false;
  var inp = document.querySelector("#writeInput");
  if (!inp) { window.__typeSlowDone = true; return false; }
  var i = 0;
  var iv = setInterval(function(){
    var cur = document.querySelector("#writeInput");
    if (!cur) { clearInterval(iv); window.__typeSlowDone = true; return; }
    cur.value = text.slice(0, ++i);
    cur.dispatchEvent(new Event("input", { bubbles: true }));
    if (i >= text.length) { clearInterval(iv); window.__typeSlowDone = true; }
  }, perMs || 300);
  return true;
};
window.__canvasInfo = function(){
  /* Longitud del dataURL del lienzo visible (dibujo o adivinanza) y si
     está en blanco: sirve para comprobar que el dibujo no se borró. */
  var cv = document.querySelector("#drawCanvas") || document.querySelector("#liveCanvas");
  if (!cv) return null;
  var url = cv.toDataURL("image/png");
  var blank = document.createElement("canvas"); blank.width = 640; blank.height = 440;
  var bctx = blank.getContext("2d"); bctx.fillStyle = "#ffffff"; bctx.fillRect(0, 0, 640, 440);
  var blankUrl = blank.toDataURL("image/png");
  return { len: url.length, blankLen: blankUrl.length, blank: url.length <= blankUrl.length + 200 };
};
window.__toolClick = function(label){
  var btns = document.querySelectorAll("#toolBar .tool-btn");
  for (var i = 0; i < btns.length; i++) if (btns[i].textContent.trim() === label) { btns[i].click(); return true; }
  return false;
};
window.__scribbleMany = function(n){
  /* Dibuja n trazos de pincel y, por el camino, usa todas las
     herramientas: línea, círculo, cuadrado, relleno, borrador, Deshacer,
     Rehacer y Limpiar. Para Adivina: el invitado debe ver lo mismo. */
  window.__scribbleManyDone = false;
  var cv = document.querySelector("#drawCanvas");
  if (!cv) { window.__scribbleManyDone = true; return false; }
  var r = cv.getBoundingClientRect();
  function pt(x, y, type){
    var e = new PointerEvent(type, { bubbles: true, cancelable: true, pointerId: 1, clientX: r.left + x * (r.width / 640), clientY: r.top + y * (r.height / 440), isPrimary: true });
    cv.dispatchEvent(e);
  }
  function stroke(x0, y0, x1, y1, steps){
    pt(x0, y0, "pointerdown");
    for (var i = 1; i <= steps; i++) pt(x0 + (x1 - x0) * i / steps, y0 + (y1 - y0) * i / steps, "pointermove");
    pt(x1, y1, "pointerup");
  }
  var done = 0;
  var total = n || 650;
  var third = Math.floor(total / 3);
  for (var k = 0; k < third; k++) { var y = 60 + (k % 12) * 28; stroke(60, y, 580, y + ((k % 2) ? 14 : -14), 4); done++; }
  window.__toolClick("Línea"); stroke(80, 380, 560, 80, 6);
  window.__toolClick("Círculo"); stroke(200, 200, 420, 320, 6);
  window.__toolClick("Cuadrado"); stroke(100, 100, 300, 300, 6);
  window.__toolClick("Cubo de relleno"); pt(320, 220, "pointerdown"); pt(320, 220, "pointerup");
  window.__toolClick("Borrador"); stroke(100, 350, 500, 350, 8);
  var undo = document.querySelector("#btnUndo"); if (undo) undo.click();
  var redo = document.querySelector("#btnRedo"); if (redo) redo.click();
  var clear = document.querySelector("#btnClear"); if (clear) clear.click();
  window.__toolClick("Pincel");
  for (var k2 = 0; k2 < total - third; k2++) { var y2 = 50 + (k2 % 14) * 26; stroke(50, y2, 590, y2 + ((k2 % 3) - 1) * 20, 4); done++; }
  window.__scribbleManyDone = true;
  window.__drawnStrokes = done; /* trazos de pincel dibujados en total */
  window.__strokeCount = (typeof S !== "undefined" && S.draw) ? S.draw.strokes.length : -1;
  return true;
};
window.__bot = function(){
  if (window.__botOff) return { screen: (document.querySelector(".screen.active") || {}).id || "", off: true };
  var scr = (document.querySelector(".screen.active") || {}).id || "";
  var st = { screen: scr, name: window.__botName };
  try {
    if (scr === "screen-pass") { var g = document.querySelector("#btnGotIt"); if (g) g.click(); st.acted = "gotit"; }
    else if (scr === "screen-play") {
      var w = document.querySelector("#writeInput");
      var d = document.querySelector("#descInput");
      var cv = document.querySelector("#drawCanvas");
      if (w) {
        if (window.__botHoldWrite) { st.acted = "hold-write"; }
        else { w.value = "Un " + window.__botName + " bailando en la playa con sombrero"; w.dispatchEvent(new Event("input", { bubbles: true })); var b = document.querySelector("#btnSendWrite"); if (b) b.click(); st.acted = "write"; }
      }
      else if (d) { d.value = "Un dibujo de " + window.__botName + " en la playa"; d.dispatchEvent(new Event("input", { bubbles: true })); var b2 = document.querySelector("#btnSendDesc"); if (b2) b2.click(); st.acted = "describe"; }
      else if (cv) {
        if (window.__botHoldDraw) { st.acted = "hold-draw"; }
        else { window.__scribble(); var b3 = document.querySelector("#btnSendDraw"); if (b3 && window.__drewKey) { b3.click(); st.acted = "draw"; } }
      }
      st.turn = (document.querySelector("#turnLabel") || {}).textContent || "";
      st.timer = (document.querySelector("#timerPill") || {}).textContent || "";
    }
    else if (scr === "screen-guess") {
      var pick = document.querySelector(".word-pick button");
      if (pick) {
        var word = pick.textContent.trim().toLowerCase();
        fetch(window.__lanOrigin + "/__test/share", { method: "POST", body: JSON.stringify({ word: word, wordRound: (document.querySelector("#guessRoundLabel") || {}).textContent || "" }) }).catch(function(){});
        pick.click(); st.acted = "choose:" + word;
      } else if (document.querySelector("#guessDrawHost #drawCanvas")) {
        window.__scribble();
        var bd = document.querySelector("#btnSendDraw");
        if (!window.__drawEndAt) window.__drawEndAt = Date.now() + 4000;
        if (bd && window.__drewKey && Date.now() > window.__drawEndAt) { bd.click(); st.acted = "draw-end"; window.__drawEndAt = 0; }
      } else if (document.querySelector("#guessInput")) {
        st.acted = "guessing";
        st.guessRound = (document.querySelector("#guessRoundLabel") || {}).textContent || "";
        st.hint = (document.querySelector("#guessHintBar") || {}).textContent || "";
      }
    }
    else if (scr === "screen-wait") { st.wait = (document.querySelector("#waitText") || {}).textContent || ""; }
    else if (scr === "screen-album") { st.album = true; st.albumTitle = (document.querySelector("#albumTitle") || {}).textContent || ""; }
    else if (scr === "screen-podium") { st.podium = true; }
  } catch (e) { st.botError = String(e && e.message || e); }
  return st;
};
window.__state = function(){
  var s = { screen: (document.querySelector(".screen.active") || {}).id || "" };
  try { s.hostActive = typeof HOST !== "undefined" ? HOST.active : null; } catch (e) {}
  try { s.hostStarted = typeof HOST !== "undefined" ? HOST.started : null; } catch (e) {}
  try { s.hostPlayers = (typeof HOST !== "undefined" && HOST.players) ? HOST.players.map(function(p){ return p.name; }) : null; } catch (e) {}
  try { s.engineStep = (typeof S !== "undefined" && S.engine) ? S.engine.step : null; s.engineFinished = (typeof S !== "undefined" && S.engine) ? S.engine.finished : null; } catch (e) {}
  try { s.albums = (typeof S !== "undefined" && S.engine && S.engine.finished) ? S.engine.albums().map(function(a){ return a.links.length; }) : null; } catch (e) {}
  try { s.mode = (typeof S !== "undefined") ? S.mode : null; } catch (e) {}
  try { s.waitText = (document.querySelector("#waitText") || {}).textContent || ""; } catch (e) {}
  try { s.joinStatus = (document.querySelector("#joinStatus") || {}).textContent || ""; } catch (e) {}
  try { s.joinMsg = (document.querySelector("#joinMsg") || {}).textContent || ""; } catch (e) {}
  try { s.wifiStatus = (document.querySelector("#wifiStatus") || {}).textContent || ""; } catch (e) {}
  try { s.roomCode = (document.querySelector("#roomCode") || {}).textContent || ""; } catch (e) {}
  try { s.hostAddr = (document.querySelector("#hostAddr") || {}).textContent || ""; } catch (e) {}
  try { s.passText = (document.querySelector("#passText") || {}).textContent || ""; } catch (e) {}
  try { s.guessPhase = (typeof HOST !== "undefined" && HOST.guess) ? HOST.guess.phase : null; } catch (e) {}
  try { s.guessRound = (typeof HOST !== "undefined" && HOST.guess) ? HOST.guess.round : null; } catch (e) {}
  s.errors = window.__errors || [];
  return s;
};
`;

/* ---------------- cliente CDP (sin dependencias) ---------------- */
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
class CDP {
  constructor(wsUrl) { this.ws = new WebSocket(wsUrl); this.id = 0; this.pend = new Map(); this.events = []; this.ready = new Promise((res, rej) => { this.ws.onopen = res; this.ws.onerror = rej; }); this.ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && this.pend.has(d.id)) { const { res, rej, timer } = this.pend.get(d.id); clearTimeout(timer); this.pend.delete(d.id); d.error ? rej(new Error(JSON.stringify(d.error))) : res(d.result); } else if (d.method) { this.events.push(d); } }; }
  /* Toda llamada CDP tiene timeout (30 s): si Chrome no responde, la
     promesa rechaza en vez de dejar el escenario colgado para siempre
     (pasó con story en la pasada completa: el juego terminó en las 4
     páginas pero una llamada no resolvió nunca). */
  async call(method, params = {}) { await this.ready; const id = ++this.id; return new Promise((res, rej) => { const timer = setTimeout(() => { if (this.pend.has(id)) { this.pend.delete(id); rej(new Error("CDP timeout: " + method)); } }, 30000); this.pend.set(id, { res, rej, timer }); this.ws.send(JSON.stringify({ id, method, params })); }); }
  async eval(expr) { const r = await this.call("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw new Error("eval: " + JSON.stringify(r.exceptionDetails).slice(0, 500)); return r.result ? r.result.value : undefined; }
  async shot(file) { const r = await this.call("Page.captureScreenshot", { format: "png" }); fs.writeFileSync(file, Buffer.from(r.data, "base64")); }
  errors() { const out = []; for (const e of this.events) { if (e.method === "Runtime.exceptionThrown") out.push("EXC: " + JSON.stringify(e.params.exceptionDetails).slice(0, 400)); if (e.method === "Runtime.consoleAPICalled" && e.params.type === "error") out.push("CONSOLE: " + e.params.args.map((a) => a.value || a.description || "").join(" ").slice(0, 300)); } return out; }
}
async function cdpJson(path, method = "GET") {
  const r = await fetch(`http://127.0.0.1:${CDP_PORT}${path}`, { method, signal: AbortSignal.timeout(15000) });
  return r.json();
}
let chromeProc = null;
async function startChrome() {
  try { await cdpJson("/json/version"); return; } catch (e) {}
  chromeProc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${CDP_PORT}`, "--no-sandbox", "--disable-gpu", "--window-size=400,850", "--user-data-dir=/tmp/gartic-wifi-test",
    // Sin esto, Chrome estrangula los temporizadores de las pestañas en
    // segundo plano (sondeo de 1 s, temporizador de turno, vigilante) y
    // la simulación se arrastra: en los teléfonos reales cada jugador
    // mira su propia pantalla, así que nada de esto se estrangula.
    "--disable-background-timer-throttling", "--disable-backgrounding-occluded-windows", "--disable-renderer-backgrounding",
    "about:blank"], { stdio: "ignore" });
  for (let i = 0; i < 40; i++) { await sleep(500); try { await cdpJson("/json/version"); return; } catch (e) {} }
  throw new Error("Chrome no arrancó");
}
async function newPage(url) {
  let t;
  try { t = await cdpJson(`/json/new?${encodeURIComponent(url)}`, "PUT"); } catch (e) { t = await cdpJson(`/json/new?${encodeURIComponent(url)}`); }
  const c = new CDP(t.webSocketDebuggerUrl);
  c._targetId = t.id;
  await c.call("Page.enable"); await c.call("Runtime.enable");
  await c.call("Page.addScriptToEvaluateOnNewDocument", { source: BOT_SRC });
  await c.call("Page.navigate", { url });
  await sleep(2500);
  await c.eval(`(function(){ var s=document.querySelector("#splash"); if(s) s.style.display="none"; return true; })()`).catch(() => {});
  return c;
}

/* ---------------- orquestación ---------------- */
const NAMES = ["Roi", "Ana", "Beto", "Carla", "Dan", "Eva", "Félix", "Greta", "Hugo", "Iris", "José", "Karla", "Leo", "Marta"];
async function setNick(page, name) {
  await page.eval(`(function(){ var n=document.querySelector("#nick"); if(n){ n.value=${JSON.stringify(name)}; n.dispatchEvent(new Event("input",{bubbles:true})); } return !!n; })()`);
}
async function hostSetup(page, mode, maxPlayers) {
  await setNick(page, NAMES[0]);
  await page.eval(`document.querySelector("#btnCreateWifi").click()`);
  for (let i = 0; i < 30; i++) { await sleep(500); const s = await page.eval("window.__state()"); if (s.wifiStatus && s.wifiStatus.indexOf("Sala lista") >= 0) return s; }
  throw new Error("la sala no llegó a estar lista: " + JSON.stringify(await page.eval("window.__state()")));
}
async function joinClient(page, name, code) {
  await setNick(page, name);
  await page.eval(`document.querySelector("#btnJoinWifi").click()`);
  await sleep(400);
  await page.eval(`(function(){ document.querySelector("#joinIp").value="127.0.0.1:${HOST_PORT}"; document.querySelector("#joinCode").value=${JSON.stringify(code)}; })()`);
  await page.eval(`document.querySelector("#btnDoJoin").click()`);
  for (let i = 0; i < 30; i++) { await sleep(500); const s = await page.eval("window.__state()"); if (s.joinStatus && (s.joinStatus.indexOf("En la sala") >= 0 || s.joinStatus.indexOf("Volviste a la sala") >= 0 || s.joinStatus.indexOf("La partida empezó") >= 0)) return s; if (s.screen === "screen-play" || s.screen === "screen-wait") return s; if (s.joinMsg && s.joinMsg.indexOf("No se pudo") >= 0) throw new Error("join falló: " + s.joinMsg); }
  throw new Error("el cliente no entró a la sala: " + JSON.stringify(await page.eval("window.__state()")));
}
async function botLoop(pages, until, timeoutMs, onTick) {
  const t0 = Date.now();
  let lastGuessWord = "";
  while (Date.now() - t0 < timeoutMs) {
    for (const p of pages) { try { await p.eval("window.__bot()"); } catch (e) {} }
    // El bot adivinador: si hay palabra compartida y un input de adivinar, la escribe.
    try {
      const w = await (await fetch(`http://127.0.0.1:${HOST_PORT}/__test/word`, { signal: AbortSignal.timeout(10000) })).json();
      if (w.word && w.word !== lastGuessWord) {
        for (const p of pages) {
          await p.eval(`(function(){ var inp=document.querySelector("#guessInput"); if(!inp || inp.dataset.guessed) return false; inp.value=${JSON.stringify(w.word)}; inp.dataset.guessed="1"; var b=document.querySelector("#btnSendGuess"); if(b) b.click(); return true; })()`);
        }
        lastGuessWord = w.word;
      }
    } catch (e) {}
    if (onTick) await onTick();
    const done = await until();
    if (done) return { ok: true, ms: Date.now() - t0 };
    await sleep(600);
  }
  return { ok: false, ms: Date.now() - t0 };
}
async function allAlbums(pages) {
  const states = [];
  for (const p of pages) states.push(await p.eval("window.__state()"));
  return states.every((s) => s.screen === "screen-album" && s.albums && s.albums.every((n) => n > 0));
}
async function allPodium(pages) {
  const states = [];
  for (const p of pages) states.push(await p.eval("window.__state()"));
  return states.every((s) => s.screen === "screen-podium");
}
function collectErrors(pages) {
  const out = [];
  pages.forEach((p, i) => { for (const e of p.errors()) out.push(`[${NAMES[i]}] ${e}`); });
  return out;
}
async function checkAuthorship(hostPage, n) {
  // Invariante del reparto: cada jugador hace exactamente un eslabón por
  // paso (total = nº de pasos). Si los pasos no superan a los jugadores,
  // además cada álbum es una permutación (sin autores repetidos).
  const alb = await hostPage.eval(`(function(){ var e=(typeof HOST!=="undefined"&&HOST.engine)?HOST.engine:null; if(!e||!e.finished) return null; return e.albums().map(function(a){ return a.links.map(function(l){ return l.author; }); }); })()`);
  if (!alb) return "sin álbum en el anfitrión";
  const steps = alb[0].length;
  const counts = new Array(n).fill(0);
  let permOk = true;
  alb.forEach((authors) => {
    if (authors.length <= n && new Set(authors).size !== authors.length) permOk = false;
    authors.forEach((a) => counts[a]++);
  });
  const countsOk = counts.every((c) => c === steps);
  return `autoría por álbum: ${JSON.stringify(alb)}; eslabones por jugador: ${JSON.stringify(counts)} (esperado ${steps}); permutación OK=${permOk}; reparto OK=${countsOk}`;
}
async function shotAll(pages, tag) {
  for (let i = 0; i < pages.length; i++) { try { await pages[i].shot(path.join(OUT, `${tag}-${NAMES[i].toLowerCase()}.png`)); } catch (e) {} }
}

/* ---------------- escenarios ---------------- */
async function scenarioNormal() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, "normal", 4);
  log.push(`sala creada: código ${st.roomCode}, ${st.hostAddr}`);
  const clients = [];
  for (let i = 1; i < 4; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); log.push(`${NAMES[i]} se unió`); }
  await sleep(1000);
  const hs = await host.eval("window.__state()");
  log.push(`lobby anfitrión: ${JSON.stringify(hs.hostPlayers)}`);
  await shotAll([host, ...clients], "normal-lobby");
  // Modo Normal (por defecto) y 4 jugadores máx.
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  await sleep(500);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(1500);
  const afterStart = await host.eval("window.__state()");
  log.push(`tras EMPEZAR, pantalla anfitrión: ${afterStart.screen}, passText: ${JSON.stringify(afterStart.passText)}`);
  await shotAll([host, ...clients], "normal-tras-empezar");
  const r = await botLoop([host, ...clients], () => allAlbums([host, ...clients]), 180000, async () => {
    const s = await host.eval("window.__state()");
    if (s.screen === "screen-pass") log.push(`PASAJE anfitrión: ${JSON.stringify(s.passText)}`);
  });
  await shotAll([host, ...clients], "normal-album");
  const finals = [];
  for (const p of [host, ...clients]) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes por página: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors([host, ...clients]))}`);
  return { name: "normal", ok: r.ok, ms: r.ms, log, finals };
}
async function scenarioMode(modeId) {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, modeId, 4);
  const clients = [];
  for (let i = 1; i < 4; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); var m=document.querySelector("#wifiModeSelect"); m.value=${JSON.stringify(modeId)}; m.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  await sleep(500);
  const hs = await host.eval("window.__state()");
  log.push(`modo en sala: ${hs.mode}, jugadores: ${JSON.stringify(hs.hostPlayers)}`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(1200);
  await shotAll([host, ...clients], `${modeId}-juego`);
  const r = await botLoop([host, ...clients], () => allAlbums([host, ...clients]), 180000);
  await shotAll([host, ...clients], `${modeId}-album`);
  const finals = [];
  for (const p of [host, ...clients]) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors([host, ...clients]))}`);
  return { name: modeId, ok: r.ok, ms: r.ms, log, finals };
}
async function scenarioGuess() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, "guess", 4);
  const clients = [];
  for (let i = 1; i < 4; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); document.querySelector("#wifiModeGuess").click(); })()`);
  await sleep(500);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(2500);
  // ¿El dibujante llegó a ver las opciones? (bug autoChoose: se elige sola en ~1 s)
  const drawerState = await host.eval(`(function(){ return { pick: !!document.querySelector(".word-pick button"), phase: (typeof HOST!=="undefined"&&HOST.guess)?HOST.guess.phase:null, word: (typeof HOST!=="undefined"&&HOST.guess)?HOST.guess.word:null }; })()`);
  log.push(`a los 2,5 s de empezar: dibujante ve opciones=${drawerState.pick}, fase=${drawerState.phase}, palabra=${JSON.stringify(drawerState.word)}`);
  await shotAll([host, ...clients], "guess-inicio");
  const r = await botLoop([host, ...clients], () => allPodium([host, ...clients]), 240000);
  await shotAll([host, ...clients], "guess-podio");
  const finals = [];
  for (const p of [host, ...clients]) finals.push(await p.eval("window.__state()"));
  log.push(`pantallas finales: ${JSON.stringify(finals.map((f) => f.screen))}`);
  log.push(`errores: ${JSON.stringify(collectErrors([host, ...clients]))}`);
  return { name: "guess", ok: r.ok, ms: r.ms, log, finals };
}
async function hostSetRapido(page) {
  // Tiempos rápidos (30/45/30) para que los escenarios de espera no tarden
  // 5 minutos: el vigilante salta al caído tras tiempo de turno + 20 s.
  await page.eval(`document.querySelector("#btnModes").click()`);
  await sleep(400);
  await page.eval(`(function(){ var s=document.querySelector("#customTime"); s.value="rapido"; s.dispatchEvent(new Event("change",{bubbles:true})); document.querySelector("#btnModesBack").click(); })()`);
  await sleep(400);
}
async function scenarioDropout() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  await hostSetRapido(host);
  const st = await hostSetup(host, "normal", 4);
  const clients = [];
  for (let i = 1; i < 4; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(6000);
  log.push("Beto (cliente 2) se cae a mitad de partida: se cierra su página");
  await cdpJson(`/json/close/${clients[1]._targetId || ""}`).catch(() => {});
  try { clients[1].ws.close(); } catch (e) {}
  clients.splice(1, 1); // los demás siguen
  let lastProbe = "";
  const r = await botLoop([host, ...clients], () => allAlbums([host, ...clients]), 360000, async () => {
    const probe = await host.eval(`(function(){ var e=(typeof HOST!=="undefined"&&HOST.engine)?HOST.engine:null; if(!e) return "sin-motor"; return "paso "+e.step+" eslabones ["+e.chains.map(function(c){return c.links.length;}).join(",")+"] saltados ["+(HOST.skippedThisStep||[]).join(",")+"] vigilante "+(HOST.watchdog?"on":"OFF")+" edad "+Math.round((Date.now()-HOST.stepStartedAt)/1000)+"s"; })()`);
    if (probe !== lastProbe) { lastProbe = probe; log.push("sonda: " + probe); }
  });
  await shotAll([host, ...clients], "dropout-album");
  const finals = [];
  for (const p of [host, ...clients]) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes tras la caída: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors([host, ...clients]))}`);
  return { name: "dropout", ok: r.ok, ms: r.ms, log, finals };
}
async function scenarioHostLeaves() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, "normal", 4);
  const clients = [];
  for (let i = 1; i < 4; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(8000);
  log.push("El anfitrión abandona la partida (Salir -> Sí)");
  await host.eval(`(function(){ if(typeof leaveGame==="function"){ leaveGame(); return "leaveGame"; } return "no-fn"; })()`);
  await sleep(3000);
  const after = [];
  for (const c of clients) after.push(await c.eval("window.__state()"));
  log.push(`clientes tras la salida del anfitrión: ${JSON.stringify(after.map((a) => ({ screen: a.screen, wait: a.waitText })))}`);
  await shotAll(clients, "host-leaves-cliente");
  const sawMsg = after.every((a) => a.screen === "screen-wait" && /anfitri.*cerró/i.test(a.waitText || ""));
  return { name: "host-leaves", ok: sawMsg, ms: 0, log, finals: after };
}
async function scenarioKick() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, "normal", 4);
  const c1 = await newPage(`http://127.0.0.1:${CLIENT_PORTS[0]}/?p=Ana`);
  await joinClient(c1, "Ana", st.roomCode);
  // Segundo cliente con el mismo nombre
  const c2 = await newPage(`http://127.0.0.1:${CLIENT_PORTS[1]}/?p=Ana`);
  await joinClient(c2, "Ana", st.roomCode);
  await sleep(800);
  let hs = await host.eval("window.__state()");
  log.push(`dos "Ana" en la sala: ${JSON.stringify(hs.hostPlayers)}`);
  // El anfitrión expulsa a la segunda Ana
  const kicked = await host.eval(`(function(){ var b=document.querySelectorAll("[data-kick]"); if(b.length<2) return "sin-boton"; b[b.length-1].click(); return "ok"; })()`);
  log.push(`expulsar: ${kicked}`);
  await sleep(500);
  hs = await host.eval("window.__state()");
  log.push(`tras expulsar: ${JSON.stringify(hs.hostPlayers)}`);
  // La expulsada intenta volver con el mismo nombre
  const rejoin = await c2.eval(`(function(){ return document.querySelector("#joinMsg") ? document.querySelector("#joinMsg").textContent : ""; })()`);
  await c2.eval(`document.querySelector("#btnDoJoin").click()`);
  await sleep(2500);
  const rs = await c2.eval("window.__state()");
  log.push(`reintento de la expulsada: joinMsg=${JSON.stringify(rs.joinMsg)}, joinStatus=${JSON.stringify(rs.joinStatus)}`);
  const stillOut = !(rs.joinStatus || "").includes("En la sala");
  log.push(`errores: ${JSON.stringify(collectErrors([host, c1, c2]))}`);
  return { name: "kick", ok: stillOut && hs.hostPlayers.filter((n) => n === "Ana").length === 1, ms: 0, log, finals: [hs, rs] };
}
async function scenarioLateJoin() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, "normal", 4);
  const clients = [];
  for (let i = 1; i < 3; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(3000);
  const late = await newPage(`http://127.0.0.1:${CLIENT_PORTS[2]}/?p=Dan`);
  await setNick(late, "Dan");
  await late.eval(`document.querySelector("#btnJoinWifi").click()`);
  await sleep(400);
  await late.eval(`(function(){ document.querySelector("#joinIp").value="127.0.0.1:${HOST_PORT}"; document.querySelector("#joinCode").value=${JSON.stringify(st.roomCode)}; })()`);
  await late.eval(`document.querySelector("#btnDoJoin").click()`);
  await sleep(3000);
  const ls = await late.eval("window.__state()");
  log.push(`llegada tardía: joinMsg=${JSON.stringify(ls.joinMsg)}, joinStatus=${JSON.stringify(ls.joinStatus)}`);
  const rejected = !(ls.joinStatus || "").includes("En la sala");
  return { name: "late-join", ok: rejected, ms: 0, log, finals: [ls] };
}
async function scenarioReconnect() {
  const log = [];
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
  const st = await hostSetup(host, "normal", 4);
  const clients = [];
  for (let i = 1; i < 4; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="4"; s.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(6000);
  log.push("Ana pierde la conexión 10 s (se cierra su página) y vuelve a unirse con el mismo código");
  const anaTarget = clients[0];
  try { await cdpJson(`/json/close/${anaTarget._targetId}`); } catch (e) {}
  try { anaTarget.ws.close(); } catch (e) {}
  clients.splice(0, 1);
  await sleep(10000);
  const ana2 = await newPage(`http://127.0.0.1:${CLIENT_PORTS[0]}/?p=Ana`);
  try { await joinClient(ana2, "Ana", st.roomCode); log.push("Ana volvió a entrar a la sala"); } catch (e) { log.push("Ana NO pudo volver: " + e.message); return { name: "reconnect", ok: false, ms: 0, log, finals: [] }; }
  clients.unshift(ana2);
  const r = await botLoop([host, ...clients], () => allAlbums([host, ...clients]), 240000);
  const finals = [];
  for (const p of [host, ...clients]) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes tras reconectar: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(`errores: ${JSON.stringify(collectErrors([host, ...clients]))}`);
  return { name: "reconnect", ok: r.ok, ms: r.ms, log, finals };
}

/* ---------------- escenarios nuevos (correcciones ChatGPT, puntos 1-5) ---------------- */
/* Muestrea el reloj y la pantalla de una página durante N ms. */
async function sampleTurn(page, ms, everyMs) {
  const samples = [];
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const s = await page.eval(`(function(){
      var w=document.querySelector("#writeInput"), d=document.querySelector("#descInput");
      return { t:(typeof S!=="undefined"?S.timeLeft:null),
        screen:(document.querySelector(".screen.active")||{}).id||"",
        value:(w?w.value:(d?d.value:"")),
        canvas:(window.__canvasInfo?window.__canvasInfo():null),
        offline:(typeof S!=="undefined"&&S.net)?S.net.offlineSince:0 };
    })()`).catch(() => null);
    if (s) samples.push(s);
    await sleep(everyMs || 500);
  }
  return samples;
}
/* El reloj del cliente no debe volver a subir (reiniciarse) mientras el
   anfitrión no cambia de paso: cada muestra debe ser <= la primera + 1. */
function timerMonotonic(samples) {
  const ts = samples.map((s) => s.t).filter((t) => typeof t === "number");
  if (ts.length < 2) return { ok: false, why: "sin muestras de reloj" };
  const first = ts[0], last = ts[ts.length - 1];
  const max = Math.max.apply(null, ts);
  if (max > first + 1) return { ok: false, why: `el reloj subió de ${first} a ${max} (se reinició)` };
  if (last > first - 3) return { ok: false, why: `el reloj apenas bajó: ${first} -> ${last}` };
  return { ok: true, first, last };
}
async function waitForTurn(page, timeoutMs) {
  const t0 = Date.now();
  while (Date.now() - t0 < (timeoutMs || 30000)) {
    const s = await page.eval(`(function(){
      var scr=(document.querySelector(".screen.active")||{}).id||"";
      return { screen:scr, write:!!document.querySelector("#writeInput"), draw:!!document.querySelector("#drawCanvas"), desc:!!document.querySelector("#descInput") };
    })()`).catch(() => null);
    if (s && s.screen === "screen-play" && (s.write || s.draw || s.desc)) return s;
    await sleep(500);
  }
  return null;
}
async function setupRoom(n, modeId) {
  const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=${NAMES[0]}`);
  const st = await hostSetup(host, modeId || "normal", n);
  const clients = [];
  for (let i = 1; i < n; i++) {
    const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`);
    await joinClient(c, NAMES[i], st.roomCode);
    clients.push(c);
  }
  await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value=${JSON.stringify(String(n))}; s.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  if (modeId && modeId !== "normal") {
    await host.eval(`(function(){ var m=document.querySelector("#wifiModeSelect"); m.value=${JSON.stringify(modeId)}; m.dispatchEvent(new Event("change",{bubbles:true})); })()`);
  }
  await sleep(500);
  return { host, clients, code: st.roomCode };
}
async function scenarioWrite12() {
  const log = [];
  const { host, clients } = await setupRoom(4, "normal");
  const ana = clients[0];
  await ana.eval(`window.__botHoldWrite = true;`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  const turn = await waitForTurn(ana, 30000);
  if (!turn || !turn.write) { log.push("Ana no llegó a su turno de escribir: " + JSON.stringify(turn)); return { name: "write-12s", ok: false, ms: 0, log, finals: [] }; }
  const text = "Un elefante rosa tocando la trompeta en la playa";
  log.push("Ana teclea 12 s sin pulsar Hecho (un sondeo cada ~1 s)");
  await ana.eval(`window.__typeSlow(${JSON.stringify(text)}, 200);`);
  const samples = await sampleTurn(ana, 12000, 500);
  const fin = await ana.eval(`(function(){ var w=document.querySelector("#writeInput"); return { value:w?w.value:"", screen:(document.querySelector(".screen.active")||{}).id||"", done:!!window.__typeSlowDone }; })()`);
  const mono = timerMonotonic(samples);
  const textOk = fin.value === text;
  const valGrowth = samples.every((s, i) => i === 0 || s.value.length >= samples[i - 1].value.length);
  log.push(`texto final: ${JSON.stringify(fin.value)} (completo=${textOk}, creció sin perder letras=${valGrowth}, tecleo terminado=${fin.done})`);
  log.push(`reloj: ${mono.ok ? "monótono " + mono.first + " -> " + mono.last : "FALLO: " + mono.why}`);
  log.push(`pantalla al final: ${fin.screen}`);
  await ana.eval(`window.__botHoldWrite = false;`);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allAlbums(pages), 180000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  return { name: "write-12s", ok: textOk && valGrowth && mono.ok && r.ok, ms: r.ms, log, finals };
}
async function scenarioDraw12() {
  const log = [];
  const { host, clients } = await setupRoom(4, "normal");
  const ana = clients[0];
  await ana.eval(`window.__botHoldDraw = true;`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  // Esperar al paso de dibujo (paso 1): el paso 0 es escribir. Durante la
  // espera hay que jugar (si no, nadie entrega el paso 0 y no se avanza).
  let turn = null;
  const pages0 = [host, ...clients];
  for (let i = 0; i < 40; i++) {
    for (const p of pages0) { try { await p.eval("window.__bot()"); } catch (e) {} }
    await sleep(500);
    const hs = await host.eval("window.__state()");
    const as = await ana.eval(`(function(){ return { screen:(document.querySelector(".screen.active")||{}).id||"", draw:!!document.querySelector("#drawCanvas") }; })()`);
    if (hs.engineStep >= 1 && as.screen === "screen-play" && as.draw) { turn = as; break; }
  }
  if (!turn) { log.push("Ana no llegó a su turno de dibujo"); return { name: "draw-12s", ok: false, ms: 0, log, finals: [] }; }
  log.push("Ana dibuja 12 s con Deshacer en medio, sin pulsar Hecho");
  await ana.eval(`window.__scribble();`);
  await sleep(1000);
  const afterUndo = await ana.eval(`(function(){ document.querySelector("#btnUndo").click(); return window.__canvasInfo(); })()`);
  log.push(`tras Deshacer: en blanco=${afterUndo.blank} (el primer trazo debe seguir: len ${afterUndo.len} vs blanco ${afterUndo.blankLen})`);
  await ana.eval(`window.__drewKey=null; window.__scribble();`);
  const samples = await sampleTurn(ana, 12000, 500);
  const mono = timerMonotonic(samples);
  const ci = await ana.eval(`window.__canvasInfo()`);
  log.push(`lienzo tras 12 s: en blanco=${ci.blank} (len ${ci.len} vs blanco ${ci.blankLen})`);
  log.push(`reloj: ${mono.ok ? "monótono " + mono.first + " -> " + mono.last : "FALLO: " + mono.why}`);
  await ana.eval(`window.__botHoldDraw = false;`);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allAlbums(pages), 180000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  return { name: "draw-12s", ok: !afterUndo.blank && !ci.blank && mono.ok && r.ok, ms: r.ms, log, finals };
}
async function scenarioNetcut() {
  const log = [];
  const { host, clients } = await setupRoom(4, "normal");
  const ana = clients[0];
  await ana.eval(`window.__botHoldWrite = true;`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  const turn = await waitForTurn(ana, 30000);
  if (!turn || !turn.write) { log.push("Ana no llegó a su turno de escribir"); return { name: "netcut-5s", ok: false, ms: 0, log, finals: [] }; }
  const text = "Un barco pirata navegando entre nubes";
  await ana.eval(`window.__typeSlow(${JSON.stringify(text)}, 250);`);
  await sleep(3000);
  log.push("Corte de red de 5 s a mitad del turno de Ana");
  await fetch(`http://127.0.0.1:${HOST_PORT}/__test/blackout`, { method: "POST", body: JSON.stringify({ ms: 5000 }) });
  const samples = await sampleTurn(ana, 6000, 500);
  const during = samples.filter((s) => s.offline > 0);
  const screenOk = samples.every((s) => s.screen === "screen-play");
  // Esperar a que el tecleo termine antes de comprobar el texto.
  for (let i = 0; i < 20; i++) {
    const d = await ana.eval(`!!window.__typeSlowDone`).catch(() => true);
    if (d) break;
    await sleep(500);
  }
  const fin = await ana.eval(`(function(){ var w=document.querySelector("#writeInput"); return { value:w?w.value:"", screen:(document.querySelector(".screen.active")||{}).id||"" }; })()`);
  const textOk = fin.value === text;
  log.push(`durante el corte: muestras sin conexión=${during.length}/${samples.length}, pantalla siempre en el turno=${screenOk}, texto intacto=${textOk}`);
  await sleep(3000);
  const rec = await ana.eval(`(function(){ return { offline:(typeof S!=="undefined"&&S.net)?S.net.offlineSince:0, screen:(document.querySelector(".screen.active")||{}).id||"" }; })()`);
  log.push(`tras el corte: offlineSince=${rec.offline} (0 = recuperado), pantalla=${rec.screen}`);
  await ana.eval(`window.__botHoldWrite = false;`);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allAlbums(pages), 180000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes tras el corte: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  return { name: "netcut-5s", ok: screenOk && textOk && during.length >= 2 && rec.offline === 0 && r.ok, ms: r.ms, log, finals };
}
async function scenarioLostSubmit() {
  const log = [];
  const { host, clients } = await setupRoom(4, "normal");
  await fetch(`http://127.0.0.1:${HOST_PORT}/__test/dropNextSubmit`, { method: "POST" });
  log.push("Armado: la primera respuesta de entrega se perderá (el anfitrión sí la procesa)");
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allAlbums(pages), 180000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes: ${JSON.stringify(finals.map((f) => f.albums))}`);
  const auth = await checkAuthorship(host, 4);
  log.push(auth);
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  const ok = r.ok && auth.indexOf("permutación OK=true") >= 0 && auth.indexOf("reparto OK=true") >= 0;
  return { name: "lost-submit", ok, ms: r.ms, log, finals };
}
async function scenarioCloseRoom() {
  const log = [];
  const { host, clients } = await setupRoom(4, "normal");
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(6000);
  log.push("El anfitrión cierra la sala a mitad de partida");
  await host.eval(`(function(){ if(typeof leaveGame==="function"){ leaveGame(); return "leaveGame"; } return "no-fn"; })()`);
  await sleep(3000);
  const after = [];
  for (const c of clients) after.push(await c.eval("window.__state()"));
  log.push(`clientes: ${JSON.stringify(after.map((a) => ({ screen: a.screen, wait: a.waitText })))}`);
  const clientsSaw = after.every((a) => a.screen === "screen-wait" && /anfitri.*cerró/i.test(a.waitText || ""));
  const hostClean = await host.eval(`(function(){ return { screen:(document.querySelector(".screen.active")||{}).id||"", pollActive:(typeof S!=="undefined"&&S.net)?S.net.pollActive:null, poll:(typeof S!=="undefined"&&S.net)?!!S.net.poll:null, pollTimer:(typeof S!=="undefined"&&S.net)?!!S.net.pollTimer:null }; })()`);
  log.push(`anfitrión tras cerrar: ${JSON.stringify(hostClean)}`);
  log.push("El anfitrión juega en un solo teléfono sin reiniciar la página");
  await host.eval(`document.querySelector("#btnSingle").click()`);
  await sleep(600);
  await host.eval(`document.querySelector("#btnStartSingle").click()`);
  await sleep(1500);
  const r = await botLoop([host], () => allAlbums([host]), 120000);
  const fin = await host.eval("window.__state()");
  log.push(`un solo teléfono: pantalla=${fin.screen}, álbumes=${JSON.stringify(fin.albums)}`);
  log.push(`errores: ${JSON.stringify(collectErrors([host]))}`);
  const ok = clientsSaw && hostClean.screen === "screen-home" && !hostClean.pollActive && !hostClean.poll && !hostClean.pollTimer && r.ok;
  return { name: "close-room-single", ok, ms: r.ms, log, finals: [fin] };
}
async function scenarioMasterpiece() {
  const log = [];
  const { host, clients } = await setupRoom(4, "masterpiece");
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(2500);
  const limit = await host.eval(`(function(){ return { stepLimit:(typeof HOST!=="undefined")?HOST.stepLimit:null, pill:(document.querySelector("#timerPill")||{}).textContent||"", engineTime:(typeof S!=="undefined"&&S.engine)?S.engine.timeFor("draw",0):null }; })()`);
  log.push(`Obra maestra: límite del paso=${limit.stepLimit}, píldora=${JSON.stringify(limit.pill)}, tiempo del motor=${limit.engineTime}`);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allAlbums(pages), 120000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, 4));
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  const ok = limit.stepLimit === 0 && limit.engineTime === 0 && /sin l.mite/i.test(limit.pill) && r.ok;
  return { name: "masterpiece", ok, ms: r.ms, log, finals };
}
async function scenarioBig(n) {
  const log = [];
  const { host, clients } = await setupRoom(n, "normal");
  log.push(`sala de ${n} jugadores: ${NAMES.slice(0, n).join(", ")}`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  await sleep(1500);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allAlbums(pages), 600000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`álbumes: ${JSON.stringify(finals.map((f) => f.albums))}`);
  log.push(await checkAuthorship(host, n));
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  return { name: `wifi-${n}`, ok: r.ok, ms: r.ms, log, finals };
}
async function scenarioGuessCanvas() {
  const log = [];
  const { host, clients } = await setupRoom(4, "guess");
  const drawer = host; // ronda 0: dibuja el anfitrión
  const guesser = clients[0];
  await drawer.eval(`window.__botHoldDraw = true;`);
  await host.eval(`document.querySelector("#btnStartWifi").click()`);
  // Esperar a la fase de dibujo con la palabra elegida.
  let phase = null;
  for (let i = 0; i < 40; i++) {
    await sleep(500);
    const st = await drawer.eval(`(function(){ return { phase:(typeof HOST!=="undefined"&&HOST.guess)?HOST.guess.phase:null, round:(typeof HOST!=="undefined"&&HOST.guess)?HOST.guess.round:null, pick:!!document.querySelector(".word-pick button"), draw:!!document.querySelector("#guessDrawHost #drawCanvas") }; })()`);
    if (st.phase === "draw" && st.draw) { phase = st; break; }
    if (st.pick) { /* el bot elige la palabra en su siguiente tick */ }
  }
  if (!phase) { log.push("no se llegó a la fase de dibujo"); return { name: "guess-canvas", ok: false, ms: 0, log, finals: [] }; }
  log.push("El dibujante usa pincel, línea, círculo, cuadrado, relleno, borrador, Deshacer, Rehacer y Limpiar, y dibuja más de 600 trazos");
  await drawer.eval(`window.__scribbleMany(650);`);
  await sleep(1000);
  const drawn = await drawer.eval(`(function(){ return { drawn:window.__drawnStrokes||0, inArray:window.__strokeCount||0, rev:(typeof S!=="undefined"&&S.guess)?S.guess.canvasRev:null }; })()`);
  log.push(`trazos dibujados=${drawn.drawn}, en el lienzo=${drawn.inArray}, revisión del dibujante=${drawn.rev}`);
  // Esperar a que la última revisión llegue al invitado.
  await sleep(4000);
  const cmp = await Promise.all([
    drawer.eval(`(function(){ var cv=document.querySelector("#guessDrawHost #drawCanvas"); return cv?cv.toDataURL("image/png"):null; })()`),
    guesser.eval(`(function(){ var cv=document.querySelector("#liveCanvas"); return cv?cv.toDataURL("image/png"):null; })()`),
  ]);
  const same = cmp[0] && cmp[1] && cmp[0] === cmp[1];
  log.push(`lienzo del dibujante len=${cmp[0] ? cmp[0].length : 0}, del invitado len=${cmp[1] ? cmp[1].length : 0}, idénticos=${same}`);
  if (!same && cmp[0] && cmp[1]) {
    let firstDiff = -1;
    for (let i = 0; i < Math.min(cmp[0].length, cmp[1].length); i++) if (cmp[0][i] !== cmp[1][i]) { firstDiff = i; break; }
    log.push(`primera diferencia en el carácter ${firstDiff}`);
  }
  // Terminar la ronda y que el juego llegue al podio.
  await drawer.eval(`window.__botHoldDraw = false;`);
  const pages = [host, ...clients];
  const r = await botLoop(pages, () => allPodium(pages), 240000);
  const finals = [];
  for (const p of pages) finals.push(await p.eval("window.__state()"));
  log.push(`pantallas finales: ${JSON.stringify(finals.map((f) => f.screen))}`);
  log.push(`errores: ${JSON.stringify(collectErrors(pages))}`);
  return { name: "guess-canvas", ok: drawn.drawn >= 600 && same && r.ok, ms: r.ms, log, finals };
}
/* Ajustes personalizados: una partida real por cada ajuste cambiado, uno
   cada vez, con 3 jugadores (rápido). */
async function setCustom(host, patch) {
  await host.eval(`document.querySelector("#btnModes").click()`);
  await sleep(400);
  await host.eval(`document.querySelector("#tabCustom").click()`);
  await sleep(300);
  // Restablecer los valores por defecto y aplicar solo el cambio pedido.
  await host.eval(`(function(){
    function setSel(id, v){ var s=document.querySelector(id); s.value=v; s.dispatchEvent(new Event("change",{bubbles:true})); }
    setSel("#customTime", "normal"); setSel("#customSequence", "write-draw");
    setSel("#customTurns", "all"); setSel("#customKeep", "off");
    function setSeg(id, v){ var seg=document.querySelector(id); if(!seg) return; var bs=seg.querySelectorAll("button"); bs.forEach(function(b){ if(b.getAttribute("data-v")===v) b.click(); }); }
    setSeg("#customScoreSeg", "off"); setSeg("#customSecretSeg", "off");
  })()`);
  await sleep(300);
  if (patch) await host.eval(`(function(){
    var p=${JSON.stringify(patch)};
    function setSel(id, v){ var s=document.querySelector(id); s.value=v; s.dispatchEvent(new Event("change",{bubbles:true})); }
    function setSeg(id, v){ var seg=document.querySelector(id); if(!seg) return; var bs=seg.querySelectorAll("button"); bs.forEach(function(b){ if(b.getAttribute("data-v")===v) b.click(); }); }
    if(p.time) setSel("#customTime", p.time);
    if(p.sequence) setSel("#customSequence", p.sequence);
    if(p.turns) setSel("#customTurns", p.turns);
    if(p.keep) setSel("#customKeep", p.keep);
    if(p.score) setSeg("#customScoreSeg", p.score);
    if(p.secret) setSeg("#customSecretSeg", p.secret);
  })()`);
  await sleep(300);
  await host.eval(`document.querySelector("#btnModesBack").click()`);
  await sleep(400);
}
async function scenarioCustom() {
  const log = [];
  const cases = [
    { name: "tiempo-rápido", patch: { time: "rapido" }, check: async (pages) => {
      // El motor del cliente del anfitrión se crea tras la cuenta atrás
      // (~2,1 s): esperar a que exista antes de leer el tiempo.
      let c = null;
      for (let i = 0; i < 20; i++) {
        await sleep(500);
        c = await pages[0].eval(`(function(){ var e=(typeof HOST!=="undefined"&&HOST.engine)?HOST.engine:null; return { cfg:(typeof HOST!=="undefined")?HOST.customCfg:null, hostTime:e?e.timeFor("write",0):null, clientTime:(typeof S!=="undefined"&&S.engine)?S.engine.timeFor("write",0):null }; })()`);
        if (c.clientTime !== null) break;
      }
      return { ok: c.cfg && c.cfg.times.write === 30 && c.hostTime === 30 && c.clientTime === 30, detail: JSON.stringify(c) };
    }},
    { name: "secuencia-solo-dibujar", patch: { sequence: "draw-only" }, check: async (pages) => {
      const c = await pages[0].eval(`(function(){ var e=(typeof HOST!=="undefined"&&HOST.engine)?HOST.engine:null; if(!e) return null; var types=[]; for(var s=0;s<e.steps;s++) types.push(e.taskType(s)); return { steps:e.steps, types:types }; })()`);
      return { ok: c && c.types.every((t) => t === "draw"), detail: JSON.stringify(c) };
    }},
    { name: "sigue-dibujando", patch: { sequence: "draw-only", keep: "on" }, check: async (pages) => {
      // Durante la comprobación no corre el bot: el paso 0 se dibuja y se
      // envía a mano en cada página, y al llegar al paso 1 el lienzo debe
      // empezar con el dibujo anterior (no en blanco).
      for (const p of pages) {
        let done = false;
        for (let i = 0; i < 30; i++) {
          await sleep(500);
          const ok = await p.eval(`(function(){
            var cv=document.querySelector("#drawCanvas");
            if(!cv) return false;
            window.__scribble();
            var b=document.querySelector("#btnSendDraw");
            if(b && window.__drewKey){ b.click(); return true; }
            return false;
          })()`);
          if (ok) { done = true; break; }
        }
        if (!done) return { ok: false, detail: "no se pudo enviar el paso 0" };
      }
      let got = null;
      for (let i = 0; i < 40; i++) {
        await sleep(500);
        const hs = await pages[0].eval("window.__state()");
        if (hs.engineStep >= 1) {
          const infos = [];
          let allDraw = true;
          for (const p of pages) {
            const s = await p.eval(`(function(){ return { draw:!!document.querySelector("#drawCanvas"), info:window.__canvasInfo?window.__canvasInfo():null }; })()`);
            if (!s.draw) allDraw = false;
            infos.push(s.info);
          }
          if (allDraw) { got = infos; break; }
        }
      }
      const nonBlank = got && got.filter((x) => x && !x.blank).length;
      return { ok: got && nonBlank === got.length, detail: `lienzos no en blanco: ${nonBlank}/${got ? got.length : 0}` };
    }},
    { name: "puntuación", patch: { score: "on" }, check: async (pages) => {
      const c = await pages[0].eval(`(function(){ return { cfg:(typeof HOST!=="undefined")?HOST.customCfg:null }; })()`);
      return { ok: c.cfg && c.cfg.score === true, detail: JSON.stringify(c) };
    }, afterAlbum: async (pages) => {
      // El voto es asíncrono (va al anfitrión y vuelve): pulsar, esperar
      // a que se actualice el marcador y leerlo después.
      const clicked = await pages[0].eval(`(function(){ var b=document.querySelector(".vote-btn"); if(!b) return false; b.click(); return true; })()`);
      if (!clicked) return { ok: false, why: "sin botón de voto" };
      let v = null;
      for (let i = 0; i < 10; i++) {
        await sleep(500);
        v = await pages[0].eval(`(function(){ var board=document.querySelector(".score-board"); return { ok:!!board && /1 pt/.test(board.textContent||""), board:board?board.textContent.slice(0,120):"" }; })()`);
        if (v.ok) break;
      }
      return v;
    }},
    { name: "secreto", patch: { secret: "on" }, check: async (pages) => {
      let veil = false, sec = false;
      for (let i = 0; i < 40; i++) {
        await sleep(500);
        const r = await pages[0].eval(`(function(){ var e=(typeof HOST!=="undefined"&&HOST.engine)?HOST.engine:null; return { veil:!!document.querySelector("#secretVeil"), taskSecret:e?!!e.taskFor(0, e.step).secret:false, screen:(document.querySelector(".screen.active")||{}).id||"" }; })()`);
        if (r.veil || r.taskSecret) { veil = r.veil; sec = r.taskSecret; break; }
      }
      return { ok: veil || sec, detail: `velo=${veil} tareaSecreta=${sec}` };
    }},
    { name: "turnos-aleatorios", patch: { turns: "random" }, check: async (pages) => {
      const c = await pages[0].eval(`(function(){ var e=(typeof HOST!=="undefined"&&HOST.engine)?HOST.engine:null; return e?{ steps:e.steps, randomRounds:(typeof HOST!=="undefined"&&HOST.customCfg)?HOST.customCfg.randomRounds:null }:null; })()`);
      return { ok: c && c.steps >= 2 && c.steps <= 3, detail: JSON.stringify(c) };
    }},
  ];
  let allOk = true;
  for (const cs of cases) {
    const host = await newPage(`http://127.0.0.1:${HOST_PORT}/?lan=host&p=Roi`);
    await setCustom(host, cs.patch);
    const st = await hostSetup(host, "custom", 3);
    const clients = [];
    for (let i = 1; i < 3; i++) { const c = await newPage(`http://127.0.0.1:${CLIENT_PORTS[i - 1]}/?p=${NAMES[i]}`); await joinClient(c, NAMES[i], st.roomCode); clients.push(c); }
    await host.eval(`(function(){ var s=document.querySelector("#wifiMaxPlayers"); s.value="3"; s.dispatchEvent(new Event("change",{bubbles:true})); var m=document.querySelector("#wifiModeSelect"); m.value="custom"; m.dispatchEvent(new Event("change",{bubbles:true})); })()`);
    await sleep(500);
    const pages = [host, ...clients];
    await host.eval(`document.querySelector("#btnStartWifi").click()`);
    await sleep(1200);
    const probe = await cs.check(pages);
    log.push(`${cs.name}: ${probe.ok ? "OK" : "FALLO"} — ${probe.detail}`);
    const r = await botLoop(pages, () => allAlbums(pages), 180000);
    let afterOk = true;
    if (cs.afterAlbum) {
      const a = await cs.afterAlbum(pages);
      afterOk = !!a.ok;
      log.push(`${cs.name} (álbum): ${a.ok ? "OK" : "FALLO"} — ${JSON.stringify(a).slice(0, 200)}`);
    }
    const finals = [];
    for (const p of pages) finals.push(await p.eval("window.__state()"));
    log.push(`${cs.name}: álbumes=${JSON.stringify(finals.map((f) => f.albums))} errores=${JSON.stringify(collectErrors(pages))}`);
    if (!probe.ok || !r.ok || !afterOk) allOk = false;
    // Cerrar las páginas de este caso para que el siguiente empiece limpio.
    try { const list = await cdpJson("/json/list"); for (const t of list.filter((t) => t.type === "page")) { try { await fetch(`http://127.0.0.1:${CDP_PORT}/json/close/${t.id}`); } catch (e) {} } } catch (e) {}
    await sleep(1500);
  }
  return { name: "custom", ok: allOk, ms: 0, log, finals: [] };
}

/* ---------------- main ---------------- */
const SCEN = { normal: scenarioNormal, story: () => scenarioMode("story"), secret: () => scenarioMode("secret"), animation: () => scenarioMode("animation"), icebreaker: () => scenarioMode("icebreaker"), missing: () => scenarioMode("missing"), guess: scenarioGuess, dropout: scenarioDropout, "host-leaves": scenarioHostLeaves, kick: scenarioKick, "late-join": scenarioLateJoin, reconnect: scenarioReconnect,
  "write-12s": scenarioWrite12, "draw-12s": scenarioDraw12, "netcut-5s": scenarioNetcut, "lost-submit": scenarioLostSubmit, "close-room-single": scenarioCloseRoom, masterpiece: scenarioMasterpiece, "wifi-10": () => scenarioBig(10), "wifi-14": () => scenarioBig(14), "guess-canvas": scenarioGuessCanvas, custom: scenarioCustom };
const wanted = process.argv[2] === "all" ? Object.keys(SCEN) : [process.argv[2] || "normal"];
const results = {};
await startChrome();
for (const name of wanted) {
  if (!SCEN[name]) { console.log("escenario desconocido:", name); continue; }
  console.log("\n=== " + name + " ===");
  await fetch(`http://127.0.0.1:${HOST_PORT}/__test/reset`).catch(() => {});
  try {
    const r = await SCEN[name]();
    results[name] = r;
    console.log((r.ok ? "OK " : "FALLO ") + name + " (" + r.ms + " ms)");
    r.log.forEach((l) => console.log("  - " + l));
  } catch (e) {
    results[name] = { name, ok: false, error: String(e && e.stack || e) };
    console.log("ERROR " + name + ": " + e.message);
  }
  // Cerrar las páginas del escenario para que el siguiente empiece limpio.
  try { const list = await cdpJson("/json/list"); for (const t of list.filter((t) => t.type === "page")) { try { await fetch(`http://127.0.0.1:${CDP_PORT}/json/close/${t.id}`); } catch (e) {} } } catch (e) {}
  await sleep(1500);
}
fs.writeFileSync(path.join(OUT, "wifi-resultados.json"), JSON.stringify(results, null, 2));
console.log("\nInforme en " + path.join(OUT, "wifi-resultados.json"));
if (chromeProc) chromeProc.kill();
process.exit(0);
