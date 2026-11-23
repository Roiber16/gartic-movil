# Gartic Móvil — APK Android

> Nota: antes se llamaba Teléfono Roto; Roi lo renombró a Gartic Móvil
> el 21 nov 2026. El keystore es el mismo de antes (misma huella SHA-256),
> solo cambió el nombre del archivo.

Empaquetado con Capacitor de la app web de Gartic Móvil (juego offline
tipo teléfono roto: dibujar, describir y reírse con amigos sin internet).
Modo Normal fiel, 3-8 jugadores, Adivina el dibujo con puntos y los
15 modos del original jugables, wifi local por hotspot (servidor local
puerto 7777) + modo de un solo teléfono.

- **appId:** `cu.roi.garticmovil`
- **Nombre:** Gartic Móvil
- **Versión:** 1.4.0 (versionCode 6, versionName 1.4.0)

## Novedades de la v2.4 (1.4.0)

Decisión de Roi (22 nov 2026): la v2.3 NO se envía. Todo lo de la v2.3
(ver abajo: atrás, botones, fluidez, ventanas, álbum aleatorio, sonidos
medidos, revisión visual) pasa a la v2.4, que añade el pase de fidelidad
completo: sonidos medidos en vídeos de AuronPlay y Juan Guarnizo,
interior comparado ventana por ventana con el original y botones
revisados uno por uno. Los 14 modos que faltan ya están implementados
en esta misma v2.4 (ver §4 abajo). El ícono quedó decidido por Roi
(22 nov): la C1 con Baloo 2 gruesa («Sí, queda así») como ícono final
de la v2.4; lo instala el trabajo del ícono. Sin compilar ni subir
nada hasta que todo esté terminado y verificado (regla de Roi).

### 1. Sonidos: vídeos de AuronPlay y Juan Guarnizo (pase de fidelidad)
- Se buscaron vídeos donde los sonidos del juego se oyeran limpios, sin
  tanta charla encima. Descargados con yt-dlp y analizados con el mismo
  método espectral de la v2.3 (STFT; scripts `analisis3.py` y
  `analisis4.py` en `VERIFICACION/v2.3-referencias/sonidos/`):
  * Juan Guarnizo «GARTIC PHONE NAVIDEÑO» `Rb6E3Eqppi4`, 798 s:
    2.147 eventos tonales, **0 arpegios**; 2 candidatos débiles de
    cuenta atrás (66,3 s y 632,5 s, frecuencias de voz/música, no del
    juego); 0 huecos de silencio.
  * Juan Guarnizo «JUANSGUARNIZO JUGANDO GARTIC PHONE CON STREAMERS»
    `UFOXXi8zsjQ`, 2149 s: 5.205 eventos; **1 arpegio confirmado a
    1759,8 s** (nota ~880 Hz con magnitud 0,215 y nota alta ~1357 Hz:
    mismo carácter que el de Vegetta; la tercera nota sale algo más
    alta que 1174 Hz, probablemente mezclada con la música). Ningún
    tic ≥4 repeticiones; 4 candidatos débiles de cuenta atrás
    (voz/música); 19 huecos de silencio ≥2 s.
  * AuronPlay «dibujando en gartic phone pero tenemos 5 años mentales»
    `KLPUA98-DuQ`, 2908 s: 5.693 eventos; **0 arpegios**; 1 candidato
    débil (2328,5 s); 16 huecos de silencio.
  * Otros vídeos localizados por búsqueda (no descargados): AuronPlay
    `1z-Kk4uAzuA`, `6ZcCFh7S6hc`, `e7sxjkwASpM`, `o8ecd0zh-YY`,
    `difTQMnfFVc`; Guarnizo `-2sgEByTULA`, `ibKrDZU1S7g`,
    `UQBcCDUh59Q`, `NUtgp2G2MsU`.
- **El arpegio de cambio de turno queda confirmado en un vídeo
  independiente** (Guarnizo, 1759,8 s). Las frecuencias de la app NO
  cambian: 784→880→1174 Hz (medidas limpias dos veces en Vegetta).
- **CORRECCIÓN (23 nov 2026): la cuenta atrás 3-2-1 SÍ existe en el
  original.** La afirmación anterior del pase de fidelidad era falsa: se
  miró el inicio de la primera partida de Vegetta a las 10:55, 11:00 y
  11:05, y la cuenta atrás dura ~3 s justo entre medias. Verificación completa en
  `VERIFICACION/v2.4/cuenta-atras/` (README.md + notas.md + fotogramas):
  fotogramas a 5 fps de `JzQOa0IW6IQ` muestran el rombo violeta con el
  **«3» a 657,6–658,1 s, el «2» a 658,2–659,1 s y el «1» a 659,4–660,5 s**,
  y la pantalla de escribir desde ~660,6 s; por audio, un **tic de
  ~1244 Hz por número** (medido a 657,6 y 659,6 s; el del «2» a 658,6 s
  se ve en el espectrograma, tapado por la voz) y el arpegio
  784→880→1174 Hz al terminar. Los «dos pitidos aislados de 1249 Hz»
  que aquí se descartaron como «sin patrón» **eran los tics del «3» y
  del «1»**. Confirmada además en 4 inicios más: Vegetta partida 2
  (~27:40), Guarnizo `UFOXXi8zsjQ` partida 1 Normal (~0:09–0:13) y
  partida 2 **Knock-Off** (18:12–18:15, 1092–1095 s: el «candidato débil»
  1092/1093/1094 s del análisis anterior era la cuenta atrás real) y
  AuronPlay `CHIE0B89olM` partida 1 (0:11–0:15, triple de tics en audio
  11,8/12,8/13,8 s). **Solo hay cuenta atrás al empezar cada partida,
  no entre turnos** (cambio de turno 791–800 s: fundido directo,
  sin rombo). Visual: rombo violeta con bombillitas y rayos sobre la
  sala oscurecida, número verde menta, ~1 s por número, ~3 s en total;
  no hay texto «¡YA!» ni «GO»: tras el 1 va el fundido al primer turno.
  La página oficial (6 pasos) y la wiki (15 modos) no la mencionan; la
  evidencia es solo de vídeo. La app MANTIENE su pantalla de cuenta
  atrás porque en un solo teléfono hace falta antes de cada turno (el
  teléfono cambia de manos), pero eso es una **adaptación funcional**,
  no una copia: en el original solo suena al empezar la partida.
  **El sonido de la app NO coincide con el original:** hoy es
  3→784 Hz, 2→880 Hz, 1→1174 Hz + «¡ya!» 1314+1550 Hz; lo medido es
  **tic ~1245 Hz por número + arpegio 784→880→1174 Hz al terminar**.
  **APLICADO el 23 nov 2026 (ver §6):** `count(n)` ahora es un tic
  de 1245 Hz (0,25 s) por número y `count(true)` es el arpegio
  784→880→1174 Hz al llegar a 0, sin «¡ya!». El «¡ya!» 1314+1550 Hz
  no es el final de la cuenta atrás (ahí el sonido final es el
  arpegio) — **ese 1314+1550 Hz SÍ existe en el original, pero es la
  alarma de poco tiempo** (ver el punto siguiente), no el final de la
  cuenta atrás. El visual también se cambió: antes número violeta en
  tarjeta lavanda; ahora **rombo violeta con bombillitas amarillas
  y número verde menta, dibujado con CSS** (como el original).
- **El tic de los últimos 10 s NO existe en el original, pero SÍ hay un
  aviso de poco tiempo (Roi tenía razón).** Recomprobado y corregido
  el 23 nov 2026: no hay tic por segundo (autocorrelación a lag 1 s en
  los últimos 10 s y 5 s de 14 fines de turno de Vegetta: sin
  periodicidad), pero el temporizador **no** baja en silencio. El
  temporizador es un **dial circular arriba a la derecha**; su cuña es
  blanca casi todo el turno y se pone **AMARILLA cuando baja a ~1/6
  del dial** (~0,17–0,18 del interior; ~22 % del tiempo restante) y en
  ese momento arranca una **alarma de dos tonos sostenidos ~1314 Hz +
  ~1550 Hz hasta el fin del turno** (medida con FFT fina: 1308–1317 Hz
  y 1546–1551 Hz en los 3 cambios medidos). Medido en Vegetta
  `JzQOa0IW6IQ` partida 2, Normal: escribir 1/7, cambio a amarillo
  ~795,5 s (turno de ~50 s, aviso a ~2 s del final, fin 797,5 s por
  ¡HECHO! de todos); dibujar 2/7, cambio ~917,0 s (turno de ~150 s,
  aviso a ~30 s del final, fin 947,0 s por tiempo); describir 3/7,
  cambio ~979,0 s (turno de ~40 s, aviso a ~3,5 s del final, fin
  982,5 s por ¡HECHO! de todos). El aviso es a una **fracción del
  temporizador**, no a N segundos fijos. El sonido «¡ya!» 1314+1550 Hz
  medido en la v2.3 a 795,58 s y descartado como «música de fondo»
  **es esta alarma**. En los fotogramas de 2021 la cuña es amarilla,
  nunca roja (el «rojo» que recuerda Roi puede ser el amarillo visto
  en pantalla pequeña, o un cambio en versiones más nuevas; sin
  confirmar en vídeo reciente). Sin confirmar en otros modos:
  Knock-Off (Guarnizo 2022: eventos 1324/1384 Hz a 1756,9/1757,3 s
  compatibles, pero sin medir el dial) y Animación (2024: no se
  pudieron aislar fines de turno limpios). **APLICADO el 23 nov 2026
  (ver §6):** el tic de 10 s se quitó (`AudioFX.tick()` eliminada);
  ahora, cuando queda ~1/6 del tiempo (`warnAt(total)=máx(2,
  floor(total/6))`), la píldora del temporizador se pone **AMARILLA**
  (antes siempre era amarilla; ahora es blanca casi todo el turno y
  amarilla solo en el aviso, como la cuña del dial original) y suenan
  los tonos **1314+1550 Hz SOSTENIDOS hasta el fin del turno**
  (`AudioFX.alarmStart()`/`alarmStop()`, con vibración [60] al
  arrancar). Vale en Normal y los 14 modos (turnos de escribir,
  dibujar y describir, en un solo teléfono y por wifi) y en Adivina
  (ronda en vivo y turno de 30 s del adivinador en un solo teléfono).
  La frecuencia de
  1250 Hz del tic actual coincide con el tic de la **cuenta atrás**
  (~1244 Hz medidos), no con ningún aviso de poco tiempo. Evidencia
  en `VERIFICACION/v2.4/cuenta-atras/` (README.md § «El tic de los
  últimos 10 s…» y notas.md § 9, con espectrogramas y fotogramas del
  dial).
- Conclusión del pase (corregida 23 nov 2026): el arpegio queda
  confirmado en Guarnizo (1759,8 s) y la cuenta atrás **existe y está
  medida** (tic ~1245 Hz por número + arpegio al terminar; ver arriba).
  **El sonido de la cuenta atrás de la app ya cambió (APLICADO el
  23 nov 2026, ver §6):** tic ~1245 Hz por número + arpegio al final,
  sin «¡ya!». **El tic de 10 s también se sustituyó (APLICADO el
  23 nov 2026, ver §6)** por la alarma de poco tiempo del original
  (píldora amarilla a ~1/6 + tonos 1314+1550 Hz sostenidos).

### 2. Botones, uno por uno (auditoría a 360x800, 19 pantallas)
- Harness `VERIFICACION/v2.4/audit_buttons.py` (Chromium headless,
  360x800): revisa todos los botones, selects e inputs visibles de
  cada pantalla (altura <44 px, texto cortado, fuera de la pantalla,
  solapamientos). Resultados en `VERIFICACION/v2.4/buttons-audit.json`
  y capturas `shot-*.png` (re-tomadas tras cada corrección).
- **Fallo real 1 — la fila de herramientas de dibujo desbordaba a la
  derecha:** a ≤400 px iba en una sola tira con desplazamiento
  horizontal sin pista visual («Línea» se veía cortada como «Lín» y el
  resto solo se alcanzaba desplazando). Ahora se parte en **3 filas
  visibles (3+3+3)**: Pincel, Borrador, Cubo de relleno / Línea,
  Círculo, Círculo hueco / Cuadrado, Cuadrado hueco, Cuentagotas,
  todas a 44 px, sin recortes ni desplazamiento. Se hace con dos
  saltos (`<div class="tool-break">` tras la 3.ª y la 6.ª herramienta,
  que solo se activan con la media query de ≤400 px) y letra .8rem
  con padding 6px 6px para que quepan las 3 por fila con la fuente
  Baloo 2 (más ancha de lo estimado).
- **Fallo real 2 — «Deshacer» con el texto cortado:** la palabra no
  cabía en su botón (69 px a .9rem). Ahora la fila
  Deshacer/Rehacer/Limpiar/✕ Salir va en **2×2 a 48 px** (cada botón
  ~150 px), con el texto completo. Aplica a dibujo Normal, dibujo con
  panel y Adivina.
- **Selects de jugadores a 48 px:** `wifiMaxPlayers` y
  `modesMaxPlayers` estaban a 41 px (`.count-bar select`,
  `padding:8px 4px`); ahora `padding:12px 6px` con `min-height:48px`
  (medido: 49 px).
