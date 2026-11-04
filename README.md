# stellaria.games

La web de Stellaria, el puzle de poliedros y estelaciones. Estática,
servida por GitHub Pages en `stellaria.games`, **en siete idiomas**:
una carpeta por idioma con la portada, la política de privacidad y el
soporte, con sus rutas en cada idioma.

| Idioma | Portada | Privacidad | Soporte |
| --- | --- | --- | --- |
| Español | `/es/` | `/es/privacidad/` | `/es/soporte/` |
| English | `/en/` | `/en/privacy/` | `/en/support/` |
| Français | `/fr/` | `/fr/confidentialite/` | `/fr/assistance/` |
| Italiano | `/it/` | `/it/privacy/` | `/it/assistenza/` |
| Português (Brasil) | `/pt-br/` | `/pt-br/privacidade/` | `/pt-br/suporte/` |
| Deutsch | `/de/` | `/de/datenschutz/` | `/de/support/` |
| 日本語 | `/ja/` | `/ja/privacy/` | `/ja/support/` |

Y el **kit de prensa**, solo en dos idiomas: `/press/` (inglés) y
`/es/prensa/` (español), con el icono, las 24 capturas de la tienda y
un ZIP con todo en `/press/` (unos 38 MB en el repo; los vídeos y las
fotos van por enlace externo, no aquí).

La raíz (`/`) reenvía al idioma del navegador (inglés si no es uno de
los siete), y `/privacidad/` y `/soporte/`, las rutas de la primera
versión, reenvían al español. Cada página lleva el selector de idiomas
al pie y las etiquetas `hreflang`.

**Las páginas no se editan a mano**: los textos viven en `generar.py`
(los de la portada, en `textos_portada.py`), y `./generar.py` las
vuelve a escribir todas. `estilo.css` es común.

La portada abre con **la estrella jugable**: la primera partida del
juego (la estrella octángula, ocho piezas alrededor de un octaedro),
dibujada en un canvas por `portada.js`, sin dependencias. Mientras
nadie juega, se monta sola; con un toque (o con Intro) se juega: un
toque a un lado gira la pieza, deslizar hacia arriba la lanza (en el
teclado, ← → y ↑). Debajo van cuatro cifras, cinco secciones con los
textos de la ficha 1.0.5 de la App Store, tres bucles del juego
(`media/portada.*`, una partida; `media/esfera.*`, la estelación de 492
piezas; `media/oro.*`, una estrella terminada en la Galería), la
captura del libro (`media/libro-es.webp` y `libro-en.webp`) y las dos
tiendas. Los bucles solo se cargan y se reproducen mientras se ven; con
«reducir movimiento», nada arranca solo. La tarjeta para compartir el
enlace es `media/compartir.jpg` (1200×630). Cómo se hizo todo, en
`docs/informe-portada-jugable.md`.
