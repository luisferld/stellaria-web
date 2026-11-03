# Informe de la sesión en la nube · La portada con el juego delante

Encargo: `docs/encargo-nube-portada.md`. Sesión del 3-11-2026, en la rama
`claude/great-dirac-4k1h86`. **Nada está en `main`**: GitHub Pages
publica `main`, y la rama no se fusiona hasta que Luis vea la portada
en su Mac.

## Qué quedó

- **La portada nueva en los siete idiomas** (`portada()` en
  `generar.py`, CSS al final de `estilo.css`). De arriba abajo:
  1. el nombre «Stellaria», el subtítulo y la marca;
  2. el vídeo en bucle (`autoplay muted loop playsinline
     preload="metadata"`, con `poster`), primero el mp4 y luego el webm;
  3. los dos botones `.boton`: «App Store · iPhone y iPad» (`TIENDA`,
     sin tocar) y «Mac App Store» (`TIENDA_MAC`, nuevo, con `ct=web` y
     `mt=12`, tal cual lo da el encargo);
  4. dos frases: la primera es el juego («Gira cada pieza con un toque,
     lánzala a su hueco y cierra la estrella antes de que se llene el
     cielo.») y la segunda lleva la estelación y la geometría;
  5. tres datos, entre filos de un píxel: «28 poliedros · 234
     estelaciones · 7 idiomas», «Gratis con cuatro poliedros, una sola
     compra para el resto · sin anuncios, sin cuentas, sin datos», «Hecho
     por una sola persona, en España»;
  6. debajo, como antes: soporte, privacidad, los idiomas y el pie
     «© 2026 Luis Fernando Lendrino Díaz».
- **Disposición.** En móvil va todo en una columna, con el vídeo a todo
  lo ancho (rompe el margen de 22 px) en 4:5 con `object-fit: cover`.
  La estrella queda entera y el vídeo no se come la pantalla: el nombre
  y el subtítulo van encima del vídeo y los dos botones justo debajo.
  Desde 760 px, dos columnas: a la izquierda el vídeo vertical entero
  (9:16, 360 px de ancho, con filo de un píxel y sin dibujar un
  teléfono) y a la derecha, centrados en vertical, el nombre, las
  frases, los botones y los datos. `main.portada` se ensancha a 980 px;
  las demás páginas siguen a 720 px.
- **Compartir.** `cabeza()` tiene un parámetro nuevo, `compartir`, que
  solo usa la portada. Mete `og:type`, `og:url`, `og:title`,
  `og:description`, `og:image` (`https://stellaria.games/media/portada.jpg`,
  720×1280), `og:video` (el mp4, con tipo y medidas) y `twitter:card`
  `summary_large_image`.
- **Sin cambios:** privacidad, soporte, kit de prensa, raíz, reenvíos y
  `hreflang`. `./generar.py` los vuelve a escribir idénticos: `git diff`
  sobre ellos sale vacío.
- `media/origen-clip-en-886x1920.mp4` se quita en el último commit
  (queda en el historial, en `af01914`).

## De qué segundos sale el bucle, y por qué

**De la Galería: la estrella terminada girando** (la estelación 6 del
icositetraedro deltoidal, en oro). Son los fotogramas **1358 a 1734**
del clip, de **22,633 s a 28,900 s**, a 60 fps.

- **Por qué la Galería y no la partida.** Miré el clip segundo a
  segundo. Del 0 al 21 s el juego está en partida, y en todos los
  fotogramas hay marcador (con «bonus ×8» en inglés), la columna de
  contadores, el panel de las piezas siguientes y los rótulos que saltan
  cada 1–2 s sobre la estrella: «+100», «MASTER ×2», «MASTER · +2
  PIECES», «BONUS +100». No hay un tramo de 8 s sin rótulo, y un recorte
  que los evitara dejaría la estrella a trozos. Del 20 al 22 s sale
  «LEVEL COMPLETE». Desde el **22,3 s** está la Galería: título en
  inglés arriba («DELTOIDAL ICOSITETRAHEDRON», «3D PRINT · STL») y, debajo,
  solo la estrella girando sobre el fondo liso del juego. El encuadre
  empieza por debajo del botón: ni barra de estado ni texto.
