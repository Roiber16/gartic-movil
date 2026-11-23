# Revisión final de Gartic Móvil v2.4 — ANTES DE COMPILAR

**Fecha:** 23 nov 2026. **Solo revisión: no se editó ningún archivo de la app.**
**Archivo revisado:** `www/index.html` md5 `4e58b6c5cc074a36c4dcda167d92ee4a` (idéntico al asset de Android), versión 1.4.0 (versionCode 6).

## Veredicto: NO APTA PARA COMPILAR (todavía)

Hay **2 fallos que lo impiden**, los dos en la pantalla de dibujo a 360 px (el ancho del Redmi 10 de Roi) y los dos pequeños y bien localizados. Todo lo demás está verificado y bien. Cuando se corrijan esos dos y se vuelvan a medir esas pantallas, se puede compilar.

### Fallos que impiden compilar

**B1. «Deshacer» con la última letra cortada en TODAS las pantallas de dibujo (360 px).**
La fila Deshacer/Rehacer/Limpiar/✕ Salir va en 1×4 (no en 2×2 como decía el LEEME §2), con botones de 69 px. «Deshacer» necesita 68 px de ancho de texto y solo tiene 61 px (`scrollWidth=68, clientWidth=61`, fuente 13,6 px, padding 10px 4px): la «r» final se ve cortada a la mitad. Se ve en `shots-360/draw.png` y en `undo-zoom.png` (ampliación de la fila). Afecta a las 13 pantallas de dibujo a 360 px (Normal, Adivina y los 14 modos; `clip=True` en `btnUndo` en todas). A 390 px cabe (botones más anchos, `clip=0`).
Arreglo: que «Deshacer» quepa — letra más pequeña o menos padding en esa fila, o la fila en 2×2 como se prometió en el LEEME (cada botón ~150 px).

**B2. La barra roja fija tapa la fila Deshacer/Rehacer/Limpiar/✕ Salir en Cadáver exquisito e Imitación (vista previa).**
La barra roja es `position:sticky; bottom:0`. Cuando la pantalla de dibujo es más alta que el viewport, la barra se sube y se pone encima de la fila de Deshacer:
- Cadáver exquisito a 360 px (docH 896): la fila queda a y=643–691 y la barra empieza a y≈660: se ve solo la mitad de arriba de los botones y la mitad de abajo queda tapada (`shots-360/play-corpse.png`).
- Imitación con vista previa (`draw-memory`) a 360 px (docH 966): la fila queda a y=713–761 y la barra a y≈660–800: la fila queda **tapada del todo** detrás de la barra (`shots-360/draw-memory.png`, `memory-zoom.png` — en la captura no se ve la fila, solo la barra). A 390 px el solape es de solo ~6 px (fila y=670–718, barra desde y=712).
En esos turnos no se puede usar Deshacer, Rehacer, Limpiar ni ✕ Salir (para salir queda el botón atrás de Android, que abre el diálogo de salir). En el resto de modos la pantalla cabe (docH 800–854) y no hay solape.
Arreglo: que la pantalla de dibujo quepa en 800 px también con la vista previa y con la tira de Cadáver (vista previa más baja o plegable, tira de 70 px más compacta), o que el contenido tenga relleno inferior igual a la altura de la barra para que nunca quede nada debajo de ella. Después, re-medir `play-corpse` y `draw-memory` a 360 px: la fila debe quedar visible entera y sin solapes.

## Método

- Chromium headless por CDP (mismo harness de la revisión general, `/tmp/revgen/driver.mjs`, con el puerto de depuración cambiado a 9333 porque el simulador wifi usaba el 9222; la primera pasada se atascó por ese choque de puertos y se descartó): **36 pantallas a 360x800 y 36 a 390x844** (las 18 base + vista previa de Imitación + escritura de Secreto + los 14 modos en mitad de partida + espera wifi), con capturas en `shots-360/` y `shots-390/` y auditoría en `revision-general-360.json` y `revision-general-390.json`. Por pantalla: errores de consola, desbordamiento, tamaño de cada botón, texto cortado, botones bajo el pliegue, solapamientos, flecha atrás, contraste, inglés residual, fuente Baloo 2.
- Partidas automáticas: `VERIFICACION/v2.4/modos/verify_modes.py` (14 modos + Normal + Adivina + navegación).
- Wifi simulado: `VERIFICACION/v2.4/wifi/run-wifi.mjs all` (12 escenarios).
- Sonidos: comprobados en el código (frecuencias) + sondas de la píldora del temporizador y la alarma.
- Comparación visual con las fotos oficiales, ref-01–ref-12 y las 6 imágenes nuevas de Pinterest de Roi (`pinterest/`).

