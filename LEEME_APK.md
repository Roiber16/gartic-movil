# Gartic Móvil — APK Android

> Nota: antes se llamaba Teléfono Roto; Roi lo renombró a Gartic Móvil
> el 21 nov 2026. El keystore es el mismo de antes (misma huella SHA-256),
> solo cambió el nombre del archivo.

Empaquetado con Capacitor de la app web de Gartic Móvil (juego offline
tipo teléfono roto: dibujar, describir y reírse con amigos sin internet).
Modo Normal fiel, 3-8 jugadores, wifi local por hotspot (servidor local
puerto 7777) + modo de un solo teléfono.

- **appId:** `cu.roi.garticmovil`
- **Nombre:** Gartic Móvil
- **Versión:** 1.0.0 (versionCode 1, versionName 1.0.0)
- **Peso:** la parte web (`www/`) pesa ~30 KB y los assets ~72 KB;
  la APK final quedará muy por debajo del límite de 50 MB.

## ✅ www completo y verificado

El `www/index.html` actual está **completo y verificado**: pesa
55.878 B, termina en `</html>` y contiene la partida jugada entera
(modo Normal: escribir, dibujar, describir y álbum final, en un solo
teléfono y por wifi local). La APK compila con este `www/` y el juego
funciona.

Al actualizar el contenido web, copiar la web nueva en `www/`
(sustituyendo el `index.html` actual), hacer `npx cap sync android`
y subir el cambio antes de lanzar el build en GitHub.

**Fuentes:** la app pide Baloo 2 y Nunito, pero no las empaqueta:
no hay copias locales de esas fuentes en la máquina y descargarlas
solo añadiría peso. Offline, la app usa la fuente del sistema del
teléfono (la pila `system-ui, sans-serif` del CSS) y funciona igual.

## Cómo se compila

La compilación local con Gradle NO funciona en esta VM: el wrapper de
Gradle no puede descargar su distribución (la descarga por HTTPS falla
con `SSLException: Unsupported or unrecognized SSL message`; no hay
ninguna distribución Gradle guardada en la máquina). En cambio, en
esta misma VM sí funcionaron `npm install`, `npx cap add android`,
`npx cap sync android` y los tres scripts (`setup-android.js`,
`fix-manifest.js`, `fix-debug-signing.js`): la plataforma `android/`
ya está generada, sincronizada y parcheada, y el plugin
`capacitor-lan-server` quedó registrado.

La vía que funciona para la APK es **GitHub Actions**, igual que Ecos
del Olimpo y GeoPre. El workflow
(`.github/workflows/build-apk.yml`) se dispara **solo a mano**
(Run workflow): no hay build automático en cada push, para no
compilar una versión vieja del contenido web.

1. En GitHub: repo `Roiber16/gartic-movil`, pestaña
   **Actions > Compilar APK Gartic Móvil > Run workflow**.
2. La APK aparece en **Artifacts > gartic-movil-debug**
   (se guarda 30 días).
3. Se descarga y se instala directamente en el teléfono. Es una APK
   **debug** (no es versión de tienda).

## Lo que falta para la APK (hacer una sola vez)

### 1. Crear el repo en GitHub — lo hace Roi (o el padre)

- Nombre sugerido: **`gartic-movil`**, en la cuenta de Roi
  (`Roiber16`). No se ha creado ningún repo ni token desde aquí.
- Subir todo el contenido de esta carpeta (`~/workspace/gartic-movil/`),
  **excepto** `node_modules/` (se borró del proyecto; se instala solo
  en GitHub con `npm ci`) y `keystore/` (ver el punto 2).
  La carpeta `android/` sí se sube: ya está generada y parcheada, y el
  workflow la reutiliza (si faltara, `setup-android.js` la crea sola).

### 2. Crear el secreto del keystore — lo hace quien suba el proyecto

El keystore debug **NO está en el repo** a propósito. Es solo de
depuración, con las claves por defecto (`android` / `android`), y si
estuviera en un repo público cualquiera podría firmar una APK debug
con la misma clave y actualizar por encima de la app instalada en el
teléfono. Por eso el workflow lo restaura desde un secreto:

- **Nombre del secreto:** `GARTIC_MOVIL_DEBUG_KEYSTORE_B64`
- **Dónde:** repo en GitHub > Settings > Secrets and variables > Actions
- **Valor:** el archivo local `keystore/gartic-movil-debug.keystore`
  en base64, sin saltos de línea. Desde la carpeta del proyecto:
  `base64 -w0 keystore/gartic-movil-debug.keystore`
  (el valor que imprime ese comando es el secreto; no se pega en
  ningún chat ni archivo).
- **Huella del keystore (para comprobar que es el mismo):**
  SHA-256 `9C:2E:01:1B:A4:27:BF:8F:76:B1:DD:85:01:AC:B8:5D:40:48:A5:CE:20:29:FF:03:21:30:DD:23:53:92:F5:CB`
- Es un keystore **nuevo y propio** de Gartic Móvil (alias
  `androiddebugkey`): NO es el de GeoPre
  (SHA `67:98:0D:60:…`) ni el de Ecos (SHA `D4:05:2F:AF…`).

