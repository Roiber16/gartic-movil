/**
 * fix-debug-signing.js — Firma debug explícita en build.gradle.
 *
 * Por qué existe: copiar el keystore fijo a ~/.android/debug.keystore no
 * basta — Gradle puede resolver su propio debug.keystore por otro camino
 * y cada build saldría con una clave efímera distinta, obligando a Roi a
 * desinstalar la APK anterior para instalar la nueva (eso pasó en Ecos
 * y en GeoPre antes de este arreglo).
 *
 * Solución robusta: configurar la firma debug EXPLÍCITAMENTE en
 * android/app/build.gradle, apuntando al keystore del repo
 * (keystore/gartic-movil-debug.keystore). Así Gradle usa siempre la misma
 * clave y las actualizaciones instalan encima sin desinstalar.
 *
 * Se ejecuta DESPUÉS de `npx cap sync android`, porque cap sync reescribe
 * android/app/build.gradle y borraría el parche si se aplicara antes.
 * Es idempotente.
 *
 * Uso: node scripts/fix-debug-signing.js
 */
const fs = require("fs");
const path = require("path");

const gradlePath = path.join(__dirname, "..", "android", "app", "build.gradle");

if (!fs.existsSync(gradlePath)) {
  console.error("No existe build.gradle en " + gradlePath);
  process.exit(1);
}

let gradle = fs.readFileSync(gradlePath, "utf8");

if (!gradle.includes("gartic-movil-debug.keystore")) {
  const anchor = "    buildTypes {";
  if (!gradle.includes(anchor)) {
    console.error('AVISO: no se encontró "buildTypes {" en build.gradle. Revisa a mano.');
    process.exit(1);
  }

  const signingBlock = `    signingConfigs {
        debug {
            storeFile file("../../keystore/gartic-movil-debug.keystore")
            storePassword "android"
            keyAlias "androiddebugkey"
            keyPassword "android"
        }
    }
`;
  gradle = gradle.replace(anchor, signingBlock + anchor);
}

// La sección debug de buildTypes debe usar esa firma. La plantilla de
// Capacitor 8 no trae bloque `debug` (solo `release`): sin él, Gradle
// firmaría el debug con su keystore automático y cada build saldría con
// otra clave. Lo creamos explícitamente si falta.
if (!/buildTypes\s*\{[^}]*\bdebug\s*\{/.test(gradle)) {
  gradle = gradle.replace(
    /(\n    buildTypes \{)/,
    "$1\n        debug {\n            signingConfig signingConfigs.debug\n        }"
  );
} else if (!/debug\s*\{\s*\n\s*signingConfig signingConfigs\.debug/.test(gradle)) {
  gradle = gradle.replace(
    /(\n    buildTypes \{\n        debug \{)/,
    "$1\n            signingConfig signingConfigs.debug"
  );
}

// La versión también la fija este script: cap sync reescribe build.gradle
// y con él versionCode/versionName, así que se reponen aquí en cada build.
// v2.2 = barra compacta, sonidos, vibración y splash SanBer (versionCode 4, versionName 1.2.0).
// Subir ambos números en cada entrega.
gradle = gradle.replace(/versionCode \d+/, "versionCode 4");
gradle = gradle.replace(/versionName "[^"]*"/, 'versionName "1.2.0"');

fs.writeFileSync(gradlePath, gradle);
console.log("build.gradle: firma debug fijada a keystore/gartic-movil-debug.keystore");

// El nombre del launcher también lo fija este script: cap sync NO actualiza
// android/app/src/main/res/values/strings.xml desde capacitor.config.json.
const stringsPath = path.join(
  __dirname,
  "..",
  "android",
  "app",
  "src",
  "main",
  "res",
  "values",
  "strings.xml"
);
if (fs.existsSync(stringsPath)) {
  let strings = fs.readFileSync(stringsPath, "utf8");
  strings = strings.replace(
    /(<string name="app_name">)[^<]*(<\/string>)/,
    "$1Gartic Móvil$2"
  );
  strings = strings.replace(
    /(<string name="title_activity_main">)[^<]*(<\/string>)/,
    "$1Gartic Móvil$2"
  );
  strings = strings.replace(
    /(<string name="package_name">)[^<]*(<\/string>)/,
    "$1cu.roi.garticmovil$2"
  );
  strings = strings.replace(
    /(<string name="custom_url_scheme">)[^<]*(<\/string>)/,
    "$1cu.roi.garticmovil$2"
  );
  fs.writeFileSync(stringsPath, strings);
  console.log("strings.xml: app_name, title_activity_main, package_name y custom_url_scheme fijados a Gartic Móvil / cu.roi.garticmovil");
} else {
  console.error("AVISO: no existe strings.xml en " + stringsPath);
}
