#!/usr/bin/env python3
"""Prueba la portada en un navegador de verdad (Playwright), servida en local.

    python3 -m http.server 8000          # en otra terminal, desde la raíz del repo
    python3 herramientas/portada/probar.py [--motor chromium|webkit] [--base URL] [--salida CARPETA] [--rapido]

Comprueba, y deja capturas en la carpeta de salida:
  1. Las siete portadas a 375, 760 y 1280 px (con --rapido, solo es/de/ja a 375 y 1280):
     sin desplazamiento horizontal, sin errores de consola, sin peticiones fallidas, y los
     tres bucles arrancan al verse.
  2. Una partida entera en pantalla ancha con los botones y el teclado, con un rebote a
     propósito; el destello de las tiendas al terminar y «Otra vez».
  3. Una partida en móvil con toques: a un lado para girar, deslizar hacia arriba para lanzar.
  4. Con «reducir movimiento»: la invitación propia, nada de animación sin jugar, una
     partida con el teclado y el foco en «Otra vez» al terminar.
Sale con código 1 si algo falla. Ojo: el Chromium de Playwright no trae H.264, así que ahí
los bucles se ven en .webm (por eso cada bucle lleva los dos formatos).
"""
import argparse
import asyncio
import pathlib
import sys
import urllib.request

from playwright.async_api import async_playwright

IDIOMAS = ["es", "en", "fr", "it", "pt-br", "de", "ja"]
ESTRELLA = "document.querySelector('[data-estrella]').estrella"
GIROS = {1: ("izq", 1), 2: ("izq", 2), 3: ("der", 1)}      # k → (botón, veces) para dejar la pieza derecha

# Un toque o un deslizamiento sobre la estrella, con pointer events sintéticos.
TOQUE = """([dx, dy, lado]) => {
  const c = document.querySelector('[data-estrella] canvas'), r = c.getBoundingClientRect();
  const x = r.left + r.width * (lado < 0 ? 0.2 : lado > 0 ? 0.8 : 0.5), y = r.top + r.height * 0.7;
  const o = {bubbles: true, cancelable: true, pointerId: 7, pointerType: 'touch', isPrimary: true};
  c.dispatchEvent(new PointerEvent('pointerdown', {...o, clientX: x, clientY: y}));
  c.dispatchEvent(new PointerEvent('pointerup', {...o, clientX: x + dx, clientY: y + dy}));
}"""


class Informe:
    def __init__(self):
        self.lineas, self.fallos = [], 0

    def ok(self, cond, texto):
        self.lineas.append(("OK   " if cond else "FALLA ") + texto)
        if not cond:
            self.fallos += 1

    def nota(self, texto):
        self.lineas.append("     " + texto)


async def pieza_lista(pag, intentos=20):
    for _ in range(intentos):
        info = await pag.evaluate(ESTRELLA + ".pieza()")
        if info and info["lista"] and not info["volando"]:
            return info
        await pag.wait_for_timeout(150)
    raise RuntimeError("la pieza no llega")


async def revisar(nav, a, inf, idioma, ancho, alto):
    movil = ancho < 700
    ctx = await nav.new_context(viewport={"width": ancho, "height": alto}, device_scale_factor=1,
                                has_touch=movil, is_mobile=movil)
    pag = await ctx.new_page()
    errores, fallidas = [], []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.on("response", lambda r: fallidas.append(f"{r.status} {r.url}") if r.status >= 400 else None)
    pag.on("requestfailed", lambda r: None if r.url.endswith(".mp4") else fallidas.append("fallo " + r.url))
    await pag.goto(f"{a.base}/{idioma}/", wait_until="networkidle")
    await pag.wait_for_timeout(1200)
    sobra = await pag.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    await pag.screenshot(path=str(a.salida / f"{idioma}_{ancho}_arriba.png"))
    await pag.screenshot(path=str(a.salida / f"{idioma}_{ancho}_entera.png"), full_page=True)
    bucles = []
    for i in range(await pag.locator("video[data-bucle]").count()):
        v = pag.locator("video[data-bucle]").nth(i)
        await v.scroll_into_view_if_needed()
        await pag.wait_for_timeout(1400)
        bucles.append(await v.evaluate("v => !v.paused && v.readyState >= 2"))
    inf.ok(sobra <= 0 and not errores and not fallidas and all(bucles) and len(bucles) == 3,
           f"{idioma} a {ancho} px: sobra {sobra} px · bucles {bucles} · errores {errores or 'no'} · fallidas {fallidas or 'no'}")
    await ctx.close()


