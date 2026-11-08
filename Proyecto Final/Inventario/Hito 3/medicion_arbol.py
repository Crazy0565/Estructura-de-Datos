"""
Mide el árbol de búsqueda y el AVL contra las alternativas.

Compara, con n claves llegando mezcladas y llegando ordenadas:
    - construcción (n inserciones) y altura resultante,
    - n búsquedas.
Contra: arreglo propio con búsqueda binaria y lineal, y (solo como referencia
de la biblioteca estándar) `dict` y `bisect`.

Uso: python medicion_arbol.py
"""

import bisect
import random
import time

from arbol_productos import ArbolAVL, ArbolBinarioBusqueda
from arreglo import ArregloDinamico
from busqueda import busqueda_binaria, busqueda_lineal

TAMANOS = (1_000, 5_000, 10_000)
BUSQUEDAS_LINEALES = 200


def clave(x: int) -> int:
    """
    Clave de un elemento del arreglo de medición (el propio número).

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return x


def segundos(funcion) -> float:
    """
    Tiempo en segundos de ejecutar la función una vez.

    Complejidad:
        Tiempo: la de la función medida.
        Espacio: O(1).
    """
    inicio = time.perf_counter()
    funcion()
    return time.perf_counter() - inicio


def construir(tipo, claves: list[int]):
    """
    Inserta todas las claves en un árbol nuevo y lo devuelve.

    Complejidad:
        Tiempo: O(n·h).
        Espacio: O(n).
    """
    arbol = tipo()

    for c in claves:
        arbol.insertar(c, c)

    return arbol


def medir(n: int, ordenadas: bool) -> None:
    """
    Imprime una fila de la tabla para n claves, mezcladas u ordenadas.

    Complejidad:
        Tiempo: O(n²) para el árbol sin balanceo con claves ordenadas.
        Espacio: O(n).
    """
    claves = list(range(1, n + 1))

    if not ordenadas:
        random.Random(n).shuffle(claves)

    consultas = random.Random(1).sample(claves, min(n, 2_000))
    orden = "ordenadas" if ordenadas else "mezcladas"
    print(f"\n-- n = {n:,} claves {orden} --".replace(",", "."))
    print(
        f"{'estructura':<26}{'construir (s)':>14}{'altura':>8}{'2000 búsq. (ms)':>17}"
    )

    for nombre, tipo in (
        ("ArbolBinarioBusqueda", ArbolBinarioBusqueda),
        ("ArbolAVL", ArbolAVL),
    ):
        arbol = None

        def crear(tipo=tipo):
            nonlocal arbol
            arbol = construir(tipo, claves)

        t_construir = segundos(crear)
        t_buscar = segundos(lambda arbol=arbol: [arbol.buscar(c) for c in consultas])
        print(
            f"{nombre:<26}{t_construir:>14.4f}{arbol.altura():>8}{t_buscar * 1e3:>17.2f}"
        )

    arreglo = ArregloDinamico()

    for c in sorted(claves):
        arreglo.agregar(c)

    t_bin = segundos(lambda: [busqueda_binaria(arreglo, c, clave) for c in consultas])
    print(f"{'arreglo + binaria (propio)':<26}{'-':>14}{'-':>8}{t_bin * 1e3:>17.2f}")

    pocas = consultas[:BUSQUEDAS_LINEALES]
    t_lin = segundos(lambda: [busqueda_lineal(arreglo, c, clave) for c in pocas])
    t_lin = t_lin * len(consultas) / len(pocas)
    print(
        f"{'arreglo + lineal (propio)':<26}{'-':>14}{'-':>8}{t_lin * 1e3:>17.2f}  (estimado)"
    )

    diccionario = {c: c for c in claves}
    t_dict = segundos(lambda: [diccionario.get(c) for c in consultas])
    print(f"{'dict (referencia stdlib)':<26}{'-':>14}{'-':>8}{t_dict * 1e3:>17.2f}")

    lista = sorted(claves)
    t_bis = segundos(lambda: [bisect.bisect_left(lista, c) for c in consultas])
    print(f"{'bisect (referencia stdlib)':<26}{'-':>14}{'-':>8}{t_bis * 1e3:>17.2f}")


def main() -> None:
    """
    Corre las mediciones para todos los tamaños y ambos órdenes de llegada.

    Complejidad:
        Tiempo: dominado por el árbol sin balanceo con claves ordenadas.
        Espacio: O(n).
    """
    for n in TAMANOS:
        medir(n, ordenadas=False)
        medir(n, ordenadas=True)


if __name__ == "__main__":
    main()
