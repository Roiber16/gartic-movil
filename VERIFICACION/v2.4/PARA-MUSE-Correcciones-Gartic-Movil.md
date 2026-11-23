# Gartic Móvil · Correcciones y pruebas para Muse

Base de trabajo: código **1.4.0**, `versionCode 6`, del ZIP `Gartic-Movil-proyecto-completo.zip`. La APK más reciente de la carpeta es **1.3.0**. Usa `www/index.html` como fuente del juego y sincronízala con Android al preparar el build. Conserva las reglas y los recursos que ya funcionan en cada preset.

Orden de trabajo: **turnos Wi‑Fi → reparto de jugadores → transporte Android → dibujo en Adivina → ajustes personalizados**. El diagnóstico de instalación puede hacerse en paralelo si hay un teléfono de prueba. Integra los arreglos en una sola entrega completa.

## 1. Conservar el turno mientras llega el estado Wi‑Fi

**Dónde mirar.** `www/index.html`, funciones `startNormalWifiClient`, `showWifiTask`, `submitCurrent`, `hostNormalState`, `hostSubmit` y `hostWatchdog`. Revisa también `startSingleGame`, `leaveGame` y los botones del álbum porque comparten el estado de red.

**Qué falla.** El cliente consulta el estado aproximadamente cada segundo. La condición actual comprueba si el paso ya se entregó y, mientras siga pendiente, vuelve a montar la pantalla. Así se pierden la frase, el lienzo y el foco del teclado, y el reloj vuelve a su valor inicial. Los bots que rellenan y entregan en una sola acción pueden pasar la prueba sin detectar el problema.

**Cómo arreglarlo.**

1. Separa el turno **mostrado** del turno **enviado**. El anfitrión debe identificar la partida y devolver el paso actual y la tarea del jugador. Construye una clave con el identificador de partida, el paso y el jugador. Guarda la última clave mostrada en el cliente y llama a `showWifiTask()` solo al recibir una clave nueva. Para la misma clave, actualiza únicamente el reloj y el estado de red. Conserva el borrador, el lienzo, el historial de deshacer y el foco.
2. Serializa el sondeo. Lanza la próxima consulta después de resolver la anterior. Si ya cambió la partida o el usuario salió, descarta el resultado tardío. Durante un corte, conserva el turno visible, muestra un aviso en esa misma pantalla y reanuda la consulta al recuperar la conexión. Si el anfitrión ya pasó a otro turno, informa qué pasó antes de mostrar la nueva tarea.
3. Haz que el anfitrión sea la referencia del tiempo. Al abrir cada paso, calcula el plazo del tipo de tarea que realmente toca. Devuelve el tiempo restante calculado en el anfitrión, o el plazo junto con la hora del anfitrión, para que cada cliente pueda dibujar su reloj sin reiniciarlo. Para los turnos sin límite usa un valor explícito, como `null`. El vigilante debe distinguir entre un jugador conectado que sigue dibujando sin límite, un jugador que avisó que salía y uno que dejó de responder.
4. Al entregar, captura una sola vez el jugador, la partida, el paso y el contenido. Reintenta con esos mismos datos si falla la red. Una entrega confirmada cuya respuesta se perdió debe obtener la misma confirmación sin crear otro eslabón. Si el anfitrión ya saltó el paso, cancela el reintento y avisa. Si al llegar a cero todavía hay un envío pendiente, conserva su contenido mientras el anfitrión pueda aceptarlo.
5. Al salir de una sala, detén sondeos, temporizadores y reintentos, e invalida las respuestas pendientes de esa sesión. Al comenzar una partida de un solo teléfono, restablece explícitamente el transporte local y el estado de red. Revisa también «Otra ronda» desde el álbum Wi‑Fi para que su acción corresponda al tipo de partida que se va a iniciar.

**Pruebas de aceptación.** En una partida Normal, escribe durante 12 segundos sin pulsar «Hecho». Pausa entre palabras y comprueba que ningún sondeo borra letras, cambia el foco ni reinicia el reloj. Dibuja durante otros 12 segundos y deshaz un trazo después de varios sondeos. Corta la red 5 segundos y reconecta durante el mismo turno. Simula que se pierde la respuesta de una entrega aceptada. Confirma un solo eslabón en el álbum. Cierra la sala, abre otra y después juega en un solo teléfono sin reiniciar la aplicación. Prueba también un turno de Obra maestra sin límite, dejando al jugador conectado más allá del antiguo tope.

## 2. Repartir correctamente los turnos con 10 y 14 jugadores

**Dónde mirar.** `buildOrders`, `GameEngine.start`, `chainFor`, `hostStart`, el selector `wifiMaxPlayers` y el informe de pruebas Wi‑Fi.

