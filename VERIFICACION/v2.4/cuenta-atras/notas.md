# Notas de la verificación de la cuenta atrás 3-2-1 (23 nov 2026)

Método: yt-dlp (360p/240p + audio), fotogramas con ffmpeg, audio con STFT
(mismo método que `VERIFICACION/v2.3-referencias/sonidos/analisis4.py`).
Todos los tiempos son del vídeo, en segundos o min:seg.

## 1. Vegetta777 — `JzQOa0IW6IQ` «Mi primera vez en GARTIC PHONE» (2:01:10)

### Partida 1, Normal — 10:57,6–11:00,6 (657,6–660,6 s) ✅ CUENTA ATRÁS

Fotogramas a 5 fps (656,4–661,6 s;
`fotogramas/vegetta-JzQOa0IW6IQ-partida1-5fps-656-662s.png`):

- 656,4–657,4 s: sala (JUGADORES 6/6, ESTILO DE JUEGO, NORMAL).
- **«3» ≈ 657,6–658,1 s** (rombo violeta, contorno rosa, número verde menta).
- **«2» ≈ 658,2–659,1 s** (contorno verde/amarillo).
- Transición (rombo vacío) ≈ 659,2 s.
- **«1» ≈ 659,4–660,5 s** (anillo amarillo).
- **Pantalla de escribir desde ≈ 660,6 s** («1/6», «EMPIECE A ESCRIBIR UNA
  HISTORIA», «Iron man japonés berreando»).

Audio (segmento 655–662 s, `seg-veg1-655-662.wav`, espectrograma en
`fotogramas/espectrograma-vegetta-655-662s.png`):

- Tic «3» a 657,6 s: pico **1244 Hz** (magnitud 25,7; 2.º pico 738 Hz, voz).
- Tic «2» a 658,6 s: en la ventana de 0,25 s manda la voz (692 Hz), pero la
  envolvente de la banda 1100–1400 Hz tiene un pico claro a 658,6 s
  (0,0849) y el espectrograma muestra la línea de ~1250 Hz.
- Tic «1» a 659,6 s: pico **1244 Hz** (magnitud 25,8).
- Envolvente 1100–1400 Hz (máx. por 0,1 s): 657,6: 0,0727; 658,6: 0,0849;
  659,6: 0,0731; huecos entre tics ≈ 0,0000–0,0016. Tres tics a ~1 s.
- Arpegio al terminar: a 660,6–660,9 s la banda 1100–1400 Hz vuelve a
  subir (0,0743 / 0,0812 / 0,0733) por la nota de 1174 Hz; el arpegio
  784→880→1174 Hz ya estaba medido a 660,3 s en la v2.3.
- Cada tic dura ~0,2–0,3 s con caída exponencial (envolvente: 0,073 →
  0,045 → 0,038 → 0,017 → 0,005 en 657,6–658,0 s).

Por qué se pasó por alto en la v2.4: el pase miró fotogramas a las 10:55
(655 s, sala), 11:00 (660 s, «1» / fundido a escribir) y 11:05 (665 s,
escribiendo). La cuenta atrás entera (657,6–660,6 s) cae entre el primer
y el segundo fotograma.

### Partida 2, Normal — ~27:40–27:45 (1650–1675 s) ✅ CUENTA ATRÁS

Fotogramas a 1 fps: álbum de Fargan → sala (JUGADORES 7/7) → rombo vacío
→ **«1»** (dos fotogramas) → «1/7», «EMPIECE A ESCRIBIR UNA HISTORIA»
(«Estrella-de-mar silbando en el club noctur»). El «3» y el «2» caen
entre fotogramas a 1 fps.

### Cambio de turno — 13:11–13:20 (791–800 s) ❌ SIN CUENTA ATRÁS

Fotogramas a 2 fps: escribir 1/7 («Kira jugando con Vegetta», temporizador
0:47) → fundido directo → dibujar 2/7 («HEY, ¡ES HORA DE DIBUJAR!
HAMBURGUESA SE COME A KIRA»). Ningún rombo, ningún número.

### Tic de los últimos 10 s — 786–798 s ❌ NO EXISTE (tic por segundo)

