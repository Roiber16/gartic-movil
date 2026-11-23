# Revisión visual y de reglas de los 15 modos — Gartic Móvil v2.4

**Fecha:** 23 nov 2026. **Alcance:** SOLO revisión, no se tocó el código de la app.
**Fuentes del original:** `garticphone.com` (portada, 6 pasos), wiki de fans
`gartic-phone.fandom.com/wiki/Game_modes` (15 presets con descripciones oficiales),
`/wiki/Album`, `/wiki/Icebreaker`, `/wiki/Knock-Off`, TheGamer
«All Game Modes in Gartic Phone, Ranked» (ene 2022, act. con Background y
Complement), y el análisis del proyecto en
`~/workspace/research_notes/gartic-phone-analisis-completo-20261121-1525/report.md`.
**Implementación revisada:** `www/index.html` (`MODE_SPECS` + `specFor()`, líneas
~640–700 y el motor de cadenas), y las capturas de verificación en
`VERIFICACION/v2.4/` y `VERIFICACION/v2.4/modos/`.

**Fotos de referencia guardadas en esta carpeta:**
- `ref-lobby-player-me.png` — sala del original (PRESETS, 14 PLAYERS, EMPTY,
  INVITE/START). Fuente: player.me (2023).
- `ref-lobby-ensigame.jpg` — sala del original, variante con Exquisite Corpse
  marcado NEW!. Fuente: ensigame.com.
- `ref-album-dailymotion.jpg` — álbum del original («LIGHT'S ALBUM», lista de
  jugadores a la izquierda, chat a la derecha). Fuente: dailymotion.
- `ref-corpse-thumb.jpg` — miniatura del modo Cadáver exquisito («FINISH BY
  DRAWING THE LEGS»). Fuente: YouTube `7Kl_sEAML4M`.
- `ref-icon-*.svg` — los 15 iconos oficiales de modo de la wiki (solo referencia;
  son assets del juego, NO se deben incrustar tal cual en la app).

**Leyenda de veredictos:** ✅ fiel · ⚠️ difiere (hay que corregir) ·
➖ falta (no existe en la app) · 🔶 aproximación documentada (el original no
publica el dato y la app eligió una regla propia y lo dice en el LEEME).

## Resumen por modo

| # | Modo | Veredicto | Diferencia principal |
|---|---|---|---|
| 1 | Normal | ✅ fiel | Nada. Álbum aleatorio, eslabón anterior, sin puntos. |
| 2 | Imitación (Knock-Off) | ✅ fiel | Reloj que se acorta (60−10/ronda, mín. 20 s) es aproximación sin números oficiales; la mecánica (ver el dibujo solo antes de trazar) es fiel. |
| 3 | Animación | ⚠️ difiere | Reproductor sin velocidades (1's–10's) ni modos de bucle; sin exposición de fotograma (0x/1x/2x/3x); sin mensaje del bot «Gartic». |
| 4 | Rompehielos (Icebreaker) | ⚠️ difiere | **La más importante.** En el original cada frase la dibujan TODOS y al final se muestran juntos todos los dibujos de la misma frase. La app hace 1 dibujo por frase (cadena de 2 pasos). La propia tarjeta del modo promete «se muestran juntos todos los dibujos» y no se cumple. |
| 5 | Cadáver exquisito | ✅ fiel | Falta solo el detalle de los colores usados antes (esquina inferior izquierda del original). |
| 6 | Complementar | ✅ fiel | Líneas iniciales no borrables y 15 s en el primer turno, fieles. |
| 7 | Obra maestra | ✅ fiel | 1 turno sin límite, fiel. |
| 8 | Historia (Story) | ✅ fiel | Solo escritura, frase anterior visible, fiel. |
| 9 | Pieza que falta (Missing Piece) | ⚠️ difiere | **La segunda más importante.** En el original se COMPLETA el dibujo incompleto (se dibuja encima) y al pasar se borra la parte más antigua. La app muestra el dibujo anterior como vista previa que desaparece y el jugador dibuja en un lienzo en blanco: nunca se añade a nada y nunca se «pierde» una parte. |
| 10 | Secreto (Secret) | ✅ fiel (con 2 matices) | El dibujo a describir SÍ se ve (bien). Falta censurar el texto al describir (en el original tus palabras salen como ● también ahí); los trazos se desvanecen en vez de ser invisibles (aproximación razonable). |
| 11 | Cooperativo (Co-Op) | ✅ fiel | 6 turnos (1 escribir + 5 dibujar), dibujo acumulado, fiel. Limitación conocida: formas y cubo no se guardan como trazos y no aparecen en el acumulado. |
| 12 | Puntuación (Score) | 🔶 aproximación | El criterio del original es opaco (las propias guías dicen que no se sabe cómo decide el punto). La app usa votación del grupo, documentada como diseño propio. No es el original, pero es la opción honesta que el propio informe de análisis recomendaba. |
| 13 | Sándwich | ✅ fiel | Solo dibujo en medio, vista breve del anterior, descripción final. Fiel. |
| 14 | Fondo (Background) | ⚠️ difiere (a verificar) | La app hace N+1 pasos (fondo + N fotogramas) y tiempo ×1,5. Una guía (DigitFeast, citada en el informe) dice que Fondo tiene el DOBLE de fotogramas que Animación. Si es así, con 4 jugadores deberían ser 8 fotogramas, no 4. Hay que confirmar con una partida real o más fuentes. |
| 15 | Solo | ⚠️ difiere (leve) | 5 fotogramas y piel de cebolla, fieles. Pero el reloj: en el original con amigos arranca cuando la mitad/mayoría termina el turno, y solo no hay presión. La app usa el tiempo fijo de dibujo (60 s por defecto): jugando solo, el turno se envía solo a los 60 s. |

