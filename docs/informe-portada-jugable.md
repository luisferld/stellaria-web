# La portada jugable (4-11-2026)

La portada deja de abrir con un vídeo y abre con el juego: la primera
partida de Stellaria, la estrella octángula (ocho piezas alrededor de un
octaedro), jugable en el navegador. Debajo, el juego de verdad en bucles
y capturas, con los textos ya revisados de la ficha 1.0.5.

## La estrella (`portada.js`)

- Canvas 2D, sin dependencias, unos 24 KB. Proyección ortográfica de la
  geometría de verdad: el octaedro y sus ocho huecos tetraédricos.
- **Modo solo** (al cargar): se monta sola, como un jugador tranquilo
  (espera, gira por el lado corto, lanza); al completarla se vuelve de oro,
  sube al centro, gira, estalla y vuelve a empezar.
- **Modo juego** (un toque en la estrella, «Juega aquí» o Intro): cada pieza
  llega girada y cuelga bajo su hueco, que se ve en discontinuo y teñido
  del color de la pieza. Toque a un lado = cuarto de vuelta; deslizar hacia
  arriba = lanzar. En teclado, ← → y ↑ (valen también con el foco en los
  botones). Mal orientada, rebota. Al completarla: oro, un puñado de
  cuadraditos (el bermellón de la marca y los colores de las piezas), el
  mensaje «quedan 233 más» y un destello en los dos botones de las tiendas.
- Solo se anima cuando se ve (IntersectionObserver y visibilitychange). En
  modo juego, `touch-action: none` sobre la estrella (para que deslizar no
  mueva la página); fuera de la partida, la página se desplaza normal.
- **Reducir movimiento**: la estrella entera y quieta, con su propia invitación
  («Esta es la estrella terminada; ahora móntala tú»); se puede jugar igual,
  sin transiciones, cuadraditos ni destellos, y sin animación mientras no se
  juega. Los bucles no arrancan solos: esperan con sus controles.
- Sin JavaScript: la imagen `media/estrella.png` y la consola oculta.
- Los textos de la estrella llegan en `data-textos` (JSON) desde
  `generar.py`; la ayuda cambia entre táctil y teclado según
  `(pointer: coarse)`.

## Los medios (`media/`)

| Archivo | Origen | Formato |
| --- | --- | --- |
| `esfera.mp4` / `.webm` / `.jpg` | ScreenRecording_10-05-2026 10-51-47_1.MP4, 0–2,8 s: la estelación 5 del dodecaedro pentakis (492 piezas) montándose. Recorte 1320×1320 desde y = 830, que deja fuera el rótulo en español y deja dentro la barra de piezas (120 · 120 · 120 · 120 · 12). Bucle de ida y vuelta: 0,6 s montada, se deshace (al revés) y se vuelve a montar. | 720×720, 30 fps, 6,2 s; H.264 CRF 27 (1,6 MB) y VP9 CRF 43 (1,8 MB) |
| `oro.mp4` / `.webm` / `.jpg` | El bucle de la Galería de `e734f6c` (icositetraedro deltoidal, estelación 6, de oro), recortado a cuadrado. | 640×640, 40 fps, 9,4 s sin costura (0,8 + 0,9 MB) |
| `portada.*` | La partida de siempre (estelación 11 del icosaedro con el marcador). | sin cambios |
| `libro-es.webp` / `libro-en.webp` | `press/capturas/stellaria-iphone-6.9-{es,en}-6-book.png`, sin la barra de estado. Las demás lenguas usan la inglesa, como en la App Store. | 600×1186 |
| `compartir.jpg` | La estrella de oro sobre el fondo del juego, el nombre en Inter Display Black, la marca e «IPHONE · IPAD · MAC». Sin texto en ningún idioma. | 1200×630 |
| `estrella.png` | La estrella quieta (sin JavaScript). | 560×560 |

Cada bucle lleva H.264 y VP9: los Chromium sin códecs propietarios (el de
las pruebas, algunos de Linux) solo reproducen el `.webm`.

## Los textos (`textos_portada.py`)