async def partida(nav, a, inf):
    ctx = await nav.new_context(viewport={"width": 1280, "height": 820}, device_scale_factor=1)
    pag = await ctx.new_page()
    errores = []
    pag.on("pageerror", lambda e: errores.append(str(e)))
    await pag.goto(f"{a.base}/es/", wait_until="networkidle")
    await pag.wait_for_timeout(600)
    estado = pag.locator("[data-estado]")
    await pag.click('[data-accion="jugar"]')
    info = await pieza_lista(pag)
    inf.ok((await estado.text_content()).startswith("Pieza 1 de 8"), "pantalla ancha: empieza la partida con «Juega aquí»")
    if info["k"] != 0:                                       # un lanzamiento torcido: rebota
        await pag.click('[data-accion="lanza"]')
        await pag.wait_for_timeout(800)
        inf.ok(await pag.evaluate(ESTRELLA + ".turno()") == 0 and "rebota" in await estado.text_content(),
               "pantalla ancha: la pieza mal orientada rebota y lo dice")
    for n in range(8):
        info = await pieza_lista(pag)
        boton, veces = GIROS.get(info["k"], (None, 0))
        for _ in range(veces):
            await pag.click(f'[data-accion="{boton}"]')
            await pag.wait_for_timeout(240)
        if n % 2:
            await pag.keyboard.press("ArrowUp")                 # con el foco en un botón de la estrella
        else:
            await pag.click('[data-accion="lanza"]')
        await pag.wait_for_timeout(900)
    await pag.wait_for_timeout(500)
    await pag.screenshot(path=str(a.salida / "partida_completa.png"))
    modo = await pag.evaluate(ESTRELLA + ".modo()")
    brilla = await pag.evaluate("document.querySelector('[data-brilla]').classList.contains('brilla')")
    inf.ok(modo == "fin" and brilla and not errores,
           f"pantalla ancha: estrella completa con botones y teclado · destello {brilla} · «{await estado.text_content()}»")
    await pag.click('[data-accion="otra"]')
    await pag.wait_for_timeout(400)
    inf.ok(await pag.evaluate(ESTRELLA + ".modo()") == "juego", "pantalla ancha: «Otra vez» vuelve a empezar")
    await ctx.close()


async def toques(nav, a, inf):
    ctx = await nav.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, has_touch=True, is_mobile=True)
    pag = await ctx.new_page()
    await pag.goto(f"{a.base}/es/", wait_until="networkidle")
    await pag.wait_for_timeout(500)
    await pag.evaluate(TOQUE, [0, 0, 0])
    await pag.wait_for_timeout(300)
    ayuda = await pag.locator("[data-estado]").text_content()
    inf.ok(await pag.evaluate(ESTRELLA + ".modo()") == "juego" and "Toca" in ayuda, "móvil: un toque empieza, con la ayuda táctil")
    for _ in range(8):
        info = await pieza_lista(pag)
        boton, veces = GIROS.get(info["k"], (None, 0))
        for _ in range(veces):
            await pag.evaluate(TOQUE, [3, 2, -1 if boton == "izq" else 1])   # un dedo nunca está quieto del todo
            await pag.wait_for_timeout(240)
        await pag.evaluate(TOQUE, [6, -80, 0])                              # deslizar hacia arriba
        await pag.wait_for_timeout(1100)
    await pag.screenshot(path=str(a.salida / "movil_completa.png"))
    tacto = await pag.evaluate("document.querySelector('[data-estrella] canvas').style.touchAction")
    inf.ok(await pag.evaluate(ESTRELLA + ".modo()") == "fin" and tacto == "",
           "móvil: estrella completa con toques y deslizando; la página vuelve a desplazarse")
    await ctx.close()