## Detalle por modo

### 1. Normal — ✅ fiel
Flujo frase→dibujo→descripción alternando, solo se ve el eslabón anterior,
reparto aleatorio con cuadrado latino, N pasos, sin puntos ni ganador. La
pantalla de escribir («EMPIECE A ESCRIBIR UNA HISTORIA», teléfono azul con
«?»), la de dibujar («HEY, ¡ES HORA DE DIBUJAR!», «¡HECHO!») y la de
describir («¿Y AHORA? DESCRIBE ESTA ESCENA») copian los textos del original.
El álbum en formato chat con avatar por eslabón, título «ÁLBUM DE ANA» en
verde y tira de jugadores con el dueño resaltado es fiel al original
(`ref-album-dailymotion.jpg`).

### 2. Imitación (Knock-Off) — ✅ fiel
Escribir en el turno 1 y solo dibujar después; el dibujo anterior se ve
brevemente y desaparece al empezar a trazar (`memory:true`, captura
`play-knockoff.png`: vista previa visible antes de trazar). El reloj se
acorta cada ronda: la app usa 60 s − 10 s por ronda, mínimo 20 s. El
original no publica el decremento exacto, así que es una aproximación
razonable y documentada. Descripción oficial: «Try to replicate the drawings
while the clock gets faster» (wiki). Nota: la ficha de la tienda citada en
el informe dice que «todos dibujan la misma primera frase»; la wiki y
TheGamer describen una frase por jugador, que es lo que hace la app. Queda
como discrepancia de fuentes, no como error de la app.

### 3. Animación — ⚠️ difiere (reproductor incompleto)
- ✅ Sin escritura; cada jugador dibuja un fotograma calcando tenuemente el
  anterior (piel de cebolla al 28 %, `onion:true`).
- ⚠️ **El reproductor del álbum es mínimo:** solo ◀ Anterior / ▶ Reproducir /
  Siguiente ▶ a 500 ms fijos (`auto-animation.png`). El original (wiki Álbum)
  tiene velocidades **1's, 2's, 3's, 4's, 10's** y **3 modos de bucle**
  (infinito; adelante y atrás repetido; una vez y pausa), y la animación la
  publica el bot **«Gartic»** (teléfono morado con cara) como respuesta
  automática tras los fotogramas sueltos. En la app no hay selector de
  velocidad, ni de bucle, ni mensaje del bot.