- **Acciones principales bajo el pliegue:** en Modos, EMPEZAR/INVITAR
  quedaban a y≈4674 (había que desplazar ~4700 px por las 15
  tarjetas); en Crear sala, INVITAR/EMPEZAR quedaban a y≈1103 por la
  lista de hasta 14 jugadores. Ahora las listas tienen desplazamiento
  propio con altura máxima (`#modesList{max-height:46vh}`,
  `#wifiLobby{max-height:20vh}`) y los botones quedan visibles sin
  desplazar: Modos INVITAR/EMPEZAR a y=671, Volver a y=745;
  Crear sala INVITAR/EMPEZAR a y=697. En Crear sala, «Volver al
  inicio» queda 49 px bajo el pliegue (botón secundario; mismo patrón
  aceptado en Álbum y Cómo se juega).
- Avisos restantes de la auditoría, todos aceptables y documentados:
  * 3 «solapamientos» en Modos: falsos positivos del harness — son
    las tarjetas de la lista con desplazamiento propio (sus rectángulos
    de posición se solapan con los botones aunque visualmente están
    recortadas dentro de la lista). Comprobado a ojo en `shot-modes.png`:
    INVITAR/EMPEZAR/Volver están despejados.
  * Muestras de color de la paleta (32 px) y puntos de grosor (34 px)
    en dibujo: como en el original; son controles secundarios junto a
    la barra principal.
  * Interruptores de Ajustes (checkbox de 26 px): toda la fila es
    táctil, no hay que corregir.
  * 0 desbordamientos horizontales del documento en las 19 pantallas,
    0 solapamientos reales, 0 textos cortados.

### 3. Visual y ventanas (re-revisión de las 18 pantallas)
- Se volvieron a comparar las 18 capturas con las referencias
  (`ref-01`–`ref-12`) y con las fotos de la APK oficial y de
  Gartic.io. Lo que ya estaba bien y no se tocó: título «ÁLBUM DE
  ANA» en verde con tira de jugadores (dueño resaltado), «HEY, ¡ES
  HORA DE DIBUJAR!», «¡HECHO!», marca de agua «Gartic Móvil» visible
  en el lienzo, Baloo 2, verde #22c55e, tarjetas lavanda, botones
  blancos con borde violeta, pantalla de escribir («EMPIECE A
  ESCRIBIR UNA HISTORIA», teléfono azul con «?»), pantalla de
  describir («¿Y AHORA? DESCRIBE ESTA ESCENA»), Adivina en vivo
  (jugadores con puntos a un lado, chat al otro, pista con guiones,
  barra de tiempo amarilla) y podio con medallas.
- Desviaciones pequeñas que quedan como están (documentadas, no
  corregidas por decisión previa): el código de sala se ve como
  «• • • •» antes de generarse (en el teléfono real se genera al
  crear la sala; en las pruebas sin servidor LAN no hay código);
  el botón «.GIF» del álbum y los fondos de color por paso siguen
  pendientes (ver «Lo que NO se copió»); la sala y los álbumes no se
  ven en `garticphone.com` sin entrar al juego, así que esa parte se
  compara solo con los fotogramas de los vídeos y las fotos de la APK
  oficial.
- Verificación v2.4 (Chromium headless, 360x800): `#auto=normal` 0
  errores, 0 desbordamiento, 4 álbumes × 4 eslabones, `fxOk:true`,
  `validPermutation:true`, `randomOrder:true`; `#auto=guess` 0
  errores, 0 desbordamiento, podio Carla:38, Dan:34, Beto:30, Ana:10;
  `#test=nav` 0 errores, pila de navegación y diálogo de salir
  correctos. Capturas nuevas en `VERIFICACION/v2.4/`, revisadas a ojo.
- Versión subida a **1.4.0 (versionCode 6)** en `package.json`,
  `android/app/build.gradle` y `scripts/fix-debug-signing.js`;
  `npx cap sync android` hecho y comprobado: `www/index.html` y
  `android/app/src/main/assets/public/index.html` idénticos (md5
  `169663184faa3bc5b2617fd21461aa98`); permiso VIBRATE presente y
  firma fija intacta. **Sin compilar ni subir nada a GitHub.**

### 4. Los 14 modos que faltaban (tandas 1-3, implementados y verificados)
- Los 15 presets del original ya son jugables: Normal, Adivina el
  dibujo y los 14 nuevos. La pantalla Modos los muestra todos con la
  etiqueta «Jugable en v2.4». Se eligen en la pantalla Modos (tocar la
  tarjeta) y se juegan desde «EMPEZAR» en un solo teléfono; por wifi,
  el anfitrión elige el modo en Crear sala (selector «Modo de la
  sala», todos los modos) y los demás lo ven en el resumen de ajustes.
- Arquitectura: el motor del Normal se generalizó sin romperse
  (`MODE_SPECS` + `specFor()`): cada modo es una especificación con
  nº de pasos, tipo de tarea por paso (escribir/dibujar/describir),
  tiempo por paso, mínimo de jugadores y reglas especiales (secreto,
  memoria, acumulado, piel de cebolla, franja, fondo fijo, votación).
  `buildOrders(n, steps, self)` reparte las cadenas con cuadrado
  latino para cualquier nº de pasos (también cuando pasos > n, como
  Cooperativo con 6, o pasos < n, como Rompehielos con 2). Cada
  eslabón de dibujo guarda también sus trazos (`strokes`), que es lo
  que permite reconstruir el fondo acumulado en Cooperativo,
  Complementar y Fondo. El álbum final muestra cada eslabón con su
  autor, como en Normal.
- **Tanda 1 — Historia:** solo escritura, N pasos (uno por jugador).
  Cada jugador ve la frase anterior y la continúa; el álbum es la
  historia completa, frase a frase. **Obra maestra:** 1 solo turno de
  dibujo por jugador, sin límite de tiempo. **Secreto:** como Normal,
  pero no se ve lo propio: al escribir, el texto sale censurado con
  ●●● (también la frase anterior) y al dibujar los trazos se van
  desvaneciendo con un velo blanco al soltar el dedo; el tiempo es
  2/3 del normal (mín. 15 s). Desde el 23 nov 2026 (ver §6), **al
  describir el texto también sale censurado con ●●●**, como en el
  original. **Sándwich:** escribir, dibujar turno
  tras turno viendo el dibujo anterior brevemente (vista previa que
  desaparece al empezar a trazar) y describir el último dibujo al
  final. **Puntuación:** como Normal; al final del álbum el grupo
  marca los eslabones que mantuvieron el significado y se ve el
  marcador (1 punto por eslabón marcado). Decisión propia y
  documentada: el criterio del original no está publicado; la
  votación del grupo es la regla más sencilla y fiel. **Rompehielos
  (rehecho el 23 nov 2026, ver §6):** N pasos (uno por jugador):
  primero cada jugador escribe una pregunta; después TODOS dibujan
  CADA pregunta (cada pregunta pasa por todas las manos, como en el
  original) y al final el álbum se agrupa por pregunta: la pregunta
  y, juntos, todos los dibujos que hicieron de ella. La tarjeta del
  modo promete «se muestran juntos todos los dibujos» y ahora se
  cumple (antes hacía 1 dibujo por frase).
- **Tanda 2 — Imitación:** solo dibujo después de la frase inicial;
  el dibujo anterior se ve brevemente y desaparece al empezar a
  trazar; el tiempo se acorta en cada ronda (60 s la primera de
  dibujo, 10 s menos en cada ronda, mínimo 20 s). Ojo: en este modo
  el reloj siempre corre, aunque en los ajustes se elija «Sin
  límite», porque el reloj que se acorta es la gracia del modo.
  **Complementar:** todos los pasos son dibujo; el primero son unas
  líneas rápidas (15 s) y después a completarlas: las líneas
  iniciales no se pueden borrar (sin borrador ni botón Limpiar).
  **Pieza que falta (rehecha el 23 nov 2026, ver §6):** todos los
  pasos son dibujo; en cada turno se dibuja ENCIMA del dibujo
  acumulado (el lienzo ya trae lo dibujado antes, con los trazos
  guardados por eslabón) y al pasar se borra la parte más antigua:
  solo queda visible la última parte añadida. Antes mostraba el
  dibujo anterior como vista previa que desaparecía y se dibujaba en
  blanco; ahora nunca se dibuja en blanco.
  **Cadáver exquisito:** 3 turnos (Cabeza, Torso, Piernas); solo se
  ve la franja inferior (90 px) del dibujo anterior. Se puede jugar
  solo (1 jugador). **Cooperativo:** 6 turnos (1 de escritura + 5 de
  dibujo); todos añaden trazos al mismo dibujo, que se va acumulando
  en el lienzo de cada turno.
- **Tanda 3 — Animación:** sin escritura; cada jugador dibuja un
  fotograma calcando tenuemente el anterior (piel de cebolla, 28 %
  de opacidad) y al final el álbum es un reproductor con el autor de
  cada fotograma. Desde el 23 nov 2026 (ver §6): el reproductor tiene
  **selector de velocidad (1's–10's), modos de bucle (Infinito,
  Adelante y atrás, Una vez), exposición por fotograma (0x/1x/2x/3x:
  0x salta el fotograma) y el mensaje del bot «Gartic»** («¡Aquí está
  la animación que crearon entre todos!»). **Fondo:** como Animación
  pero el paso 0 dibuja un fondo fijo que permanece en todos los
  fotogramas (cada fotograma guarda el lienzo completo, con el fondo
  incluido) y con **el doble de fotogramas que Animación: 1 fondo +
  2N fotogramas (2N+1 pasos)** y tiempos ×1,5. Confirmado con la
  guía citada en la revisión de modos (DigitFeast: «el doble de
  fotogramas que Animation»); el «N+1 pasos» que decía el LEEME antes
  era contradictorio y estaba mal. **Solo:** tu propia animación en 5
  fotogramas; cada jugador trabaja en su propia cadena (nadie
  continúa la de otro). Se puede jugar solo (1 jugador) o con
  amigos, cada uno con la suya. Desde el 23 nov 2026 (ver §6),
  **jugando solo no hay límite de tiempo**: el reloj no corta al
  jugador (con amigos sigue el tiempo de dibujo normal).
- Wifi: los 14 modos funcionan por wifi (el anfitrión genera el
  orden y lo reparte; el cliente recibe su tarea con la imagen que
  toca: vista previa, fondo acumulado o piel de cebolla). Mínimos por
  modo (Normal/Historia/Secreto/Sándwich/Puntuación/Rompehielos/
  Imitación/Complementar/Pieza que falta/Cooperativo: 3; Obra
  maestra/Animación/Fondo: 2; Cadáver exquisito/Solo: 1). Verificado
  por wifi simulado con dos instancias reales del juego (ver §5
  abajo); **solo queda probarlo con dos teléfonos reales** (hotspot
  de verdad, dos Redmi).
- Limitaciones conocidas (documentadas, no errores): el fondo
  acumulado solo recoge los trazos de pincel y borrador; las formas
  (línea, círculo, cuadrado) y el cubo de relleno no se guardan como
  trazos y no aparecen en el fondo acumulado. El álbum de animación
  es un reproductor dentro de la app, no un archivo GIF: el botón
  «.GIF» del álbum sigue pendiente (hace falta codificar GIF en el
  teléfono). En Imitación la vista previa solo existe a partir del
  paso 2 (en el paso 1 se dibuja una frase, no hay dibujo anterior
  que recordar). En Pieza que falta ya no hay vista previa: se
  dibuja encima del dibujo acumulado (ver §6).
- Verificación (Chromium headless, 360x800; harness
  `VERIFICACION/v2.4/modos/verify_modes.py`, resultados en
  `VERIFICACION/v2.4/modos/modos-verificacion.json`): por cada modo,
  `#auto=mode:<id>` juega una partida completa de 4 jugadores hasta
  el álbum y `#shot=play-<id>` captura la pantalla de juego en mitad
  de la partida; además `#shot=draw-memory` (Imitación paso 2, vista
  previa) y `#shot=secret-write` (Secreto paso 0, censura ●●●).
  **Los 14 modos: 0 errores de consola, 0 desbordamiento**; álbumes
  y eslabones correctos (Historia 4×4, Obra maestra 4×1, Secreto 4×4,
  Sándwich 4×4, Puntuación 4×4 con marcador y voto, Rompehielos 4×4
  (todos dibujan cada pregunta; álbum agrupado por pregunta),
  Imitación 4×4, Complementar 4×4, Pieza que falta 4×4, Cadáver
  exquisito 4×3, Cooperativo 4×6, Animación 4×4 con reproductor,
  Fondo 4×9 (1 fondo + 8 fotogramas), Solo 4×5). Regresión: `#auto=normal` sigue con
  `validPermutation:true, randomOrder:true` y `#auto=guess` llega al
  podio. Capturas en `VERIFICACION/v2.4/modos/` (álbum y juego por
  modo), revisadas a ojo: vista previa de Imitación, franja inferior
  del Cadáver, piel de cebolla de Animación, frase anterior de
  Historia, fondo acumulado de Complementar (sin borrador ni Limpiar)
  y fondo fijo de Fondo se ven como deben. **Sin compilar ni subir
  nada a GitHub.**

### 5. Auditoría y endurecimiento del wifi local (el objetivo final)
- Roi dejó claro que el objetivo final es jugar por wifi local y que
  debe funcionar muy bien ahí. Se auditó el flujo wifi completo y se
  probó con dos instancias reales del juego (anfitrión + clientes en
  Chromium headless, pilotados por CDP, con un servidor Node que hace
  de red local y reenvía las peticiones al anfitrión como el plugin
  LanServer). Harness `VERIFICACION/v2.4/wifi/run-wifi.mjs`,
  resultados en `VERIFICACION/v2.4/wifi/wifi-resultados.json`,
  capturas en `VERIFICACION/v2.4/wifi/`.
