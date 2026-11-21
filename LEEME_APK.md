# Gartic Móvil — APK Android

> Nota: antes se llamaba Teléfono Roto; Roi lo renombró a Gartic Móvil
> el 21 nov 2026. El keystore es el mismo de antes (misma huella SHA-256),
> solo cambió el nombre del archivo.

Empaquetado con Capacitor de la app web de Gartic Móvil (juego offline
tipo teléfono roto: dibujar, describir y reírse con amigos sin internet).
Modo Normal fiel, 3-8 jugadores, y Adivina el dibujo con puntos,
wifi local por hotspot (servidor local puerto 7777) + modo de un solo
teléfono.

- **appId:** `cu.roi.garticmovil`
- **Nombre:** Gartic Móvil
- **Versión:** 1.1.1 (versionCode 3, versionName 1.1.1)

## Novedades de la v2.1 (1.1.1) — solo el ícono

- El ícono v2 se veía bien a 1024 px pero en el launcher de MIUI (Redmi 10
  de Roi) el nombre no se veía: el diseño estaba pegado a los bordes y el
  launcher solo enseña la zona segura central del ícono adaptativo (cuadro
  central de 66 dp de 108 dp, el 61% del lienzo).
- Corrección: todo el contenido ("Gartic", auricular partido con rayo,
  "MÓVIL") cabe dentro del cuadro central de 626 px, con márgenes de
  22-30% por cada lado. Medido: contenido en x 240-800, y 294-744.
- Verificado con máscaras en `VERIFICACION/v2.1/`: simulación MIUI (recorte
  central 626 px), squircle y círculo, a 48, 96 y 192 px — el nombre se lee
  completo en todas. Script: `scripts/make-icon-v2.1.py`.
- El juego no cambió nada en esta versión.
- **Peso:** la parte web (`www/`) pesa ~132 KB y los assets ~72 KB;
  la APK final quedará muy por debajo del límite de 50 MB.

## Novedades de la v2 (1.1.0)