- ➖ **Exposición de fotograma** (0x = quitar el fotograma, 1x, 2x, 3x) no
  existe en la app.

### 4. Rompehielos (Icebreaker) — ⚠️ difiere (mecánica central distinta)
- El original (TheGamer): «After the questions have been chosen, **everyone
  will get the chance to draw the same prompts**… **All the drawings are
  displayed**, and you can then take the time to present and discuss what
  you decided to draw». Wiki: «Can previous prompt be seen? Yes (only the
  writing prompt)». Descripción oficial: «Play with just one sentence!».
- La app (`icebreaker`, 2 pasos: escribir + dibujar) hace **una sola
  cadena por pregunta: 1 pregunta + 1 dibujo** (`auto-icebreaker.png`: álbum
  con la frase y un único dibujo). Cada pregunta solo la dibuja una persona
  y nunca se ven juntos varios dibujos de la misma frase.
- Además la propia tarjeta del modo en la app dice «Al final se muestran
  juntos todos los dibujos» y la pista en partida dice lo mismo: la app
  promete lo que el original hace y lo que la implementación no hace.
- **Corrección:** cada pregunta debe repartirse a todos los jugadores (o a
  varios) para dibujarla, y el álbum debe agrupar por pregunta todos los
  dibujos de esa pregunta juntos.

### 5. Cadáver exquisito — ✅ fiel
3 turnos (Cabeza, Torso, Piernas), solo se ve la franja inferior (90 px) del
dibujo anterior (`play-corpse.png`: la franja se muestra en una cajita
encima del lienzo, con el rótulo «Dibuja: Torso (solo se ve la franja
inferior del dibujo anterior)»). Jugable solo (mín. 1), como en el original.
- Matiz: en el original, en la esquina inferior izquierda se muestran los
  **colores usados antes** para mantener la continuidad de la paleta. La
  app no los muestra.
- Matiz visual: en el original hay una **línea discontinua** que marca
  hasta dónde llega cada parte; la app muestra la franja en una caja
  separada, sin línea en el lienzo.

### 6. Complementar — ✅ fiel
Primer turno: unas líneas rápidas en 15 s; después, completarlas; las líneas
iniciales no se pueden borrar (sin borrador ni Limpiar, verificado en
`play-complement.png`). TheGamer: «You have a very limited time… Next,
everyone else will get the chance to add onto these initial few lines…
you cannot erase it». Fiel.

### 7. Obra maestra — ✅ fiel
Un solo turno de dibujo por jugador, sin límite de tiempo, sin escritura
(`masterpiece`: 1 paso, tiempo 0). Descripción oficial: «Create a piece of
art! Play in a single turn with no time limit». Fiel. (El álbum muestra una
obra por álbum; en el original se presentan todas las obras juntas al final:
la app las muestra álbum por álbum, que es el mismo patrón que en Normal y
no contradice ninguna fuente.)

### 8. Historia (Story) — ✅ fiel
Solo escritura, N pasos, cada jugador ve solo la frase anterior y la
continúa; el álbum es la historia completa frase a frase. Descripción
oficial: «Write a narrative using only the previous sentence as a
reference». Fiel. (La wiki marca «Has Writing: ✔, Has Drawing: ✗».)

### 9. Pieza que falta (Missing Piece) — ⚠️ difiere (mecánica distinta)
- El original (informe §2.13, Medium oficial): el jugador 1 crea un dibujo
  incompleto; el jugador 2 lo recibe y **lo completa a su manera** (dibuja
  ENCIMA); al pasar al jugador 3, el juego **ha borrado la parte original
  del jugador 1**, así que vuelve a haber un dibujo incompleto que
  completar. En cada ronda se añade una parte y se pierde otra. Equivalente
  en ajustes: «Keep Drawing: Only the previous drawing».