- Lema, concepto, las cinco secciones, el cierre, el rótulo del libro y el
  aviso «Imagen del juego completo»: **tal cual** de la ficha 1.0.5 de la
  App Store (ya revisada en sus nueve localizaciones; aquí van las de es-ES,
  en-US, fr-FR, it, pt-BR, de-DE y ja). Los títulos van en minúscula de
  frase y el CSS los pone en mayúsculas; se comprobó que, en mayúsculas,
  son exactamente los revisados.
- Nuevos: los de la estrella (invita, invita_quieta, jugar, otra, pieza,
  ayuda_toque, ayuda_teclas, no_encaja, completa, izq, der, lanza, lienzo),
  las cuatro cifras, los pies de los bucles y «Prensa». Pasaron una revisión
  aparte, en los siete idiomas.
- Los tres bucles y la captura del libro muestran poliedros del juego
  completo: todos llevan en el pie el aviso de la ficha («Imagen del juego
  completo»).
- En japonés, el lema lleva un `<wbr>` tras «ピースから» y los títulos
  `word-break: keep-all` (Safari no tiene `auto-phrase`), para que no se
  partan a media palabra.
- Sin precios escritos; los enlaces de las tiendas son los mismos
  `TIENDA` y `TIENDA_MAC` (campaña `ct=web`).

## La cabecera

- `og:image` es ahora la tarjeta de 1200×630 (antes, el póster vertical);
  `og:video` sigue siendo el bucle de la partida.
- `theme-color` (#F1ECDC) y datos estructurados `VideoGame` en JSON-LD, sin
  precio ni valoraciones.

## El favicon

`favicon.ico` (16, 32 y 48 px: la marca, el cuadrado bermellón y la barra de
tinta, sobre papel) y `apple-touch-icon.png` (180 px, el icono del juego) en
la raíz: los navegadores y el iPhone los piden solos, así que ninguna página
cambia por ellos.

## Las pruebas

`herramientas/portada/probar.py` (Playwright), con la web servida en local:
las siete portadas a 375, 760 y 1280 px sin desbordes horizontales, sin
errores de consola y con los tres bucles arrancando al verse. También una
partida entera con los botones y el teclado (con un rebote a propósito, el
destello y «Otra vez»), otra en móvil con toques y deslizando, y otra con
reducir movimiento (quieta, sin animación sin jugar, foco en «Otra vez»).
Las 29 comprobaciones pasan en Chromium. Falta WebKit y Safari de verdad: es
lo primero de `docs/encargo-code-portada.md`.

`herramientas/portada/medios.py todo` rehace todos los medios desde sus
fuentes: los `.mp4`, `.jpg`, `.webp` y el favicon salen idénticos byte a
byte. `textos_desde_ficha.py` comprueba que los textos copiados de la ficha
siguen iguales.

## Para tocarla

- Un texto: `textos_portada.py` (o `generar.py` para los de siempre), y
  `./generar.py`.
- La estrella: `portada.js` (los colores de las piezas en `COLORES`, el
  orden de montaje en `ORDEN`, cuánto cuelga la pieza en `CAIDA`).
- El aspecto: el bloque «La portada» al final de `estilo.css`.
- Un medio: `herramientas/portada/medios.py <tarea>` (su `LEEME.md` lo explica).
- Después de cualquier cambio: `./generar.py` y `herramientas/portada/probar.py`.

## Después (5-11-2026, en el Mac)

- La rama se trajo del paquete sobre `9951056`, regeneró igual y se
  sirvió en local; Luis la vio en Safari: «La web muy bien».
- Añadido bajo la estrella un pie en los siete idiomas que dice lo que
  es (una muestra de dos gestos, girar y lanzar) y dónde está el juego de
  verdad (los vídeos de abajo): duda de Luis sobre si el minijuego es
  representativo, resuelta sin pedir perdón.
- Decisiones de Luis: botones de las tiendas con texto blanco
  (4,46:1); el Mac en soporte, privacidad y prensa, con «macOS 15 o
  posterior» (la versión mínima del proyecto de Xcode), en los siete
  idiomas y en los dos del kit de prensa.
- No se pasó `probar.py` con WebKit (instalar Playwright pide bajar
  navegadores y el control de permisos de la sesión lo bloquea); la
  portada se comprobó en el navegador de la sesión (carga, sin errores de
  consola, sin desbordamiento) y en Safari por Luis.
- Publicada el 5-11-2026 fusionando `portada-jugable` en `main`.