**Qué falla.** El selector ofrece 10 y 14 plazas. Cuando el reparto aleatorio llega a su respaldo, la lista de jugadores sale de una lista fija de ocho índices. Aparecen asignaciones vacías o repetidas que pueden impedir completar el álbum.

**Cómo arreglarlo.**

1. Construye la lista de índices a partir del número real de jugadores, por ejemplo `Array.from({ length: n }, (_, i) => i)`. Usa un reparto cíclico barajado como respaldo garantizado. Baraja el orden de jugadores y los desplazamientos de ronda, con desplazamiento cero en la primera. Para una cadena cuyo autor ocupa la posición `j` en el orden barajado, el jugador del paso `s` es `orden[(j + desplazamiento[s]) % n]`. Dentro del primer ciclo usa cada desplazamiento una sola vez. Si el preset tiene más pasos que jugadores, reutiliza un ciclo completo y comprueba el salto entre ciclos. Conserva el reparto propio de Solo.
2. Reconstruye `stepMap` desde cero en cada `GameEngine.start()`. Antes de empezar, comprueba que cada columna asigna exactamente una tarea a cada jugador, que cada índice es válido y que los primeros pasos de cada cadena respetan la regla del preset. Si el reparto falla, regénéralo antes de anunciar la cuenta atrás.
3. Usa una validación común para el cupo elegido y el total real de la sala. El anfitrión congela los jugadores y el reparto al comenzar. Deriva la lista y el contador del lobby de ese mismo cupo. Si la tira de avatares muestra solo ocho por espacio, el total y la lista completa deben poder consultarse. Mantén el máximo actual de ocho en un solo teléfono.

**Pruebas de aceptación.** Fuerza el reparto de respaldo para evitar depender del azar. Comprueba tamaños de 1 a 14 respetando el mínimo de cada modo y prueba especialmente 8, 10 y 14. Incluye un modo más corto que el número de jugadores y otro más largo, como Fondo. Completa partidas Wi‑Fi simuladas de 10 y 14 con dibujos y álbumes. Confirma que todos reciben un turno por paso y que el álbum se abre sin solicitudes que agoten el tiempo de espera.

## 3. Usar el transporte nativo para el Wi‑Fi en Android

**Dónde mirar.** `capacitor.config.json`, `HttpTransport._fetch`, el botón `btnDoJoin` y el plugin `capacitor-lan-server`, en particular `LanServer.java` y `LanServerPlugin.java`.

**Qué comprobar.** La vista web de Android se abre con HTTPS y el anfitrión escucha por HTTP en la red local. El flujo del invitado usa `fetch`, incluido un `fetch` directo para probar la IP. Capacitor desactiva el contenido mixto por defecto. El navegador de la simulación usa otro origen y un plugin simulado, así que su resultado por sí solo no demuestra qué ocurre en la APK.

**Cómo arreglarlo.**

1. Mantén el esquema HTTPS de la aplicación y usa el puente nativo `CapacitorHttp.request` específicamente para las solicitudes al anfitrión en Android. En navegador, mantén `fetch` para la simulación. Haz que `ping`, `join`, estados, entregas, salidas y Adivina pasen por el mismo transporte. Sustituye el `fetch` directo de `btnDoJoin` por el método `ping` del transporte.
2. Valida la IPv4 y el puerto de la sala antes de enviar una petición. Configura `connectTimeout` y `readTimeout`, evita redirecciones y distingue respuesta HTTP, JSON incorrecto, sala cerrada, código incorrecto y tiempo de espera agotado. Si el puente nativo responde después de haber salido, ignora su resultado mediante el identificador de sesión. Mantén el acceso HTTP nativo acotado a la sala local. Deja desactivada la opción global `allowMixedContent` de la vista web.
3. Prueba primero la IP que anuncia el anfitrión, en especial cuando tiene datos móviles y hotspot encendidos a la vez. `detectLanIp()` prioriza prefijos. Si anuncia la interfaz equivocada, revisa la selección en Java y ofrece una IP Wi‑Fi o de hotspot que el invitado pueda alcanzar. Muestra la IP y el puerto que usa el servidor, incluido un puerto alternativo cuando 7777 esté ocupado.
4. Guarda el identificador del listener `onRequest` y elimínalo al cerrar la sala. Llama a `disconnect()` en el mismo cierre, tanto si salieron del lobby como si abandonaron la partida. Verifica que reabrir la sala crea un solo listener. Con `targetSdk 36` basta el permiso `INTERNET` para acceso local según la guía actual de Android. Si el proyecto sube a SDK 37, revisa el flujo de solicitud en tiempo de ejecución de `ACCESS_LOCAL_NETWORK`.