Banda 1100–1400 Hz, rms por 0,5 s: 786,0: 0,0028; 786,5: 0,0170; 787,0:
0,0016; 787,5: 0,0000; 788,0: 0,0000; 788,5: 0,0071; 789,0: 0,0000; 789,5:
0,0052; 790,0: 0,0119; 790,5: 0,0046; 791,0: 0,0106; 791,5: 0,0049; 792,0:
0,0015; 792,5: 0,0013; 793,0: 0,0004; 793,5: 0,0034; 794,0: 0,0000; 794,5:
0,0000; 795,0: 0,0002; 795,5: 0,0096; 796,0: 0,0143; 796,5: 0,0189; 797,0:
0,0283; 797,5: 0,0162. Sin periodicidad a 1 s.

**Corrección (23 nov 2026):** la subida de 795,5–797,0 s que aquí se
atribuyó al arpegio **es en realidad la alarma de poco tiempo** (tonos
1314+1550 Hz; el arpegio empieza a ~797,3 s). Y el «temporizador 0:47»
de la línea de arriba era un error de lectura: es el contador de
¡HECHO! (5/7), no el temporizador. El temporizador es un dial circular
arriba a la derecha. Ver la sección 9: **el aviso de poco tiempo SÍ
existe** — dial que se pone amarillo a ~1/6 del tiempo + alarma de dos
tonos 1314+1550 Hz sostenidos hasta el fin del turno. Lo que NO existe
es un tic por segundo.

## 2. Juan Guarnizo — `UFOXXi8zsjQ` «JUGANDO GARTIC PHONE CON STREAMERS» (35:49)

### Partida 1, Normal — ~0:09–0:13 ✅ CUENTA ATRÁS

Fotogramas a 2 fps (0–20 s): sala (PREESTABLECIDOS, NORMAL, JUGADORES
10/10, EMPEZAR) → «3» tenue (~9,5 s) → «3» (~10 s) → «2» (~10,5–11 s)
→ «1» (~11,5–12,5 s) → «ESCRIBE UNA FRASE» («Ardilla charlando en el
hospital», ~13 s). Los subtítulos empiezan: «listo, ya estamos todos,
están listos para iniciar» (0:00).

### Partida 2, Knock-Off — 18:12–18:15 (1092–1095 s) ✅ CUENTA ATRÁS

Fotogramas a 2 fps (1090–1097 s): sala con **IMITACIÓN seleccionada** →
«3» (1092,0 y 1092,5 s) → «2» (1093,0 s) → rombo vacío (1093,5 s) →
«1» (1094,0 y 1094,5 s) → «HEY, ¡ES HORA DE DIBUJAR!» (1095 s). El
primer turno de Knock-Off es dibujar; la cuenta atrás aparece igual.
El triple de tics 1092/1093/1094 s ya salía en el detector de audio.

## 3. AuronPlay — `CHIE0B89olM` «DIBUJANDO EN GARTIC PHONE #2» (28:18)

### Partida 1, Normal — 0:11–0:15 (11,8–15 s) ✅ CUENTA ATRÁS

Fotogramas a 2 fps (10–16 s): sala (JUGADORES 6/6, NORMAL) → «3»
(12,0 s) → «2» (13,0 s) → rombo vacío (13,5 s) → «1» (14,0 y 14,5 s)
→ «EMPIECE A ESCRIBIR UNA HISTORIA» («Conejo loco tosiendo», 15,0 s).
Triple de tics en audio: 11,8 / 12,8 / 13,8 s.

### Segundo triple de tics (357,0 / 358,1 / 359,0 s) — FALSO POSITIVO

Fotogramas a 2 fps (355–362 s): es el **álbum** de Polispol («LA LA
LAND», «BATMAN CANTANDO»), no un inicio de partida. Los tics de ~1245 Hz
también suenan durante los álbumes. Lección: el triple de tics por sí
solo no basta; hay que ver los fotogramas.

## 4. Juan Guarnizo — `ibKrDZU1S7g` «IMITANDO DIBUJOS» (13:03), Knock-Off

Inicio de partida buscado con escaneo (1 fotograma/30 s) + ventanas a
2 fps (355–395 s) y 5 fps (380,5–385,5 s):