- **Fallo grave 1 — el anfitrión jugaba TODOS los turnos en su
  teléfono.** En wifi Normal el anfitrión usaba el flujo de un solo
  teléfono: tras EMPEZAR le salía «Pásale el teléfono a Ana…» y
  jugaba el turno de cada jugador en su propio teléfono, mientras los
  clientes esperaban su turno sin que les llegara nunca (el anfitrión
  avanzaba el paso antes de que vieran su tarea y sus entregas se
  rechazaban). Reproducido en la simulación: la partida «terminaba»
  con el álbum completo, pero los clientes nunca jugaron. Corregido:
  el anfitrión juega como un cliente más (`HostTransport`, sin HTTP,
  sondea su propio estado igual que los demás) y solo hace su turno
  de cada paso. Verificado: en cada álbum los autores son una
  permutación de los jugadores y cada uno hizo exactamente sus
  eslabones (p. ej. Normal: [[0,3,2,1],[1,0,3,2],[2,1,0,3],
  [3,2,1,0]]).
- **Fallo grave 2 — la partida se colgaba si un jugador no
  entregaba.** No había ningún temporizador en el anfitrión para el
  modo Normal: si a un cliente se le caía el hotspot o cerraba la
  app, el paso no avanzaba nunca. Corregido con un vigilante
  (`hostWatchdog`, cada 2 s): si falta un turno, lo salta con un
  eslabón vacío y la partida sigue. El que avisó que se iba se salta
  a los 5 s; el que desapareció sin avisar (sin sondear desde hace
  20 s, latido `HOST.lastSeen`) se salta a los 10 s de paso; el resto,
  al acabarse su tiempo + 15 s de margen para que su envío llegue.
  Sin límite (Obra maestra): tope de 5 min por turno. Los turnos
  saltados se avisan en la espera («Se saltó el turno de X (no
  respondía)»).
- **Fallo 3 — la entrega del turno se perdía en silencio.** Si el
  envío fallaba (el hotspot parpadeó), no se reintentaba y el turno
  se perdía. Corregido: reintentos cada 2 s hasta que entre, con
  aviso en pantalla; la entrega es idempotente en el anfitrión (si la
  respuesta se perdió y el cliente reintenta, no se duplica: devuelve
  `already:true`). Timeout de envío 5 s → 15 s.
- **Fallo 4 — el cliente no se enteraba de nada al desconectarse.**
  El sondeo en partida ignoraba los errores en silencio y el jugador
  se quedaba en la espera para siempre. Corregido: aviso «Sin
  conexión con el anfitrión… (N s). Seguimos reintentando» y, si el
  anfitrión cerró la sala, «El anfitrión cerró la sala. Vuelve al
  inicio para crear o unirte a otra.» (también en Adivina y en el
  lobby). El sondeo del cliente pasó de 2 s a 1 s.
- **Fallo 5 — Adivina: el dibujante nunca elegía palabra.** El
  temporizador del anfitrión auto-elegía al cabo de 1 s, así que el
  dibujante nunca veía las 3 opciones. Corregido: 15 s para elegir
  (se ven en la píldora: «Elige · 14 s»); si no elige, se auto-elige.
- **Fallo 6 — el expulsado volvía a entrar.** La expulsión no se
  recordaba (la lista era de ids y al volver le daban otro) y la
  pantalla decía «En la sala» aunque no había entrado. Corregido:
  el anfitrión recuerda los nombres expulsados y rechaza el reingreso
  («expulsado»); el expulsado lo ve en su pantalla («El anfitrión te
  expulsó de la sala»); y solo se dice «En la sala» cuando el
  anfitrión aceptó de verdad (`j.ok`). Además dos jugadores con el
  mismo apodo ya no se confunden: el segundo entra como «Ana 2».
- **Fallo 7 — EMPEZAR no dejaba jugar con 2 jugadores en los modos
  de mínimo 2** (Obra maestra, Animación, Fondo): el botón usaba un
  mínimo fijo de 3. Corregido: usa `specFor(modo).min`.
- Otros: el cliente avisa al anfitrión al salir (`/api/leave`; en el
  lobby sale de la lista, en partida el vigilante lo salta a los 5 s);
  reconexión: el teléfono guarda su id de jugador y si se le cae el
  hotspot y vuelve a unirse con el mismo código, el anfitrión lo
  readmite aunque la partida ya empezó; el botón Unirse no se puede
  pulsar dos veces seguidas; INVITAR copia el puerto real (no
  siempre 7777); el fondo acumulado se cachea por cadena+paso (antes
  el anfitrión lo volvía a componer en cada sondeo); timeout de
  unirse 3 s → 8 s.
- Verificación wifi (10 escenarios, todos OK, 0 errores de consola):
  Normal, Historia, Secreto y Animación por wifi (4 jugadores,
  partida completa hasta el álbum, autoría verificada); Adivina por
  wifi (podio en las 4 páginas, el dibujante elige palabra);
  jugador que se cae a mitad de partida (la partida termina, 55 s);
  anfitrión que abandona (los clientes ven el aviso); expulsión y
  reingreso; llegada tardía (rechazada con mensaje claro);
  reconexión a mitad de partida (vuelve a entrar y termina el
  juego). Regresión de un solo teléfono intacta (ver §4 y la
  verificación de modos: 0 errores).
- Lo que SOLO se puede probar con dos teléfonos reales (pendiente de
  Roi): el hotspot de verdad entre dos Redmi (la simulación usa
  127.0.0.1 y el plugin LanServer real no se ejecuta en el navegador),
  dibujar con el dedo, sonidos y vibración por wifi, y que la IP que
  anuncia el anfitrión sea la del punto de acceso (192.168.43.x) en
  su teléfono.

### 6. Correcciones de la revisión general y de modos (23 nov 2026)
- Todo lo de esta sección se aplicó el 23 nov 2026 en `www/index.html`
  (md5 final `4e58b6c5cc074a36c4dcda167d92ee4a`, idéntico entre `www` y
  el asset de Android tras `npx cap sync android`) y se verificó con los
  harnesses de modos y de wifi (0 errores) y con medidas y capturas
  nuevas en `VERIFICACION/v2.4/correcciones/` (harness de medida
  `measure.py`, Chromium headless 360x800; capturas `med-*.png`,
  `ice-album.png`, `anim-album.png`). **Sin compilar ni subir nada
  a GitHub** (regla de Roi: solo la versión completa).
- **ALTA — pantalla de dibujo (revisión general A1/A2):** la pantalla
  medía 936–958 px en un viewport de 800 px; la paleta no se veía sin
  bajar con el dedo y ¡HECHO! quedaba bajo el pliegue en Imitación,
  Pieza que falta y Cadáver exquisito, y cortado en Sándwich,
  Puntuación, Rompehielos y Cooperativo. Se compactó: herramientas en
  2 filas de 5+4 (el salto ya no es tras la 3.ª y la 6.ª, sino solo
  tras la 5.ª); barra roja con `position:sticky; bottom:0` (¡HECHO! y
  la paleta quedan siempre visibles aunque la página haga scroll);
  lienzo más estrecho (máx. 330 px centrado); texto de progreso
  escondido a ≤400 px; caja de la frase y márgenes más compactos;
  tira de Cadáver de 90→70 px y su rótulo fusionado con el de la
  parte («Dibuja: Torso (solo se ve la franja inferior…)») para no
  repetirlo. Medido tras el arreglo (360x800): **inicio 800 px,
  Normal/Rompehielos/Imitación/Sándwich/Animación 800 px, Pieza que
  falta 800 px, con ¡HECHO! visible (bottom 645–694) y paleta visible
  (bottom 668–731)**; Cadáver exquisito 854 px (la tira añade altura)
  pero con ¡HECHO! (bottom 716) y paleta (bottom 793) visibles por
  la barra fija. El lienzo sigue siendo 640x440 y la barra compacta
  oficial (lápiz, ↕, color, paleta en 2 filas, ✔) no se tocó.
- **ALTA — Rompehielos (revisión de modos):** en el original cada
  frase la dibujan TODOS los jugadores y al final se muestran juntos
  todos los dibujos de la misma frase. La app hacía 1 dibujo por
  frase (cadena de 2 pasos). **Rehecho:** `steps(n)=n` (escribir +
  n−1 de dibujo), flag `icebreaker:true`; en el paso de dibujo la
  tarea es siempre la frase inicial de la cadena (`links[0].text`),
  así todos dibujan cada pregunta; el álbum se agrupa por pregunta
  (pregunta + todos sus dibujos juntos) con el título «Álbum de
  Rompehielos: así quedó la cadena.» y un álbum por pregunta (Álbum
  1 de N). La tarjeta del modo ya prometía «se muestran juntos todos
  los dibujos» y ahora se cumple. Verificado: partida automática de
  4 jugadores (4×4) y álbum agrupado revisado a ojo
  (`correcciones/ice-album.png`: pregunta de Ana + dibujos de Dan,
  Carla y Beto juntos).
- **ALTA — Pieza que falta (revisión de modos):** en el original se
  dibuja ENCIMA del dibujo incompleto y al pasar se borra la parte
  más antigua. La app mostraba el anterior como vista previa que
  desaparecía y dibujaba en blanco. **Corregida con los trazos ya
  guardados por eslabón:** nueva función `strokesImage(strokes)`
  (lienzo 640×440 blanco + trazos → dataURL); en el paso de dibujo,
  `promptImage = strokesImage(last.strokes)` (solo la última parte
  añadida) y el lienzo arranca con esa imagen (`initialImage`), así
  el jugador dibuja encima; al entregar, el siguiente paso solo
  recibe los trazos de ese eslabón, así la parte más antigua se
  pierde. Funciona en un solo teléfono y por wifi (`showWifiTask`
  pasa `initialImage` con el mismo `partLabel`). Verificado: partida
  automática 4×4, 0 errores; captura `med-play-missing.png` (el
  trazo anterior ya está pintado en el lienzo).
- **ALTA — sonidos de la cuenta atrás (ver §1):** `count(n)` ahora es
  tic 1245 Hz (0,25 s) por número y `count(true)` es el arpegio
  784→880→1174 Hz al llegar a 0, sin «¡ya!». **Alarma de poco
  tiempo:** se quitó `AudioFX.tick()` (el tic de 10 s no existe);
  cuando queda ~1/6 del tiempo (`warnAt`, mín. 2 s), la píldora del
  temporizador se pone AMARILLA (la base ahora es blanca, no
  amarilla) y suenan los tonos 1314+1550 Hz SOSTENIDOS
  (`AudioFX.alarmStart()`/`alarmStop()`) hasta el fin del turno,
  con vibración [60] al arrancar. Integrada en `setTimer`/`drawTimer`
  (Normal y 14 modos), en Adivina (ronda en vivo y turno de 30 s del
  adivinador) y por wifi (`renderGuessFromState`, fase «draw»); se
  para al acabar el turno (`stopTimer`, `guessStopTimers`). **Visual
  de la cuenta atrás:** rombo violeta con bombillitas amarillas y
  número verde menta, dibujado con CSS (`.cd-wrap`, `.cd-starburst`
  con rayos girando, `.cd-diamond` rotado 45° con borde `#ffc531`,
  8 `.cd-bulb`), como el original (antes número violeta en tarjeta
  lavanda). Captura `med-countdown.png`.
- **ALTA — pestaña PREESTABLECIDOS ilegible (revisión general A3):**
  verde `#22c55e` sobre violeta oscuro (contraste 2,28) y a 360 px
  la palabra desbordaba la pestaña. Copiado el original: pestaña
  **activa: fondo blanco + texto verde**; **inactiva: texto blanco
  sobre violeta oscuro**; fuente .85rem. Captura `med-home.png`
  (ANÓNIMO en verde sobre blanco, VERIFICADO en blanco sobre
  violeta, se lee bien).
- **MEDIA — reproductor de animación (revisión de modos):** el
  reproductor del álbum era mínimo (500 ms fijos, sin velocidad ni
  bucle). Ahora tiene **selector de velocidad (1's–10's: 100–1000 ms
  por fotograma, 4's por defecto), selector de bucle (Infinito,
  Adelante y atrás, Una vez), exposición por fotograma (0x/1x/2x/3x,
  botones «F1 · 1x» que ciclan 1→2→3→0→1; 0x salta el fotograma) y
  el mensaje del bot «Gartic»** («¡Aquí está la animación que
  crearon entre todos!»). En Fondo, el primer dibujo (fondo fijo) se
  excluye de los fotogramas. Captura `correcciones/anim-album.png`.
- **MEDIA — Fondo: fotogramas confirmados (revisión de modos):** el
  LEEME decía «el doble (N+1 pasos)» y una guía decía el DOBLE de
  fotogramas que Animación: era contradictorio. Confirmado con la
  guía citada en el informe (DigitFeast: «el doble de fotogramas que
  Animation»): **Fondo = 1 fondo + 2N fotogramas (2N+1 pasos)**,
  con 4 jugadores 9 pasos (antes 5). Corregido en `MODE_SPECS` y en
  el texto del modo. Verificado: partida automática 4×9.
