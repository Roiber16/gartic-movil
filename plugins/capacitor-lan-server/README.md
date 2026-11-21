# capacitor-lan-server (Gartic Móvil)

Pequeño plugin Capacitor propio para **Gartic Móvil** (solo Android),
copiado de Ecos del Olimpo (`ecos-apk/plugins/capacitor-lan-server`) y
adaptado: paquete Java `com.garticmovil.lanserver`.

El anfitrión de una partida por wifi local lleva un pequeño servidor HTTP
dentro de la app (NanoHTTPD). El invitado se conecta a ese servidor para
unirse a la partida y enviar sus dibujos y frases, sin internet, sin
servidor externo y sin QR.

Por qué un plugin propio y no `@cappitolian/http-local-server`: ese paquete
publicado obtiene la IP con `WifiManager.getConnectionInfo()`, que devuelve
0 cuando el teléfono es el punto de acceso (hotspot). Este plugin, en
cambio, enumera las interfaces de red y escucha en `0.0.0.0`, así que
funciona también cuando el anfitrión crea el punto de acceso.

## Cambios respecto a Ecos

El patrón de Ecos **ya era de reenvío genérico**: TODA petición HTTP
(cualquier método y ruta) se entrega a JavaScript con el evento
`onRequest` (`{ requestId, method, path, body, headers, query }`) y la
respuesta vuelve con `sendResponse({ requestId, body })`; el servidor
espera hasta 10 segundos la respuesta de JS. Por eso los endpoints del
juego (`POST /api/join`, `/api/state`, `/api/submit`, `/api/start`) **no
necesitaron ninguna ampliación**: llegan a JS tal cual y es el JS del
juego quien decide qué responder. No hay señalización WebRTC aquí: el
contenido es JSON del juego (jugadores, estado, dibujos, frases).

Único cambio real en `LanServer.java`: `GET /ping` se responde
directamente en Java con `{"ok":true}`, sin pasar por JS, para que el
invitado pueda comprobar que el anfitrión está alcanzable antes de
unirse. Todo lo demás sigue el reenvío genérico a JS.

## API (JS)

```js
const LanServer = Capacitor.registerPlugin('LanServer');

// Arranca el servidor. Devuelve la IP LAN y el puerto real.
const { ip, port } = await LanServer.connect(); // puerto fijo 7777 si está libre

// IP LAN del teléfono (fiable, por APIs de Android)
const { ip } = await LanServer.getLanIp();

// Peticiones entrantes: { requestId, method, path, body, headers, query }
// path es "/api/join", "/api/state", "/api/submit" o "/api/start"
// (y "/ping" nunca llega aquí: se responde en Java).
await LanServer.addListener('onRequest', async (data) => {
  const respuesta = procesarEnElJuego(data); // según data.path y data.body
  await LanServer.sendResponse({ requestId: data.requestId, body: JSON.stringify(respuesta) });
});

await LanServer.disconnect();
```

Puerto: se intenta el **7777** primero (fijo, para que el invitado solo
tenga que escribir la IP) y, si está ocupado, 7778…7786. La IP que
devuelve `connect()` es la mejor IPv4 local: primero la del punto de
acceso (`192.168.43.x`) y luego cualquier IPv4 de la red local.

El invitado, desde su teléfono, llama con `fetch` a
`http://<IP>:7777/ping` para comprobar la conexión y a
`http://<IP>:7777/api/...` para jugar.

## Permisos y tráfico sin cifrar

El manifiesto del plugin declara `INTERNET`, `ACCESS_NETWORK_STATE` y
`ACCESS_WIFI_STATE` (se fusionan solos en el manifiesto de la app).

La app además necesita `android:usesCleartextTraffic="true"` (lo pone
`scripts/fix-manifest.js` en CI, igual que en Ecos), porque el invitado
llama por HTTP claro (`http://192.168.x.x:7777`) a la red local. Sin
esto, Android 9+ bloquea esas llamadas y «Unirse por IP» nunca
conectaría. Solo afecta a la red local: el juego no usa internet.

**Riesgo a probar en teléfono real:** en Ecos este mismo arreglo
(`usesCleartextTraffic="true"` en el manifiesto de la app) es el que se
usa y el duelo wifi está pendiente de probar con dos teléfonos reales.
En Gartic Móvil pasa igual: el `fetch` desde la WebView de Capacitor
(esquema `https`) hacia `http://IP:7777` puede tropezar además con la
política de contenido mixto de la WebView. Si en el teléfono real el
invitado no conecta aunque el `/ping` responda desde el navegador, hay
que probar (en ese orden): 1) que el manifiesto final tenga
`usesCleartextTraffic="true"`, 2) un Network Security Config que
permita texto claro solo a IPs privadas, 3) servir el juego por el
mismo origen. No se deja un Network Security Config en el proyecto
porque el punto 1 es lo que usa Ecos y basta en teoría; si la prueba
real lo desmiente, se añade entonces.