## Lo que está bien (correcciones verificadas una por una)

- **Pantalla de dibujo cabe en 800 px** en Normal, Adivina y 12 de los 14 modos: ¡HECHO! y paleta visibles sin bajar (Normal: ¡HECHO! bottom 645, paleta bottom 722; medido de nuevo con `correcciones/measure.py`: `play-missing` docH 800, `play-corpse` docH 854 con ¡HECHO! visible). Solo fallan Cadáver e Imitación-preview por B2.
- **Rompehielos rehecho:** todos dibujan cada pregunta; el álbum se agrupa por pregunta (`ice-album.png`, `auto-icebreaker.png`: frase de Ana + dibujos de Dan, Carla y Beto juntos). Partida automática 4×4, 0 errores.
- **Pieza que falta rehecha:** el lienzo ya trae pintado el trazo anterior y se dibuja encima (`med-play-missing.png`: la línea anterior está en el lienzo). Partida automática 4×4, 0 errores.
- **Sonidos nuevos en el código, con las frecuencias medidas:** `count(n)` = tic 1245 Hz, 0,25 s por número; `count(true)` = arpegio 784→880→1174 Hz; `AudioFX.tick()` eliminada (no hay tic de 10 s); alarma con `warnAt(total)=máx(2, floor(total/6))`, píldora blanca que se pone amarilla a ~1/6 y tonos 1314+1550 Hz sostenidos (`alarmStart`/`alarmStop`) + vibración [60] al arrancar. Comprobado con sondas: a 52 s de 60 s la píldora es blanca y `alarmKey=null`; a 10 s de 60 s la píldora es amarilla (`timer-pill warn`, píxel #ffc531) y `alarmKey=turn`. Vale en Normal, los 14 modos y Adivina.
- **Cuenta atrás con el rombo del original** (`shots-360/countdown.png`, `med-countdown.png`): rombo violeta con 8 bombillitas amarillas y número verde menta (#2ee6a8), dibujado con CSS (`.cd-diamond`, `.cd-bulb`).
- **Pestaña PREESTABLECIDOS como el original** (`shots-360/modes.png`): activa con fondo blanco y texto verde; inactiva con texto blanco sobre violeta oscuro; «PREESTABLECIDOS» cabe a 360 px. La tarjeta del modo seleccionado lleva borde verde, como el preset seleccionado del original.
- **Reproductor de Animación** (`anim-album.png`): velocidad (1's–10's, 4's por defecto), bucle (Infinito, Adelante y atrás, Una vez), exposición por fotograma (F1·1x…F4·1x) y mensaje del bot «Gartic». En wifi con trazos reales el fotograma se reproduce bien (`wifi/animation-album-ana.png`).
- **Fondo:** 1 fondo + 2N fotogramas (2N+1 pasos); partida automática 4×9, 0 errores.
- **Solo sin límite jugando solo** (`time` devuelve 0 si n≤1); con amigos sigue el tiempo normal.
- **Secreto con censura al describir** (●●● también en la descripción).
- **Inicio con perfil guardado cabe en 800 px** (`med-home.png`, con el perfil de Roi guardado: todo visible). Sin perfil guardado (primera vez) sigue siendo ~1000 px por el editor de avatar — ver «No bloqueante» F4.
- **Selector duplicado arreglado:** las etiquetas son solo «JUGADORES» (el número está en el select, 48 px).
- **Adivina en vivo con contraste:** `.hint-bar` y `.g-players` son tarjetas blancas con tinta oscura (#2a1a5e); aciertos en verde oscuro.
- **Fila de avatares:** 5 avatares caben a 360 px; la tira de jugadores del álbum se parte en dos filas.
- **Herramientas a 48 px** (9 botones); muestras de color (32 px) y puntos de grosor (34 px) como en el original, sin tocar.
- **Temporizador de Cadáver en una sola fila** (título con ellipsis: «Turno de Beto · Cadáver…»).
- **Álbum al límite:** «Nueva partida» visible; «Volver al inicio» queda bajo el pliegue por scroll (pantalla larga por diseño).
- **Textos de Tiempo acortados** («Normal (45/60/45 s)») y subtítulo del inicio escondido a ≤400 px.
- **Ícono C1 instalado:** `assets/icon-1024.png` md5 `c2c205f3…` (Baloo 2 ExtraBold), mipmap correctos.
- **Sin errores ni desbordamientos:** 0 errores de consola y 0 desbordamientos horizontales en las 72 auditorías de pantalla; 0 solapamientos reales salvo B2; flecha atrás siempre SVG (el único «←» del archivo es un comentario CSS); Baloo 2 cargada (700/800); sin inglés visible (ver nota sobre «Score» abajo).
- **Modos:** los 14 + Normal + Adivina pasan sus partidas automáticas de 4 jugadores hasta el álbum, 0 errores, 0 desbordamiento (`modos-verificacion.json` re-generado en esta revisión: Historia 4×4, Obra maestra 4×1, Secreto 4×4, Sándwich 4×4, Puntuación 4×4, Rompehielos 4×4, Imitación 4×4, Complementar 4×4, Pieza que falta 4×4, Cadáver 4×3, Cooperativo 4×6, Animación 4×4, Fondo 4×9, Solo 4×5; Normal `validPermutation:true, randomOrder:true`; Adivina hasta el podio).
- **Wifi:** los 12 escenarios OK, 0 errores (`wifi-resultados.json` re-generado en esta revisión): Normal, Historia, Secreto, Animación, Rompehielos y Pieza que falta (4 jugadores, partida completa, autoría verificada), Adivina (podio en las 4 páginas), jugador que se cae (la partida termina), anfitrión que abandona (aviso visible), expulsión y reingreso, llegada tardía, reconexión.

## Tiempos de carga (medidos de nuevo)

| Qué | Medido |
|---|---|
| Carga inicial (archivo local) | DOMContentLoaded 245 ms, load 246 ms (390 px); 494/497 ms en la pasada a 360 por CDP |
| Apertura con logo de SanBer | menú a los ~2,9 s (sonda de tiempo virtual; la revisión general midió 3.497 ms en tiempo real). Los números 532/270 ms del harness son un artefacto de su doble navegación, no se usan |
| Tocar la apertura para saltarla | menú en ~60–100 ms |
| Cambio de pantalla | 17–54 ms (inicio→ajustes 20–29 ms, ajustes→modos 46–54 ms) |
| Abrir el lienzo de dibujo | ~427–436 ms medidos (incluyen 300 ms de retardo del gancho de prueba; real ~130 ms) |
| Mostrar el álbum / Adivina en vivo | ~354–426 ms (mismo retardo incluido) |
| Fuente Baloo 2 | cargada y aplicada (700/800), woff2 local de 33 KB, `font-display:swap`, sin bloqueo |

Sin pantallas en blanco ni cargas lentas.

## Comparación con las imágenes de Pinterest de Roi (`pinterest/`)

### Logo oficial (`logo-oficial.jpg`) frente a nuestro ícono C1 y al logo de la app
El logo oficial es un teléfono de disco (auricular + base con dial) con «Gartic» en letras redondeadas con contorno blanco y «PHONE» enorme con el dial como O, rodeado de dibujos (lápiz, libreta, auricular, bocadillo) sobre degradado violeta-magenta. Roi señala que el ícono de verdad tiene las vibras de Gartic Phone por el teléfono y la tipografía.
- Nuestro ícono C1 (aprobado por Roi, «Sí, queda así») guarda los dos elementos que señala Roi — teléfono + tipografía — pero con un móvil moderno reconocible (pantalla agrietada, lápiz amarillo dibujando la grieta) y Baloo 2 ExtraBold (redondeada y gruesa, del mismo espíritu que las letras del logo oficial). No copia el teléfono de disco del logo oficial: es marca propia, decisión correcta.
- La apertura usa el logo real de SanBer de Roi (su marca), no un logo de Gartic: también decisión propia y correcta. Dentro de la app el nombre «Gartic Móvil» va en Baloo 2 y la mascota es el pájaro violeta con pico amarillo dibujado en la app.
- Nada que corregir aquí.

### Sala con rejilla 3×3 (`sala-presets-3x3.jpg`) frente a nuestra sala
El original: columna izquierda con PLAYERS 1/14 y huecos EMPTY; pestañas PRESETS (activa, verde sobre claro) / CUSTOM SETTINGS; **rejilla 3×3** de tarjetas con **iconos dibujados** (NORMAL seleccionado con borde verde y engranaje, KNOCK-OFF, SECRET, ANIMATION, ICEBREAKER, COMPLEMENT, SCORE, SPEEDRUN, SANDWICH); botones INVITE (con icono de enlace) / START (con play) abajo; BACK arriba a la izquierda y logo arriba en el centro.
Nuestra sala (`shots-360/modes.png`): avatar TÚ + 4 VACÍO (5 caben a 360 px), selector «JUGADORES 14», pestañas PREESTABLECIDOS (activa, verde sobre blanco) / AJUSTES PERSONALIZADOS, **lista vertical** de tarjetas grandes con **emojis** y descripciones largas, tarjeta seleccionada con borde verde, INVITAR/EMPEZAR fijos abajo y «Volver al inicio».
- Lo que ya coincide: jugadores con VACÍO, selector 14, pestañas con el mismo patrón, tarjeta seleccionada con borde verde, INVITAR/EMPEZAR con iconos.
- Lo que difiere: lista vertical en vez de rejilla 3×3, emojis en vez de iconos dibujados, sin BACK arriba a la izquierda (tenemos «Volver al inicio» abajo y el botón atrás).
- Qué se puede acercar sin romper nada: pasar las tarjetas a **rejilla 3×3 compacta** (solo CSS, sin tocar el motor) y marcar la seleccionada con borde verde + engranaje (ya tiene el borde). Los iconos dibujados necesitan arte nuevo en el estilo de la app (pendiente conocido, no trivial). **SPEEDRUN no se pide como modo nuevo:** aparece en esa captura como preset antiguo, pero en la lista actual de 15 no está; es una variante recreable con ajustes (tiempo rápido), como ya dice el informe de análisis.

### Álbumes (`album-wine-glass.jpg`, `album-douglass.jpg`, `album-milly.jpg`, `album-purplekog.jpg`) frente a nuestro álbum
El original (móvil): tira de jugadores arriba (avatares con nombre, corona en el dueño), título «X'S ALBUM» en verde con contorno oscuro, tarjetas en formato chat (nombre del autor arriba en mayúsculas, avatar a un lado alternando izquierda/derecha, bocadillos blancos con el texto centrado o el dibujo en lienzo blanco), divisor «— END OF X'S ALBUM —» al final, y botones de compartir + BACK / NEXT (blancos, redondeados, texto violeta en negrita con iconos). En escritorio añade una columna PLAYERS a la izquierda con el dueño resaltado en verde.
- Nuestro álbum (`shots-360/album.png`): título «ÁLBUM DE ANA» en verde, tira de jugadores (se parte en dos filas), tarjetas en formato chat con avatar + nombre + texto o dibujo, «… (dibujo en blanco)» cuando el dibujo está vacío, botones «Álbum anterior/siguiente» con flechas SVG y «Volver a jugar» / «Nueva partida». El formato es fiel.
- Lo que falta (no bloqueante, pero visible comparando): **el divisor «— FIN DEL ÁLBUM DE ANA —» al final** (trivial de añadir, mucho valor de fidelidad) y **el botón de compartir** (en el original comparte el álbum; en la app haría falta el plugin Share de Capacitor; el botón «.GIF» sigue pendiente por separado). El nombre del autor va dentro de la cabecera de la tarjeta, no encima del bocadillo en mayúsculas como en el original, y los avatares van siempre a la izquierda (no alternan): cosmético.

## No bloqueante (para después de compilar, o en la misma tanda si da tiempo)

- **F3. Herramientas en 3 filas 4+1+4 en vez de 2 filas 5+4.** El salto se pone tras la 5.ª herramienta, pero a 360 px solo caben 4 botones de ~75 px por fila, así que «Círculo» cae solo a la segunda fila y se estira a todo el ancho (`shots-360/draw.png`). Se ve raro pero funciona y nada se corta. Arreglo: botones más estrechos, letra más pequeña, o salto tras la 4.ª (4+5).
- **F4. Inicio en primera vez (sin perfil guardado) a 360 px:** docH 1002, «Cómo se juega» y «⚙️ Ajustes» bajo el pliegue (y=821) y botones de las filas a 44–47 px (no 48 px como dice el LEEME §6: `#screen-home .btn-row .btn{min-height:44px}` a ≤400 px). Con perfil guardado (el caso del teléfono de Roi) cabe en 800 px y todo se ve. Arreglo: subir las filas a 48 px y compactar un poco más el editor de primera vez.
- **F5. Álbum sin divisor «FIN DEL ÁLBUM DE X» ni botón de compartir** (ver Pinterest arriba).
- **F6. Modos en lista vertical con emojis** en vez de rejilla 3×3 con iconos dibujados (ver Pinterest arriba).
- **F7. `AudioFX.chime()` reusa las frecuencias de la alarma (1314+1550 Hz, 0,5 s) para los sonidos de fin de ronda/álbum.** No es el «¡ya!» de la cuenta atrás (ese ya no existe), pero usa los mismos tonos que la alarma de poco tiempo y puede confundirse con ella. Valorar otro sonido para el fin de ronda.
- **F8. Sin `onerror` en las imágenes del álbum.** En juego real las imágenes son dataURL de lienzo y se ven bien (comprobado en wifi con trazos reales). Pero en las capturas automáticas se ven iconos de imagen rota porque el autotest envía la imagen falsa `data:image/png;base64,AAA`; si alguna vez una imagen llega corrupta por wifi, el álbum mostraría el icono roto en vez del «… (dibujo en blanco)». Poner un `onerror` que sustituya por el texto de dibujo en blanco.
- **F9. «ANÓNIMO» verde sobre blanco (contraste 2,28).** Es la pestaña activa, igual que en el original (verde sobre claro). Fiel al original; el ratio es bajo pero es el diseño del original.
- **F10. «Volver al inicio» bajo el pliegue en Crear sala (y=887 a 360, y=876 a 390) y en el álbum (y=833 a 360).** Botón secundario; el scroll ahí es normal y aceptado.
- **F11. «Score» marcado una vez por el detector de inglés en `play-score`.** No reproducible: un volcado directo del texto visible de esa misma pantalla no contiene «Score» (la UI dice «Puntuación» en todas partes). Probablemente un elemento transitorio. No es un fallo.
- **F12. El logo de SanBer en la apertura (194x194 mostrado a 230 px) se ve un poco blando** y con fondo negro cuadrado. Es el logo real de Roi; solo cambiarlo si él lo pide.

## Pendiente solo con dos teléfonos reales (no se puede probar aquí)

Hotspot de verdad entre dos Redmi, la IP que anuncia el anfitrión (192.168.43.x), el plugin LanServer real, dibujar con el dedo, sonidos y vibración a oído y por wifi, ícono C1 en el launcher, y el problema de instalación de la v2.1 (reiniciar, espacio libre, instalar desde Chrome, probar si la v2 vuelve a instalar).

## Archivos de esta revisión

- Este informe: `VERIFICACION/v2.4/revision-final/README.md`
- Capturas 360x800: `VERIFICACION/v2.4/revision-final/shots-360/` (36 PNG)
- Capturas 390x844: `VERIFICACION/v2.4/revision-final/shots-390/` (36 PNG)
- Auditoría 360: `VERIFICACION/v2.4/revision-final/revision-general-360.json`
- Auditoría 390: `VERIFICACION/v2.4/revision-final/revision-general-390.json`
- Ampliaciones: `VERIFICACION/v2.4/revision-final/undo-zoom.png` («Deshacer» cortado), `VERIFICACION/v2.4/revision-final/memory-zoom.png` (barra tapando la fila)
- Imágenes de Pinterest de Roi: `VERIFICACION/v2.4/revision-final/pinterest/`
- Modos re-verificados: `VERIFICACION/v2.4/modos/modos-verificacion.json`
- Wifi re-verificado: `VERIFICACION/v2.4/wifi/wifi-resultados.json`
- Nota: la primera pasada del harness se atascó porque usaba el puerto de depuración 9222, que ya ocupaba el simulador wifi; se mató y se repitió con el puerto 9333 (51 s a 360, 50 s a 390). Las capturas de correcciones `med-play-missing.png` y `med-play-corpse.png` mostraban la píldora amarilla a 0:51–0:52: eran de un estado intermedio del archivo; re-medidas con el archivo actual la píldora es blanca a 52 s y amarilla solo a ≤10 s, como debe ser.
