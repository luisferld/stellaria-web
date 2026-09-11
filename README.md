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

La raíz (`/`) reenvía al idioma del navegador (inglés si no es uno de
los siete), y `/privacidad/` y `/soporte/`, las rutas de la primera
versión, reenvían al español. Cada página lleva el selector de idiomas
al pie y las etiquetas `hreflang`.

**Las páginas no se editan a mano**: los textos viven en `generar.py`,
y `./generar.py` las vuelve a escribir todas. `estilo.css` y
`solido.js` (el icosaedro a tinta de la portada) son comunes.
