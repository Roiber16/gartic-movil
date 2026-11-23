# Correcciones de ChatGPT — Gartic Móvil v2.4 (1.4.0)

Fecha: 23 nov 2026. Documento base:
`VERIFICACION/v2.4/PARA-MUSE-Correcciones-Gartic-Movil.md` (ChatGPT analizó
el proyecto desde Drive). Se aplicaron los puntos 1–5. **El punto 6
(diagnóstico de instalación) NO se hizo**: Roi avisó el 23 nov 01:52–01:54
que la v2.1 «me instaló solo al final» — problema resuelto solo, sin causa
identificada; queda como antecedente por si vuelve a pasar. Constancia en
`LEEME_APK.md` («Problema de instalación RESUELTO SOLO»).

No se tocó el ícono (D5 a medio instalar), no se hizo commit, no se subió
nada a GitHub y no se lanzó ningún build.

Estado final de `www/index.html`: md5 `d8447c9d72e7b9321414266ea6f479b8`
(partida: `ce56ed40258adf8df149b18ee04270a7`). `npx cap sync android` OK:
el asset de Android tiene el mismo md5. **La app queda lista para
compilar** (pendiente solo la decisión de Roi sobre el ícono D5 y la
prueba en dos teléfonos reales).

## Qué se corrigió en cada punto

### 1. Turnos Wi-Fi (el sondeo ya no vuelve a montar la pantalla)
- Turno mostrado separado del enviado: clave `gameId|paso|jugador`
  (`S.net.taskKey`); `showWifiTask` solo con clave nueva. Con la misma
  clave solo se actualizan el reloj (tiempo restante calculado por el
  anfitrión, `hostSetStepClock` + `stepLimit`) y el estado de red.
- Sondeo serializado (cadena con `setTimeout`, no `setInterval`);
  respuestas tardías descartadas por `S.net.session`.
- `setTimer(sec, onExpire, total)` con duración total separada del
  tiempo restante (el cliente puede entrar a mitad de turno).
- Entrega idempotente con reintentos cada 2 s; si el anfitrión ya saltó
  el turno (`skipped:true`), el reintento se cancela con aviso.
- Al salir: `stopNetPoll` limpia `pollTimer`/`poll`/`replayTimer` y sube
  la sesión; `leaveGame`/`goHome` suben `submitToken`. Aviso (toast) al
  perder/recuperar la conexión sin salir de la pantalla.
- «Otra ronda» desde el álbum Wi-Fi: el anfitrión vuelve al lobby con
  los mismos jugadores (reset de `HOST.started/engine/guess/scoreVotes`);
  el invitado espera con `waitForNextWifiGame()` hasta un `gameId` nuevo.

### 2. Reparto con 10 y 14 jugadores
- Respaldo con lista fija de 8 índices eliminado. Nuevo `cyclicOrders(n,
  steps)` (orden barajado + desplazamientos barajados con 0 en la
  primera) y `validateOrders` (cada columna es permutación, índices
  válidos, paso 1 ≠ autor salvo 1 jugador).
- `GameEngine.start()` reconstruye `stepMap` desde cero y valida/regenera
  el reparto si falla (salvo Solo).
- Nuevo gancho `#auto=distrib` en `www/index.html` y prueba en
  `VERIFICACION/v2.4/modos/verify_modes.py`.

### 3. Transporte nativo en Android
- `nativeHttp()` (CapacitorHttp en Android, `fetch` en navegador).
  `HttpTransport._fetch` usa `CapacitorHttp.request` con timeouts y
  errores clasificados (`address`/`http`/`timeout`/`network`); `ping`,
  `join`, estados, entregas, salidas y Adivina por el mismo transporte.
- `btnDoJoin` usa `transport.ping()` (antes `fetch` directo) con
  mensajes distintos (timeout / sin conexión / dirección no válida) y
  validación de octetos IPv4 (0–255) y puerto (1–65535).
- `stopLanServer()` (elimina el listener `onRequest` guardado y llama a
  `plugin.disconnect()`), llamado desde `leaveGame`, atrás desde
  crear-sala y `btnCreateWifiBack`; el listener se registra una sola vez
  por sala (`S.wifi.lanListening`). Botón ↻ para refrescar la IP
  anunciada (`plugin.getLanIp()`).