- La app (`missing`, `strokesOnly:true`): el jugador recibe el dibujo
  anterior como **vista previa que desaparece al trazar** y dibuja en un
  **lienzo en blanco** (`drawOptsFor`: solo `previewImage`, no
  `initialImage`). Nunca se dibuja encima de nada y nunca se borra una
  parte: cada eslabón es un dibujo nuevo hecho de memoria, no un dibujo que
  evoluciona.
- **Corrección:** el turno debe empezar con el dibujo anterior ya pintado
  en el lienzo (como `accumulate`) y al pasar al siguiente jugador debe
  borrarse la parte más antigua (los trazos de hace 2 turnos). La app ya
  guarda los trazos por eslabón (`lk.strokes`), así que es viable: dibujar
  encima con los trazos de los 2 últimos eslabones y descartar los
  anteriores.

### 10. Secreto (Secret) — ✅ fiel, con 2 matices
- ✅ Al escribir, las palabras salen censuradas con ● (overlay
  `#censorOverlay`, `shot-secret-write.png`). Al dibujar, los trazos se van
  desvaneciendo con un velo blanco al soltar el dedo (`secret-veil`).
- ✅ El dibujo a describir SÍ se ve en los turnos de descripción
  (`renderDescribe` muestra `descImg` sin censurar): coincide con el
  original — TheGamer: «Can you see the previous prompt?: Yes».
- ⚠️ **Matiz 1:** en los turnos de descripción, el texto que escribes NO se
  censura en la app (`renderDescribe` usa un textarea normal). En el
  original, al escribir (también al describir) tus palabras aparecen
  censuradas (NamuWiki: sustituidas por ●). Falta el overlay de censura en
  describir.
- ⚠️ **Matiz 2:** en el original, al dibujar «la pantalla está en blanco»
  (TheGamer) / los trazos «desaparecen gradualmente» (NamuWiki). La app
  deja ver el trazo mientras se dibuja y lo tapa al soltar el dedo: es una
  aproximación razonable y jugable, no un error.
- ✅ Tiempo rápido: la app usa 2/3 del tiempo normal (mín. 15 s). El
  original dice solo «Fast», sin cifras: aproximación razonable.

### 11. Cooperativo (Co-Op) — ✅ fiel
6 turnos fijos (1 de escritura + 5 de dibujo), todos añaden trazos al mismo
dibujo acumulado (`accumulate:true`, `coop`: 6 pasos). Descripción oficial:
«Create together! Starting from a sentence, add your touch to the
drawings». Fiel. Limitación ya documentada en el LEEME: el acumulado solo
recoge trazos de pincel/borrador; las formas y el cubo no se guardan como
trazos y no aparecen en el fondo acumulado.

### 12. Puntuación (Score) — 🔶 aproximación documentada
Flujo igual que Normal, 1 punto por eslabón que mantiene el significado.
TheGamer: «Every time you write or draw something consistent with the
previous prompt, you receive a point. It is a little unclear how the game
determines if your contribution matches the one before it or not». La app
usa votación del grupo en el álbum (marcador por álbum, botón «Mantuvo el
significado»). Es diseño propio, no original, pero es la opción honesta que
el informe de análisis recomendaba y está documentada en el LEEME. No se
pide cambiarla; solo dejar constancia de que no es el criterio del original
(que nadie conoce).

### 13. Sándwich — ✅ fiel
Escribir, solo dibujar turno tras turno viendo el dibujo anterior
brevemente (`memory:true`), y descripción final. TheGamer: «You are only
allowed to see the previous image before you start to draw it. Sandwich
adds a final written stage that acts as a bookend». Fiel.

### 14. Fondo (Background) — ⚠️ difiere (a verificar)
- ✅ El paso 0 dibuja un fondo fijo que permanece en todos los fotogramas
  (`bg:true`, `initialImage` = fondo en los pasos siguientes) y el resto
  anima encima calcando el fotograma anterior (piel de cebolla).