- **MEDIA — reloj de Solo (revisión de modos):** en el original con
  amigos el reloj arranca cuando la mitad termina el turno y solo no
  hay presión. **Jugando solo (1 jugador) ya no hay límite de
  tiempo** (`time` devuelve 0 si n≤1; `timeFor` recibe `this.n`);
  con amigos sigue el tiempo de dibujo normal. Verificado: partida
  automática 4×5.
- **MEDIA — censura al describir en Secreto (revisión de modos):**
  el texto al describir no se censuraba (en el original tus palabras
  salen como ● también ahí). Ahora `renderDescribe` muestra el
  overlay de ●●● cuando el modo es Secreto (igual que al escribir).
- **MEDIA — ¡HECHO! bajo el pliegue en Cadáver exquisito:** cubierto
  por la compactación de la pantalla de dibujo (ver ALTA arriba);
  medido: ¡HECHO! a bottom 716, visible.
- **MEDIA — inicio bajo el pliegue (revisión general M1):** «Cómo se
  juega» y «⚙️ Ajustes» quedaban a y=867 (docH 1067). El perfil
  ahora es **plegable**: si ya hay apodo guardado se muestra el
  resumen (avatar + apodo + «Cambiar perfil») y el editor solo al
  tocarlo; si no hay perfil, se muestra el editor (primera vez).
  Además: logo más pequeño, botones a 48 px, nota al pie acortada.
  Medido con perfil guardado (como en el teléfono de Roi): **inicio
  800 px, todo visible sin desplazar** (captura `med-home.png`).
  Sin perfil guardado (primera vez) sigue siendo ~1000 px por el
  editor de avatar.
- **MEDIA — selector duplicado (M2):** «14 JUGADORES 14 ⌄» en Modos
  y en Crear sala. Las etiquetas de los `count-bar` ahora son solo
  «JUGADORES» (el número ya está en el select). (El de wifi ya era
  solo HTML, sin setter JS.)
- **MEDIA — Adivina en vivo con poco contraste (M3):** nombres y
  puntos en blanco sobre lavanda y pista en blanco sobre
  gris-lavanda. Ahora `.hint-bar` y `.g-players` son tarjetas
  blancas con tinta oscura (`#2a1a5e`); los «+» y aciertos en verde
  oscuro `#0a7a5c`. Medido: Adivina en vivo 800 px.
- **MEDIA — álbum al límite (M4):** «Nueva partida» al límite y
  «Volver al inicio» bajo el pliegue. Margen de `.album-step` de
  12→8 px; docH del álbum 921 px (la pantalla es larga por diseño:
  muestra todos los eslabones; el scroll ahí es normal). La tira de
  jugadores del álbum ahora **se parte en dos filas a ≤400 px** en
  vez de cortar al 4.º jugador (M6).
- **MEDIA — fila de avatares con el 5.º cortado (M6):** los
  `.avatar-slot` ahora son de 54 px (círculo 46 px) a ≤400 px, así
  caben 5 a 360 px; la tira de jugadores del álbum se parte en filas
  (ver M4).
- **MEDIA — herramientas a 44 px (M7):** los 9 botones de
  herramientas ahora tienen `min-height:48px` en toda la app. Las
  muestras de color (32 px) y los puntos de grosor (34 px) NO se
  tocaron: son como en el original.
- **MEDIA — temporizador de Cadáver a segunda fila (M9):**
  `#turnLabel` ahora tiene ellipsis (`flex:1`, sin salto de línea);
  el título largo («Turno de Beto · Cadáver exquisito») se recorta
  como «Cadáver…» y el temporizador queda en la misma fila.
- **BAJA — texto de Tiempo cortado (B7):** la opción «Normal (45 s
  escribir · 60 s dibujar · 45 s describir)» se cortaba en el select
  («…60 s dibu»). Ahora: «Normal (45/60/45 s)», «Rápido
  (30/45/30 s)», «Lento (90/120/90 s)».
- **BAJA — subtítulo del inicio partido (B8):** «Dibujar · describir
  · adivinar — sin internet» se partía en dos líneas a 360 px. El
  subtítulo (`.logo-sub`) ahora se esconde a ≤400 px; la nota al pie
  acortada ya dice lo mismo.
- **BAJA — NO hecho (queda pendiente):** iconos de modo dibujados en
  vez de emojis (los 15 iconos oficiales están como referencia en
  `VERIFICACION/v2.4/revision-modos-visual/`, pero no se incrustaron:
  haría falta dibujarlos en el estilo de la app); ajustes de
  exhibición del álbum del original (automático/manual, voz en off,
  flujo principio/fin). B1 (logo de SanBer blando en la apertura:
  imagen de 194x194 mostrada a 230 px) solo se cambia si Roi lo
  pide: es su logo real. B2 (verde del álbum sobre lavanda) es como
  el original y se queda.
- Verificación de estas correcciones (Chromium headless, 360x800):
  * **Modos** (`VERIFICACION/v2.4/modos/verify_modes.py`, resultados
    en `modos-verificacion.json`): los 14 modos + Normal + Adivina +
    navegación, **0 errores de consola, 0 desbordamiento**; partidas
    completas de 4 jugadores hasta el álbum (Historia 4×4, Obra
    maestra 4×1, Secreto 4×4, Sándwich 4×4, Puntuación 4×4,
    Rompehielos 4×4, Imitación 4×4, Complementar 4×4, Pieza que
    falta 4×4, Cadáver 4×3, Cooperativo 4×6, Animación 4×4, Fondo
    4×9, Solo 4×5); Normal `validPermutation:true,
    randomOrder:true`; Adivina hasta el podio.
  * **Wifi** (`VERIFICACION/v2.4/wifi/run-wifi.mjs all`, resultados
    en `wifi-resultados.json`): **12 escenarios, todos OK, 0 errores
    de consola** (Normal, Historia, Secreto, Animación, **Rompehielos
    y Pieza que falta (nuevos en el simulador)**, Adivina, jugador que
    se cae, anfitrión que abandona, expulsión, llegada tardía,
    reconexión). Confirmado al cerrar las correcciones.
  * **Medidas** (`VERIFICACION/v2.4/correcciones/measure.py`): ver
    ALTA arriba (inicio 800, dibujo 800 salvo Cadáver 854 con todo
    visible, cuenta atrás 800, Adivina en vivo 800).
  * El autotest interno (`#auto=*`) ya no usa `AudioFX.tick()`:
    prueba `count(false)`, `count(true)`, `alarmStart()` y
    `alarmStop()` (antes `tick()` no existía y `fxOk` salía false).

### 7. Corrección de los 2 fallos bloqueantes de la revisión final (23 nov 2026)
La revisión final (`VERIFICACION/v2.4/revision-final/README.md`)
encontró 2 fallos que impedían compilar, los dos en la pantalla de
dibujo a 360 px. Corregidos y re-verificados; también se aplicaron el
divisor de fin de álbum y el cambio de sonido F7, y se amplió la
verificación a 7 tamaños de pantalla por pedido de Roi (sus amigos
tienen otros teléfonos; Android 9+ está cubierto por minSdk 24,
`android/variables.gradle`).
- **B1 — «Deshacer» cortado (antes: `scrollWidth=68, clientWidth=61`,
  la «r» final se veía a la mitad en las 13 pantallas de dibujo a
  360 px).** La fila Deshacer/Rehacer/Limpiar/✕ Salir queda en 1×4
  con fuente .75rem y padding 10px 2px (antes .85rem y 10px 4px), y a
  ≤340 px pasa a 2×2 con fuente .8rem (botones de ~134 px). Después:
  «Deshacer» 65v65, `clip=False` en las 13 pantallas de dibujo a
  360 px y a 390 px; la fila sigue a 48 px de alto.
- **B2 — la barra roja fija tapaba la fila Deshacer en Cadáver e
  Imitación (antes: docH 896 y 966 a 360 px, la fila tapada del todo
  en Imitación-preview).** Tres cambios que suman: (1) la vista
  previa de Imitación ya no es un bloque en la pantalla: va ENCIMA
  del lienzo (`position:absolute; inset:0`, `pointer-events:none`,
  con una píldora «Desaparece al empezar a trazar»), se ve a tamaño
  completo con `object-fit:contain` y desaparece sola al empezar a
  trazar, como en el original (se quitó el toque para ampliar); (2)
  la tira de Cadáver pasa de 70 px a 48 px y su etiqueta se acorta a
  «Dibuja: Torso · solo ves la franja inferior» (antes ocupaba 2
  líneas); (3) el lienzo pasa de 330 px a 300 px y la barra de
  herramientas queda en 2 filas (5+4, fuente .68rem, padding 6px 3px,
  gap 4px; a ≤340 px fuente .6rem). Después: pantalla de dibujo
  docH=800 a 360 px en Normal, Cadáver e Imitación-preview (antes
  854/896/966), fila entera visible y pulsable, sin solapes con la
  barra roja (medido también a scroll máximo).
- **Divisor de fin de álbum (extra, fidelidad):** al final de cada
  álbum sale «— FIN DEL ÁLBUM DE ANA —», como en las fotos de
  Pinterest del original. Primer intento con color lavanda claro
  `#efe6ff` casi no se veía sobre la tarjeta lavanda: ahora usa
  `var(--muted)` (violeta apagado) y se lee bien.
- **F7 — fin de ronda (extra, sonido):** `chime()` ya no reusa
  1314+1550 Hz (las frecuencias de la alarma de poco tiempo): ahora
  es un acorde mayor 523+659+784 Hz simultáneo, distinto de la
  alarma (1314+1550 Hz sostenidos) y del arpegio de cambio de turno
  (784→880→1174 Hz seguidos). Las frecuencias medidas de la cuenta
  atrás (tic 1245 Hz + arpegio) y de la alarma no se tocaron.
- **Verificación multi-tamaño (nuevo, pedido de Roi):** 320x568,
  360x640, 360x740, 360x800, 384x854, 412x915 y 430x932, con driver
  de emulación móvil (`VERIFICACION/v2.4/revision-final/fix-b1b2/`,
  `measure_b1b2.py` + `driver-390.mjs` para 390x844; la variante
  multi-tamaño del driver (con alto parametrizable y auditoría a
  scroll máximo) vivía en /tmp y se perdió en un reinicio del
  servicio, pero los JSON con sus resultados
  `revision-general-<WxH>-extra.json` sí quedaron guardados). En cada tamaño:
  inicio, dibujo (paleta y ¡HECHO! visibles, fila Deshacer entera y
  pulsable, también Cadáver e Imitación-preview, medido a scroll 0 y
  a scroll máximo), álbum con el divisor, sala (Crear) y Modos.
  Resultado: **0 errores de consola y 0 desbordamiento horizontal en
  los 7 tamaños**. Dos hallazgos extra y sus arreglos: (1) a 320 px
  el inicio desbordaba a lo ancho (scrollW 354): la rejilla de
  avatares (6 columnas de 48 px) no cabía; a ≤340 px pasa a 4
  columnas; después overflow=False. (2) a 412 y 430 px la pantalla
  de dibujo medía 1612 px y la paleta se apilaba en una columna
  vertical (el diseño compacto solo existía a ≤400 px): nueva media
  query 401–480 px con el mismo diseño compacto (lienzo 340 px);
  después docH=915/932, igual que el viewport, con paleta en 2 filas
  y ¡HECHO! visibles. En pantallas cortas (320x568, 360x640) la
  pantalla de dibujo necesita bajar con el dedo (docH 807/759 frente
  a viewport 568/640), pero la fila Deshacer y ¡HECHO! se ven y se
  pueden pulsar, también a scroll máximo; el inicio en primera vez
  (sin perfil guardado) también es largo en esos tamaños (docH
  1123/1002) y se baja con el dedo, como ya estaba documentado (F4).
  Con perfil guardado el inicio cabe en 800 px a 360 px.
- **Verificación final de esta tanda (Chromium headless):**
  * **360x800** (driver de emulación móvil, 18 pantallas): 0
    errores, 0 desbordamiento; dibujo docH=800 en las 17 pantallas
    de dibujo, «Deshacer» sin recorte en todas, sin solapes en la
    fila, barra de herramientas en 2 filas (104 px); capturas en
    `VERIFICACION/v2.4/revision-final/fix-b1b2/shots-360/`
    (draw.png, play-corpse.png, draw-memory.png, album.png),
    revisadas a ojo.
  * **390x844** (driver recreado `driver-390.mjs`, 36 pantallas):
    0 errores, 0 desbordamiento, 0 elementos recortados; dibujo
    docH=844 en las 17 pantallas de dibujo; Baloo 2 700/800 cargada;
    capturas en `.../fix-b1b2/shots-390/`, revisadas a ojo
    (draw-memory con la vista previa encima del lienzo, álbum con
    el divisor visible).
  * **Modos** (`verify_modes.py` re-ejecutado tras los arreglos):
    14 modos + Normal + Adivina + navegación, **0 errores, 0
    desbordamiento** (`modos-verificacion.json` re-generado).
  * **Wifi** (`run-wifi.mjs normal` y `run-wifi.mjs guess`,
    re-ejecutados tras los arreglos): Normal OK (4 álbumes de 4
    eslabones, autoría y permutación correctas) y Adivina OK (las 4
    páginas llegan al podio), **0 errores de consola**. Nota: la
    pasada completa de 12 escenarios (05:01 UTC) era con el www
    anterior a estos arreglos; los arreglos no tocan el motor wifi
    (HostTransport y hostWatchdog intactos), solo el dibujo, el
    álbum y el sonido de fin de ronda.

