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
- **Versión:** 1.3.0 (versionCode 5, versionName 1.3.0)

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
  * **Repique antes del cambio de turno («¡ya!» / cuenta atrás):**
    dos tonos sostenidos **1314 Hz (Mi6) + ~1550 Hz** juntos, ~1,5 s,
    que empiezan de golpe. Medidos en `JzQOa0IW6IQ` a 795,58 s (justo
    antes del arpegio de 797,1 s) y a 947,3 s. El tono de 1314 Hz
    aparece además 150+ veces en el audio, así que también es una nota
    de la música de fondo (Mi6): por sí solo NO es fiable como sonido
    del juego, pero aparece justo antes del arpegio en los cambios de
    turno (795,7–797,7; 979,1–982,0; 1508,1–1510,5) y ~30 s antes de
    que acaben los turnos de dibujo — confianza media. Antes (v2.2):
    880→1318 Hz. Ahora: **1314 + 1550 Hz juntos, 0,4 s**.
  * **Cuenta atrás 3-2-1:** no se pudo aislar una cuenta atrás 3-2-1
    con números separados en los vídeos (Vegetta habla encima y la
    música no deja huecos: no hay silencios ≥2,5 s entre 13:00 y
    28:20 del vídeo de 2 h). Se usan las mismas notas medidas del
    arpegio: **3→784 Hz, 2→880 Hz, 1→1174 Hz** (0,2 s cada una),
    porque en el original la cuenta atrás y el inicio de turno usan
    el mismo carácter. Antes (v2.2): 660→480 Hz.
  * **Fin de tiempo:** medido en `JzQOa0IW6IQ` a 944,5–947,5 s: el
    espectro salta al azar (voz de Vegetta), silencio 946,9–947,2 s y
    luego repique 1305 Hz a 947,3 s + arpegio 783/880/1174 a 947,4–
    947,6 s. **No hay un pitido distinto de «fin de tiempo»**: el
    turno termina y el siguiente empieza con repique + arpegio. Por
    eso la app no añade un sonido nuevo de fin de tiempo: usa el
    repique + arpegio del cambio de turno.
  * **Últimos 10 segundos / tic-tac:** NO se pudo medir. En 937–947 s
    no hay periodicidad de 1 s en las frecuencias altas; manda la voz
    (rms hasta 0,3) y hay 2,4 s de silencio a 942,3–944,7 s. Se deja
    el tic de la v2.2 (**1250 Hz, 0,045 s, bajo**) y se dice claro:
    es una aproximación, no una medida.
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
  reporta `fxOk:true`.
- Dificultad honesta de la medición: el audio lleva música de fondo
  continua (bucle lofi en Sol mayor: Sol4 392 Hz, Re5 587 Hz, Sol5
  784 Hz…) y Vegetta hablando sin parar; los dos primeros detectores
  automáticos fallaron (0 eventos) y la medida salió de mirar los
  espectrogramas en los cambios de turno (bloque rectangular de tonos
  apilados a 796–799 s) y de buscar la plantilla del arpegio en todo
  el audio. El juicio final a oído sigue siendo de Roi en su Redmi.

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

## ✅ www completo y verificado (v2.3)

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
- El wifi local con dos teléfonos reales (igual que en v2.2).
- La instalación de la v2.3 en su Redmi (la v2.1 no instalaba; ver el
  problema pendiente abajo) y el ícono A en el launcher (Roi elige
  entre A, B y C).
- Baloo 2 en la WebView de Android (en el headless se ve bien; en el
  teléfono debería verse igual, es una fuente empaquetada).
- El portapapeles del botón INVITAR dentro de la APK (en el navegador
  funciona; en la WebView de Android también debería, con el
  fallback a `execCommand` si hace falta).

### Problema de instalación SIN RESOLVER (21 nov 2026, sigue igual)
La v2.1 NO se instala en el Redmi de Roi («no se instaló la
aplicación»), ni desinstalando la v2 antes; lo mismo pasa con
«¡A la frente!» v1.0.1. Los archivos están verificados buenos aquí
(ZIP íntegro, firma correcta, minSdk 24, compatible con Android 12);
apunta a cosa del teléfono, no del archivo. Pendiente en su teléfono:
reiniciar, revisar espacio libre, probar instalar desde Chrome y
probar si la v2 vuelve a instalar. La v2 SÍ está instalada y corriendo
en su Redmi (captura 21 nov 13:53: dibujo «Lobo», Ronda 2 de 3).

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