- **Por qué cierra sin salto.** La Galería gira a 1 rad/s, así que da
  una vuelta en 2π s = 377 fotogramas. Lo medí comparando fotogramas:
  el 1735 se diferencia del 1358 en 0,49 (media de la diferencia en
  gris), menos que el paso entre dos fotogramas seguidos (1,05). El
  bucle es esa vuelta exacta, y al volver al principio el salto es el
  de un fotograma más. En el mp4 final, la costura mide 0,92 contra
  0,72 de paso medio y 0,91 de paso máximo. En el webm, 0,79 contra
  0,72 y 0,83. Los primeros 0,3 s de la Galería son la transición de
  entrada y quedan fuera.
- **La duración.** Una vuelta dura 6,3 s, por debajo de los 8–12 s que
  pide el encargo, y dos vueltas, 12,6 s, se pasan. Por eso va **a 2/3
  de la velocidad**, con todos los fotogramas del original y nada
  inventado: 377 fotogramas a 40 fps dan **9,425 s**. La estrella gira a
  unos 38 °/s en lugar de 57 °/s. Ralentizar a otras proporciones
  obligaba a saltar fotogramas de forma desigual, y se notaría el
  traqueteo.
- **El encuadre.** El recorte es de 886×1299 del original (y de 500 a
  1799) y se completa por arriba con el mismo color del fondo del
  juego, `#ECE6D6`. El relleno se hace en RGB, así que no deja raya
  visible. Así la estrella queda centrada en 720×1280 y ocupa el 80 %
  del ancho. Comprobado en los 377 fotogramas: fuera del fondo solo hay
  píxeles entre y 357–924 y x 72–650, es decir, la estrella.

## Pesos (`ls -la media/`)

| Fichero | Formato | Peso | Límite |
| --- | --- | --- | --- |
| `media/portada.mp4` | H.264 high, 720×1280, 40 fps, 9,425 s, sin audio, `faststart` | 1 750 507 B (1,75 MB) | ≤ 3 MB |
| `media/portada.webm` | VP9 a dos pasadas, 720×1280, 40 fps, 9,425 s, sin audio | 1 700 062 B (1,70 MB) | ≤ 3 MB |
| `media/portada.jpg` | el primer fotograma, 720×1280 | 67 424 B (67 KB) | ≤ 150 KB |

El vídeo va etiquetado BT.709, con rango limitado, igual que el
original. El póster se convirtió aparte para que su color coincida con
el del vídeo (235, 229, 213) y no haya cambio de tono al empezar.

## Lo que decidí donde el encargo dejaba decidir

- **`solido.js` se va** (con su regla de CSS `canvas.solido` y la línea
  del `README.md`). Con el vídeo delante, un segundo sólido girando
  debajo competía con él, y el encargo pide que lo demás esté quieto.
  La portada no lleva ningún JavaScript, y el resto del sitio tampoco lo
  usaba. Queda en el historial.
- **El subtítulo de la portada** pasa de «Poliedros y estelaciones · un
  puzle» a **«Un puzle de poliedros»**, el nombre de la tienda en
  español; en inglés, «A polyhedra puzzle». Así lo primero que se lee
  es un juego. La raíz (`/`) mantiene su subtítulo en inglés, porque el
  encargo pide no tocar el resto. El `<title>` tampoco cambia.
- **La `meta description`** solo añade el Mac («para iPhone, iPad y
  Mac»). El **`og:description`** son las dos frases de la portada, con
  el juego primero, y el **`og:title`** es «Stellaria · Un puzle de
  poliedros».
