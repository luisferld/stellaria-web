# Encargo para Claude Code en el Mac · Rematar y publicar la portada jugable

Es el encargo de una sesión de Claude Code abierta en la carpeta del repo
`stellaria-web`, en el Mac de Luis. Luis está delante: lo que sea suyo
decidir, se le pregunta; lo demás, se decide con `CLAUDE.md` y se apunta.

## Dónde estamos

- La rama `portada-jugable` (sobre `main` en `9951056`) trae la portada
  nueva en los siete idiomas. Abre con la primera partida del juego (la
  estrella octángula, ocho piezas), jugable en el navegador. Debajo van
  cuatro cifras, cinco secciones con los textos de la ficha 1.0.5, tres
  bucles, la captura del libro y las dos tiendas. Qué es y cómo se hizo:
  `docs/informe-portada-jugable.md`. Las reglas de la casa: `CLAUDE.md`.
- Está probada en Chromium (Linux) a 375, 760 y 1280 px, en los siete
  idiomas: 29 comprobaciones de `herramientas/portada/probar.py`, todas
  bien. También pasó una revisión independiente de los textos y de la
  accesibilidad, ya aplicada. Luis la vio en una vista previa y le gusta.
- **No se ha probado aún en Safari ni en dispositivos de verdad.** Eso es
  lo primero que queda.

## Qué hacer, en orden

1. **La rama.** Si no está en el repo, se trae del bundle. Antes, `main`
   tiene que tener `9951056`:
   ```sh
   git switch main && git pull
   git fetch ~/Desktop/grabaciones/web-portada/stellaria-web-portada-jugable.bundle portada-jugable:portada-jugable
   git switch portada-jugable
   ```
   Comprueba que regenera igual: `./generar.py` y `git status` sin
   cambios.
2. **Las pruebas automáticas.** Instala lo de
   `herramientas/portada/LEEME.md`, arranca `python3 -m http.server 8000`
   y pasa `probar.py` con `--motor webkit` (el de Safari) y con
   `--motor chromium`. Mira las capturas de `/tmp/pruebas-portada`, sobre
   todo las de japonés y las de móvil. Si WebKit falla donde Chromium no,
   eso es lo primero que se arregla.
3. **Safari de verdad, con Luis.** Sirve la web en la red local
   (`python3 -m http.server 8000 --bind 0.0.0.0`; la IP del Mac la da
   `ipconfig getifaddr en0`). Pídele que la abra en Safari en el Mac
   (`http://localhost:8000/es/`) y en el iPhone y el iPad
   (`http://<IP>:8000/es/`), y que mire:
   - la estrella: tocar, girar, lanzar deslizando sin que se mueva la
     página, el rebote, el final de oro y «Otra vez»;
   - que los tres bucles arranquen al llegar a ellos;
   - que nada se salga de lado en el iPhone, en vertical y en horizontal;
   - el japonés (`/ja/`): el lema en dos líneas, sin palabras partidas;
   - con «Reducir movimiento» (Ajustes → Accesibilidad → Movimiento): la
     estrella quieta y entera, y los bucles parados.
4. **Arreglos.** Lo que salga, siempre en la fuente (`generar.py`,
   `textos_portada.py`, `estilo.css`, `portada.js`) y después
   `./generar.py`. Haz un commit por arreglo, en la rama, y vuelve a pasar
   `probar.py`. Un texto nuevo va en los siete idiomas, con los términos de
   la tabla de `CLAUDE.md`.
5. **Dos decisiones de Luis** (pregúntaselas tal cual):
   - **Contraste de los botones de las tiendas.** El texto papel sobre
     bermellón da 3,8:1, por debajo del 4,5:1 que pide la accesibilidad
     para texto pequeño. Pasa en todo el sitio, no solo en la portada. Las
     opciones son:
     - dejarlo como está;
     - texto blanco: 4,46:1, casi llega;
     - letra de 19 px o más: no cabe en una línea en móvil;
     - un bermellón más oscuro solo en los botones: toca la marca.
   - **El Mac en soporte, privacidad y prensa.** Hoy solo dicen iPhone y
     iPad: «¿Qué necesito?» en soporte, «Quién es el responsable» en
     privacidad y «Platforms» en el kit de prensa. Hace falta la versión
     mínima de macOS, que la sabe Luis. Privacidad es un texto legal: el
     cambio exacto lo aprueba él. Va en los siete idiomas (el kit de
     prensa, en sus dos).
6. **Publicar**, solo cuando Luis lo diga: fusiona `portada-jugable` en
   `main` y empuja. GitHub Pages tarda unos minutos. Después comprueba
   que responden `https://stellaria.games/es/`, `/ja/`, `/favicon.ico`,
   `/media/compartir.jpg` y `/media/esfera.mp4`, y que la página
   publicada es la nueva (busca `data-estrella`).
7. **El informe.** Añade al final de `docs/informe-portada-jugable.md` una
   sección «Después», corta: qué se probó en los dispositivos, qué se
   arregló, qué decidió Luis y cuándo se publicó.

## Lo que no se toca

Las reglas de `CLAUDE.md`, sobre todo:

- ni precios, ni Bulatov, ni ofertas de entrevistas;
- nada de terceros;
- los enlaces de campaña de las tiendas;
- el pie;
- `main`, sin el visto bueno de Luis.
