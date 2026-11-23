#!/usr/bin/env node
/* Driver compacto para la verificación a 390x844 (recreado tras perder
   /tmp en un reinicio; misma auditoría AUDIT_JS que /tmp/revgen/driver.mjs).
   Uso: node driver-390.mjs
   Escribe capturas en VERIFICACION/v2.4/revision-final/fix-b1b2/shots-390/
   y revision-general-390.json en la misma carpeta. */
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const PROJ = path.join(os.homedir(), "workspace", "gartic-movil");
const OUT = path.join(PROJ, "VERIFICACION", "v2.4", "revision-final", "fix-b1b2");
const W = 390, H = 844;
const SHOTDIR = path.join(OUT, `shots-${W}`);
fs.mkdirSync(SHOTDIR, { recursive: true });
const URL_BASE = "file://" + path.join(PROJ, "www", "index.html");
let navN = 0;
const navUrl = (hash) => URL_BASE + "?n=" + (++navN) + (hash ? "#" + hash : "");

const SHOTS = ["splash", "home", "modes", "setup", "settings", "how", "join",
  "create", "countdown", "pass", "write", "describe", "draw", "draw-tools",
  "album", "guess-draw", "guess-live", "podium", "rooms",
  "draw-memory", "secret-write",
  "play-story", "play-masterpiece", "play-secret", "play-sandwich",
  "play-score", "play-icebreaker", "play-knockoff", "play-complement",
  "play-missing", "play-corpse", "play-coop", "play-animation",
  "play-background", "play-solo"];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitHttp(url, tries = 60) {
  for (let i = 0; i < tries; i++) {
    try { const r = await fetch(url); if (r.ok) return r; } catch {}
    await sleep(250);
  }
  throw new Error("sin DevTools en " + url);
}

const AUDIT_JS = `(() => {
  const errs = window.__errs || [];
  const active = document.querySelector(".screen.active");
  const screenId = active ? active.id : "(ninguna)";
  const txt = active ? (active.innerText || "").trim() : "";
  const overflow = document.documentElement.scrollWidth > window.innerWidth;
  const docH = document.documentElement.scrollHeight;
  const items = [];
  const rects = [];
  if (active) active.querySelectorAll("button, select, input, textarea, [role=button], a.btn").forEach((el) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    if (r.width === 0 && r.height === 0) return;
    const t = (el.textContent || el.value || el.placeholder || el.getAttribute("aria-label") || "").trim().replace(/\\s+/g, " ").slice(0, 44);
    const clipX = el.scrollWidth > el.clientWidth + 1, clipY = el.scrollHeight > el.clientHeight + 1;
    const belowFold = r.top >= window.innerHeight;
    items.push({ tag: el.tagName.toLowerCase(), id: el.id || "", text: t,
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      low48: r.height < 48, low44: r.height < 44, clip: clipX || clipY,
      outH: r.x < -1 || r.right > window.innerWidth + 1,
      belowFold: belowFold, outV: r.bottom > window.innerHeight && !belowFold });
    rects.push({ id: el.id || t, x: r.x, y: r.y, r: r.right, b: r.bottom });
  });
  const overlaps = [];
  for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
    const a = rects[i], b = rects[j];
    const ox = Math.min(a.r, b.r) - Math.max(a.x, b.x), oy = Math.min(a.b, b.b) - Math.max(a.y, b.y);
    if (ox > 4 && oy > 4) overlaps.push(a.id + " ~ " + b.id);
  }
  const bodyTxt = document.body.innerText || "";
  const hasArrowGlyph = bodyTxt.indexOf("←") >= 0;
  const fontOk700 = document.fonts ? document.fonts.check('700 16px "Baloo 2"') : false;
  const fontOk800 = document.fonts ? document.fonts.check('800 16px "Baloo 2"') : false;
  const fontStatus = document.fonts ? document.fonts.status : "?";
  function lum(rgb){ const m = rgb.match(/(\\d+)[,\\s]+(\\d+)[,\\s]+(\\d+)/); if(!m) return null;
    const f = (c)=>{ c/=255; return c<=0.03928? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
    return 0.2126*f(+m[1])+0.7152*f(+m[2])+0.0722*f(+m[3]); }
  function ratio(c1, c2){ const l1=lum(c1), l2=lum(c2); if(l1===null||l2===null) return null;
    const a=Math.max(l1,l2), b=Math.min(l1,l2); return Math.round(((a+0.05)/(b+0.05))*100)/100; }
  const contrast = [];
  if (active) active.querySelectorAll("h1,h2,h3,p,span,small,label,button").forEach((el) => {
    const t = (el.textContent || "").trim(); if (!t || el.children.length > 3) return;
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    const r = el.getBoundingClientRect(); if (r.width === 0 || r.top < 0 || r.top > window.innerHeight) return;
    let bg = null, n = el;
    while (n && n !== document.body) { const b = getComputedStyle(n).backgroundColor;
      if (b && b !== "rgba(0, 0, 0, 0)" && b !== "transparent") { bg = b; break; } n = n.parentElement; }
    const fg = cs.color;
    const against = bg || "rgb(122, 42, 160)";
    const rr = ratio(fg, against);
    const fs = parseFloat(cs.fontSize);
    if (rr !== null && ((fs >= 18 && rr < 3) || (fs < 18 && rr < 4.5)))
      contrast.push({ text: t.slice(0, 34), fg, bg: against, ratio: rr, size: fs });
  });
  const EN = ["Done","Start","Settings","Players","Join","Create","Back","Next","Cancel","Skip","Play","Score","Room","Invite","Loading","Write","Draw","Describe","Album","Round","Sound","Vibrate","Home","How to play","Turns","Time"];
  const enFound = [];
  EN.forEach((w) => { const re = new RegExp("\\\\b" + w + "\\\\b", "i");
    if (re.test(bodyTxt)) enFound.push(w); });
  const canvas = active ? active.querySelector("canvas") : null;
  const canvasInfo = canvas ? { w: canvas.width, h: canvas.height, rw: Math.round(canvas.getBoundingClientRect().width), rh: Math.round(canvas.getBoundingClientRect().height) } : null;
  const boxes = {};
  [".app", ".screen.active .card", ".toolbar", ".btn-row", ".draw-bar", ".canvas-wrap", ".draw-top", ".prompt-box", ".draw-preview", ".strip-preview", "#screen-play", "#topbar"].forEach((sel) => {
    const el = document.querySelector(sel);
    if (el) { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
      boxes[sel] = { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), disp: cs.display }; }
  });
  return { screen: screenId, errors: errs, overflow, scrollW: document.documentElement.scrollWidth,
    docH, innerH: window.innerHeight, textLen: txt.length, items, overlaps, boxes,
    hasArrowGlyph, fontOk700, fontOk800, fontStatus, contrast, enFound, canvas: canvasInfo,
    title: document.title };
})()`;

