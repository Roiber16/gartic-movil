/**
 * setup-android.js — Prepara la plataforma Android antes de compilar.
 *
 * Si la carpeta android/ no existe, la crea con `npx cap add android`.
 * Copia los iconos y el splash desde assets/res/ y assets/splash.png,
 * y aplica el manifiesto (fix-manifest.js) y la firma debug fija
 * (fix-debug-signing.js). NO fuerza orientación: Gartic Móvil se juega
 * en vertical (dibujar) y el giro lo decide el usuario.
 *
 * Después de este script, el flujo es:
 *   npx cap sync android
 *   node scripts/fix-debug-signing.js   (otra vez, porque cap sync
 *                                        reescribe build.gradle)
 *   cd android && ./gradlew assembleDebug
 *
 * Uso: node scripts/setup-android.js
 */
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const root = path.join(__dirname, "..");
const androidDir = path.join(root, "android");
const resSrc = path.join(root, "assets", "res");
const resDst = path.join(androidDir, "app", "src", "main", "res");

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

if (!fs.existsSync(androidDir)) {
  console.log("No existe android/. Creando la plataforma con Capacitor...");
  execSync("npx cap add android", { cwd: root, stdio: "inherit" });
} else {
  console.log("La carpeta android/ ya existe. No se regenera.");
}

console.log("Copiando iconos desde assets/res/ ...");
copyDir(resSrc, resDst);
console.log("Iconos copiados.");

// Splash sencillo: fondo #f4f1ff con el icono centrado (assets/splash.png).
// Capacitor 8 usa drawable/splash.png si existe; se copia como tal.
const splashSrc = path.join(root, "assets", "splash.png");
const splashDst = path.join(resDst, "drawable", "splash.png");
if (fs.existsSync(splashSrc)) {
  fs.mkdirSync(path.dirname(splashDst), { recursive: true });
  fs.copyFileSync(splashSrc, splashDst);
  console.log("Splash copiado a res/drawable/splash.png.");
} else {
  console.log("AVISO: no existe assets/splash.png, se salta el splash.");
}

require("./fix-manifest.js");
require("./fix-debug-signing.js");
console.log("setup-android.js terminado.");