### 8. Correcciones de ChatGPT (23 nov 2026, puntos 1–5; el 6 no se hizo)

ChatGPT analizó el proyecto completo desde Drive y dejó 5 puntos
graves/medios (más el 6, de instalación, que ya no se hace: ver
abajo). Se aplicaron todos en `www/index.html`, sin tocar el ícono
(D5 a medio instalar) y sin compilar. Informe completo en
`VERIFICACION/v2.4/correcciones-chatgpt/README.md`.

**1. Turnos Wi-Fi: el sondeo ya no vuelve a montar la pantalla.**
El cliente sondeaba cada 1 s y volvía a montar el turno en cada
respuesta: se perdían la frase, el lienzo, el foco y el reloj se
reiniciaba. Ahora el turno mostrado se separa del enviado: clave
`gameId|paso|jugador`; `showWifiTask` solo se llama con clave nueva
y con la misma clave solo se actualizan el reloj (con el tiempo
restante que calcula el anfitrión, `hostSetStepClock`) y el estado
de red. El sondeo es serializado (cadena con `setTimeout`, no
`setInterval`) y las respuestas tardías se descartan por `session`.
La entrega es idempotente con reintentos cada 2 s; si el anfitrión
ya saltó el turno, el reintento se cancela con aviso. Al salir se
detienen sondeos, temporizadores y reintentos (`stopNetPoll` sube
la sesión; `leaveGame`/`goHome` suben `submitToken`). Aviso (toast)
al perder/recuperar la conexión sin salir de la pantalla. «Otra
ronda» desde el álbum Wi-Fi: el anfitrión vuelve al lobby con los
mismos jugadores y el invitado espera (`waitForNextWifiGame`) hasta
que llegue un `gameId` nuevo.

**2. Reparto con 10 y 14 jugadores.** El respaldo usaba una lista
fija de 8 índices: con 10 o 14 jugadores salían asignaciones vacías
o repetidas. Ahora `cyclicOrders(n, steps)` construye los índices
desde el nº real de jugadores (orden barajado + desplazamientos
barajados con 0 en la primera) y `validateOrders` comprueba cada
columna como permutación, índices válidos y paso 1 ≠ autor (salvo
1 jugador). `GameEngine.start()` reconstruye `stepMap` desde cero
y valida/regenera el reparto si falla. Verificado con
`#auto=distrib`: 2.240 comprobaciones (n=1..14, pasos 1, 2, n,
2n+1), 0 fallos; partidas completas de Obra maestra (1 paso),
Fondo (2n+1 pasos), Normal a 10 y 14 jugadores y Personalizado con
turnos aleatorios.

**3. Transporte nativo en Android.** La WebView es HTTPS y el
anfitrión HTTP: contenido mixto bloqueado en la APK. Ahora todas
las peticiones al anfitrión van por `CapacitorHttp.request` en
Android (`nativeHttp()`; `fetch` solo en navegador/simulación),
con timeouts y errores clasificados (`address`/`http`/`timeout`/
`network`). El ping de «Unirse» va por `transport.ping()` (antes
era un `fetch` directo) con mensajes distintos según el error, y
la IP se valida octeto a octeto (0–255) y el puerto (1–65535). El
servidor local se cierra bien (`stopLanServer`: elimina el listener
`onRequest` guardado y llama a `plugin.disconnect()` al cerrar la
sala, al salir y al ir atrás desde crear-sala; el listener se
registra una sola vez por sala). Botón ↻ para refrescar la IP
anunciada. `detectLanIp()` ya priorizaba 192.168.43.x; no se cambió
Java. Sin `allowMixedContent` global.

**4. Adivina por revisión, no por trazos.** Antes se sincronizaba
la lista de trazos y el cursor por longitud se rompía al cortar a
600 (y las formas, el relleno, Deshacer, Rehacer y Limpiar solo
cambiaban el lienzo local). Ahora el dibujante sube la imagen
completa del lienzo (640×440) con su nº de revisión cada vez que
cambia (`notifyCanvasChange` en pincel, borrador, formas, relleno,
Deshacer, Rehacer y Limpiar; envío agrupado con reintento y
confirmación del último dibujo al pulsar «¡Hecho!»). El invitado
informa qué revisión tiene (`knownRev`) y el anfitrión le devuelve
la imagen solo si cambió; la aplicación comprueba ronda y revisión
en `onload` para no sobrescribir un dibujo posterior. Verificado:
650 trazos con todas las herramientas, lienzo del invitado
idéntico byte a byte al del dibujante.

**5. Ajustes personalizados.** «Personalizado» es ahora la
configuración de una partida basada en Normal, con configuración
efectiva validada al empezar (`effectiveCustom`: tiempo por tipo de
tarea, secuencia, turnos, sigue dibujando, puntuación, secreto)
que usan el motor, las pantallas y el resumen de sala; el
anfitrión comparte la configuración congelada (`customCfg` en el
estado; `randomRounds` se sortea una sola vez). La pestaña AJUSTES
PERSONALIZADOS pone `S.mode="custom"` y PREESTABLECIDOS vuelve a
Normal. En el álbum, la puntuación también vale en Personalizado
(voto común por wifi con `scoreVote`, marcador compartido sin
re-montar el álbum; criterio «Conservó la idea del dibujo
anterior» en Solo dibujar). Verificado: 6 partidas reales cambiando
un ajuste cada vez (tiempo rápido, solo dibujar, sigue dibujando,
puntuación, secreto, turnos aleatorios).

**Endurecimiento extra encontrado al probar:** `taskFor` reventaba
si el motor no había llamado a `start()` (el motor del cliente en
wifi no lo llama: `chains` vacío). Ahora devuelve la tarea sin
pista en vez de reventar (también la rama de Rompehielos).

**6. Instalación (punto 6 de ChatGPT): NO SE HACE.** Roi avisó el
23 nov 01:52–01:54: «Nada, me instaló solo al final» — la v2.1
terminó instalándose sola en su Redmi, sin causa concreta
identificada (ni espacio, ni reinicio, ni Chrome: simplemente al
final instaló). Queda como antecedente por si vuelve a pasar con
otra versión; el motivo exacto queda pendiente de que Roi lo
confirme. No se preparó el diagnóstico ni queda como pendiente.
Ver la constancia en «Problema de instalación» más abajo.

## Novedades de la v2.3 (1.3.0)

Regla de Roi para esta versión: no se compila ni se entrega ninguna APK
intermedia o a medias; todo lo pedido va dentro de la misma v2.3 y solo
cuando esté terminado y verificado se lanza la compilación. Por eso esta
versión trae los 6 puntos juntos (atrás, botones, fluidez, ventanas,
álbum aleatorio, ícono) más la investigación de los vídeos de Vegetta777,
los sonidos medidos del original y la revisión visual completa.

### 1. Ir atrás (botón de Android y botón dentro de la app)
- Se instaló el plugin `@capacitor/app` 8.1.2 (su evento `backButton` y
  `exitApp()`); `npx cap sync android` lo registra junto a
  `capacitor-lan-server`. En el navegador (pruebas) hay un estado
  guardián con `history.pushState` + `popstate` para que el botón atrás
  del navegador haga lo mismo.
- La app lleva una pila de pantallas (`navStack`): cada pantalla segura
  (inicio, modos, ajustes, crear/unirse, salas, álbum, podio…) se apila
  al entrar; las pantallas de partida (cuenta atrás, pasar el teléfono,
  dibujar, describir) NUNCA entran en la pila.
- `goBack()` siempre vuelve a la pantalla anterior lógica: cierra el
  diálogo si está abierto, cierra el panel de grosor/opacidad si está
  abierto, en partida abre el diálogo «¿Salir de la partida?» (salir
  pierde lo jugado; si eres anfitrión wifi se cierra la sala), en la
  sala wifi cierra la sala o el sondeo, y si no, va a la anterior. Nunca
  salta pantallas ni se queda atascado.
- En el menú (inicio): la 1.ª pulsación muestra el aviso «Pulsa de
  nuevo para salir» (toast abajo) y la 2.ª (antes de 2,5 s) sale de la
  app con `App.exitApp()`. En el navegador solo se muestra el aviso.
- Se arregló una fuga de la cuenta atrás: los 4 `setInterval` de la
  cuenta atrás ahora viven en `S.cdTimer` con `stopCountdown()`, que se
  llama al salir; antes, salir en mitad de la cuenta atrás dejaba el
  intervalo vivo y saltaba a la pantalla de pasar el teléfono después.
- Botones nuevos para salir sin depender del botón físico: «Cancelar
  partida» en la cuenta atrás, «Salir de la partida» en la pantalla de
  pasar el teléfono, «✕ Salir» en la fila Deshacer/Rehacer/Limpiar al
  dibujar (Normal y Adivina) y «Salir de la partida» en las pantallas de
  Adivina. El diálogo de salir ahora es genérico (título y texto según
  el caso).

### 2. Botones
- Alturas mínimas para tocar cómodo: `.btn.small` 44→48 px,
  `.tool-btn` 42→44 px (40 px a ≤400 px), `.kick` 40→44 px, botón de
  refrescar el avatar 38→44 px, muestras de color 28→32 px, pestañas y
  segmentos 48 px, Deshacer/Rehacer/Limpiar 36→44 px a ≤400 px.
- El botón atrás dentro de la app (`.back-btn`) usa una flecha de trazo
  SVG, nunca el glifo de texto ← (igual que se corrigió en
  «¡A la frente!»). Las flechas de «Álbum anterior/siguiente» también
  pasaron a SVG.
- Transición `fadeIn` de 0,18 s al cambiar de pantalla y un toast
  (`.toast`) para los avisos («Pulsa de nuevo para salir»,
  «Copiado: IP y código de la sala»…).
- Todo sigue con la estética violeta-magenta: tarjetas lavanda, botones
  blancos redondeados con borde violeta, EMPEZAR con play verde.
  Formas simples y planas, nada con aspecto de IA.

### 3. Fluidez
- El trazo ya no se retrasa: al previsualizar una forma (línea, círculo,
  cuadrado…) la app ya no guarda ni decodifica una imagen en cada
  movimiento del dedo; usa un lienzo oculto (`S.draw.snap`) y lo
  restaura en cada movimiento. Deshacer/rehacer siguen usando imágenes
  (solo de vez en cuando, no se nota).
- Los puntos de grosor del lienzo pasaron de 30 a 34 px para tocarlos
  mejor. Las transiciones entre pantallas son el `fadeIn` de 0,18 s; si
  algo tarda (generar la sala, unirse), hay texto de estado («Generando
  la sala…»), no una pantalla congelada.

### 4. Ventanas (todas revisadas a 360 px)
- Las 18 pantallas se capturaron y se revisaron una por una a 360x800
  (ver «Verificación v2.3»): menú, modos, ajustes, cómo se juega,
  crear/unirse, cuenta atrás, pasar el teléfono, escribir, describir,
  dibujar sin/con panel, álbum, Adivina (dibujar, en vivo, podio) y
  apertura. Sin desbordamiento horizontal en ninguna (comprobado por la
  prueba automática y a ojo).
- **Fallo encontrado y corregido en la revisión:** el bloque CSS de
  pantallas pequeñas (`@media(max-width:400px)`, el que esconde las
  muestras de color y los controles de grosor y deja la barra de dibujo
  compacta) NO se estaba aplicando nunca. La causa: justo antes de ese
  bloque había un comentario al que le faltaba el `/*` de apertura
  («En pantallas pequeñas se esconde la fila de controles… --- */»),
  con un `*/` huérfano; el navegador descartaba el bloque entero.
  Por eso en la primera revisión el botón ✔ ¡HECHO! quedaba a y=1376
  (fuera de la pantalla de 800 px) y había que desplazar para dibujar.
  Corregido el comentario (19 `/*` frente a 20 `*/` → ahora 20 y 20) y
  las reglas ya se aplican: ✔ ¡HECHO! visible a y=597 en dibujo Normal
  y a y=570 en Adivina, con el lienzo y la marca de agua visibles en la
  misma pantalla. Comprobado en la prueba automática (`listoVisible`
  pasó de `false` a `true`).
- **Cuadro amarillo vacío en «Crear sala wifi»:** el resumen de ajustes
  de la sala (`#wifiSettingsSummary`, clase `.notice`) se veía como un
  rectángulo amarillo vacío antes de generarse la sala. Ahora
  `.notice:empty{display:none}` lo esconde mientras no tenga contenido.
- **Dibujo en blanco al describir:** si el dibujo a describir venía
  vacío, la pantalla mostraba el icono de imagen rota del navegador.
  Ahora muestra «… (dibujo en blanco)» en una caja, igual que ya hacía
  el álbum. En juego real el lienzo siempre guarda una imagen (aunque
  esté en blanco), pero el caso queda cubierto.

### 5. Álbum ALEATORIO en el modo Normal (lo más importante)
- Antes, cada frase pasaba al siguiente jugador en orden de lista
  (cadena = autor, autor+1, autor+2…). Ahora cada álbum sigue una
  **permutación aleatoria** de los jugadores, como en Gartic Phone:
  Roi pone la palabra, Alejo la dibuja, Robeidy intenta adivinarla y
  Evelyn la dibuja de nuevo — ese orden es aleatorio y distinto en cada
  álbum y en cada partida.
- Reglas que se cumplen: cada jugador participa exactamente una vez por
  álbum; nadie recibe su propia frase en el primer eslabón (nadie
  dibuja su propia frase); el número de eslabones es N (nº de
  jugadores): 1 frase + N−1 pasos, como hasta ahora. En el álbum final
  cada eslabón muestra su autor, como ya hacía.