- **El orden de las fuentes de vídeo:** mp4 primero y webm de reserva.
  Pesan casi lo mismo, el H.264 lo descodifica el hardware en todos los
  Apple y el VP9 en Safari depende de la versión. El webm queda para los
  navegadores sin H.264.
- **El dato de la compra.** En lugar de «una compra» a secas, que podría
  leerse como «se paga para bajarlo», va el texto del kit: «Gratis con
  cuatro poliedros, una sola compra para el resto». Sin precio.
- **Los textos nuevos** (las dos frases, los botones y la etiqueta del
  vídeo en los siete idiomas) los escribí a partir de los del sitio y
  del kit de prensa. Los datos son traducciones de los del kit, sin
  cifras nuevas. Los de francés, italiano, portugués, alemán y japonés
  conviene que los lea alguien que hable el idioma, como se hizo con
  los demás textos del sitio.

## Comprobaciones hechas

- `./generar.py` sin errores: «páginas: 26». Siete portadas, una por
  idioma, más privacidad, soporte, prensa, raíz y reenvíos. **Ojo:** el
  encargo habla de «las catorce portadas», pero el generador escribe
  siete (una por idioma). No encontré catorce de nada en la portada;
  quizá se contaron también las de privacidad y soporte. Lo dejo dicho.
- Una `<main>` y un `<h1>` por portada: contado en el DOM de `es`, `de`
  y `ja`.
- Además de leer el CSS, en el contenedor había **Chromium**: serví la
  web en local y la abrí con Playwright a 375×667, 760×900 y 1280×800,
  en español, alemán y japonés. En los tres anchos `scrollWidth` es
  igual a `clientWidth`, sin desbordamiento horizontal. El vídeo se
  reproduce solo (`currentSrc` es el mp4, `paused: false`). Los dos
  botones caben en una línea incluso en alemán a 375 px (48 px de alto
  cada uno).
- Bucle sin barra de estado ni rótulos: comprobado fotograma a fotograma
  (ver arriba).

## Qué mirar con los ojos en el Mac antes de publicar

1. **El bucle en Safari** (Mac, iPhone, iPad): que arranque solo, que
   la costura no se note y que el giro a 2/3 de velocidad no se vea
   lento. En iPhone con **modo de bajo consumo**, Safari no reproduce
   solo: se verá el póster quieto, como pide el encargo.
2. **El rectángulo del vídeo.** Su fondo es el del juego (`#ECE6D6`), un
   punto más oscuro que el papel de la web (`#F1ECDC`). Por eso va
   enmarcado con filos de tinta de un píxel, como una placa. Ver si
   gusta así o si se prefiere aclarar el fondo del vídeo para que case
   con el papel, aunque en cada navegador el color del vídeo sale un
   poco distinto.
3. En el fondo liso del vídeo, el H.264 deja variaciones de 1–2 niveles.
   En la captura de Chromium se intuía alguna raya muy tenue: mirarlo
   en una pantalla buena.
4. **La vista previa al compartir** (iMessage, WhatsApp, X). La imagen
   es vertical (720×1280) y `summary_large_image` espera apaisada, así
   que X recortará por el centro, donde está la estrella. Si se quiere
   una tarjeta apaisada a propósito, habría que hacer una imagen aparte.
5. Los textos nuevos en los cinco idiomas que no son español ni inglés.
6. `prefers-reduced-motion`: el vídeo se mueve aunque el sistema pida
   menos movimiento. Respetarlo sin JavaScript no se puede, y el
   encargo pide no añadirlo. Queda apuntado por si Luis lo quiere.

## Lo que no se pudo hacer

- **El push.** La sesión clonó el repositorio en modo de solo lectura (es
  público). Para subir hace falta adjuntarlo con permiso de escritura, y
  el clasificador de permisos de la sesión rechazó esa petición. Los
  commits están hechos en la rama local `claude/great-dirac-4k1h86`, y
  se deja un `git bundle` para traerlos (ver el mensaje de la sesión).
