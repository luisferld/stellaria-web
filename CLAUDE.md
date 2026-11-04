# stellaria.games

La web de Stellaria, un puzle de poliedros y estelaciones para iPhone, iPad y
Mac, hecho por una sola persona (Luis Fernando Lendrino Díaz, en España).
Es estática: GitHub Pages publica la rama `main` en `stellaria.games`. Está
en siete idiomas (`es`, `en`, `fr`, `it`, `pt-br`, `de`, `ja`). Todo se
escribe en español, salvo los textos del sitio, que van en su idioma.

## Cómo está hecha

- **Las páginas HTML no se editan a mano.** Las escribe `./generar.py` con
  los textos de `generar.py` (`T`, por idioma; `PRENSA`, el kit de prensa) y
  de `textos_portada.py` (la portada). Después de cualquier cambio, se
  ejecuta `./generar.py` y se suben juntas la fuente y las páginas.
- `estilo.css` es común a todo el sitio; el bloque de la portada va al
  final.
- `portada.js` lleva la estrella jugable de la portada (un canvas sin
  dependencias) y los bucles que solo se cargan al verse.
- `media/` guarda los bucles, los pósteres, las capturas y la tarjeta para
  compartir. Se rehacen con `herramientas/portada/medios.py`.
- Para verla en local hace falta un servidor, porque las rutas son
  absolutas: `python3 -m http.server 8000` y abrir
  `http://localhost:8000/es/`.
- Las pruebas están en `herramientas/portada/` (su `LEEME.md` explica cómo
  instalarlas): `python3 herramientas/portada/probar.py --motor webkit`.

## Publicar

Se trabaja siempre en una rama. **Nada pasa a `main` ni se empuja sin que
Luis lo diga**: él mira antes los cambios en su Mac y sus dispositivos. Los
commits van en español, y explican qué cambia y por qué.

## La casa (no se cambia)

- Colores: papel `#F1ECDC`, hoja `#F6F2E6`, tinta `#211F1C`, tinta suave
  `#6B665C` y el bermellón `#D54529`, el único color vivo.
- Se usa la tipografía del sistema (`-apple-system`…). Los títulos van en
  mayúsculas, con aire y en peso 900.
- Esquinas vivas, filos de un píxel y la marca: el cuadrado bermellón y la
  barra de tinta a −30°.
- Nada de degradados, sombras, tipografías nuevas ni iconos.
- Sin dependencias, sin analítica, sin fuentes externas y sin CDN.

## Lo que no se hace ni se dice

- Ninguna referencia a Vladimir Bulatov ni al applet original (eso va en la
  parte legal, dentro de la app).
- Ninguna oferta de entrevistas ni de charlas.
- Ningún precio escrito, porque cambia por país. La única excepción es el kit
  de prensa, que da el de España.
- Ningún script de analítica ni de terceros.
- Los enlaces de las tiendas (`TIENDA`, `TIENDA_MAC` y `TIENDA_PRENSA` en
  `generar.py`) llevan la campaña (`pt`, `ct`) y no se tocan.
- El pie «© 2026 Luis Fernando Lendrino Díaz» se queda tal cual.

## Datos del juego (no inventar otros)

- 28 poliedros y 234 estelaciones, calculadas en el dispositivo.
- Gratis, sin límite de tiempo, con 4 poliedros (10 estelaciones). Una sola
  compra, «El juego completo», abre los otros 24.
- El premio final son los 59 icosaedros, contados en 1938 por Coxeter, Du
  Val, Flather y Petrie; se ganan completando todas las demás.
- Exporta a STL. Sin anuncios, sin cuentas y sin recogida de datos. Game
  Center es opcional y funciona sin conexión.
- Salió en la App Store (iPhone y iPad) el 21-9-2026 y en la Mac App Store
  el 2-11-2026.
- Los poliedros que enseñan los bucles y las capturas son del juego
  completo. Por eso llevan el aviso «Imagen del juego completo».

## Textos en siete idiomas

- Un texto nuevo va en los siete idiomas, con los términos de los textos que
  ya hay:

  | Idioma | pieza | hueco | girar | lanzar | partida | trato |
  | --- | --- | --- | --- | --- | --- | --- |
  | es | pieza | hueco | girar | lanzar | partida | tú |
  | en | piece | slot | turn | launch | round | — |
  | fr | pièce | emplacement | pivoter | lancer | partie | vous |
  | it | pezzo | incastro | ruotare | lanciare | partita | tu |
  | pt-br | peça | encaixe | girar | lançar | partida | você |
  | de | Teil | Lücke | drehen | werfen | Runde | du |
  | ja | ピース | 場所 | 回す | 発射 | ゲーム | — |

- En francés va un espacio no separable (U+00A0) antes de `;`, `:`, `!` y `?`.
  Los apóstrofos son curvos (’).
- Si cambia la ficha de la App Store, `herramientas/portada/textos_desde_ficha.py`
  comprueba qué textos de la portada hay que copiar de nuevo.

## Documentos

- `docs/informe-portada-jugable.md`: cómo se hizo la portada actual.
- `docs/encargo-code-portada.md`: lo que queda por hacer.
- `docs/encargo-nube-portada.md` y `docs/informe-nube-portada.md`: la
  portada anterior, la del vídeo.
