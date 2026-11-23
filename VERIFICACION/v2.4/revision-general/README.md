# Revisión general de Gartic Móvil v2.4

**Fecha:** 23 nov 2026. **Solo revisión: no se editó ningún archivo de la app.**

## Método

- Chromium headless (HeadlessChrome 134) por CDP y por `--dump-dom`, a **360x800** y a **390x844**.
- **37 capturas a 360x800**: las 18 pantallas base (apertura, inicio, modos, configurar, ajustes, cómo se juega, unirse, crear sala, cuenta atrás, pasar el teléfono, escribir, describir, dibujar, dibujo con panel, álbum, Adivina-dibujar, Adivina-en vivo, podio, salas) + vista previa de Imitación + escritura de Secreto + los 14 modos en mitad de partida + espera wifi + pestaña de ajustes personalizados.
- **25 capturas a 390x844**: 12 base + 13 de juego (dibujar, panel, álbum, Adivina, podio, salas, vista previa, Secreto, Cadáver, Pieza que falta, Sándwich, Animación).
- Por pantalla: errores de consola, desbordamiento horizontal, tamaño medido de cada botón/select/input (mínimo ~48 px), texto cortado, botones bajo el pliegue, solapamientos, flecha atrás (SVG, nunca el glifo ←), contraste aproximado, textos en inglés, fuente Baloo 2 y contenido vacío.
- Tiempos medidos en tiempo real (no virtual): arranque, apertura, salto con toque, cambios de pantalla, apertura del lienzo y del álbum, carga de la fuente.
- Lo visual se comparó a ojo con las fotos oficiales (`workspace/user/files/1000376637_0_bfgp.jpg` … `1000376647_9_uo4i.jpg`, sala y barra de dibujo) y con `VERIFICACION/v2.3-referencias/ref-01`–`ref-12`.

## El archivo cambió durante la revisión (trabajo de wifi en paralelo)

El trabajo de wifi estaba editando `www/index.html` mientras se revisaba:

| Momento | md5 de `www/index.html` |
|---|---|
| Al empezar la revisión | `4798828c…` |
| Durante la primera pasada a 360 | `42918892…` |
| Al terminar (estable, sin cambios en 45 s) | `e934f66c…` |

Las mediciones clave (paleta, ¡HECHO!, inicio, álbum, crear sala) se **re-comprobaron en el archivo final** con `final_check.py` (`final-check-e934f66c.json`) y coinciden con la primera pasada (dibujar: docH 936→958 px; el resto igual). Las capturas de `shots-360/` son de la primera pasada y de la repetición; los números del informe son los del archivo final.

## Tiempos medidos

| Qué | Medido |
|---|---|
| Carga inicial (archivo local) | DOMContentLoaded 240 ms, load 241 ms |
| Apertura con logo de SanBer (3 s, saltable) | Se va sola a los ~3,5 s desde la navegación (3 s + fundido 0,4 s); medida fina: 3497 ms desde navegación, 3274 ms desde load |
| Tocar la apertura para saltarla | Menú en ~60 ms tras el toque (+ fundido de 0,35 s) |
| Cambio de pantalla | 20–82 ms (inicio→ajustes 35 ms, ajustes→modos 82 ms por renderizar las 15 tarjetas, resto ~30 ms) |
| Abrir el lienzo de dibujo | ~428 ms desde navegación (incluye 300 ms de retardo del gancho de prueba; real ~130 ms) |
| Mostrar el álbum | ~426 ms (mismo retardo incluido) |
| Adivina en vivo | ~422 ms |
| Fuente Baloo 2 | Cargada y aplicada (checks 700/800/400 correctos, estado `loaded`); woff2 local de 33 KB con `font-display:swap`, sin bloqueo. El tiempo de descarga no se puede medir en `file://` (las entradas de `performance` salen vacías en este entorno) |
| Animaciones | `fadeIn` 0,18 s al cambiar de pantalla, fundido de apertura 0,35 s, toast 0,2 s, velo de Secreto 1,2 s. Sin tirones medibles en headless |

**Conclusión de tiempos:** la app arranca y cambia de pantalla rápido. No hay pantallas que se queden en blanco ni cargas lentas. El único problema de "fluidez" real es de diseño, no de velocidad: la pantalla de dibujo es más alta que el viewport y hay que hacer scroll en mitad de la partida (ver A1 y A2).

## Lo que está bien