async function main() {
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "rev390-"));
  const chrome = spawn(process.env.HOME + "/.cache/ms-playwright/chromium_headless_shell-1161/chrome-linux/headless_shell",
    ["--no-sandbox", "--disable-gpu", "--hide-scrollbars",
     `--user-data-dir=${profile}`, "--remote-debugging-port=9337",
     `--window-size=${W},${H}`, "about:blank"],
    { stdio: "ignore" });
  const results = {};
  try {
    await waitHttp("http://127.0.0.1:9337/json/version");
    const put = await fetch("http://127.0.0.1:9337/json/new?about:blank", { method: "PUT" });
    const target = await put.json();
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    let mid = 0; const pending = new Map();
    const consoleErrs = [];
    ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
      if (m.method === "Runtime.exceptionThrown")
        consoleErrs.push("EXC: " + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text || "?").slice(0, 200));
      if (m.method === "Runtime.consoleAPICalled" && (m.params.type === "error" || m.params.type === "warning"))
        consoleErrs.push(m.params.type + ": " + m.params.args.map(a => a.value ?? a.description ?? "?").join(" ").slice(0, 200));
      if (m.method === "Network.loadingFailed")
        consoleErrs.push("NETFAIL: " + (m.params.errorText || "?"));
    };
    const send = (method, params = {}) => new Promise((res) => {
      const id = ++mid; pending.set(id, res);
      ws.send(JSON.stringify({ id, method, params }));
    });
    const evalJs = async (expr) => {
      const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
      if (r.result?.exceptionDetails) return { __ex: r.result.exceptionDetails.text || "eval error" };
      return r.result?.result?.value;
    };
    const shot = async (name) => {
      const r = await send("Page.captureScreenshot", { format: "png" });
      fs.writeFileSync(path.join(SHOTDIR, name + ".png"), Buffer.from(r.result.data, "base64"));
    };
    await send("Page.enable"); await send("Runtime.enable"); await send("Network.enable");
    await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: true });

    for (const name of SHOTS) {
      consoleErrs.length = 0;
      const t = Date.now();
      await send("Page.navigate", { url: navUrl(`shot=${name}`) });
      let ready = false;
      for (let i = 0; i < 100; i++) {
        const title = await evalJs(`document.title`);
        if (typeof title === "string" && title.startsWith("TEST")) { ready = true; break; }
        await sleep(100);
      }
      await sleep(300);
      const audit = await evalJs(AUDIT_JS);
      audit._ready = ready; audit._ms = Date.now() - t; audit._console = consoleErrs.slice();
      results[name] = audit;
      await shot(name);
      console.log(name, "->", audit.screen, "errs:", (audit.errors || []).length, "overflow:", audit.overflow, "items:", (audit.items || []).length);
    }
    results._timings = { viewport: `${W}x${H}`, skipped: true };
    fs.writeFileSync(path.join(OUT, `revision-general-${W}.json`), JSON.stringify(results, null, 2));
    console.log("OK", `${W}x${H}`);
    ws.close();
  } finally {
    chrome.kill();
  }
}
main().catch((e) => { console.error(e); process.exit(1); });
