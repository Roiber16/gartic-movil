/**
 * fix-manifest.js — Manifiesto para Gartic Móvil.
 *
 * Se ejecuta en GitHub Actions antes de compilar, por si `npx cap sync`
 * o un `cap add android` nuevo regenera el AndroidManifest.xml.
 * Es idempotente: si el cambio ya existe, no toca nada.
 *
 * 1. Permite tráfico sin cifrar (android:usesCleartextTraffic="true"):
 *    el invitado llama por HTTP claro al servidor local del anfitrión
 *    (http://192.168.x.x:7777). Sin esto, Android 9+ bloquea esas
 *    llamadas y «Unirse por IP» nunca conectaría.
 *    Solo afecta a la red local: el juego no usa internet.
 *    (Mismo arreglo que en Ecos del Olimpo.)
 * 2. Declara el permiso de red local de Android 17
 *    (android.permission.ACCESS_LOCAL_NETWORK). El proyecto apunta a
 *    SDK 36 (Android 16): ahí el acceso a la red local sigue implícito
 *    por INTERNET y esta declaración es inerte (los permisos
 *    desconocidos se ignoran). Si el objetivo sube a SDK 37, esa
 *    declaración pasa a ser obligatoria Y además habrá que pedir el
 *    permiso en tiempo de ejecución antes de crear la sala o unirse;
 *    sin concederlo, en Android 17 las conexiones TCP locales agotan
 *    el tiempo. Esta declaración solo prepara el terreno.
 *
 * NO fija orientación (el juego se usa en vertical para dibujar) ni
 * pide cámara (Gartic Móvil no usa QR).
 *
 * Uso: node scripts/fix-manifest.js
 */
const fs = require("fs");
const path = require("path");

const manifestPath = path.join(__dirname, "..", "android", "app", "src", "main", "AndroidManifest.xml");

if (!fs.existsSync(manifestPath)) {
  console.error("No existe AndroidManifest.xml en " + manifestPath);
  console.error("Ejecuta primero: npx cap add android");
  process.exit(1);
}

let xml = fs.readFileSync(manifestPath, "utf8");
let changed = false;

// 1. Tráfico sin cifrar para la red local.
if (!xml.includes('android:usesCleartextTraffic="true"')) {
  const before = xml;
  xml = xml.replace(
    /(<application[\s\S]*?)>/,
    function (m) {
      return m.includes("android:usesCleartextTraffic")
        ? m
        : m.replace(/>$/, '\n        android:usesCleartextTraffic="true">');
    }
  );
  if (xml !== before && xml.includes('android:usesCleartextTraffic="true"')) {
    console.log('Añadido android:usesCleartextTraffic="true" a <application>.');
    changed = true;
  } else {
    console.error("AVISO: no se pudo añadir usesCleartextTraffic. Revisa el manifiesto a mano.");
  }
} else {
  console.log('usesCleartextTraffic="true" ya estaba.');
}

// 2. Permiso de red local de Android 17 (inerte con targetSdk 36).
if (!xml.includes("android.permission.ACCESS_LOCAL_NETWORK")) {
  const before = xml;
  xml = xml.replace(
    /(<uses-permission android:name="android\.permission\.INTERNET" \/>)/,
    '$1\n    <uses-permission android:name="android.permission.ACCESS_LOCAL_NETWORK" />'
  );
  if (xml !== before) {
    console.log("Añadido permiso ACCESS_LOCAL_NETWORK (preparado para SDK 37).");
    changed = true;
  } else {
    console.error("AVISO: no se pudo añadir ACCESS_LOCAL_NETWORK. Revisa el manifiesto a mano.");
  }
} else {
  console.log("El permiso ACCESS_LOCAL_NETWORK ya estaba.");
}

if (changed) {
  fs.writeFileSync(manifestPath, xml, "utf8");
  console.log("AndroidManifest.xml actualizado.");
} else {
  console.log("AndroidManifest.xml ya estaba correcto. Sin cambios.");
}