- **0 errores de consola y 0 desbordamientos horizontales** en las 37 pantallas a 360 y en las 25 a 390.
- **Ningún texto cortado en botones, ningún botón fuera por los lados, ningún solapamiento real.** (Los 3 avisos de solape en Modos son falsos positivos: la lista tiene scroll propio y los rectángulos medidos incluyen la parte recortada por el contenedor.)
- **Flecha atrás siempre SVG** (chevron `M15 5 L8 12 L15 19`, trazo 2,5, en «Álbum anterior/siguiente»); no hay ningún glifo «←» en toda la app. El botón atrás de Android va por `goBack()` con su pila y su aviso.
- **Baloo 2 cargada y aplicada** en toda la app (700/800). Degradado violeta→magenta (`#5b1fa6`→`#d63384`), tarjetas lavanda `#e6dcff`, verde `#22c55e`, botones blancos con borde violeta: fiel a las fotos oficiales.
- **Ícono C1 instalado**: `assets/icon-1024.png` md5 `c2c205f3…`, mipmap 48/72/96/144/192 correctos. **Logo de SanBer real** en la apertura. **Marca de agua «Gartic Móvil» visible** en el lienzo.
- **Ajustes completos y funcionando**: Tiempo (Normal/Rápido/Lento), Secuencia, Turnos, Sigue dibujando, Tablero de puntuaciones y Secretismo en la pestaña AJUSTES PERSONALIZADOS (el cambio de pestaña funciona, `shots-360/modes-custom.png`); sonido y vibración en Ajustes, con interruptores que se guardan en el teléfono.
- **Pantallas de juego fieles al original**: «HEY, ¡ES HORA DE DIBUJAR!», «EMPIECE A ESCRIBIR UNA HISTORIA», «Pásale el teléfono a…», álbum en formato chat con autor por eslabón y orden aleatorio, podio con medallas.
- **Sin textos en inglés**: «DESCRIBE ESTA ESCENA» es español del original; «Score» no aparece como texto visible en el archivo final.
- **Sin pantallas vacías ni huecos raros**: todas las pantallas tienen contenido; la espera wifi muestra su mensaje.

## Correcciones priorizadas

### ALTA

**A1. La paleta de colores no se ve al dibujar sin bajar con el dedo.**
En Normal, Adivina y los 14 modos: la 1.ª fila de colores queda justo en el borde del pliegue (y=801–823 a 360x800; y=817–844 a 390x844) y la 2.ª fila queda fuera (y=833–870 a 360; y=844–881 a 390). Para cambiar de color en mitad del dibujo hay que hacer scroll. Causa: la pantalla de dibujo mide 936–958 px de alto en un viewport de 800 px (cabecera + progreso + cartel + frase + rejilla 3×3 de herramientas + lienzo + Deshacer/Rehacer/Limpiar/Salir + barra roja con la paleta en 2 filas). En la foto oficial la paleta va dentro de la barra roja y se ve entera, porque el original no tiene la rejilla 3×3 ni la fila Deshacer encima.
Propuesta: compactar la pantalla para que quepa en 800 px (lienzo más bajo; rejilla de herramientas en 2 filas; o paleta en una sola fila de 6 colores + color actual), o fijar la barra roja abajo con `position:sticky`.

**A2. El botón ¡HECHO! queda bajo el pliegue en varios modos.**
- Imitación (vista previa): ¡HECHO! a y=954; Deshacer/Rehacer a y=822; docH 1145 px.
- Pieza que falta (vista previa): ¡HECHO! a y=986; Deshacer/Rehacer a y=854; docH 1177 px.
- Cadáver exquisito (franja): ¡HECHO! a y=884; Limpiar/✕ Salir a y=816; docH 1075 px.
- Sándwich, Puntuación, Rompehielos y Cooperativo: ¡HECHO! cortado 25 px (y=777, h=48, bottom 825).
No se puede terminar el turno sin bajar con el dedo. Misma causa raíz que A1, agravada por la vista previa y la franja.
Propuesta: mismo arreglo que A1; en Imitación y Pieza que falta, hacer la vista previa más baja o plegable.

**A3. La pestaña PREESTABLECIDOS se lee mal.**
Texto verde `#22c55e` sobre violeta oscuro, contraste 2,28, y a 360 px la palabra desborda la pestaña y se ve cortada por los bordes (captura `shots-360/modes.png`). A 390 px cabe en una línea pero el contraste sigue flojo. En el original la pestaña activa es AJUSTES PERSONALIZADOS (verde sobre fondo claro) y PREESTABLECIDOS va en blanco sobre violeta oscuro.
Propuesta: copiar el original (activa: fondo claro + texto verde; inactiva: blanco sobre violeta oscuro) y/o bajar el tamaño de letra para que «PREESTABLECIDOS» quepa a 360 px.

### MEDIA

**M1. En el inicio, «Cómo se juega» y «⚙️ Ajustes» quedan bajo el pliegue** (y=867; docH 1067 px a 360). Hay que bajar para llegar a Ajustes (sonido/vibración).
Propuesta: compactar el inicio para que quepa en 800 px (p. ej. rejilla de avatares o botones más compactos).

**M2. El selector duplica el 14: «14 JUGADORES 14 ⌄»**, en Modos y en Crear sala (etiqueta + valor del select).
Propuesta: un solo selector con el texto «14 JUGADORES».

**M3. En Adivina en vivo, los nombres y puntos de los jugadores van en blanco sobre lavanda claro**, poco contraste; la barra de pista («ADIVINA LA PALABRA _ _ _ _») va en blanco sobre gris-lavanda, floja.
Propuesta: texto en tinta oscura (`#2a1a5e`) en la lista de jugadores y en la barra de pista.

