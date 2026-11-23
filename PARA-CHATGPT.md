# Gartic Móvil — contexto para análisis

## Qué es
«Gartic Móvil» es un clon offline de Gartic Phone para jugar con amigos sin internet en Cuba, con multijugador por wifi local (hotspot, servidor local en puerto 7777). Paquete Android: `cu.roi.garticmovil`. Repositorio: https://github.com/Roiber16/gartic-movil

## Estado actual (23 nov 2026, 01:36 hora de Cuba)
- Versión en código: **1.4.0 (versionCode 6), sin compilar todavía**. La última APK compilada es la v2.3 (1.3.0) en `APK-v2.3/`.
- La v2.4 trae: modo Normal fiel + los 15 presets oficiales de Gartic Phone (Normal, Historia, Obra maestra, Secreto, Sándwich, Puntuación, Rompehielos, Imitación, Complementar, Pieza que falta, Cadáver exquisito, Cooperativo, Animación, Fondo, Solo) + modo Adivina (estilo Gartic.io, 75 palabras, 5 temas).
- Revisión final hecha el 23 nov: 2 fallos bloqueantes (B1 «Deshacer» cortado a 360 px, B2 barra roja tapando botones en Cadáver e Imitación) ya corregidos y verificados en 7 tamaños de pantalla (320x568 a 430x932, 0 errores, 0 desbordamientos). Modos y wifi re-verificados (12 escenarios wifi OK). La app está lista para compilar.
- Pendiente de decisión: el ícono. La C1 (lápiz dibujando sobre un móvil) sigue instalada; hay variantes D1–D5 que intentan parecerse al logo oficial de Gartic Phone (teléfono antiguo de disco), en `VERIFICACION/v2.3/iconos-nuevos/`.
- Pendiente solo en teléfono real: sonidos a oído, vibración, wifi entre dos teléfonos con hotspot real, y un problema de instalación de la v2.1 en el Redmi 10 de Roi («no se instaló la aplicación»).

## Archivos clave
- `www/index.html` — toda la app en un solo archivo autocontenido (3.500+ líneas).
- `LEEME_APK.md` — guía del proyecto: sonidos, modos, wifi, correcciones.
- `package.json`, `capacitor.config.json` — Capacitor 8.
- `android/` — proyecto Android (minSdk 24, Android 7.0+; firma fija en `keystore/`).
- `.github/workflows/build-apk.yml` — compilación en GitHub Actions (solo manual).
- `scripts/` — scripts de Python (íconos, verificación).
- `VERIFICACION/` — informes de verificación: `v2.4/revision-final/` (revisión final), `v2.4/modos/`, `v2.4/wifi/`, `v2.4/cuenta-atras/`, `v2.4/revision-general/`, `v2.3-referencias/` (fotos y audios de referencia del Gartic Phone original).
- `APK-v2.3/Gartic-Movil-1.3.0.apk` — última APK compilada.

## Excluido de esta copia en Drive
- `node_modules/` y `.git/` (regenerables).
- Los audios crudos de `VERIFICACION/v2.3-referencias/` (grabaciones de vídeos de YouTube de Vegetta, Guarnizo y AuronPlay, ~825 MB, usados solo para medir sonidos). Las mediciones ya están documentadas en los informes (`v2.4/cuenta-atras/`, `v2.3-referencias/sonidos/`).

## Reglas del dueño (Roi)
- Nada de versiones incompletas: solo se compila y envía la versión completa cuando todo esté terminado y verificado.
- La app debe copiar Gartic Phone lo más fielmente posible, pero que funcione bien en la app (compactar donde no quepa).
- Nada debe notarse que es IA (ni visual, ni sonidos, ni botones).
- Todo debe funcionar sin internet y en teléfonos Android 9 o superior, de varios tamaños de pantalla.