async def quieto(nav, a, inf):
    ctx = await nav.new_context(viewport={"width": 1280, "height": 820}, device_scale_factor=1, reduced_motion="reduce")
    pag = await ctx.new_page()
    await pag.add_init_script("""window.__cuadros = 0; const raf = window.requestAnimationFrame.bind(window);
      window.requestAnimationFrame = f => { window.__cuadros++; return raf(f); };""")
    await pag.goto(f"{a.base}/es/", wait_until="networkidle")
    await pag.wait_for_timeout(1500)
    c1 = await pag.evaluate("window.__cuadros")
    await pag.wait_for_timeout(1000)
    c2 = await pag.evaluate("window.__cuadros")
    texto = await pag.locator("[data-estado]").text_content()
    controles = await pag.evaluate("[...document.querySelectorAll('video[data-bucle]')].every(v => v.controls && v.paused)")
    inf.ok(c2 == c1 and "terminada" in texto and controles,
           f"reducir movimiento: quieta ({c2 - c1} cuadros en 1 s), «{texto}», bucles parados con controles")
    await pag.click('[data-accion="jugar"]')
    for _ in range(8):
        info = await pieza_lista(pag)
        boton, veces = GIROS.get(info["k"], (None, 0))
        for _ in range(veces):
            await pag.click(f'[data-accion="{boton}"]')
        await pag.focus('[data-accion="lanza"]')
        await pag.keyboard.press("Enter")
        await pag.wait_for_timeout(250)
    await pag.wait_for_timeout(500)
    foco = await pag.evaluate("document.activeElement.getAttribute('data-accion')")
    inf.ok(await pag.evaluate(ESTRELLA + ".modo()") == "fin" and foco == "otra",
           f"reducir movimiento: partida entera; el foco acaba en «Otra vez» ({foco})")
    await pag.locator("[data-estrella]").screenshot(path=str(a.salida / "quieta_completa.png"))
    await ctx.close()


async def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--motor", default="chromium", choices=["chromium", "webkit", "firefox"])
    p.add_argument("--base", default="http://127.0.0.1:8000")
    p.add_argument("--salida", default="/tmp/pruebas-portada")
    p.add_argument("--rapido", action="store_true")
    a = p.parse_args()
    a.base = a.base.rstrip("/")
    a.salida = pathlib.Path(a.salida)
    a.salida.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlopen(f"{a.base}/es/", timeout=5).read(1)
    except OSError:
        sys.exit(f"No responde {a.base}: arranca antes el servidor desde la raíz del repo "
                 f"(python3 -m http.server 8000) o pasa otra dirección con --base.")
    inf = Informe()
    async with async_playwright() as pw:
        nav = await getattr(pw, a.motor).launch()
        try:
            casos = ([(i, w) for i in ("es", "de", "ja") for w in (375, 1280)] if a.rapido else
                     [(i, w) for i in IDIOMAS for w in (375, 760, 1280)])
            for idioma, ancho in casos:
                await revisar(nav, a, inf, idioma, ancho, 820 if ancho > 700 else 812)
            for prueba in (partida, toques, quieto):
                try:
                    await prueba(nav, a, inf)
                except Exception as e:                       # una prueba rota no tapa las demás
                    inf.ok(False, f"{prueba.__name__}: {e}")
        finally:
            await nav.close()
    print(f"Portada · {a.motor} · {a.base}")
    print("\n".join(inf.lineas))
    print(f"{inf.fallos} fallos · capturas en {a.salida}")
    sys.exit(1 if inf.fallos else 0)


if __name__ == "__main__":
    asyncio.run(main())