**M4. En el álbum, «Nueva partida» queda al límite** (bottom 809 a 360, 9 px bajo el pliegue) y «Volver al inicio» bajo el pliegue (y=817).
Propuesta: compactar el álbum o aceptar el scroll (es una pantalla larga por diseño).

**M5. La cuenta atrás no se parece a la del original.** La app muestra un número violeta grande en tarjeta lavanda; el original es un rombo violeta con bombillitas amarillas y número verde menta (verificado en vídeo, `VERIFICACION/v2.4/cuenta-atras/`). El sonido también está pendiente (tic ~1245 Hz por número + arpegio al terminar, sin «¡ya!»).
Propuesta: dibujar el rombo con CSS y el número en verde menta.

**M6. Fila de avatares (inicio, modos, crear sala): a 360 px el 5.º avatar queda cortado por la mitad.** La fila hace scroll horizontal (`scrollWidth` 556 > `clientWidth` 304) pero sin pista visual. A 390 px caben los 5.
Propuesta: que quepan 5 avatares a 360 px (más pequeños) o añadir una pista de scroll.

**M7. Herramientas de dibujo a 44 px (9 botones), puntos de grosor a 34 px y muestras de color a 32 px**, por debajo del mínimo de 48 px. Las muestras y los puntos son como en el original; las 9 herramientas deberían ser 48 px.

**M8. En Crear sala, «Volver al inicio» queda bajo el pliegue** (y=890, secundario). En el archivo final INVITAR/EMPEZAR ya caben en la primera vista. Aceptable; queda anotado.

**M9. En Cadáver exquisito el temporizador baja a una segunda fila** porque el título es largo («Turno de Beto · Cadáver exquisito»). Menor.

### BAJA

**B1. Logo de SanBer en la apertura**: imagen de 194x194 mostrada a 230 px (un poco blanda) y con fondo negro cuadrado sobre el degradado. Es el logo real de Roi; solo cambiarlo si él quiere.

**B2. «ÁLBUM DE ANA» en verde sobre lavanda** (contraste 1,74): se lee bien por ser grande y en negrita, y es como el original. Opcional: un verde más oscuro.

**B3. Iconos de modo con emojis** (no dibujados como los del original). Conocido.

**B4. «▶» verde sobre blanco (2,28) en EMPEZAR**: decorativo junto al texto, como el original.

**B5. Interruptores de Ajustes de 26 px** (nativos): la fila entera es táctil. Bien.

**B6. Botón ↻ (cambiar pájaro) de 44x44.** Bien.

**B7. La opción de Tiempo «Normal (45 s escribir · 60 s dibujar · 45 s describir)» se corta en el select** («…60 s dibu»).
Propuesta: texto más corto, «Normal (45/60/45 s)».

**B8. El subtítulo del inicio «Dibujar · describir · adivinar — sin internet» se parte en dos líneas a 360 px** («sin» / «internet»). Menor.

## Falsos positivos y cosas que NO son fallos (para no corregir por gusto)

- **Contraste 1,0 en emojis y en textos sobre fondos translúcidos**: el medidor compara contra el fondo translúcido en sí, no contra el degradado que hay detrás. En la captura se ve bien: texto blanco sobre degradado violeta, «ANÓNIMO» verde sobre pestaña violeta, etc. La única excepción real es A3 y el verde del álbum (B2).
- **«Describe» no es inglés**: es «DESCRIBE ESTA ESCENA», español del original. «Score» no aparece como texto visible en el archivo final.
- **El select de modo wifi vacío en la captura de Crear sala** es un artefacto del gancho de prueba (`#shot=create` no llama a `syncWifiModeButtons()`); en el flujo real `createWifiRoom()` sí lo llena. Igual que el código «• • • •» y el «Generando la sala…», que en el navegador no tienen servidor local.
- **Los modos bajo el pliegue en la lista** son normales: la lista tiene scroll propio y se llega a todos.
- **«Generando la sala…» y «Dirección de la sala: —»** en el navegador son esperados (sin plugin LanServer); en la APK instalada aparece la IP.

## Archivos

- Este informe: `VERIFICACION/v2.4/revision-general/README.md`
- Capturas 360x800: `VERIFICACION/v2.4/revision-general/shots-360/` (37 PNG: 35 pantallas + espera wifi + ajustes personalizados)
- Capturas 390x844: `VERIFICACION/v2.4/revision-general/shots-390/` (25 PNG)
- Auditoría 360 (primera pasada): `VERIFICACION/v2.4/revision-general/revision-general-360.json`
- Auditoría 390 (resto de juego): `VERIFICACION/v2.4/revision-general/revision-general-390-extra.json`
- Tiempos finos (apertura y fuente): `VERIFICACION/v2.4/revision-general/timing-fino.json`
- Comprobación final en el archivo estable (`e934f66c…`): `VERIFICACION/v2.4/revision-general/final-check-e934f66c.json`
- Scripts de la revisión (no son parte de la app): `/tmp/revgen/driver.mjs`, `/tmp/revgen/final_check.py` (en `/tmp`, se pierden al reiniciar)