- Sin `allowMixedContent` global. `detectLanIp()` ya priorizaba
  192.168.43.x; no se cambió Java.

### 4. Adivina por revisión, no por trazos
- `GuessEngine.setCanvas(playerIdx, round, revision, image)` valida
  dibujante, ronda y revisión mayor que la aceptada; descarta viejas y
  duplicadas. `canvasRev`/`canvasImage` por ronda; `beginRound` resetea.
- `guessCanvasDirty()` / `guessCanvasSend()` / `guessFlushCanvas()`: el
  dibujante sube la imagen completa (640×440) al cambiar el lienzo;
  `notifyCanvasChange()` en pincel, borrador, formas, relleno, Deshacer,
  Rehacer y Limpiar (con callback en `restoreData`); «¡Hecho!» confirma
  el último dibujo antes de cerrar la ronda.
- `guessIoFor`: `postCanvas` en lugar de `postStroke`; `pollGuessNet`
  pasa `knownRev`; el anfitrión devuelve la imagen solo si cambió
  (`/api/guess/canvas`, `/api/score/vote`; `/api/guess/stroke`
  eliminada). El invitado aplica por revisión con comprobación de
  ronda/revisión en `onload`. Retirado el cursor por longitud
  (`lastStrokeCount`); `addStrokes` se conserva solo para el modo local.

### 5. Ajustes personalizados
- `CURRENT_CUSTOM_CFG`, `effectiveCustom()`, `customSteps()`,
  `customType()`, `customSpec()`; entrada `MODE_SPECS.custom` y modo
  «Personalizado» (⚙️) en `MODES`. `specFor("custom")` devuelve
  `customSpec()`. `GameEngine` guarda `customCfg`, usa `customSteps` y
  `customType`/`customCfg.times`; `taskFor` marca `secret` por
  `customCfg.secret`.
- El anfitrión congela la config efectiva al empezar (`hostStart`:
  `randomRounds` sorteado una sola vez entre 2 y nº de jugadores) y la
  comparte (`customCfg` en el estado; `hostNormalState` la devuelve).
- `drawOptsFor`: `secret` y `initialImage` (sigue dibujando) en custom.
  `showWifiTask`: mismo tratamiento con `S.customCfg`.
  `syncSetupMode`: título, pista y selectores de tiempo con los valores
  de la config en custom. Pestañas: `tabCustom` pone `S.mode="custom"`,
  `tabPresets` vuelve a Normal.
- Álbum: puntuación activa también en custom (`score`); criterio
  «Conservó la idea del dibujo anterior» en Solo dibujar; voto por wifi
  vía `transport.scoreVote` con `refreshScoreVotes()` (sin re-montar el
  álbum); el sondeo del álbum sigue tras el fin para recibir
  `scoreVotes` del anfitrión. `btnNewGame`/`btnReplay` llaman
  `stopNetPoll()`.
- «Otra ronda» local en custom vuelve a sortear `randomRounds`.

### Endurecimiento extra (encontrado al probar)
- `taskFor` reventaba si el motor no había llamado a `start()` (el
  motor del cliente en wifi no lo llama: `chains` vacío). Ahora devuelve
  la tarea sin pista en vez de reventar (también la rama de
  Rompehielos). No lo golpea el juego normal; solo lo encontró la
  prueba de Secreto.

## Pruebas de aceptación (todas OK)

Simulador wifi `VERIFICACION/v2.4/wifi/run-wifi.mjs` (22 escenarios,
Chromium real por CDP; informe en `wifi-resultados.json`):

