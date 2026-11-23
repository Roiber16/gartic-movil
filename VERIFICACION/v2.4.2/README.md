# Verificación v2.4.2 — los 6 cambios de Roi (23 nov 2026 10:48)

**Fecha:** 23 nov 2026. **Solo se editó `www/index.html`** (y se copió la
imagen D5 exacta a `www/assets/icon-1024.png`, md5 `b0d502d5…`, sin
redibujarla). **No se tocó el ícono del launcher** (mipmaps intactos),
no se compiló APK, no hay commit.

## Método

- Chromium headless (headless_shell 1161) a **360x800** y **320x568**,
  con el script `verify.py` (9 escenarios) y `verify2.py` (álbum de
  Animación y pantalla de dibujo). Las copias temporales se crean dentro
  de `www/` para que las rutas relativas (`assets/`, `fonts/`) resuelvan
  como en la app, y se borran al terminar.
- Resultados en `reporte.json` y `reporte-extra.json`; capturas en
  `shots-360/` y `shots-320/`.

## Resultados (los 9 + 2 escenarios)

| Control | Resultado |
|---|---|
| Errores de consola | 0 en los 11 escenarios |
| Desbordamiento horizontal | 0 a 360x800 y a 320x568 |
| Pestañas ANÓNIMO/VERIFICADO | No existen (`tabAnon`/`tabVerif` ausentes); sin texto de verificación; `.profile-box` con radio 16 px completo |
| Avatares | 22 en la rejilla (12 animales + 10 personas), grupos «Animales» / «Personas»; a 320 px la rejilla pasa a 4 columnas por la media query que ya existía (≤400 px) |
| «Jugable en vX» | 0 en todo el texto visible; 0 etiquetas `.tag` en las tarjetas de modo |
| Logo D5 en cabecera | `img.logo` con `src="assets/icon-1024.png"`, carga correcta (`ok:true`) en inicio, configurar, modos, crear sala y unirse; también visible en ajustes, cómo se juega y salas; sigue oculto en cuenta atrás, paso del teléfono, turno, Adivina, espera, álbum y podio |
| Flecha del menú | 18 px del borde derecho (mínimo pedido: 12 px), medida en el botón de «Número de jugadores» |
| Menús propios | 0 `<select>` visibles en todas las pantallas; 16-17 botones `.menu-btn` según la pantalla |

## Pruebas funcionales (el menú actualiza el estado como el select)

- **Número de jugadores:** abrir el menú y elegir «5 jugadores» →
  `numPlayers.value="5"`, etiqueta «5 jugadores», 5 filas de jugadores.
- **Avatar por jugador:** abrir el menú de avatar del jugador 1 y elegir
  👩🏼 → el select oculto vale «👩🏼» (se ve en `shot-setup.png`).
- **JUGADORES (modos):** elegir «8» → etiqueta «8» y 8 huecos de avatar.
- **Modo de la sala (wifi):** 17 opciones, etiqueta «Normal» al crear sala.
- **Reproductor de animación:** velocidad «2's» (`value="2"`) y bucle
  «Adelante y atrás» (`value="pingpong"`); la etiqueta larga se partió
  en dos líneas para que se lea entera (antes se veía «Adel…»).
- **Grosor del lienzo:** el menú de `brushSize` existe y se crea al
  abrir el lienzo; sigue oculto con su contenedor en la pantalla de
  juego, igual que lo estaba el select original.
- **Menú abierto:** 6 opciones, panel blanco con borde violeta
  (`shot-setup-menu.png`); se cierra al tocar fuera, con Escape, al
  hacer scroll o al cambiar de tamaño.

## Selects convertidos (todos)

numPlayers, timeWrite, timeDraw, timeDescribe, guessRoundTime,
modesMaxPlayers, customTime, customSequence, customTurns, customKeep,
wifiMaxPlayers, wifiModeSelect, avatar por jugador, brushSize,
animSpeed, animLoop. Ninguno quedó con el desplegable nativo.

## Cómo funciona (para el futuro)

El `<select>` original sigue en el DOM, oculto (`display:none`), y
guarda el valor: al elegir en el menú se le asigna el valor y se
dispara su evento `change`, así ningún handler cambió. El panel es
`position:fixed` y se coloca con `getBoundingClientRect` para que no
lo recorte ningún contenedor con scroll. Cuando el código pone el
valor por programa (reparto de jugadores, modo wifi, círculos de
grosor), llama a `syncMenu(sel)` para refrescar la etiqueta.