- Cómo se genera (`buildOrders(n)` en `www/index.html`): se construye
  un **cuadrado latino aleatorio**: cada fila (cadena) es una
  permutación de los jugadores que empieza por su autor, y cada columna
  (paso) es también una permutación — en cada paso cada jugador hace
  exactamente una tarea y cada cadena recibe exactamente un eslabón.
  Se construye fila a fila eligiendo al azar entre los jugadores
  válidos (sin repetir en la fila ni en la columna, y sin que nadie
  dibuje su propia frase en el paso 1); si se atasca, se reintenta
  (hasta 100 veces). Como último recurso, el orden cíclico con los
  jugadores re-etiquetados al azar, que también es aleatorio y válido.
- **Fallo encontrado y corregido:** la primera versión de la v2.3
  barajaba cada cadena por separado (`[autor].concat(shuffle(resto))`).
  Eso rompía la regla de las columnas: dos cadenas podían pedir al
  mismo jugador en el mismo paso y otro se quedaba sin tarea; el motor
  no terminaba («el motor Normal no terminó» en `#auto=normal`) y los
  álbumes quedaban incompletos. La prueba automática lo cazó antes de
  entregar. Con el cuadrado latino el motor termina siempre.
- Vale para un solo teléfono (3–8 jugadores) y para wifi: el anfitrión
  genera el orden aleatorio en su motor y lo reparte a los clientes
  (el reparto usa el mismo `stepMap` del motor del anfitrión).
- Verificación: 1.200 partidas simuladas en Node (de 3 a 8 jugadores,
  200 por tamaño): 0 fallos — todas las filas y columnas son
  permutaciones, nadie dibuja su propia frase, todos los motores
  terminan y todos los álbumes salen completos. Álbumes no secuenciales:
  68% con 3 jugadores (con 3 solo hay 2 órdenes posibles por cadena),
  88% con 4, 97% con 5, 99% con 6, 99,5% con 7 y 100% con 8. En la
  prueba `#auto=normal` del navegador: `validPermutation:true`,
  `randomOrder:true`, con órdenes como
  «Ana>Dan>Carla>Beto | Beto>Ana>Dan>Carla | Carla>Beto>Ana>Dan |
  Dan>Carla>Beto>Ana» (ninguno es el orden de la lista).

### 6. Ícono nuevo (3 variantes, instalada la A)
- Misma idea: teléfono roto (auricular clásico partido en dos) con
  «Gartic» arriba en blanco y «MÓVIL» en grande abajo en amarillo,
  todo dentro de la zona segura central de 626 px (márgenes 199–823 de
  1024 px), colores planos, degradado violeta a magenta. Script:
  `scripts/make-icon-v2.3.py`. Las tres variantes están en
  `VERIFICACION/v2.3/icon-A.png`, `icon-B.png`, `icon-C.png` (1024 px)
  con su simulación de recorte del launcher a 96 px
  (`icon-X-miui-96.png`) y 192 px (`icon-X-miui-192.png`).
  * **A «Clásico mejorado» (INSTALADA):** como la v2.1 pero con el
    auricular más grande (rx 215, ry 130, copas r78), la rotura más
    ancha (56 px), el rayo más grande (1,15×), «Gartic» 88 y «MÓVIL»
    116. Es la que se lee mejor a 96 px: auricular horizontal, las dos
    copas a la misma altura, rayo amarillo grande y nombre completo
    legible.
  * **B «Diagonal»:** todo el auricular girado −12°, «Gartic» 76,
    «MÓVIL» 122, rayo 1,2×. El giro se lee como una sonrisa o un
    accidente, no como un teléfono roto.
  * **C «Partido abierto»:** las dos mitades bien separadas (72 px,
    giros ±8/9°), chispas amarillas en la rotura, teléfono más pequeño,
    «Gartic» 80, «MÓVIL» 110. El teléfono se lee peor que en la A.
- La variante A está instalada: `assets/icon-1024.png` y todos los
  `mipmap-*` (mdpi 48, hdpi 72, xhdpi 96, xxhdpi 144, xxxhdpi 192) en
  `android/app/src/main/res/` y en `assets/res/` (`ic_launcher.png`,
  `ic_launcher_round.png` por recorte circular,
  `ic_launcher_foreground.png`). Roi elegirá entre las tres cuando
  pruebe la APK; cambiarla es rápido.

### 7. Investigación: vídeos de Vegetta777 y web oficial
- Vídeos vistos (transcripción + fotogramas con yt-dlp y ffmpeg;
  los mp4 se borraron tras sacar los fotogramas para no engordar el
  repo; las transcripciones quedan en `VERIFICACION/v2.3-referencias/`):
  * «Mi primera vez en GARTIC PHONE (Vegetta777)», YouTube
    `JzQOa0IW6IQ`, 2:01:10 (31 ene 2023). Capítulos del propio vídeo:
    0:00 primera partida, 13:18 «HAMBURGUESA SE COME A KIRA», 19:33
    «PERRO SANTA CLAUS CON FALDA ROSA», 28:24 «GATO EN LLAMAS
    CORRIENDO», 31:34 «RUBIUS HACIENDO EL PUENTE EN LA ARENA Y CIELO»
    (los títulos de los capítulos son los resultados de los álbumes).
  * «Vegetta777 y su AUTORETRATO en Gartic Phone», YouTube
    `avQw9MnhpIo`, 16:25. Es modo **Animación**, no Normal: Vegetta
    dibuja su autorretrato fotograma a fotograma (con piel de cebolla:
    el fotograma anterior se ve tenue a la derecha).
  * También se localizó «Who draws better? - GARTIC PHONE»,
    `OrB9DNkQikU`, 1:54:20 (no hizo falta usarlo).
- Web oficial `garticphone.com` (consultada 23 nov 2026, cargó bien
  esta vez, sin bloqueo de Cloudflare): la portada solo explica los
  6 pasos (1. llamar es mejor, 2. escribir, 3. dibujar, 4. describir,
  5. ver qué pasó, 6. hacer amigos). La sala y los álbumes no se ven
  sin entrar al juego. Guías de internet (progameguides, gamertweak,
  abrainrot) confirman: la exhibición final muestra la cadena
  completa, frase a frase y dibujo a dibujo, y las salas son solo por
  invitación, sin salas públicas.
- Fotogramas de referencia guardados en
  `VERIFICACION/v2.3-referencias/` (`ref-01` a `ref-12`, con un
  `README.md` que dice de dónde salió cada uno y qué muestra), más las
  dos transcripciones en español (`.es.vtt`) y la foto de contacto de
  la APK oficial (`apk-oficial-contacto.png`).
- Lo que se vio en el original y se aplicó en la v2.3:
  * Sala (lobby): VOLVER arriba a la izquierda, lista de JUGADORES
    con avatar + nombre y huecos VACÍO, ajustes a la derecha (ESTILO
    DE JUEGO con NORMAL seleccionado, TIEMPO, TURNOS, NÚM. MÁXIMO DE
    JUGADORES, SECUENCIA Escribir→Dibujar) y abajo el texto de espera
    del anfitrión. En la app: huecos VACÍO hasta el máximo en la sala
    wifi y botón INVITAR junto a EMPEZAR (copia la IP y el código de
    la sala al portapapeles, con aviso).
  * Escribir: fondo naranja en el original, teléfono azul con «?» y
    título «EMPIECE A ESCRIBIR UNA HISTORIA» en verde; en la app se
    copiaron el teléfono azul SVG y ese texto exacto (el fondo sigue
    siendo el degradado violeta-magenta de la app, aprobado por Roi).
  * Dibujar: barra violeta arriba con el paso («2/7») y la frase en
    verde, paleta a la izquierda, herramientas a la derecha, lienzo
    blanco con marca de agua «Gartic PHONE», abajo tamaños, deslizador
    de opacidad y botón verde con tick + «¡HECHO!». En la app: la barra
    superior ahora dice «HEY, ¡ES HORA DE DIBUJAR!» (texto del
    original) y el botón de envío dice «¡HECHO!» (antes «¡Listo!»).
  * Describir: barra «¿Y AHORA? DESCRIBA ESTA ESCENA», el dibujo, campo
    de texto y «¡HECHO!» (en el original, tras enviar, el botón pasa a
    «EDITAR»; en un solo teléfono no aplica, porque el turno pasa al
    siguiente jugador).
  * Álbum: título «ÁLBUM DE <nombre>» en verde, subtítulo «Álbum N de
    M», lista de JUGADORES con el dueño del álbum resaltado en verde y
    la cadena como un chat vertical (avatar + burbuja de texto o dibujo
    en tarjeta blanca, con su autor en cada eslabón). Se enseña un
    álbum cada vez, en el orden de la lista de jugadores. En la app la
    lista de la izquierda pasa a ser una tira horizontal arriba (en el
    móvil no cabe al lado) con el dueño resaltado en verde.
  * Consejo del original (paso 1 de la web: «CALLING IS BETTER»): en
    «Cómo se juega» se añadió que, si no están en la misma habitación,
    jueguen en llamada de voz (Discord, Zoom) para reírse juntos.
- Lo que NO se copió (y por qué):
  * El botón «.GIF» para descargar el álbum como GIF animado: hace
    falta codificar un GIF en el teléfono; queda pendiente para una
    versión posterior.
  * Los colores de fondo por paso (naranja al escribir, rojo al
    dibujar, azul al describir): la app mantiene su degradado único
    violeta-magenta, aprobado por Roi a partir de las fotos de la APK
    oficial.
  * El logo oficial «Gartic PHONE»: la app usa su logo propio
    (teléfono blanco + lápiz amarillo, SVG) a propósito.
  * La pestaña VERIFICADO del inicio es decorativa (no hay cuentas).

### 8. Sonidos medidos del original (re-afinados, síntesis propia)
- No se copió ningún archivo de sonido del juego (material con
  derechos): sigue siendo síntesis propia con Web Audio (ondas seno),
  pero afinada con valores MEDIDOS del audio de los vídeos de
  Vegetta777 (descargado con yt-dlp, formato 140; analizado con
  ffmpeg y Python: espectrogramas y STFT). Archivos y scripts en
  `VERIFICACION/v2.3-referencias/sonidos/` (`analisis.py`,
  `analisis2.py`, audios `.m4a`/`.wav`, espectrogramas `spec-*.png`,
  segmentos `seg-*.wav`).
