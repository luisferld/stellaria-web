# Encargo para la sesión autónoma en la nube · La portada con el juego delante

Este texto es el encargo entero de una sesión de Claude Code en la nube
sobre el repositorio `luisferld/stellaria-web`. La sesión trabaja sola,
sin nadie que responda preguntas: donde haya una duda, decide con las
reglas de abajo, lo apunta y sigue. Se pega tal cual como primer mensaje.
Presupuesto ajustado (unos 90 $ de crédito para todo lo que quede): se
hace lo que se dice, se comprueba, se escribe el informe y se para.

---

Lee `README.md` y `generar.py` antes de nada: las páginas **no se
editan a mano**, viven en `generar.py` y `./generar.py` las escribe
todas (siete idiomas, privacidad, soporte y el kit de prensa). El sitio
es estático, lo sirve GitHub Pages en `stellaria.games`, sin
dependencias, sin analítica, sin fuentes externas, sin CDN.

**El problema.** Stellaria es un juego que se entiende en tres segundos
viéndolo y en ningún tiempo leyéndolo. La portada de hoy es texto, un
icosaedro a tinta y un enlace. De 52 correos a prensa y creadores con
el juego explicado, contestaron dos y canjearon un código: nadie llegó
a ver el juego. Desde el 2-11-2026 está también en la Mac App Store.

**La tarea:** rehacer la portada (`portada()` en `generar.py`, con su
CSS en `estilo.css`) para que **lo primero que se vea sea el juego en
movimiento**, y debajo, poco texto y los dos botones de las tiendas. En
los siete idiomas. El resto del sitio (privacidad, soporte, kit de
prensa, reenvíos, `hreflang`) se queda como está.

**La portada nueva, arriba a abajo:**

1. **El vídeo.** `media/origen-clip-en-886x1920.mp4` es un clip de
   29 s del juego (vertical, 886×1920, el de la vista previa de la App
   Store; lleva algún rótulo en inglés: elige los tramos sin rótulo).
   Con `ffmpeg` (instálalo: `apt-get install ffmpeg`) corta un **bucle
   de 8 a 12 s** que empiece con el juego ya en acción —piezas volando y
   encajando, o la estrella terminada girando— y vuelva a su principio
   sin salto visible. Salida: `media/portada.mp4` (H.264, 720×1280, sin
   pista de audio, ≤ 3 MB) y `media/portada.webm` (VP9, ≤ 3 MB), más un
   fotograma de portada `media/portada.jpg` (720×1280, ≤ 150 KB). El
   `<video>` va `autoplay muted loop playsinline preload="metadata"`
   con el `poster`; si el navegador no reproduce, se ve el póster. Quita
   `media/origen-clip-en-886x1920.mp4` del repo en el último commit (es
   solo materia prima; en el historial se queda).
2. **La disposición.** En móvil, el vídeo ocupa el ancho entero, con el
   nombre «Stellaria», el subtítulo y los dos botones encima del vídeo o
   justo debajo, lo que mejor se lea. En pantalla ancha, dos columnas
   sobre el papel: el vídeo vertical a un lado (como un teléfono, sin
   dibujar un teléfono) y, al otro, el nombre, una frase, los dos
   botones y tres datos. Nada de carruseles, ni animaciones de entrada,
   ni JavaScript nuevo salvo lo imprescindible (el `solido.js` de hoy
   puede quedarse debajo o irse: decide por lo que se vea mejor y dilo).
3. **Los dos botones**, en el estilo de la casa (la clase `.boton`):
   «App Store · iPhone y iPad» con el enlace `TIENDA` que ya existe, y
   «Mac App Store» con
   `https://apps.apple.com/app/apple-store/id6819857964?pt=129444067&ct=web&mt=12`
   (nuevo: añádelo como `TIENDA_MAC` junto a `TIENDA`). Sin insignias
   oficiales de Apple (no se pueden descargar desde la sesión).
4. **Una frase y tres datos**, por idioma, con lo que ya dice el sitio
   (reusa los textos de `T` y del kit de prensa; no inventes cifras):
   28 poliedros, 234 estelaciones, 7 idiomas; una compra, sin anuncios,
   sin cuentas, sin datos; un solo desarrollador. Primero es un juego:
   «estelación» y «geometría» van en la segunda frase, nunca en la
   primera.
5. **Compartir.** En `cabeza()`, para la portada: `og:title`,
   `og:description`, `og:image` (`media/portada.jpg`, con URL absoluta
   `https://stellaria.games/…`) y `og:video` con el mp4; y
   `twitter:card` `summary_large_image`.
6. **Debajo**, como hasta ahora: soporte, privacidad, los idiomas, el
   pie «© 2026 Luis Fernando Lendrino Díaz» tal cual.

**La casa (no se cambia):** papel `#F1ECDC`, hoja `#F6F2E6`, tinta
`#211F1C`, bermellón `#D54529` como único color vivo; mayúsculas con
aire en los títulos, esquinas vivas, filos de un píxel, la marca (el
cuadrado rojo y la barra) donde está. Nada de degradados, sombras,
tipografías nuevas ni iconos. El vídeo es lo espectacular; lo demás,
quieto.

**Lo que no se hace ni se dice:** ninguna referencia a Vladimir Bulatov
ni al applet original (es de la parte legal, dentro de la app);
ninguna oferta de entrevistas ni charlas; ningún precio escrito (cambia
por país); ningún script de analítica ni de terceros; no se tocan los
enlaces de campaña (`pt`, `ct`) salvo para añadir el del Mac.

**Comprobar:** `./generar.py` sin errores y las catorce portadas
escritas; HTML válido a ojo (una `<main>`, un `<h1>`); los tres
ficheros de `media/` con los tamaños pedidos (`ls -la`); que el bucle
no muestre barra de estado ni rótulos; que la página en móvil (375 px)
no desborde en horizontal (lee el CSS con cuidado: no hay navegador).

**El informe**, `docs/informe-nube-portada.md`: qué quedó, de qué
segundos del clip sale el bucle y por qué, pesos de los ficheros, qué
se decidió donde el encargo dejaba decidir, y qué conviene mirar con los
ojos en el Mac antes de publicar (GitHub Pages publica `main`: la rama
no se fusiona hasta que Luis la vea).

**Idioma:** todo en español salvo los textos del sitio, que van en su
idioma.

**Push:** a la rama de la sesión (el entorno no deja empujar a `main`);
`main` lo fusiona Luis después de ver la portada en su Mac.