### 1. Rediseño visual fiel a Gartic Phone
- Fondo degradado vertical violeta oscuro arriba (#5b1fa6) a magenta/rosa
  abajo (#d63384) en TODAS las pantallas, igual que en las fotos de Roi.
- Logo propio: teléfono blanco con lápiz amarillo (SVG dibujado, no el
  logo "Gartic PHONE"); mascota pájaro violeta con pico amarillo y ojos
  grandes dibujada con formas CSS (sin imagen externa).
- Tarjetas de modo en lavanda claro (#e6dcff) con icono a la izquierda,
  título violeta oscuro en negrita y descripción violeta; la seleccionada
  lleva borde verde.
- Botones grandes blancos redondeados con borde violeta y texto violeta
  oscuro; EMPEZAR lleva el play verde (#2ee6a8).
- Pantalla inicial con pestañas ANÓNIMO (verde) / VERIFICADO, avatar
  circular con botón ↻ y campo de apodo. El apodo y el avatar se guardan
  en el teléfono (localStorage) y se recuerdan al abrir la app; VERIFICADO
  avisa que necesita internet y no está disponible offline.
- Lobby con fila de avatares arriba (anfitrión con corona 👑) y VACÍO en
  los huecos; barra violeta con el selector de jugadores (en wifi, hasta
  14 como en el original; en un solo teléfono, 3-8 en Normal y 2-8 en
  Adivina).
- Pestañas PREESTABLECIDOS / AJUSTES PERSONALIZADOS (activa en verde) en
  Modos: Tiempo, Secuencia (Escribir, Dibujar), Turnos, Sigue dibujando,
  Tablero de puntuaciones y Secretismo. Solo el creador de la sala cambia
  los ajustes; los que se unen solo los ven.
- Pantalla de dibujo con barra superior violeta ("TURNO 2/4 · DIBUJA ESTA
  FRASE"), lienzo blanco con marca de agua tenue "Gartic Móvil", y barra
  inferior roja/coral (#e94f5a) con lápiz, paleta (negro, grises, azul,
  verde, rojo, naranja, amarillo, blanco, celeste) y botón ✔ ¡Listo!
  violeta. Selector de grosor por círculos y deslizador vertical de
  opacidad al lado izquierdo del lienzo, en los dos modos. En pantallas
  de 360 px la fila de controles (grosor, color personalizado, zoom) se
  esconde: el grosor queda en los círculos laterales y el zoom no está
  disponible en ese ancho.
- Misma tipografía gruesa de la v1 (Baloo 2 / Nunito con fallback del
  sistema, sin CDN), sin aspecto IA.

### 2. Nuevo modo "Adivina el dibujo" (jugable en v2)
Mecánica de Gartic.io, pero con la estética violeta-magenta única de
esta app en todo (nada de fondo azul ni botones amarillos/celestes de
io; de io solo la disposición: jugadores a un lado, chat al otro, pista
arriba y barra de tiempo).
- Por turnos, un jugador dibuja una palabra secreta (elige 1 de 3) y los
  demás ven el dibujo en vivo y adivinan en el chat.
- 75 palabras en español, 15 por tema: Animales, Comida, Objetos,
  Lugares, Deportes. El creador puede elegir los temas; sin temas, van
  todos. Las palabras no se repiten en la misma partida.
- Puntos por orden de acierto: 10 al primero, luego 8, 6, 4 y 2 (del 6.º
  en adelante, 2). El dibujante gana +5 por cada jugador que acierta
  (con 7 adivinadores, hasta +35 en una ronda).
- Pista con guiones arriba ("_ _ _ _"); se revela 1 letra a 1/3 del
  tiempo de ronda y otra a 2/3 (en rondas de 60 s: a los 20 s y 40 s).
- Tiempo por ronda configurable (30/60/90/120 s), por defecto 60 s.
- Cada jugador dibuja una vez; al final, podio con 1.º, 2.º y 3.º.
- En un solo teléfono (simplificado): el dibujante dibuja, luego se pasa
  el teléfono y cada jugador escribe su adivinanza sin ver la palabra,
  con 30 s cada uno y los mismos puntos. Un acierto se muestra en el
  chat como "¡X acertó! +N" SIN la palabra, para no revelarla a los
  siguientes.
- Por wifi local: el dibujante sube sus trazos en lotes al anfitrión y
  los demás los ven sondeando el estado cada ~0,9 s (en vivo con ~1 s de
  retraso). El plugin LanServer NO empuja nada (no hay WebSocket ni SSE):
  para trazos instantáneos haría falta añadir SSE o WebSocket al plugin.
  El anfitrión atiende en JS los endpoints `/api/guess/*` (ver
  `plugins/capacitor-lan-server/README.md`); no hizo falta tocar Java.
- Pantalla "SALAS LOCALES": solo salas wifi cercanas, sin salas
  públicas (la sala de este teléfono si la hay, o unirse por IP).
- Diálogo de salir de la sala con la misma estética violeta (círculo
  amarillo con 🚪, NO blanco y SÍ, SALIR verde).
- El anfitrión wifi ya responde también a los endpoints del modo Normal
  (`/api/join`, `/api/state`, `/api/submit`, `/api/start`): en la v1 el
  servidor arrancaba pero nadie respondía en JS. Los clientes Normal
  sondean el estado y juegan su turno cuando les toca.

### 3. Ícono nuevo
Teléfono roto: auricular clásico partido en dos con un rayo amarillo
en la rotura, "Gartic" arriba en blanco y "MÓVIL" en grande abajo en
amarillo, sobre degradado violeta a magenta. Colores planos, bordes
gruesos, sin aspecto IA. Generado con Python/PIL
(`scripts/make-icon-v2.py`): `assets/icon-1024.png` y todos los
`mipmap-*` (launcher, round y foreground) en `android/...` y en
`assets/res/...`. Verificado a 48 y 96 px (se lee el nombre y el
auricular partido).

## ✅ www completo y verificado (v2)

El `www/index.html` actual está **completo y verificado**: pesa
135.401 B, termina en `</html>` y contiene la partida jugada entera
(modo Normal y Adivina el dibujo, en un solo teléfono y por wifi local).

### Verificación v2 (Chromium headless, 360x800)
Capturas en `VERIFICACION/v2/` (todas a 360x800 reales, con el binario
`chromium_headless_shell`; el Chrome completo impone un mínimo de 500 px
de ancho de layout y sus capturas salen recortadas, no usarlo para esto):
`shot-home.png`, `shot-modes.png`, `shot-setup.png`, `shot-draw.png`,
`shot-guess-live.png`, `shot-guess-draw.png`, `shot-podium.png`,
`shot-rooms.png`, `shot-album.png`, más `icono-48.png`, `icono-96.png`
e `icono-192.png`. La página lleva ganchos de prueba (`#shot=<pantalla>`
y `#auto=normal|guess`) que escriben el resultado en `#testResult`.
- Partida Normal automática de 4 jugadores en un solo teléfono:
  0 errores de consola, 0 desbordamiento horizontal, 4 álbumes con
  4 eslabones cada uno.
- Ronda automática de Adivina (4 jugadores): 0 errores, 0
  desbordamiento, podio correcto (puntos 10/8 por orden de acierto y
  +5 al dibujante por acierto, comprobados a mano).
- Botón ✔ ¡Listo! visible sin desplazar en dibujo Normal (y=699) y en
  dibujo de Adivina (y=666), a 360x800.
- 0 errores de consola y 0 desbordamiento horizontal en las 9 pantallas.

### Qué NO se pudo probar sin el teléfono real de Roi
- El wifi local con dos teléfonos reales (hotspot, unirse por IP,
  trazos en vivo y chat de Adivina, y el turno Normal por wifi): el
  código del anfitrión y del cliente está implementado, pero solo se
  probó en un navegador, sin el plugin LanServer ni dos dispositivos.
  Tampoco se probó el tráfico sin cifrar desde la WebView (ver «Riesgo
  a probar» en `plugins/capacitor-lan-server/README.md`).
- El dibujo táctil con el dedo, el rendimiento del lienzo y los sonidos
  (no hay sonidos) en el Redmi 10.
- El ícono instalado en el launcher (solo se vio a 48/96 px en
  capturas); el tamaño y el recorte del launcher lo decide Android.
- La APK v2 todavía NO se ha compilado: hay que subir los cambios y
  lanzar el workflow en GitHub (ver abajo).

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
