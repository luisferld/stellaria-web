#!/usr/bin/env python3
"""Compara los textos de la portada con los de la ficha de la App Store (y, si se pide, los copia).

    python3 herramientas/portada/textos_desde_ficha.py [ruta de textos.py de la ficha] [--escribir]

La ruta por defecto es ~/Desktop/grabaciones/ficha-1.0.5/herramientas/textos.py.

textos_portada.py es la fuente de los textos de la portada. Una parte se copió tal cual de la
ficha 1.0.5 (ya revisada): el concepto, el cuerpo de las cinco secciones, el cierre y el aviso
«Imagen del juego completo». Este script comprueba que siguen iguales a los de la ficha y que los
títulos (en minúscula de frase en textos_portada.py) son, en mayúsculas, los de la ficha. Con
--escribir, copia en textos_portada.py los cuerpos que hayan cambiado en la ficha; los títulos no
los toca (si cambian, hay que pasarlos a minúscula de frase a mano) ni tampoco los textos propios
de la portada (la estrella, las cifras, los pies).
"""
import importlib.util
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
LOCAL = {"es": "es-ES", "en": "en-US", "fr": "fr-FR", "it": "it", "pt-br": "pt-BR", "de": "de-DE", "ja": "ja"}
ORDEN = ["lema", "concepto", "secciones", "cierre", "libro", "aviso", "invita", "invita_quieta", "jugar", "otra",
         "pieza", "ayuda_toque", "ayuda_teclas", "no_encaja", "completa", "izq", "der", "lanza", "lienzo", "cifras",
         "bucle", "esfera", "prensa"]
CABECERA = '''"""Los textos de la portada (generar.py), en los siete idiomas de la web.

El lema, el concepto, las cinco secciones, el cierre, el rótulo del libro y el aviso salen tal cual
de la ficha 1.0.5 de la App Store, ya revisada (los títulos, en minúscula de frase: el CSS los pone
en mayúsculas). Lo demás es de la portada: la estrella jugable, las cifras y los pies de los bucles.
En el lema, «|» marca el salto de línea.
"""

P = {}
'''


def cargar(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def como_ficha(titulo, idioma, salto=" "):
    """Un título de la portada tal como lo escribe la ficha: en mayúsculas (salvo en japonés)."""
    t = titulo.replace("<wbr>", "").replace("|", salto)
    return t if idioma == "ja" else t.upper()


def cadena(s):
    return json.dumps(s, ensure_ascii=False).replace(" ", "\\u00a0")


def escribir(P):
    lineas = [CABECERA]
    for idioma, d in P.items():
        assert set(d) == set(ORDEN), (idioma, set(d) ^ set(ORDEN))
        lineas.append(f'P["{idioma}"] = dict(')
        for k in ORDEN:
            v = d[k]
            if k == "secciones":
                lineas.append("    secciones=[")
                for t, c in v:
                    lineas += [f"        ({cadena(t)},", f"         {cadena(c)}),"]
                lineas.append("    ],")
            elif isinstance(v, list):
                lineas.append(f"    {k}=[{', '.join(cadena(x) for x in v)}],")
            else:
                lineas.append(f"    {k}={cadena(v)},")
        lineas += [")", ""]
    (RAIZ / "textos_portada.py").write_text("\n".join(lineas), encoding="utf-8")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ruta = pathlib.Path(args[0] if args else "~/Desktop/grabaciones/ficha-1.0.5/herramientas/textos.py").expanduser()
    if not ruta.exists():
        sys.exit(f"No encuentro la ficha en {ruta}: pasa la ruta de su textos.py.")
    LOCALES = cargar(ruta, "textos_ficha").LOCALES
    P = cargar(RAIZ / "textos_portada.py", "textos_portada").P
    avisos, cambios = [], 0
    for idioma, loc in LOCAL.items():
        d, f = P[idioma], LOCALES[loc]
        partes = f["descripcion"].split("\n\n")
        if len(partes) != 8:
            avisos.append(f"{idioma}: la descripción de la ficha ya no tiene 8 párrafos; revisa a mano")
            continue
        # títulos: solo se comprueban
        if como_ficha(d["lema"], idioma, "\n") != f["capturas"]["hero"][0]:
            avisos.append(f"{idioma}: el lema ya no es el de la ficha ({f['capturas']['hero'][0]!r})")
        libro_ficha = f["capturas"]["libro"][0].replace("\n", "" if idioma == "ja" else " ")
        if como_ficha(d["libro"], idioma) != libro_ficha:
            avisos.append(f"{idioma}: el rótulo del libro ya no es el de la ficha ({libro_ficha!r})")
        # cuerpos: se comprueban y, con --escribir, se copian
        nuevas = []
        for (titulo, cuerpo), parte in zip(d["secciones"], partes[2:7]):
            cab, cuerpo_ficha = parte.split("\n", 1)
            if como_ficha(titulo, idioma) != cab:
                avisos.append(f"{idioma}: el título «{titulo}» ya no es el de la ficha ({cab!r})")
            if cuerpo != cuerpo_ficha:
                avisos.append(f"{idioma}: cambió el cuerpo de «{titulo}»")
                cambios += 1
            nuevas.append((titulo, cuerpo_ficha))
        d["secciones"] = nuevas
        for clave, valor in (("concepto", partes[1]), ("cierre", partes[7]), ("aviso", f["aviso_imagen"])):
            if d[clave] != valor:
                avisos.append(f"{idioma}: cambió «{clave}»")
                cambios += 1
                d[clave] = valor
    print("\n".join(avisos) if avisos else "Los textos de la portada coinciden con los de la ficha.")
    if "--escribir" in sys.argv and cambios:
        escribir(P)
        print(f"{cambios} textos copiados en textos_portada.py. Ahora: ./generar.py")
    elif cambios:
        print("Para copiarlos: el mismo comando con --escribir.")


if __name__ == "__main__":
    main()