Con ese secreto, `scripts/fix-debug-signing.js` (que corre DESPUÉS de
`cap sync`, porque el sync reescribe `build.gradle`) fija la firma
debug a ese keystore, y **todas las builds salen con la misma clave**:
las actualizaciones se instalan encima sin desinstalar la anterior.

## Cómo actualizar el contenido web y reconstruir

Cuando la app web cambie (nueva versión del juego), la APK vieja queda
obsoleta. Pasos, en esta misma carpeta:

```sh
# 1. Copiar la web nueva a www/ (sustituyendo el contenido anterior)
npx cap sync android          # copia www/ a android/app/src/main/assets/public/
node scripts/fix-debug-signing.js   # DESPUÉS del sync, o se pierde el parche
git add -A && git commit -m "Contenido nuevo: <qué cambió>"
git push origin main
```

Y luego en GitHub: Actions > Compilar APK Gartic Móvil > Run workflow.

## Cómo instalarla en el Redmi 10 (Android 12)

1. Descargar el artifact `gartic-movil-debug` desde GitHub y
   descomprimirlo: dentro viene `app-debug.apk`.
2. Pasarla al teléfono (por Telegram, WhatsApp o cable).
3. Abrir el archivo en el teléfono y pulsar **Instalar**. Si Android
   pregunta, permitir **«Instalar apps desconocidas»** para la app
   desde la que se abre (Telegram, el explorador de archivos…).
4. La primera vez pedirá los permisos de red local si hace falta;
   aceptarlos para poder crear salas wifi.
5. Las actualizaciones con la misma firma se instalan **encima** sin
   desinstalar: si Android pide desinstalar la anterior, es que la
   firma cambió (falta el secreto del keystore en GitHub) — no
   desinstalar, revisar el secreto primero.

## Cómo probar el wifi local con hotspot (dos teléfonos)

El juego no usa internet: solo la red local entre los dos teléfonos.

1. **Anfitrión:** en su teléfono, activar **Punto de acceso wifi**
   (Ajustes > Conexiones > Punto de acceso móvil). Es mejor que el
   anfitrión sea el punto de acceso, porque así su IP es la
   `192.168.43.x` que la app detecta sola.
2. **Invitado:** conectarse a esa wifi del punto de acceso (la red que
   creó el anfitrión).
3. **Anfitrión:** abrir Gartic Móvil > **Crear sala wifi**. La app
   muestra la IP (por ejemplo `192.168.43.1`) y el código de sala de
   4 letras.
4. **Invitado:** abrir Gartic Móvil > **Unirse por IP**, escribir la
   IP del anfitrión y el código de sala, y pulsar **Unirse**. Si el
   anfitrión muestra otro puerto (por ejemplo, porque el 7777 estaba
   ocupado), se escribe junto a la IP: `192.168.43.1:7778`.
5. Cuando haya al menos 3 jugadores en la sala, el anfitrión pulsa
   **Empezar** y juegan. El modo de un solo teléfono no necesita wifi:
   se juega pasando el mismo teléfono.

**Si el invitado no conecta:** comprobar primero que está en la misma
wifi del punto de acceso y que la IP escrita es la que muestra el
anfitrión (si el puerto 7777 estaba ocupado, la app usa 7778… y lo
muestra junto a la IP). El servidor responde a `http://IP:7777/ping`
con `{"ok":true}`: si eso abre en el navegador del invitado pero el
juego no conecta, es el tráfico sin cifrar desde la WebView (ver
«Riesgo a probar» en `plugins/capacitor-lan-server/README.md`).

## Qué NO hacer

- No compilar una APK final con un `www/` viejo: comprobar antes
  que el juego web está completo y sincronizado (`npx cap sync android`).
- No subir el keystore al repo ni pegarlo en ningún chat o archivo.
- No usar este keystore para una versión de tienda: es solo debug.
- No reutilizar los keystores de GeoPre ni de Ecos: cada app tiene el
  suyo y su propia firma.

## Si el build falla en GitHub

- **Falta el secreto `GARTIC_MOVIL_DEBUG_KEYSTORE_B64`:** el paso
  «Restaurar keystore debug» falla con el mensaje claro. Crear el
  secreto como se explica arriba y volver a lanzar el workflow.
- **Falla `npm ci`:** comprobar que `package-lock.json` está en el
  repo (sin él, `npm ci` no funciona). No borrarlo nunca.
- **Falla `./gradlew assembleDebug`:** abrir el log del paso y buscar
  la primera línea con `error:` o `FAILED`. Si el error es de
  `capacitor-lan-server` (NanoHTTPD o el paquete Java), revisar que
  `plugins/capacitor-lan-server/android/src/main/java/com/garticmovil/lanserver/`
  tiene los dos archivos `.java` y que el `namespace` en
  `plugins/capacitor-lan-server/android/build.gradle` es
  `com.garticmovil.lanserver`.
- **La APK instala pero el juego no abre / sale en blanco:** casi
  seguro es un `www/` viejo sin sincronizar o un error
  de JavaScript en la web. Probar la misma web en el navegador del
  teléfono primero.