| Prueba | Resultado |
|---|---|
| write-12s: teclear 12 s sin pulsar Hecho | Texto completo, creció sin perder letras; reloj monótono 45 → 33 |
| draw-12s: dibujar 12 s con Deshacer | Tras Deshacer queda el primer trazo (len 34546 vs blanco 7822); reloj 59 → 46 |
| netcut-5s: corte de red 5 s a mitad de turno | 8/12 muestras sin conexión, pantalla siempre en el turno, texto intacto, recuperado (offlineSince=0) |
| lost-submit: respuesta de entrega perdida | Reintento → `already:true`; un solo eslabón por jugador y paso |
| close-room-single: cerrar sala y jugar solo | Clientes ven «El anfitrión cerró la sala»; anfitrión sin sondeos (`pollActive=false`); partida en un solo teléfono hasta el álbum sin reiniciar |
| masterpiece: turno sin límite | `stepLimit=0`, píldora «Sin límite», nadie saltado |
| wifi-10: partida wifi de 10 jugadores | 10 álbumes × 10 eslabones; 10 por jugador; permutación OK |
| wifi-14: partida wifi de 14 jugadores | 14 álbumes × 14 eslabones; 14 por jugador; permutación OK |
| guess-canvas: 650 trazos, todas las herramientas | Lienzo del invitado idéntico byte a byte al del dibujante (len 25986); podio |
| custom: 6 partidas cambiando un ajuste cada vez | Tiempo rápido (30 s), solo dibujar, sigue dibujando (3/3 lienzos no en blanco), puntuación (voto compartido: Roi 1 pt), secreto, turnos aleatorios (3 rondas) |

Regresión (mismo simulador, con el código final): normal, story,
secret, animation, icebreaker, missing, guess, dropout, host-leaves,
kick, late-join, reconnect — **todos OK, 0 errores de consola**.

Modos (`VERIFICACION/v2.4/modos/verify_modes.py`, con el código final):
14 modos + Normal + Adivina + navegación, **0 errores, 0
desbordamientos**. Nuevo `#auto=distrib`: **2.240 comprobaciones
(n=1..14, pasos 1, 2, n, 2n+1), 0 fallos**; partidas completas de Obra
maestra (1 paso), Fondo (9 y 21 pasos), Normal a 10 y 14 jugadores y
Personalizado con turnos aleatorios (2 pasos).

B1/B2 (Deshacer y barra roja) re-verificados a 360 y 390 px con
`/tmp/check-b1b2.mjs`: 6 mediciones, **0 desbordamientos, 0 botones
cortados, todos visibles** (capturas `b1b2-*.png` en este directorio).

## Incidencias del harness (no de la app)
- La pasada completa `run-wifi.mjs all` se colgó dos veces en story
  (el juego terminó en las 4 páginas con 0 errores, pero una llamada
  CDP no resolvió nunca). Se añadieron timeouts de 30 s a las llamadas
  CDP y de 10–15 s a los `fetch` del harness: un cuelgue ahora es un
  fallo visible, no un silencio. Tras el cambio, story pasa (5,5 s).
  Los escenarios se re-ejecutaron por separado con el código final.

## Qué quedó pendiente solo para teléfono real
- Sonidos a oído, vibración, dibujo con el dedo, wifi entre dos
  teléfonos con hotspot de verdad (la IP 192.168.43.x y el plugin
  LanServer real solo se prueban ahí), ícono D5 en el launcher
  (instalación a medio terminar: verificar todos los tamaños y el
  `cap sync`), Baloo 2 en la WebView, portapapeles de INVITAR.
- La instalación de la v2.4 en el Redmi de Roi (la v2.1 ya instaló
  sola; el motivo exacto queda pendiente de que Roi lo confirme).

## Archivos tocados
- `www/index.html` (md5 `d8447c9d72e7b9321414266ea6f479b8`; sincronizado
  a Android con `npx cap sync android`).
- `LEEME_APK.md` (§8 de la v2.4 con lo corregido; constancia del
  punto 6 y del problema de instalación resuelto solo).
- `VERIFICACION/v2.4/wifi/run-wifi.mjs` (10 escenarios nuevos,
  ganchos de red `/__test/blackout` y `/__test/dropNextSubmit`,
  timeouts CDP), `VERIFICACION/v2.4/wifi/README.md`,
  `VERIFICACION/v2.4/modos/verify_modes.py` (`#auto=distrib`).
- Sin commit, sin push, sin build. 67 archivos modificados sin
  commitear (incluidos los mipmap de la D5, de la instalación a medias
  anterior a esta tarea).
