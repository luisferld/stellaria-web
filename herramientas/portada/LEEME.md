# Herramientas de la portada

Todo se ejecuta desde la raíz del repo. Nada de esto lo carga la web: son
utilidades para probarla y para rehacer sus medios y sus textos.

## Requisitos (una vez, en el Mac)

```sh
python3 -m pip install --user playwright pillow numpy
python3 -m playwright install chromium webkit
brew install ffmpeg            # solo para medios.py
```

Para la tarjeta de compartir hacen falta además las fuentes Inter Display
Black y Medium instaladas (las mismas que usan las herramientas de la ficha).

## `probar.py`: la portada en un navegador

```sh
python3 -m http.server 8000 &                       # o en otra terminal
python3 herramientas/portada/probar.py --motor webkit
python3 herramientas/portada/probar.py --motor chromium
```

Pasa 29 comprobaciones y deja capturas en `/tmp/pruebas-portada` (`--salida`
para otra carpeta, `--rapido` para menos anchos, `--base` para otra
dirección):

- las siete portadas a 375, 760 y 1280 px: sin desplazamiento horizontal,
  sin errores de consola, sin peticiones fallidas, y los tres bucles
  arrancan al verse;
- una partida entera en pantalla ancha con los botones y el teclado, con un
  rebote a propósito, el destello de las tiendas y «Otra vez»;
- una partida en móvil con toques: a un lado para girar, deslizar hacia
  arriba para lanzar;
- con «reducir movimiento»: la invitación propia, nada de animación sin
  jugar y el foco en «Otra vez» al terminar.

Sale con código 1 si algo falla. WebKit es el motor de Safari: es el que más
importa. El Chromium de Playwright no trae H.264, así que ahí los bucles se
ven en `.webm` (por eso cada bucle lleva los dos formatos). Nada de esto
sustituye a mirarla en Safari de verdad, en el Mac, el iPhone y el iPad.

## `medios.py`: los medios de la portada

```sh
python3 herramientas/portada/medios.py esfera|oro|libro|compartir|estrella|favicon|todo
```

| Tarea | Escribe | Sale de |
| --- | --- | --- |
| `esfera` | `media/esfera.{mp4,webm,jpg}` | `ScreenRecording_10-05-2026 10-51-47_1.MP4` en `STELLARIA_GRABACIONES` (por defecto `~/Desktop/grabaciones`) |
| `oro` | `media/oro.{mp4,webm,jpg}` | el bucle de la Galería del commit `e734f6c` |
| `libro` | `media/libro-{es,en}.webp` | `press/capturas/stellaria-iphone-6.9-{es,en}-6-book.png` |
| `compartir` | `media/compartir.jpg` | el bucle de la Galería y el nombre (Inter Display) |
| `estrella` | `media/estrella.png` | la propia portada con «reducir movimiento» |
| `favicon` | `favicon.ico`, `apple-touch-icon.png` | la marca dibujada y `press/stellaria-icon-1024.png` |

Los recortes, tiempos y calidades están explicados en el propio script y en
`docs/informe-portada-jugable.md`. Rehecho todo, los `.mp4`, `.jpg`, `.webp`
y el favicon salen idénticos byte a byte; los `.webm` cambian algún
identificador interno, no la imagen.

## `textos_desde_ficha.py`: los textos que vienen de la ficha

```sh
python3 herramientas/portada/textos_desde_ficha.py [ruta de textos.py] [--escribir]
```

`textos_portada.py` es la fuente de los textos de la portada. El concepto,
los cuerpos de las cinco secciones, el cierre y el aviso «Imagen del juego
completo» se copiaron tal cual de la ficha 1.0.5 de la App Store (por
defecto, `~/Desktop/grabaciones/ficha-1.0.5/herramientas/textos.py`). El
script comprueba que siguen iguales y que los títulos, en mayúsculas, son
los de la ficha. Con `--escribir` copia los cuerpos que hayan cambiado. No
toca los títulos ni los textos propios de la portada. Después,
`./generar.py`.
