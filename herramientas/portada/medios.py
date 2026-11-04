#!/usr/bin/env python3
"""Rehace los medios de la portada desde sus fuentes, en media/ (y el favicon en la raíz).

    python3 herramientas/portada/medios.py esfera|oro|libro|compartir|estrella|favicon|todo

  esfera     media/esfera.{mp4,webm,jpg}: de «ScreenRecording_10-05-2026 10-51-47_1.MP4», en
             STELLARIA_GRABACIONES (por defecto ~/Desktop/grabaciones), 0–2,8 s: la estelación 5 del
             dodecaedro pentakis (492 piezas) montándose. Recorte cuadrado sin el rótulo en español
             y con la barra de piezas; quieta 0,6 s, se deshace (al revés) y se vuelve a montar.
  oro        media/oro.{mp4,webm,jpg}: el bucle de la Galería del commit e734f6c (icositetraedro
             deltoidal, estelación 6), recortado a cuadrado. 9,4 s sin costura.
  libro      media/libro-{es,en}.webp: press/capturas/stellaria-iphone-6.9-{es,en}-6-book.png
             sin la barra de estado.
  compartir  media/compartir.jpg (1200×630): la estrella de oro, el nombre y la marca. Necesita las
             fuentes Inter Display Black y Medium instaladas.
  estrella   media/estrella.png: la estrella quieta, sacada de la propia portada con «reducir
             movimiento» (arranca un servidor local un momento). Para quien no tenga JavaScript.
  favicon    favicon.ico (la marca sobre papel) y apple-touch-icon.png (el icono del juego).

Necesita ffmpeg con libx264 y libvpx-vp9 (brew install ffmpeg), Pillow y Playwright con Chromium.
"""
import asyncio
import functools
import http.server
import math
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import threading

RAIZ = pathlib.Path(__file__).resolve().parents[2]
MEDIA = RAIZ / "media"
GRABACIONES = pathlib.Path(os.environ.get("STELLARIA_GRABACIONES", "~/Desktop/grabaciones")).expanduser()
FUENTE_ESFERA = "ScreenRecording_10-05-2026 10-51-47_1.MP4"
COMMIT_ORO = "e734f6c"                       # el commit con el bucle de la Galería
FONDO_JUEGO = (235, 229, 213)                 # el fondo de la Galería, para la tarjeta


def ff(*args):
    if not shutil.which("ffmpeg"):
        sys.exit("Falta ffmpeg (brew install ffmpeg).")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, args)], check=True)


def h264(crf):
    return ["-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", str(crf),
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]


def vp9(entrada, salida, crf):
    ff("-i", entrada, "-an", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", crf, "-row-mt", "1",
       "-deadline", "good", "-cpu-used", "2", "-pix_fmt", "yuv420p", salida)


def poster(video, jpg):
    ff("-i", video, "-frames:v", "1", "-q:v", "4", jpg)


def bucle_galeria(destino):
    """El bucle de la Galería tal como estaba en el commit e734f6c (720×1280, 40 fps)."""
    datos = subprocess.run(["git", "-C", RAIZ, "show", f"{COMMIT_ORO}:media/portada.mp4"],
                           check=True, capture_output=True).stdout
    destino.write_bytes(datos)
    return destino


def esfera():
    fuente = GRABACIONES / FUENTE_ESFERA
    if not fuente.exists():
        sys.exit(f"Falta {fuente}: indica su carpeta con STELLARIA_GRABACIONES.")
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        ff("-ss", "0", "-t", "2.8", "-i", fuente, "-an", "-vf",
           "crop=1320:1320:0:830,scale=720:720:flags=lanczos,fps=30", "-c:v", "ffv1", d / "ida.mkv")
        ff("-i", d / "ida.mkv", "-vf", "reverse,tpad=start_mode=clone:start_duration=0.6", "-c:v", "ffv1", d / "vuelta.mkv")
        ff("-i", d / "ida.mkv", "-vf", "trim=start_frame=1,setpts=PTS-STARTPTS", "-c:v", "ffv1", d / "ida1.mkv")
        ff("-i", d / "vuelta.mkv", "-i", d / "ida1.mkv", "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
           "-map", "[v]", *h264(27), MEDIA / "esfera.mp4")
    vp9(MEDIA / "esfera.mp4", MEDIA / "esfera.webm", 43)
    poster(MEDIA / "esfera.mp4", MEDIA / "esfera.jpg")


def oro():
    with tempfile.TemporaryDirectory() as d:
        galeria = bucle_galeria(pathlib.Path(d) / "galeria.mp4")
        ff("-i", galeria, "-an", "-vf", "crop=680:680:20:300,scale=640:640:flags=lanczos", *h264(26), MEDIA / "oro.mp4")
    vp9(MEDIA / "oro.mp4", MEDIA / "oro.webm", 42)
    poster(MEDIA / "oro.mp4", MEDIA / "oro.jpg")


def libro():
    from PIL import Image
    for l in ("es", "en"):
        im = Image.open(RAIZ / f"press/capturas/stellaria-iphone-6.9-{l}-6-book.png").convert("RGB")
        im = im.crop((0, 150, 1320, 2760)).resize((600, round(2610 * 600 / 1320)), Image.LANCZOS)
        im.save(MEDIA / f"libro-{l}.webp", quality=82, method=6)