- 375–382,3 s: sala (JUGADORES 9/9, PREESTABLECIDOS, IMITACIÓN).
- **382,5 s: corte duro a «HEY, ¡ES HORA DE DIBUJAR!»** (el lienzo ya
  tiene una «C» dibujada a 383,5 s). Ningún rombo en los fotogramas a
  5 fps.
- Audio 376–386 s: banda 1245 Hz sin patrón de 3 tics (0,003–0,028,
  irregular); la energía total cae de ~0,09 a ~0,025 justo a 382,4–
  382,5 s. Es un **corte de edición** (el vídeo lleva memes intercalados
  y cortes bruscos): el editor recortó los ~3 s de la cuenta atrás.
  ⚠️ No concluyente, no es evidencia en contra.

## 5. Juan Guarnizo — `Rb6E3Eqppi4` «GARTIC PHONE NAVIDEÑO» (13:18)

Escaneo (1 fotograma/30 s): el fotograma 1 (0 s) es una sala (JUGADORES
6/6); el fotograma 2 (30 s) ya es un dibujo (Grinch). Ventana 0–30 s a
2 fps: sala hasta ~13 s, luego la **webcam a pantalla completa** (~13–
23 s) y el lienzo de dibujo desde ~23,5 s. La transición cae dentro del
plano de la webcam: ⚠️ no concluyente. Los «2 candidatos débiles de
cuenta atrás» (66,3 s y 632,5 s) del análisis anterior eran voz/música.
El vídeo tiene también una partida de Animación (~3:00, «CREAR EL PRIMER
DIBUJO DE LA ANIMACIÓN»), que empieza fuera de cámara.

## 6. Vídeos sin inicio de partida visible

- Vegetta777 `e0lMb9Vqbko` «RUBIUS HACIENDO EL PUENTE EN LA ARENA»
  (12:12): empieza a mitad de partida (2/7, «GATO EN LLAMAS
  CORRIENDO»); turnos 2/7→7/7 y álbumes; al final (~12:00) se forma
  una sala nueva, fuera del vídeo. Sin arpegios de inicio en audio
  (1 arpegio a 611,4 s = cambio de turno).
- Juan Guarnizo `UQBcCDUh59Q` «GARTIC PHONE BILINGÜE» (17:26):
  recopilación de álbumes («ÁLBUM DE ELJUANIQUILADOR», «ÁLBUM DE
  SYLVEE»…); un turno de dibujo al principio («FOOLISH GAMERS FUMANDO
  WEED») y luego solo álbumes. Sin inicio visible.
- Vegetta777 `avQw9MnhpIo` (16:25), Animación: empieza a mitad de
  partida (1/7, «CREAR EL PRIMER DIBUJO DE LA ANIMACIÓN»); pasos de
  animación 1/7→7/7 y álbumes. Sin inicio visible. 0 arpegios y 0
  triples de tic en su audio.

## 7. Página oficial y wiki (23 nov 2026)

- `garticphone.com`: 6 pasos, sin mención de cuenta atrás.
- `gartic-phone.fandom.com/wiki/Game_modes`: 15 modos, sin mención de
  cuenta atrás.
- Búsqueda web «gartic phone countdown 3 2 1»: sin resultados sobre el
  juego.

## 8. No verificados (descargas fallidas)

- Vegetta777 `dyp3r1ga7ug` (3:09:25): el inicio de partida está a
  ~12:55–13:10 («vale empezamos» 12:58, subtítulos), pero la descarga
  por secciones falló (formato no disponible).
- AuronPlay `KLPUA98-DuQ` (48:28): HTTP 403 y formato no disponible.
- AuronPlay `difTQMnfFVc` (2:24:56) y `-gAQqh88nOg` (1:38:48): secciones
  fallidas (formato no disponible). Subtítulos: «¿qué os parece si
  empezamos por un clásico?» 04:43 (difTQMnfFVc); «Le doy a empezar»
  02:57 (-gAQqh88nOg).
- AuronPlay `6ZcCFh7S6hc` (32:53): descarga parcial (solo vídeo, 14 MB).
- AuronPlay `o8ecd0zh-YY` (34:34): no descargado.
- Juan Guarnizo `NUtgp2G2MsU` «GARTIC PHONE CON LOS DEL QSMP» (3:34:00):
  subtítulos con HTTP 429; vídeo no descargado.

