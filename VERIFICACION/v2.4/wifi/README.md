# Wifi local — simulación con dos instancias reales del juego

Auditoría y endurecimiento del wifi local de Gartic Móvil v2.4 (ver
`LEEME_APK.md` §5). El objetivo final de Roi es jugar por wifi local,
así que aquí se prueba el flujo completo sin dos teléfonos reales.

## Cómo funciona

`run-wifi.mjs` (Node 24, sin dependencias) hace tres cosas:

1. **Servidor de red local simulada** (puertos 18081–18094): sirve la app
   en un origen distinto por página (cada página tiene su propio
   `localStorage`, como dos teléfonos distintos) y reenvía las
   peticiones `/api/*` a la página del anfitrión, igual que el plugin
   LanServer: la petición queda pendiente, el anfitrión la recoge con
   `GET /__lan/pending` (cada 120 ms), la atiende con `hostRouter` y
   devuelve la respuesta con `POST /__lan/respond`.
2. **Dos o más páginas reales de Chromium** (el de Playwright,
   pilotadas por CDP con el WebSocket global de Node 24). La página del
   anfitrión lleva un stub de `window.Capacitor.Plugins.LanServer`
   (`connect` + `addListener` + `sendResponse`); las demás son la app
   tal cual, uniéndose a `127.0.0.1:18081`.
3. **Un bot por página** que juega sus turnos de verdad: escribe,
   describe, dibuja con PointerEvents reales sobre el lienzo, elige
   palabra en Adivina y adivina la del dibujante.

## Uso

```sh
node run-wifi.mjs normal|story|secret|animation|icebreaker|missing|guess|dropout|host-leaves|kick|late-join|reconnect|write-12s|draw-12s|netcut-5s|lost-submit|close-room-single|masterpiece|wifi-10|wifi-14|guess-canvas|custom [all]
```

Cada escenario crea sala, une clientes, juega y comprueba el resultado.
Escribe `wifi-resultados.json` (OK/FALLO por escenario, con el registro)
y capturas `<escenario>-<jugador>.png` (lobby, juego, álbum/podio).

## Escenarios

| Escenario | Qué comprueba |
|---|---|
| normal | Partida Normal por wifi, 4 jugadores; cada álbum es una permutación de autores |
| story, secret, animation, icebreaker, missing | Esos modos por wifi, partida completa y autoría |
| guess | Adivina por wifi; el dibujante ve las 3 opciones y tiene 15 s para elegir; podio |
| dropout | Un cliente se cae a mitad de partida: el vigilante salta sus turnos y la partida termina |
| host-leaves | El anfitrión abandona: los clientes ven «El anfitrión cerró la sala» |
| kick | Dos con el mismo apodo («Ana 2»); el expulsado no vuelve a entrar |
| late-join | Llegada tardía rechazada con mensaje claro |
| reconnect | Un cliente pierde la conexión 10 s y vuelve a unirse con el mismo código |
| write-12s | (Punto 1) Un cliente teclea 12 s sin pulsar Hecho: ningún sondeo borra letras ni reinicia el reloj |
| draw-12s | (Punto 1) Un cliente dibuja 12 s con Deshacer en medio: el lienzo no se borra y el reloj no se reinicia |
| netcut-5s | (Punto 1) Corte de red de 5 s a mitad de turno: la pantalla no se pierde, el texto sigue y al recuperar se sigue en el mismo turno |
| lost-submit | (Punto 1) La respuesta de una entrega se pierde: el cliente reintenta, el anfitrión devuelve `already:true` y hay un solo eslabón |
| close-room-single | (Punto 1) El anfitrión cierra la sala: los clientes lo ven, no quedan sondeos ni reintentos, y el anfitrión juega en un solo teléfono sin reiniciar |
| masterpiece | (Punto 1) Obra maestra sin límite: `stepLimit=0`, píldora «Sin límite», nadie es saltado por el vigilante |
| wifi-10, wifi-14 | (Punto 2) Partidas wifi completas de 10 y 14 jugadores, con autoría por álbum |
| guess-canvas | (Punto 4) Adivina con pincel, línea, círculo, cuadrado, relleno, borrador, Deshacer, Rehacer y Limpiar y más de 600 trazos: el lienzo del invitado es idéntico al del dibujante |
| custom | (Punto 5) Seis partidas reales cambiando un ajuste cada vez: tiempo rápido, solo dibujar, sigue dibujando, puntuación, secreto y turnos aleatorios |

## Notas

- Chrome se lanza con `--disable-background-timer-throttling` (y
  variantes): sin eso, Chrome estrangula los temporizadores de las
  pestañas en segundo plano y la simulación se arrastra. En los
  teléfonos reales cada jugador mira su propia pantalla, así que nada
  de esto se estrangula.
- Lo que esto NO prueba: el hotspot de verdad entre dos Redmi, el
  plugin LanServer real (aquí lo sustituye el stub), dibujar con el
  dedo, sonidos y vibración por wifi, y la IP que anuncia el anfitrión
  (192.168.43.x). Eso solo se prueba con dos teléfonos reales.