TARJETA = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1200px;height:630px;background:transparent;overflow:hidden}
.t{position:absolute;left:640px;top:200px;font-family:"Inter Display";color:#211F1C}
h1{margin:0;font-weight:900;font-size:84px;letter-spacing:.06em;line-height:1}
.m{position:relative;width:120px;height:62px;margin:34px 0 0 4px}
.m:before{content:"";position:absolute;left:0;top:0;width:30px;height:30px;background:#D54529}
.m:after{content:"";position:absolute;left:15px;top:38px;width:86px;height:6px;background:#211F1C;transform:rotate(-30deg);transform-origin:left center}
p{margin:22px 0 0 2px;font-weight:500;font-size:25px;letter-spacing:.16em;color:#6B665C}
</style></head><body><div class="t"><h1>STELLARIA</h1><div class="m"></div><p>IPHONE · IPAD · MAC</p></div></body></html>"""


def compartir():
    from PIL import Image
    from playwright.async_api import async_playwright

    async def texto(html, png):
        async with async_playwright() as p:
            nav = await p.chromium.launch()
            pag = await nav.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            await pag.set_content(html)
            await pag.wait_for_timeout(300)
            if not await pag.evaluate("document.fonts.check('900 84px \"Inter Display\"')"):
                sys.exit("Falta la fuente Inter Display (Black y Medium) para la tarjeta.")
            await pag.screenshot(path=str(png), omit_background=True)
            await nav.close()

    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        ff("-ss", "0", "-i", bucle_galeria(d / "galeria.mp4"), "-frames:v", "1", "-vf", "crop=620:620:50:330", d / "estrella.png")
        asyncio.run(texto(TARJETA, d / "texto.png"))
        carta = Image.new("RGB", (1200, 630), FONDO_JUEGO)          # el mismo fondo que el fotograma: sin costura
        carta.paste(Image.open(d / "estrella.png").convert("RGB"), (12, 5))
        carta = Image.alpha_composite(carta.convert("RGBA"), Image.open(d / "texto.png").convert("RGBA")).convert("RGB")
        carta.save(MEDIA / "compartir.jpg", quality=86, optimize=True, progressive=True)


def estrella():
    from PIL import Image
    from playwright.async_api import async_playwright

    class Callado(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    manejador = functools.partial(Callado, directory=str(RAIZ))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()

    async def captura(png):
        async with async_playwright() as p:
            nav = await p.chromium.launch()
            ctx = await nav.new_context(viewport={"width": 560, "height": 900}, device_scale_factor=1, reduced_motion="reduce")
            pag = await ctx.new_page()
            await pag.goto(f"http://127.0.0.1:{servidor.server_address[1]}/es/", wait_until="networkidle")
            await pag.wait_for_timeout(600)
            await pag.locator("[data-estrella] canvas").screenshot(path=str(png))   # a 560 px de ancho, la estrella ocupa todo: 560×560
            await nav.close()

    try:
        with tempfile.TemporaryDirectory() as d:
            png = pathlib.Path(d) / "estrella.png"
            asyncio.run(captura(png))
            im = Image.open(png).convert("RGB")
            lado = min(im.size)                                   # a veces sale un píxel de más por redondeo
            im.crop((0, 0, lado, lado)).quantize(colors=96, method=Image.FASTOCTREE).save(MEDIA / "estrella.png", optimize=True)
    finally:
        servidor.shutdown()


def favicon():
    from PIL import Image, ImageDraw
    n = 512
    im = Image.new("RGB", (n, n), (241, 236, 220))              # papel
    d = ImageDraw.Draw(im)
    d.rectangle((64, 96, 232, 264), fill=(213, 69, 41))         # el cuadrado bermellón
    x, y, largo, grueso, ang = 130, 330, 400, 52, math.radians(30)
    ux, uy = math.cos(ang), -math.sin(ang)                      # la barra de tinta, a −30°
    nx, ny = -uy * grueso / 2, ux * grueso / 2
    d.polygon([(x + nx, y + ny), (x + ux * largo + nx, y + uy * largo + ny),
               (x + ux * largo - nx, y + uy * largo - ny), (x - nx, y - ny)], fill=(33, 31, 28))
    im.save(RAIZ / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    Image.open(RAIZ / "press/stellaria-icon-1024.png").convert("RGB").resize((180, 180), Image.LANCZOS).save(
        RAIZ / "apple-touch-icon.png", optimize=True)


TAREAS = {"esfera": esfera, "oro": oro, "libro": libro, "compartir": compartir, "estrella": estrella, "favicon": favicon}

if __name__ == "__main__":
    pedidas = sys.argv[1:] or ["--help"]
    if pedidas[0] in ("-h", "--help") or any(t not in TAREAS and t != "todo" for t in pedidas):
        sys.exit(__doc__)
    for t in (list(TAREAS) if "todo" in pedidas else pedidas):
        print("·", t)
        TAREAS[t]()
    print("Hecho. Si cambió algo que se ve en la portada, pasa herramientas/portada/probar.py.")