## 9. Aviso de poco tiempo — el dial se pone AMARILLO + alarma 1314+1550 Hz (23 nov 2026)

Roi recordaba que «el teléfono sonaba cuando quedaba poco tiempo». La
verificación anterior buscó un tic por segundo y no lo encontró; la
búsqueda estaba mal enfocada. Roi añadió la pista clave (22 nov
22:51): en los vídeos, cuando los streamers se olvidaban del tiempo,
«el teléfono sonaba y les avisaba; el reloj sale como un cronómetro en
la parte de arriba y cuando se ponía en rojo sonaba una vez».

### 9.1 El dial (Vegetta `JzQOa0IW6IQ`, partida 2, Normal)

El temporizador es un **dial circular arriba a la derecha** (una cuña
que se vacía), no un contador numérico. Arriba a la izquierda está el
paso (p. ej. «1/7») y debajo una píldora con ✓ y el contador de
jugadores que pulsaron ¡HECHO! (p. ej. «5/7»). La escala completa del
dial es ~0,76 del interior del círculo (la cuña nunca llena el círculo
entero: empieza en ~0,76).

La cuña es **blanca** casi todo el turno y se vuelve **AMARILLA**
cuando se encoge hasta ~0,17–0,18 del interior del dial (~22 % del
tiempo restante, si el dial se vacía lineal desde 0,76). **No se
observó rojo** en estos vídeos (2021): la cuña sigue amarilla hasta
el final del turno. Roi lo recuerda como rojo; en una pantalla pequeña
el amarillo puede verse rojizo, o en versiones más nuevas puede ser
rojo — queda por comprobar en un vídeo reciente con el dial bien
visible.

Medida por color (fotogramas a 0,5 s, ratio cuña/interior del círculo;
el medidor solo contaba píxeles blancos, así que la lectura «0,00» en
un turno amarillo es un artefacto: la cuña amarilla no se contaba):

- **Escribir 1/7** (turno de ~50 s): blanca 0,17 a 795,0 s → amarilla
  0,15 a 795,5 s (cambio ~795,0–795,5 s). El turno termina a 797,5 s
  (todos pulsaron ¡HECHO! antes de tiempo; el dial no llegó a cero).
  El aviso llega a ~2 s del final.
- **Dibujar 2/7** (turno de ~150 s): blanca 0,17 a 916,5 s → amarilla
  0,15 a 917,0 s (cambio ~916,5–917,0 s). El turno termina a 947,0 s
  por tiempo agotado (cuña ~0). El aviso llega a ~30 s del final.
- **Describir 3/7** (turno de ~40 s): blanca 0,18 a 978,5 s → amarilla
  0,14 a 979,0 s (cambio ~978,5–979,0 s). El turno termina a 982,5 s
  (todos pulsaron ¡HECHO!). El aviso llega a ~3,5 s del final.

Conclusión: el aviso NO es a N segundos fijos, sino a una fracción del
temporizador (~1/6 del dial ≈ 22 % del tiempo del turno). Por eso en
un turno corto suena a 2 s del final y en uno largo a 30 s.

Evidencia visual: `fotogramas/dial-blanco-a-amarillo-tira.png` (tira
de fotogramas 786–798 s), `dial-amarillo-796s.png` (amarillo, 796 s),
`dial-blanco-915s.png` (blanco, 915 s), `dial-amarillo-945s.png`
(amarillo, 945 s).

### 9.2 La alarma: dos tonos sostenidos ~1314 + ~1550 Hz

En cada cambio a amarillo arranca un sonido de **dos tonos sostenidos,
~1314 Hz y ~1550 Hz**, que sigue hasta el fin del turno. En el
espectrograma se ven dos líneas horizontales continuas (1314 y 1550 Hz)
desde el cambio hasta el final del turno — no es un pitido único ni un
tic por segundo.

Medida fina (FFT de 0,5 s con interpolación parabólica):
- Cambio 1 (796,0–796,5 s): **1308,4 Hz + 1548,0 Hz**.
- Cambio 2 (917,6–918,1 s): **1317,4 Hz + 1551,2 Hz**.
- Cambio 3 (980,0–980,5 s): **1313,0 Hz + 1546,0 Hz**.