**Pruebas de aceptación.** Usa dos Android y un hotspot con salida a internet desactivada. Alterna cuál es el anfitrión. Comprueba entrada por IP y código, una partida Normal, una de Adivina, un corte breve y el cierre de sala. Repite en Wi‑Fi de router sin salida a internet si está disponible. Anota modelos, versiones de Android, IP/puerto y fase exacta donde ocurrió cualquier error. En las pruebas simuladas conserva además los casos de expulsión, sala llena y unión tardía.

Documentación: [CapacitorHttp](https://capacitorjs.com/docs/apis/http), [configuración Android de Capacitor](https://capacitorjs.com/docs/config) y [permiso de red local de Android](https://developer.android.com/privacy-and-security/local-network-permission).

## 4. Mostrar el mismo dibujo de Adivina en todos los teléfonos

**Dónde mirar.** `GuessEngine.addStrokes`, `hostGuessStroke`, `hostGuessState`, `guessIoFor`, `renderGuessFromState`, `initCanvas`, `onPointerUp`, `doUndo`, `doRedo` y «Limpiar».

**Qué falla.** La red transmite trazos de pincel y borrador. Las formas, el relleno y los cambios de historial alteran el lienzo local sin actualizar el remoto. Además, el receptor usa la cantidad de trazos como cursor. Cuando el host corta la lista a 600, esa cantidad se mantiene fija y los demás dejan de recibir trazos nuevos.

**Cómo arreglarlo.**

1. Para Adivina por Wi‑Fi, propongo sincronizar el **estado completo del lienzo con un número de revisión**. Cada cambio confirmado en el lienzo incrementa la revisión de esa ronda. Usa el mismo mecanismo para pincel, borrador, formas, relleno, Deshacer, Rehacer y Limpiar. Los gestos se dibujan localmente con la rapidez de ahora. Agrupa varios cambios cercanos si el jugador dibuja rápido.
2. Envía una imagen del lienzo de 640 × 440 con la partida, la ronda y la revisión. Mantén un solo envío de dibujo en curso por teléfono y conserva la última revisión pendiente. Si se pierde una respuesta, reenvía la última imagen disponible. El anfitrión conserva la última revisión aceptada de la ronda, valida que provenga del dibujante de turno y descarta revisiones viejas o duplicadas. Al pulsar «Hecho», confirma primero el último dibujo si hubo cambios pendientes. Limita el tamaño de la imagen al máximo razonable para el lienzo y compruébalo con dibujos densos.
3. El invitado informa en su sondeo qué revisión tiene. El anfitrión devuelve la imagen solo cuando su revisión cambió o cuando el invitado se reincorpora sin imagen. Al decodificar, comprueba de nuevo la ronda y la revisión para evitar que una carga lenta sobrescriba un dibujo posterior. Retira el cursor por longitud de lista de este flujo. En el cambio de ronda se inicia un lienzo y una revisión nuevos.
4. Evalúa la frecuencia de envío en el Redmi y ajusta la agrupación si la codificación o la red afectan la fluidez. El mismo resultado debe verse con lápiz, relleno y herramientas de edición, y debe llegar aunque la última operación sea limpiar el lienzo. El dibujo de un solo teléfono conserva su flujo local.

**Pruebas de aceptación.** Compara el lienzo del dibujante y el del invitado tras línea, círculo, cuadrado, relleno, borrador, deshacer, rehacer y limpiar. Prueba más de 600 trazos, pérdida de una respuesta, reconexión a mitad de ronda, un envío tardío de la ronda anterior y «Hecho» justo al soltar el último trazo. Verifica anfitrión e invitado como dibujantes. Comprueba pistas, puntos y podio al final.

## 5. Hacer que funcionen los ajustes personalizados

**Dónde mirar.** `S.custom`, `applyCustomTimes`, `settingsSummaryText`, `startSingleGame`, `createWifiRoom`, `hostStart`, `GameEngine`, `drawOptsFor`, `showWifiTask` y `renderAlbum`.

**Cómo arreglarlo.** Aísla «Personalizado» como la configuración de una partida basada en Normal. Crea una configuración efectiva, validada al empezar, con secuencia, duración por tipo de tarea, rondas, acumulación, puntuación y secreto. Úsala en el motor, en las pantallas y en el resumen de sala. El anfitrión comparte la configuración congelada y el total real de rondas. El cliente aplica las reglas recibidas y los presets siguen usando sus reglas actuales. Las siguientes reglas son propuestas para concretar etiquetas que hoy no tienen efecto.

| Ajuste | Comportamiento propuesto |
| --- | --- |
| Tiempo | Aplica los valores Rápido, Normal o Lento al tipo de tarea que toca. En un solo teléfono, muestra también esos valores en la configuración antes de iniciar. |
| Secuencia | «Escribir y dibujar» empieza con una frase y luego alterna dibujo y descripción, como el Normal actual. «Solo dibujar» empieza con un lienzo en blanco y usa dibujo en todas las rondas. |
| Turnos | «Todos» juega tantas rondas como jugadores. «Cantidad aleatoria de rondas» sortea una duración entre 2 y el máximo válido para esa partida, una sola vez al iniciar. Todos juegan en cada ronda y el progreso muestra cuántas rondas salieron. La etiqueta ampliada aclara qué parte se sortea. |
| Sigue dibujando | Si la tarea actual y la anterior de la cadena son dibujos, el anterior se carga como fondo editable con la imagen final que recibió el álbum. Si la tarea parte de una frase, abre un lienzo nuevo. Una pausa de red o una consulta de estado no vuelve a cargar el fondo. |
| Puntuación | Reusa el voto del álbum. El criterio en Solo dibujar puede ser «Conservó la idea del dibujo anterior». En Wi‑Fi, usa un marcador común decidido por el anfitrión y actualízalo en los invitados. El primer eslabón no se puntúa porque carece de un eslabón previo. |
| Secreto | Reusa la censura de texto y el velo de dibujo durante la tarea. Guarda lo que el jugador realmente entregó para el álbum. Si también está activo «Sigue dibujando», el fondo se inicializa según esa regla y el velo sigue la lógica de Secreto al dibujar. |

**Pruebas de aceptación.** Cambia un ajuste cada vez y comprueba su efecto en una partida real, no solo en el resumen. Juega la combinación «Solo dibujar + Sigue dibujando + Secreto», prueba puntuación en dos teléfonos y verifica que un nuevo preset Normal vuelve a sus valores propios. Comprueba que todos los jugadores ven el mismo total de rondas y, con puntuación activa, el mismo resultado.

## 6. Diagnosticar la instalación del Redmi y cerrar la entrega

Las cinco APK archivadas tienen el mismo certificado entre sí y sus ZIP son legibles. Sigue abierta la causa del mensaje «No se instaló la aplicación» de la 1.1.1 en el Redmi 10. El mensaje genérico, por sí solo, tampoco permite saber si la descarga se truncó, si había una versión más nueva, si faltaba espacio o si el instalador rechazó algo más.

1. Compila una candidata con el flujo del repositorio. Ejecuta `npm ci`, `node scripts/setup-android.js`, `npx cap sync android`, `node scripts/fix-debug-signing.js` y `./gradlew assembleDebug` desde `android/` para el último paso. Conserva `cu.roi.garticmovil`, el certificado del proyecto y un `versionCode` mayor que el de cualquier APK ya entregada al grupo. Comprueba la versión efectiva después de aplicar `fix-debug-signing.js`, que fija esos valores. Comprueba que el HTML empaquetado coincide con `www/index.html`.
2. Ejecuta `apksigner verify --verbose --print-certs <archivo.apk>` en la candidata y compara el certificado con el de la APK base. Compara también el tamaño y SHA‑256 de la descarga con los de la compilación. Conserva los datos instalados durante el diagnóstico.
3. Prueba abrir el mismo APK desde la app de Archivos del Redmi. Si vuelve a salir el aviso genérico y tienes acceso al teléfono de prueba por ADB, comprueba la versión instalada y ejecuta `adb install -r <archivo.apk>` para obtener el código exacto del instalador. Si devuelve un error de bajada de versión, revisa el `versionCode`. Si devuelve un conflicto de actualización, compara el certificado de la copia efectivamente instalada. Si devuelve un error de análisis, comprueba integridad y manifiesto. Si devuelve un error de espacio, confirma el almacenamiento libre. Una prueba de instalación limpia puede hacerse en un segundo equipo de prueba.
4. Para el resultado final, anota qué se comprobó en el navegador y qué se comprobó en Android. Incluye instalación sobre 1.3.0, partida de un solo teléfono, hotspot completo, sonido, vibración y dibujo táctil. En pantallas estrechas, repite el caso de «Deshacer» y la barra roja de Cadáver e Imitación para detectar regresiones. Actualiza `LEEME_APK.md` y el informe Wi‑Fi con la versión realmente probada, los resultados y cualquier comprobación física que siga pendiente.

Documentación: [verificación de firma con apksigner](https://developer.android.com/tools/apksigner) e [instalación con ADB](https://developer.android.com/tools/adb).