- Lo medido (con vídeo y momento):
  * **Cambio de turno / inicio de turno:** arpegio ascendente
    **Sol5 784 Hz → La5 880 Hz → Re6 1174 Hz**, notas separadas ~90 ms,
    cada una ~0,15–0,2 s con caída rápida. Medido en el vídeo de 2 h
    `JzQOa0IW6IQ` a 797,11/797,20/797,30 s (cambio a dibujo 2/7) y en
    todos los cambios de turno (660,3; 754,9; 796,9; 947,0; 982,3;
    1132,8; 1172,3; 1322,8; 1510,4; 1670,4; 1702,7; 1853,2; 1892,7;
    2042,9; 2082,8; 2233,0 s…): el patrón sigue la partida (unos 150 s
    de dibujo + 35–40 s de descripción por turno, 3 partidas), no un
    bucle de música. Confirmado en el vídeo de 16 min `avQw9MnhpIo` a
    80,86 s (783 Hz) y 81,02 s (880 Hz), también al empezar un turno.
    Antes (v2.2): 523→659→784 Hz. Ahora: **784→880→1174 Hz**.
  * **Alarma de poco tiempo (CORREGIDO 23 nov 2026 — antes se llamaba
    «repique antes del cambio de turno» / «¡ya!»):** dos tonos
    sostenidos **1314 Hz (Mi6) + ~1550 Hz** juntos, que arrancan
    cuando el dial del temporizador se pone **amarillo** (~1/6 del
    dial, ~22 % del tiempo del turno) y siguen hasta el fin del turno.
    Medidos con FFT fina en `JzQOa0IW6IQ` partida 2: cambio 1
    (1308,4 + 1548,0 Hz, desde 795,7 s hasta ~797,3 s), cambio 2
    (1317,4 + 1551,2 Hz, desde 917,5 s), cambio 3 (1313,0 + 1546,0 Hz,
    desde 979,3 s hasta ~982,3 s). No es un repique de 0,4 s ni el
    final de la cuenta atrás: es una alarma sostenida que dura hasta
    30 s en un turno largo de dibujo. El tono de 1314 Hz aparece
    además en la música de fondo (Mi6), pero **el par 1314+1550 Hz
    juntos, sostenidos, solo aparece en los cambios a amarillo** (16
    eventos 1250–1600 Hz en toda la partida 2, agrupados en 796–806,
    916–926 y 976–986 s; en el lobby solo 1 evento suelto). El «repique
    1305 Hz a 947,3 s» que se citaba antes como «fin de tiempo» es la
    cola de esta alarma. Antes (v2.2): 880→1318 Hz. Ahora: **1314 +
    1550 Hz sostenidos desde que el dial se pone amarillo** (pendiente
    de aplicar en el código: sustituir el tic de 10 s por esta alarma).
  * **Cuenta atrás 3-2-1 (CORREGIDO 23 nov 2026): SÍ existe y está
    medida** (ver `VERIFICACION/v2.4/cuenta-atras/`): rombo violeta con
    el número en verde menta sobre la sala oscurecida, ~1 s por número,
    ~3 s en total, solo al empezar cada partida (no entre turnos). Sonido:
    **tic de ~1244 Hz por número** (~0,2–0,3 s, medido a 657,6 y 659,6 s
    en `JzQOa0IW6IQ`) y **arpegio 784→880→1174 Hz al terminar**, cuando
    aparece el primer turno; no hay texto «¡YA!» ni repique distinto.
    La app todavía usa las notas del arpegio por número (**3→784 Hz,
    2→880 Hz, 1→1174 Hz**, 0,2 s cada una) + «¡ya!» 1314+1550 Hz:
    eso NO coincide con lo medido y hay que cambiarlo (`count(n)` a tic
    ~1245 Hz por número, arpegio al llegar a 0; el 1314+1550 Hz **sí
    existe en el original, pero es la alarma de poco tiempo**, no el
    final de la cuenta atrás). Antes (v2.2): 660→480 Hz.
  * **Fin de tiempo:** medido en `JzQOa0IW6IQ` a 944,5–947,5 s: el
    espectro salta al azar (voz de Vegetta), silencio 946,9–947,2 s y
    luego la cola de la alarma de poco tiempo (1305 Hz a 947,3 s) +
    arpegio 783/880/1174 a 947,4–947,6 s. **No hay un pitido distinto
    de «fin de tiempo»**: el turno termina y el siguiente empieza con
    la alarma (si el dial ya estaba amarillo) + arpegio. Por eso la
    app no añade un sonido nuevo de fin de tiempo: usa la alarma +
    arpegio del cambio de turno.
  * **Últimos 10 segundos / tic-tac (CORREGIDO 23 nov 2026): no hay tic
    por segundo, pero SÍ hay un aviso de poco tiempo.** Recomprobado
    en `JzQOa0IW6IQ` 786–798 s (los ~11 s antes del arpegio de cambio
    de turno a 797,1 s): la banda de 1245 Hz no tiene periodicidad de
    1 s; en 937–947 s tampoco había periodicidad de 1 s en las
    frecuencias altas; manda la voz (rms hasta 0,3) y hay 2,4 s de
    silencio a 942,3–944,7 s. Autocorrelación a lag 1,0 s en los
    últimos 10 s y 5 s de 14 fines de turno: sin periodicidad. **Pero
    el temporizador no baja en silencio: es un dial circular que se
    pone AMARILLO a ~1/6 del tiempo y ahí arranca la alarma de dos
    tonos 1314+1550 Hz sostenidos hasta el fin del turno** (ver
    «Alarma de poco tiempo», arriba). El tic de la v2.2 (**1250 Hz,
    0,045 s, una vez por segundo**) hay que **sustituirlo por esa
    alarma**, no dejarlo como ayuda propia (esa frecuencia coincide
    con la del tic de la cuenta atrás, ~1244 Hz medidos).
  * **Acierto:** Gartic Phone no tiene sonido de acierto (no hay
    puntos ni ganador en Normal); en los vídeos de Vegetta no se midió
    ninguno. Se deja el de la v2.2 (**659→880→1318 Hz**) para Adivina,
    como aproximación, no como medida.
- Nuevas frecuencias en la app (`AudioFX` en `www/index.html`):
  `count(n)`: 3→784, 2→880, 1→1174 Hz (0,2 s); `count(true)` «¡ya!»:
  1314 + 1550 Hz (0,4 s); `turn()`: arpegio 784→880→1174 Hz con
  ~90 ms entre notas; `chime()`: 1314 + 1550 Hz (0,5 s, álbum/fin);
  `tick()`: 1250 Hz, 0,045 s (sin cambios, v2.2); `hit()`: 659→880→
  1318 Hz (sin cambios, v2.2). Envolvente igual que antes (ataque
  12 ms, caída exponencial, ondas seno). La prueba automática
  (`#auto=normal` y `#auto=guess`) ejecuta los cinco sonidos y
  reporta `fxOk:true`. **Pendiente (23 nov 2026, ver arriba):**
  `count(n)` debe pasar a tic ~1245 Hz por número y el arpegio al
  llegar a 0 (sin «¡ya!»); `tick()` de 10 s debe sustituirse por la
  alarma de poco tiempo (tonos 1314+1550 Hz sostenidos desde que el
  temporizador baja a ~1/6). El `count(true)` «¡ya!» 1314+1550 Hz
  (0,4 s) es en realidad el sonido de la alarma de poco tiempo, no el
  final de la cuenta atrás.
- Dificultad honesta de la medición: el audio lleva música de fondo
  continua (bucle lofi en Sol mayor: Sol4 392 Hz, Re5 587 Hz, Sol5
  784 Hz…) y Vegetta hablando sin parar; los dos primeros detectores
  automáticos fallaron (0 eventos) y la medida salió de mirar los
  espectrogramas en los cambios de turno (bloque rectangular de tonos
  apilados a 796–799 s) y de buscar la plantilla del arpegio en todo
  el audio. El juicio final a oído sigue siendo de Roi en su Redmi.
- **Añadido en la v2.4 (pase de fidelidad) — CORREGIDO 23 nov 2026:**
  se probaron vídeos de AuronPlay (`KLPUA98-DuQ`, 2908 s) y Juan
  Guarnizo (`Rb6E3Eqppi4`, 798 s; `UFOXXi8zsjQ`, 2149 s) buscando la
  cuenta atrás y el tic limpios. El arpegio quedó confirmado en un vídeo
  independiente (Guarnizo streamers, 1759,8 s: ~880 Hz + ~1357 Hz).
  **La cuenta atrás 3-2-1 SÍ existe en el original** (la afirmación
  contraria de este mismo párrafo era falsa: se había mirado Vegetta a
  las 10:55, 11:00 y 11:05 y la cuenta atrás dura ~3 s justo entre
  medias). Verificación completa en `VERIFICACION/v2.4/cuenta-atras/`
  (README.md, notas.md, fotogramas): 5 inicios de partida confirmados
  en vídeo (Vegetta ×2 Normal, Guarnizo Normal y Knock-Off, AuronPlay
  Normal), rombo violeta con número verde menta, ~1 s por número, tic
  de ~1244 Hz por número + arpegio 784→880→1174 Hz al terminar, solo al
  empezar cada partida (entre turnos no hay: fundido directo). El
  sonido de la cuenta atrás de la app (784/880/1174 por número +
  «¡ya!» 1314+1550 Hz) no coincide con lo medido y hay que cambiarlo
  (tic ~1245 Hz por número + arpegio al final). **El tic de los
  últimos 10 s NO existe como tic por segundo** (recomprobado en
  Vegetta 786–798 s: banda 1245 Hz sin periodicidad a 1 s), **pero SÍ
  hay un aviso de poco tiempo: el dial se pone amarillo a ~1/6 del
  tiempo y suena una alarma de dos tonos 1314+1550 Hz sostenidos hasta
  el fin del turno** (corregido 23 nov 2026; ver el punto de la cuenta
  atrás, arriba). El tic de 1250 Hz hay que sustituirlo por esa
  alarma, no dejarlo como ayuda propia. Scripts nuevos:
  `analisis3.py` (detector de tonos puros) y `analisis4.py` (detector
  genérico de arpegio/tic/cuenta atrás); espectrogramas
  `spec-veg-935-950.png`, `spec-veg-420-480.png`,
  `spec-guarn-1747-1762.png`. Los audios descargados no se suben al
  repo (están en `.gitignore`: `*.m4a`, `*.webm`, `audio-*.wav`).

### 9. Revisión visual completa (toda la app como un todo)
- **Fuente de verdad:** la app pedía «Baloo 2» en el CSS pero no la
  empaquetaba, así que en Android caía a Roboto. Ahora la fuente
  **Baloo 2** (variable, pesos 700 y 800, subconjunto latino woff2 de
  33 KB, licencia OFL) está en `www/fonts/baloo2-latin.woff2` con dos
  `@font-face` y se sincroniza a Android. Nunito sigue sin empaquetarse
  (solo es fallback en la pila).
- **Verde del original:** `--green` pasó de #2ee6a8 (menta) a **#22c55e**
  (el verde vivo del original: triángulos de play, pestaña
  PREESTABLECIDOS, borde de la tarjeta seleccionada, título del dibujo,
  tick de ✔, jugador resaltado en el álbum).
- **Marca de agua del lienzo:** existía en el CSS pero era INVISIBLE
  (el lienzo se pintaba de blanco por encima). Ahora tiene `z-index:2`
  y el lienzo `z-index:1`: se ve «Gartic Móvil» tenue y diagonal sobre
  el dibujo, como en el original, sin afectar a la imagen guardada (es
  DOM, no contenido del lienzo).
- **Textos copiados del original:** «¡Listo!» → **«¡HECHO!»** en 7
  sitios (escribir, describir, dibujar y Adivina); barra de dibujo
  «HEY, ¡ES HORA DE DIBUJAR!» (texto del original); título del álbum
  «ÁLBUM DE <nombre>» en verde con subtítulo «Álbum N de M»; espera
  de unirse: «Esperando a que el anfitrión configure y comience el
  juego.» (texto del original).
- **Cabecera:** la barra superior con el logo (`#topbar`) ahora se
  esconde en las pantallas de juego y de sala (modos, crear/unirse,
  cuenta atrás, pasar el teléfono, dibujar, describir, espera, álbum,
  podio) para que se vean como el original, sin el logo de la app
  estorbando arriba; sigue visible en inicio, modos de un solo
  teléfono, ajustes, cómo se juega y salas.
- **Sala wifi:** botón **INVITAR** junto a EMPEZAR (copia «Gartic
  Móvil · sala CÓDIGO · IP x.x.x.x:puerto · puerto 7777» al
  portapapeles, con aviso), como en la sala del original
  ([puerta] INVITAR EMPEZAR).
- Lo que no se pudo copiar exactamente (dicho en el LEEME, sin inventar
  otro estilo): los fondos de color por paso y el botón «.GIF» del
  álbum (ver §7); el logo oficial (se usa el propio); el «EDITAR» tras
  enviar en un solo teléfono (no aplica).

## ✅ www completo y verificado (v2.4)

### Verificación v2.4 (Chromium headless, 360x800)
Capturas nuevas en `VERIFICACION/v2.4/` (19 PNG a 360x800: las 18 de
la v2.3 + `rooms`, re-tomadas tras las correcciones) y auditoría de
botones en `VERIFICACION/v2.4/buttons-audit.json` (harness
`audit_buttons.py`).
- `#auto=normal` (4 jugadores): 0 errores de consola, 0
  desbordamiento, 4 álbumes con 4 eslabones cada uno, `fxOk:true`,
  `validPermutation:true`, `randomOrder:true`. Órdenes de ejemplo:
  «Ana>Beto>Dan>Carla | Beto>Ana>Carla>Dan | Carla>Dan>Ana>Beto |
  Dan>Carla>Beto>Ana».
- `#auto=guess` (4 jugadores): 0 errores, 0 desbordamiento, podio
  correcto (Carla:38, Dan:34, Beto:30, Ana:10), `drawerBonusCheck:34`,
  `fxOk:true`.
- `#test=nav` (navegación atrás): 0 errores, 0 desbordamiento. Registro
  completo: inicio → setup → modos → atrás → setup → atrás → inicio;
  en partida, atrás abre el diálogo; salir → inicio; en inicio, atrás
  muestra el aviso «Pulsa de nuevo para salir».
- Auditoría de botones (19 pantallas): 0 desbordamientos horizontales,
  0 textos cortados, 0 solapamientos reales. Corregidos: herramientas
  de dibujo en 3 filas visibles (antes desbordaban), «Deshacer» sin
  recorte (fila 2×2 a 48 px), selects de jugadores a 49 px,
  INVITAR/EMPEZAR visibles en Modos (y=671) y Crear sala (y=697).
  Avisos restantes, aceptables: 3 falsos positivos de solape en Modos
  (lista con desplazamiento propio), muestras de color (32 px) y
  puntos de grosor (34 px) como en el original, interruptores de
  Ajustes (fila completa táctil).
- Revisión visual de las 19 capturas nuevas: nada cortado, botones
  coherentes, marca de agua visible en el lienzo, Baloo 2 cargando.
- Wifi local (ver §5 de la v2.4): 10 escenarios simulados con dos
  instancias reales del juego, todos OK, 0 errores de consola:
  Normal, Historia, Secreto y Animación por wifi (autoría verificada),
  Adivina por wifi (podio), jugador que se cae (la partida termina),
  anfitrión que abandona (aviso visible), expulsión y reingreso,
  llegada tardía y reconexión a mitad de partida. Harness
  `VERIFICACION/v2.4/wifi/run-wifi.mjs`, resultados en
  `VERIFICACION/v2.4/wifi/wifi-resultados.json`.
- **Correcciones del 23 nov 2026 (ver §6 y §7):** modos re-verificados
  (`verify_modes.py`: 14 modos + Normal + Adivina + navegación, 0
  errores, 0 desbordamiento; Rompehielos 4×4, Fondo 4×9, Solo 4×5);
  medidas nuevas (`VERIFICACION/v2.4/correcciones/measure.py`,
  360x800 y 390x844): inicio 800/844 px, dibujo Normal 800/844 px
  con ¡HECHO! y paleta visibles, Cadáver 854 px con todo visible por
  la barra fija, cuenta atrás 800/844 px, Adivina en vivo 800 px;
  capturas nuevas en `VERIFICACION/v2.4/correcciones/` (dibujo,
  cuenta atrás con el rombo, pestaña PREESTABLECIDOS, inicio con el
  perfil plegado, álbum agrupado de Rompehielos, reproductor de
  Animación), revisadas a ojo.