Inicio y duración (envolvente de la banda 1250–1600 Hz):
- Cambio 1: energía desde 795,7 s (0,2 s después del cambio visual)
  hasta ~797,3 s (fin del turno).
- Cambio 2: energía desde 917,5 s hasta al menos 922 s (el turno
  acaba a 947 s; el sonido sigue).
- Cambio 3: energía desde 979,3 s hasta ~982,3 s (fin del turno).

**Este sonido es el que en la v2.3 se midió como «¡ya!» (1314+1550 Hz
a 795,58 s) y se descartó como «nota de la música de fondo». No es
música de fondo: aparece solo en los cambios a amarillo.** Distribución
de eventos tonales 1250–1600 Hz en la partida 2 de Vegetta (756–1000 s):
16 eventos en total, agrupados en 796–806 s (5), 916–926 s (2) y
976–986 s (4); en el lobby (720–756 s, sin temporizador) solo 1 evento
suelto. La música de fondo no se sincroniza con el estado del juego
tres veces seguidas.

Evidencia: `fotogramas/espectrograma-alarma-3-cambios.png` (los 3
cambios), `fotogramas/espectrograma-785-798-sin-aviso-10s.png`
(silencio en 792–795,5 s y alarma desde 795,5 s).

### 9.3 No hay tic por segundo (recomprobación)

- Autocorrelación del envolvente RMS a lag 1,0 s en los últimos 10 s y
  5 s de **14 fines de turno** de Vegetta: media +0,06 y −0,02, igual
  que los controles (+0,06 y +0,05). Sin periodicidad a 1 s.
- Tampoco hay rachas de transitorios de banda ancha (flujo espectral y
  HF 4–8 kHz) ni eventos tonales agrupados por offset en los últimos
  15 s antes de los fines de turno.
- El 1314/1550 Hz NO sube sistemáticamente en los últimos 3 s antes de
  los fines de turno, salvo en los cambios a amarillo.
- En Guarnizo `UFOXXi8zsjQ` (Knock-Off, fin de turno con arpegio a
  1759,8 s): autocorrelación −0,23/−0,11, sin tic.

### 9.4 Otras comprobaciones

- **Knock-Off (Guarnizo `UFOXXi8zsjQ`, 2022): sin confirmar.** En el
  audio hay eventos 1324/1384 Hz a 1756,9/1757,3 s, ~2,5–3 s antes del
  arpegio de 1759,8 s, compatibles con la alarma, pero ese arpegio es
  probablemente el inicio de una partida nueva (a 1750 s se ve el
  álbum «ÁLBUM DE ALDO_GEO»; a 1800–1820 s siguen los álbumes «ÁLBUM
  DE RIVERS» y «ÁLBUM DE CAROLA»), no un fin de turno, y no se pudo
  medir el dial en ese vídeo (webcam + anuncios encima). El detector
  de arpegios por envolventes de banda recupera 15/16 arpegios
  conocidos en Vegetta pero da 107 falsos positivos (la música de
  fondo contiene 784/880/1174 Hz); no sirve solo para encontrar fines
  de turno.
- **Animación (Vegetta `avQw9MnhpIo`, 2024): sin confirmar.** No se
  pudieron aislar fines de turno limpios: el vídeo tiene la webcam
  encima del temporizador y cambios de plano constantes; el detector de
  arpegios da 25 candidatos (la mayoría falsos positivos de la
  música) y el análisis por diferencia de fotogramas a 1 fps da
  cambios grandes en casi todos los segundos (dibujo en curso + zooms),
  así que no aísla los cambios de turno. Un fotograma a 200 s muestra
  el lienzo a pantalla completa con la webcam arriba a la derecha y
  sin temporizador visible (puede estar tapado).
- **Guarnizo 2026 `ibKrDZU1S7g` (Knock-Off): dial no seguible.** El
  vídeo lleva memes intercalados, cortes bruscos y cambios de encuadre;
  el dial no está en posición fija. Un fotograma a 400 s muestra el
  mismo dial circular con la cuña blanca ~85 % llena
  (`fotogramas/dial-guarnizo-2026-400s.png`).