- ⚠️ **Número de fotogramas:** la app hace N+1 pasos (fondo + N
  fotogramas) y tiempo ×1,5. El informe (§2.6, citando a DigitFeast) dice
  que Fondo tiene **el doble de fotogramas que Animación** y relojes
  extendidos. Con 4 jugadores eso serían 8 fotogramas, no 4. El LEEME dice
  «con el doble de fotogramas que Animación (N+1 pasos)», que es
  contradictorio (N+1 no es el doble). Hay que confirmar con una partida
  real del original o más fuentes antes de cambiarlo.
- El tiempo ×1,5 es una aproximación razonable de «relojes extendidos»
  (sin cifras oficiales).

### 15. Solo — ⚠️ difiere (leve, el reloj)
- ✅ 5 fotogramas, cada jugador en su propia cadena (`self:true`), piel de
  cebolla con el fotograma propio anterior, jugable solo (mín. 1).
  TheGamer: «you are creating your very own animation. You will have five
  frames… You will faintly see your previous design each turn».
- ⚠️ **El reloj:** en el original, con amigos el reloj **solo arranca
  cuando la mitad (o la mayoría) ha terminado su turno**; solo, no hay
  presión de grupo. La app usa el tiempo fijo de dibujo (60 s por defecto)
  y el turno se envía solo al agotarse. Jugando solo, eso corta al jugador
  a los 60 s por fotograma aunque nadie espere. Corrección: en Solo con
  1 jugador, sin límite de tiempo (o que el tiempo solo corra como en
  Dynamic cuando la mitad termina).

## Lo visual general (sala, modos, dibujo, álbum)

Comparado con `ref-lobby-player-me.png`, `ref-lobby-ensigame.jpg` y
`ref-album-dailymotion.jpg`, y con las capturas de la app
(`VERIFICACION/v2.4/shot-*.png`):

### Sala / lobby — ✅ fiel en estructura, ⚠️ en presentación
- ✅ Selector «14 JUGADORES» (como «14 PLAYERS» del original), huecos
  VACÍO/EMPTY, corona al anfitrión, botones INVITAR y EMPEZAR, pestañas
  PREESTABLECIDOS / AJUSTES PERSONALIZADOS (PRESETS / CUSTOM SETTINGS).
- ⚠️ **Los modos van en una lista vertical con tarjetas grandes y
  descripciones largas** (`shot-modes.png`); el original es una **rejilla
  compacta 3×3** con el icono y solo el nombre, y la tarjeta seleccionada
  lleva **borde verde y un engranaje** arriba a la izquierda. En móvil la
  lista es una adaptación razonable, pero la distancia visual es grande:
  para elegir modo hay que desplazar mucho (la v2.4 ya lo mitigó con
  desplazamiento propio de la lista).
- ⚠️ **Los iconos de modo son emojis** (🧟🍎🖼️📖🧩🤫🤝🏆🥪🌄🧍). El
  original usa iconos dibujados propios por modo (bloc+lápiz, cartas,
  martillo+hielo, medalla, sándwich…). Los 15 iconos oficiales están en
  esta carpeta como referencia (`ref-icon-*.svg`): la app debería tener
  iconos dibujados sencillos en ese espíritu (no copiar los SVG oficiales
  tal cual, son assets del juego), igual que ya hace con su logo propio.
- ⚠️ **Contraste de la pestaña seleccionada:** «PREESTABLECIDOS» en verde
  `#22c55e` sobre violeta se lee con dificultad a tamaño pequeño
  (`shot-modes.png`). En el original la pestaña seleccionada también es
  verde, pero sobre un fondo de pestaña más oscuro. Mejora: fondo de
  pestaña más oscuro o texto blanco con subrayado verde.
- ✅ El botón INVITAR junto a EMPEZAR, como en el original.

### Pantalla de dibujo — ✅ fiel con matices
- ✅ Barra superior violeta con el paso, «HEY, ¡ES HORA DE DIBUJAR!»,
  marca de agua «Gartic Móvil» en el lienzo, paleta, botón ✔ ¡HECHO!
  violeta, barra inferior compacta como la foto de la APK oficial.