- **Correcciones B1/B2 del 23 nov 2026 (ver §7):** «Deshacer» sin
  recorte en las 13 pantallas de dibujo a 360 px (65v65, antes
  68v65); pantalla de dibujo docH=800 a 360 px también en Cadáver e
  Imitación-preview (antes 896/966), con la vista previa encima del
  lienzo y la tira de Cadáver a 48 px; divisor «— FIN DEL ÁLBUM DE
  ANA —» al final de cada álbum; fin de ronda con acorde mayor
  523+659+784 Hz; verificación en 7 tamaños (320x568, 360x640,
  360x740, 360x800, 384x854, 412x915, 430x932): 0 errores y 0
  desbordamiento en todos; 390x844 re-verificado con 36 pantallas
  (0 errores, 0 desbordamiento, 0 recortes).
- `npx cap sync android` OK (2 plugins: @capacitor/app 8.1.2,
  capacitor-lan-server 1.0.0); `www/index.html` y
  `android/app/src/main/assets/public/index.html` idénticos (md5
  `ce56ed40258adf8df149b18ee04270a7` tras las correcciones B1/B2 del
  23 nov);
  permiso VIBRATE intacto
  (AndroidManifest línea 43); firma fija intacta (keystore
  `keystore/gartic-movil-debug.keystore`, SHA-256
  `9C:2E:01:1B:A4:27:BF:8F:76:B1:DD:85:01:AC:B8:5D:40:48:A5:CE:20:29:FF:03:21:30:DD:23:53:92:F5:CB`).
  Versión 1.4.0 (versionCode 6) en `package.json`,
  `android/app/build.gradle` y `scripts/fix-debug-signing.js`.
  **Sin compilar ni subir nada a GitHub** (regla de Roi: la v2.4 se
  compila solo cuando esté terminada y verificada, con los modos y el
  ícono elegidos incluidos).

### Verificación v2.3 (Chromium headless, 360x800)
Capturas en `VERIFICACION/v2.3/` (18 PNG a 360x800, con
`chromium_headless_shell`; el Chrome completo impone un mínimo de
500 px de ancho y sus capturas salen recortadas, no usarlo): `splash`,
`home`, `modes`, `setup`, `settings`, `how`, `join`, `create`,
`countdown`, `pass`, `write`, `describe`, `draw`, `draw-tools`,
`album`, `guess-draw`, `guess-live`, `podium`, más las tres variantes
de ícono (`icon-A/B/C.png` a 1024 px) con su simulación de recorte
MIUI a 96 y 192 px. Referencias del original en
`VERIFICACION/v2.3-referencias/` (ver §7).
- `#auto=normal` (4 jugadores): 0 errores de consola, 0
  desbordamiento, 4 álbumes con 4 eslabones cada uno, `fxOk:true`,
  `validPermutation:true`, `randomOrder:true`. Órdenes de ejemplo:
  «Ana>Dan>Carla>Beto | Beto>Ana>Dan>Carla | Carla>Beto>Ana>Dan |
  Dan>Carla>Beto>Ana».
- `#auto=guess` (4 jugadores): 0 errores, 0 desbordamiento, podio
  correcto (Carla:38, Dan:34, Beto:30, Ana:10), `drawerBonusCheck:34`,
  `fxOk:true`.
- `#test=nav` (navegación atrás): 0 errores, 0 desbordamiento. Registro
  completo: inicio → modos → atrás → modos → atrás → inicio; en
  partida, atrás abre el diálogo; salir → inicio; en inicio, atrás
  muestra el aviso «Pulsa de nuevo para salir».
- Pantallas de dibujo: ✔ ¡HECHO! visible sin desplazar (y=597 en
  Normal, y=570 en Adivina) tras corregir el bloque CSS roto (ver §4);
  panel de grosor/opacidad abre y cierra bien (`draw-tools`).
- Revisión visual de las 18 capturas: nada cortado, botones
  coherentes, ventanas limpias, marca de agua visible en el lienzo,
  Baloo 2 cargando, cabecera escondida en juego/sala, «¡HECHO!» en los
  botones, título de álbum en verde con la tira de jugadores, huecos
  VACÍO y fila INVITAR+EMPEZAR en la sala. Dos notas de la revisión:
  la fila de avatares de la sala se desplaza horizontalmente (lleva
  barra de desplazamiento en el escritorio; en Android es deslizable)
  y la captura del podio salió apagada la primera vez por un artefacto
  del headless (la animación `fadeIn` de 0,18 s no avanza con
  `--virtual-time-budget`); con `--run-all-compositor-stages-before-draw`
  sale bien. En el teléfono real la animación dura 0,18 s y termina
  normal.
- `npx cap sync android` OK (2 plugins: @capacitor/app 8.1.2,
  capacitor-lan-server 1.0.0); `www/index.html` y
  `android/app/src/main/assets/public/index.html` idénticos (md5
  `8020eeaf03ee003e376fffb57f0cad3d`); fuente Baloo 2 sincronizada;
  permiso VIBRATE intacto (AndroidManifest línea 43); firma fija
  intacta (keystore `keystore/gartic-movil-debug.keystore`, SHA-256
  `9C:2E:01:1B:A4:27:BF:8F:76:B1:DD:85:01:AC:B8:5D:40:48:A5:CE:20:29:FF:03:21:30:DD:23:53:92:F5:CB`,
  verificado con keytool).
- **Peso:** la parte web (`www/`) sigue siendo pequeña (un solo
  `index.html` + fuente Baloo 2 de 33 KB + logo SanBer); la APK final
  queda muy por debajo del límite de 50 MB.

### Qué NO se pudo probar sin el teléfono real de Roi
- Los sonidos a oído (las frecuencias nuevas son medidas reales, pero
  el timbre final solo lo juzga Roi), la vibración real, el dibujo
  táctil con el dedo y la fluidez real al dibujar.
- El wifi local con dos teléfonos reales: el flujo completo SÍ está
  probado con dos instancias simuladas (ver §5 y §8 de la v2.4: 22
  escenarios, todos OK), pero el hotspot de verdad entre dos Redmi,
  la IP que anuncia el anfitrión (192.168.43.x) y el plugin LanServer
  real solo se prueban en los teléfonos.
- La instalación de la v2.4 en su Redmi (el problema de la v2.1 se
  resolvió solo; ver abajo) y el ícono en el launcher (Roi eligió la
  D5 como ícono final; la instalación quedó a medias, pendiente de
  verificar todos los tamaños y el `cap sync`).
- Baloo 2 en la WebView de Android (en el headless se ve bien; en el
  teléfono debería verse igual, es una fuente empaquetada).
- El portapapeles del botón INVITAR dentro de la APK (en el navegador
  funciona; en la WebView de Android también debería, con el
  fallback a `execCommand` si hace falta).

### Problema de instalación RESUELTO SOLO (21–23 nov 2026)
La v2.1 NO se instalaba en el Redmi de Roi («no se instaló la
aplicación»), ni desinstalando la v2 antes; lo mismo pasaba con
«¡A la frente!» v1.0.1. Los archivos estaban verificados buenos aquí
(ZIP íntegro, firma correcta, minSdk 24, compatible con Android 12).
El 23 nov 01:52–01:54 Roi avisó: «Nada, me instaló solo al final» —
la v2.1 terminó instalándose sola en su Redmi, sin causa concreta
identificada (ni espacio, ni reinicio, ni Chrome: simplemente al
final instaló). Roi considera el problema de instalación solucionado.
Queda como antecedente por si vuelve a pasar con otra versión; el
motivo exacto queda pendiente de que Roi lo confirme. La v2 SÍ está
instalada y corriendo en su Redmi (captura 21 nov 13:53: dibujo
«Lobo», Ronda 2 de 3). El problema de instalación de «¡A la frente!»
(v1.0.1) es otro tema y sigue sin probarse con la v1.0.3/v1.0.4.

### 1. Barra de dibujo compacta, como la foto oficial
- Ya NO hay columna izquierda fija de grosor/opacidad ocupando el lienzo.
  La barra inferior es compacta como en la foto de Gartic Phone: botón
  lápiz ✏️, botón ↕ de grosor/opacidad, color actual (cuadro alto),
  paleta en 2 filas y botón ✔ ¡Listo! violeta.
- Los círculos de grosor y el deslizador de OPACIDAD salen SOLO al tocar
  el botón ↕, como un panel pequeño flotante sobre el lienzo; se esconden
  al tocar ↕ de nuevo o al empezar a dibujar.
- El lienzo ahora es más alto (640x440 en vez de 640x400) y ocupa todo el
  ancho: a 360 px gana ~30% de ancho visible respecto a la v2.1. Vale para
  Normal y para Adivina. A 360 px la fila superior de colores se esconde
  (los colores ya están en la barra inferior) y la barra inferior se parte
  en dos filas (herramientas arriba, paleta abajo) para que el botón
  ✔ ¡Listo! siga visible sin desplazar.

### 2. Sonidos sintetizados (Web Audio, offline, sin archivos)
- Cuenta atrás 3-2-1 (pop suave que baja + nota brillante al llegar a 0),
  tic-tac en los últimos 10 segundos de cada turno, sonido al cambiar de
  turno (pop corto) y al cambiar de ronda / llegar al podio (campanita de
  3 notas), y sonido de acierto en Adivina (dos notas ascendentes).
- Solo ondas seno con caída exponencial: suenan a campana/pop redondo,
  nunca a pitido cuadrado de 8 bits. El AudioContext se crea al primer
  toque (los navegadores no dejan sonar nada antes de interactuar).
- Interruptor de sonido en Ajustes (activado por defecto), guardado en el
  teléfono.
- **Honestidad sobre la referencia:** en esta máquina no hay audio para
  escuchar los sonidos del Gartic Phone original: la página
  myinstantplay.com/sounds/gaming/gartic-phone lista 1 sonido pero no lo
  describe por escrito, y las búsquedas de gameplay no dan una descripción
  escrita del timbre (solo se sabe que hay un sonido de alarma de 6,1 s
  para el fin de tiempo y que el carácter general es de juego de fiesta,
  con efectos de dibujos animados). Así que estos tonos son una
  aproximación afinada a ese carácter (pops suaves, tic ligero,
  campanitas), NO una copia verificada a oído. **Roi los juzga a oído en
  su Redmi: si alguno no suena como Gartic, que diga cuál y se re-afina
  o se quita.**
- Frecuencias: cuenta atrás 660 Hz con caída a 480 Hz (0,12 s), "¡ya!"
  880 → 1318 Hz; tic 1250 Hz (0,045 s, bajo); cambio de turno 740 → 560
  Hz; ronda 523 → 659 → 784 Hz; acierto 659 → 880 → 1318 Hz.
  **Estas frecuencias quedaron sustituidas en la v2.3 por valores
  medidos del original (ver §8 de la v2.3): cuenta atrás 784/880/1174
  Hz, «¡ya!» 1314 + 1550 Hz, cambio de turno 784→880→1174 Hz; el tic
  (1250 Hz) y el acierto (659→880→1318 Hz) siguen como en la v2.2
  porque no se pudieron medir.**

### 3. Vibración
- `navigator.vibrate` en los mismos momentos que los sonidos: cuenta
  atrás (25 ms por número, 70 ms al llegar a 0), aviso de 10 s
  (60-60-60 ms), cambio de turno (40 ms), cambio de ronda (80-60-140 ms)
  y acierto (50-50-90 ms).
- Permiso `android.permission.VIBRATE` añadido al manifiesto y a
  `scripts/fix-manifest.js` (paso 3), para que sobreviva a `cap sync`.
  Es un permiso normal: no hay que pedirlo en tiempo de ejecución.
- Interruptor de vibración en Ajustes (activado por defecto), guardado
  en el teléfono.
- **Sin probar en teléfono real:** en la WebView de Android la vibración
  de la web suele funcionar, pero si en el Redmi no vibra, haría falta
  llamar al vibrador desde el plugin nativo (Capacitor Haptics) en vez
  de `navigator.vibrate`; Roi lo confirma probando.

### 4. Pantalla de apertura con el logo de SanBer
- Al abrir la app sale primero el logo real de SanBer de Roi (su foto
  recuperada de YouTube, aprobada por él en ¡A la frente!), copiado tal
  cual a `www/assets/sanber-logo.png` (SHA-256
  `f8767697749916f036f507c422519558588942ac92a3201aa976fc37298dd0c2`,
  idéntico al original). No se redibujó ni se cambió nada: solo dice
  "SanBer", nunca Santana ni Roiber.
- Fondo degradado violeta-magenta de la app, logo centrado y debajo
  "Gartic Móvil" en blanco. Dura 3 segundos y se salta tocando la
  pantalla. No sale el logo oficial de Gartic en la apertura.

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

**Fuentes (actualizado en v2.3):** la app pedía Baloo 2 y Nunito, pero
no las empaquetaba: offline usaba la fuente del sistema del teléfono.
Desde la v2.3, **Baloo 2 sí está empaquetada** (ver §9): la fuente
variable (pesos 700 y 800, subconjunto latino, 33 KB) está en
`www/fonts/baloo2-latin.woff2` y se sincroniza a Android con
`cap sync`. Nunito sigue sin empaquetarse (solo es fallback en la
pila `system-ui, sans-serif` del CSS).

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