- **Color rojo: sin confirmar.** En los fotogramas de 2021 la cuña es
  amarilla, nunca roja. Queda pendiente ver si en vídeos recientes
  (2024–2026) el dial llega a ponerse rojo o si el «rojo» que recuerda
  Roi es el amarillo visto en pantalla pequeña.
- **Wiki y página oficial:** la wiki de fans y `garticphone.com` no
  mencionan ningún sonido de temporizador ni aviso de tiempo. La
  búsqueda web («gartic phone timer sound ticking last seconds hurry
  up») no dio ningún resultado útil sobre el juego.

### 9.5 Correcciones a conclusiones anteriores

1. El sonido «¡ya!» 1314+1550 Hz de la v2.3 (795,58 s) **es la alarma
   de poco tiempo**, no música de fondo ni el final de la cuenta atrás.
2. El fin de turno de escribir 1/7 a 797,0 s, que se creía por tiempo
   agotado, **terminó antes de tiempo** (todos pulsaron ¡HECHO!): el
   dial no llegó a cero; la lectura «dial=0,00» era un artefacto
   (el medidor solo contaba píxeles blancos y la cuña ya era amarilla,
   0,12 amarilla a 797 s). El turno de dibujar 2/7 sí terminó por
   tiempo agotado a 947,0 s (cuña ~0).
3. Varios de los 16 «arpegios conocidos» de `analisis3.py`
   ([660.3, 754.9, 796.9, 947.0, 982.3, 1132.8, 1172.3, 1322.8, 1510.4,
   1670.4, 1702.7, 1853.2, 1892.7, 2042.9, 2082.8, 2233.0]) son en
   realidad inicios de partida (660.3 y 754.9 son tras la cuenta atrás)
   o fines anticipados, no fines por tiempo agotado.
4. El tic de los últimos 10 s **sigue sin existir** como tic por
   segundo, pero el temporizador **no** baja en silencio: a ~1/6 del
   dial se pone amarillo y arranca la alarma 1314+1550 Hz.

### 9.6 Qué cambia para la app (pendiente de aplicar en el código)

- **Sustituir el tic de 10 s** (1250 Hz, una vez por segundo) por la
  alarma del original: cuando el temporizador llegue a ~1/6 del tiempo
  restante, el dial (o el temporizador) se pone **amarillo** y suenan
  los tonos **1314 Hz + 1550 Hz sostenidos** hasta el fin del turno.
- **Cambiar el sonido de la cuenta atrás** (ya documentado antes): tic
  ~1245 Hz por número + arpegio 784→880→1174 Hz al terminar; sin
  «¡ya!».
- La frecuencia de 1250 Hz del tic actual de la app coincide con el tic
  de la **cuenta atrás** (~1244 Hz), no con ningún aviso de poco
  tiempo.

Archivos de trabajo (scratch, `/tmp/aviso-tiempo/`): `veg-2h.webm`
(65 MB, vídeo completo de Vegetta 2 h, 360p), `guarnizo-2022.webm`
(27 MB), `guarnizo-knockoff-2026.webm` (11 MB), `veg-anim-2024.webm`
(8 MB); audios `audio-guarnizo-2026.wav`, `audio-veg-anim2024.wav`;
scripts `detect_arp.py`, `detect_arp2.py`, `aviso.py`, `offset_hist.py`,
`autocorr.py`, `dial.py`, `dial2.py`, `dial3.py`, `color_dial.py`,
`switch.py`; imágenes `spec-785-798.png`, `spec-chimes.png`,
`dial-tira.png`, `dial-crop-790.png`, `dial-crop-796.png`,
`dial-draw-915.png`, `dial-draw-945.png`, `sheet-786-798.png`,
`sheet-744-756.png`, `f715.png`, `f915.png`, `full-790.png`,
`full-700.png`, `g2022-*.png`, `g2026-dial-400.png`; envolventes
`bands_audio-2h.npz`, `bands_audio-guarnizo-streamers.npz`,
`bands_audio-veg-anim2024.npz`. Los vídeos/audios de trabajo (~500 MB
en total) se pueden borrar; la evidencia queda en
`VERIFICACION/v2.4/cuenta-atras/fotogramas/`.