- ⚠️ **La parrilla de herramientas 3×3 va ENCIMA del lienzo** y empuja el
  lienzo y la barra inferior hacia abajo. En Normal y en Imitación el
  botón ¡HECHO! sigue visible a 360×800 (`shot-draw.png`,
  `play-knockoff.png`), pero en **Cadáver exquisito** la caja de la
  franja + el rótulo añaden ~120 px y el ¡HECHO! queda **bajo el pliegue**
  (`play-corpse.png`: se ven Deshacer/Rehacer pero no la barra inferior).
  Lo mismo puede pasar en los modos con vista previa. Corrección: que la
  parrilla de herramientas sea plegable o vaya debajo del lienzo, o que la
  caja de vista previa sea más compacta, para que ¡HECHO! no se pierda.
- ➖ Sin zoom (pellizcar), sin cuadrícula y sin herramienta de notas: el
  original las tiene (atajos H, G, N, +/−). No son críticas en móvil, pero
  son parte del lienzo oficial. El botón «Limpiar» tampoco está confirmado
  en el original (el informe ya lo señalaba); la app lo tiene y en
  Complementar se desactiva correctamente.
- Matiz: en Cadáver exquisito falta la **línea discontinua** en el lienzo
  y los **colores usados antes** en la esquina inferior izquierda.

### Álbum final — ✅ fiel, ➖ faltan los ajustes de exhibición
- ✅ Formato chat con avatar por eslabón, título «ÁLBUM DE <nombre>» en
  verde, subtítulo «Álbum N de M», tira de jugadores con el dueño
  resaltado, botones Álbum anterior/siguiente, «Volver a jugar (mismos
  jugadores)» y «Nueva partida» (`shot-album.png`, `auto-icebreaker.png`).
- ➖ **Ajustes de exhibición del original** (wiki Álbum, los controla el
  anfitrión): **Display mode** (automático o manual), **Voice-over** (voz
  que lee las frases; disponible en Normal, Secret, Icebreaker, Story,
  Co-Op, Score, Sandwich, Crowd y Solo; NO en Knock-Off, Animation,
  Complement, Masterpiece, Missing Piece ni Background) y **Exhibition
  flow** (álbumes desde el principio o desde el final). La app solo tiene
  avance manual por botones.
- ➖ **Guardar el álbum como GIF animado** (botón «.GIF») y **replay trazo
  a trazo** (1x, 0,5x, 0,1x): ya estaban pendientes en el LEEME, se
  confirman aquí como faltantes del original.

### Ajustes personalizados (pestaña CUSTOM SETTINGS) — ⚠️ incompletos
La app tiene: Tiempo, Secuencia (Escribir/Dibujar, Solo dibujar), Turnos
(Todos/Aleatorios), Sigue dibujando (Keep Drawing), Puntuaciones
(Scoreboard), Secretismo (Secrecy). Frente al original faltan:
- ➖ **Turnos numérico (hasta 15 rondas)** con duración estimada de la
  partida. La app tiene «Todos/Aleatorios», que no es lo mismo: en el
  original Turnos es el número de turnos por cadena.
- ➖ **Animación** (on/off + velocidad de fotogramas y bucle).
- ➖ **Formato de lienzo** (Estándar o Cuadrado, ajuste fijo).
- ➖ **Moderación** (ajuste fijo).
- ➖ **Tiempo Dynamic** (el reloj solo arranca cuando la mayoría pulsa
  Done) y **Sin límite** como opción de tiempo por fase.
- Nota: la pestaña VERIFICADO del inicio es decorativa en el original
  también; no es un faltante.

### Cuenta atrás 3-2-1 — en verificación aparte
El informe de análisis (§6 y §8) dice que **sí hay una cuenta atrás 3, 2, 1
antes de empezar** (rediseñada en 2026). El pase de fidelidad de la v2.4
afirmó que no existe basándose en no haberla visto en los vídeos revisados.
Esa duda la está verificando otro trabajo en paralelo con 13 vídeos
(Vegetta, AuronPlay, Guarnizo) y la página oficial. **No se concluye aquí.**

## Wifi local (objetivo final, según Roi)
La lógica wifi de los 14 modos está implementada (el anfitrión genera el
orden y lo reparte; el cliente recibe su tarea con la imagen que toca:
vista previa, fondo acumulado, piel de cebolla o franja — líneas 2649–2654
de `www/index.html`), pero **solo se probó en el navegador, nunca entre
dos teléfonos reales** (ya consta en el LEEME). Es la prueba pendiente más
importante: Roi lo marcó como objetivo final («debe funcionar muy bien
ahí»). Puntos a probar con dos teléfonos cuando llegue la v2.4: crear sala
con cada modo, unirse, recibir la tarea correcta (vista previa en Imitación
y Pieza que falta, franja en Cadáver, fondo en Cooperativo/Fondo, piel de
cebolla en Animación/Solo), y que el álbum llegue completo a todos.

## Correcciones priorizadas (para aplicar después)

### Alta prioridad (cambian cómo se juega)
1. **Rompehielos:** cada pregunta la dibujan todos los jugadores; el álbum
   agrupa por pregunta todos sus dibujos juntos. Hoy: 1 dibujo por pregunta
   y la tarjeta promete lo contrario.
2. **Pieza que falta:** dibujar ENCIMA del dibujo anterior y, al pasar,
   borrar la parte más antigua (usar los trazos guardados por eslabón).
   Hoy: vista previa que desaparece y lienzo en blanco.
3. **Cadáver exquisito / modos con vista previa:** que el botón ¡HECHO! no
   quede bajo el pliegue a 360×800 (parrilla de herramientas plegable o
   caja de vista previa más compacta).

### Media prioridad (fidelidad visible)
4. **Reproductor de Animación/Fondo/Solo:** selector de velocidad (1's,
   2's, 3's, 4's, 10's) y de bucle (infinito / adelante-atrás / una vez),
   y mensaje del bot «Gartic» al publicar la animación. Añadir exposición
   de fotograma (0x/1x/2x/3x) si es viable.
5. **Secreto:** censurar también el texto al describir (overlay ● como al
   escribir).
6. **Solo:** sin límite de tiempo cuando se juega solo (1 jugador); con
   amigos, que el reloj arranque cuando la mitad termina (modo Dynamic).
7. **Fondo:** confirmar si de verdad son el doble de fotogramas que
   Animación; si se confirma, pasar de N+1 a 2N fotogramas (+ fondo).
8. **Ajustes de exhibición del álbum:** modo automático/manual y flujo
   principio/fin (el anfitrión los elige); voz en off opcional donde el
   original la tiene.

### Baja prioridad (pulido visual y ajustes)
9. **Iconos de modo dibujados** en el espíritu de los oficiales (no emojis
   ni copias de los SVG), con borde verde + engranaje en la tarjeta
   seleccionada; rejilla más compacta en la lista de modos.
10. **Contraste de la pestaña PREESTABLECIDOS** (fondo más oscuro o texto
    blanco con subrayado verde).
11. **Cadáver exquisito:** línea discontinua en el lienzo y colores usados
    antes en la esquina inferior izquierda.
12. **Ajustes personalizados:** Turnos numérico (1–15) con duración
    estimada; Animación (velocidad/bucle); formato de lienzo
    (Estándar/Cuadrado); tiempo Dynamic y Sin límite.
13. **Pendientes ya conocidos (no nuevos):** botón «.GIF» del álbum, replay
    trazo a trazo, zoom/cuadrícula/notas en el lienzo.

## Lo que NO se pudo verificar
- La sala y los álbumes no se ven en `garticphone.com` sin entrar al juego;
  la sala se comparó con fotos de guías (player.me, ensigame) y el álbum
  con capturas de Dailymotion y de la wiki.
- No hay vídeos de gameplay revisados fotograma a fotograma para cada modo
  en este pase (salvo los de Vegetta ya usados en la v2.3); las reglas se
  contrastaron con la wiki, TheGamer y el informe de análisis, que citan
  las mismas fuentes.
- El wifi entre dos teléfonos reales no se pudo probar (hace falta el
  Redmi de Roi y otro teléfono).
