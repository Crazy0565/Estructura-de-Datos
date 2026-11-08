"""
Mide las estructuras propias contra la biblioteca estándar y genera las
gráficas del informe directamente desde los datos medidos (sin copiar números).

Uso: python -m mediciones.benchmark   (escribe PNG en docs/entrega2/graficas/)
La biblioteca estándar (list, deque) se usa aquí solo como referencia.
"""

import time
from collections import deque
from collections.abc import Callable
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from inventario.estructuras.arreglo import ArregloDinamico
from inventario.estructuras.cola_circular import ColaCircular
from inventario.estructuras.cola_enlazada import ColaEnlazada
from mediciones.lotes import construir_lista

CARPETA = Path(__file__).resolve().parents[1] / "docs" / "entrega2" / "graficas"
TAMANOS = [1000, 5000, 10000, 50000, 100000]


def promedio(funcion: Callable[[], Any], repeticiones: int) -> float:
    """
    Tiempo medio en segundos de ejecutar la función.

    Complejidad:
        Tiempo: O(r) ejecuciones de la función.
        Espacio: O(1).
    """
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    return (time.perf_counter() - inicio) / repeticiones


def medir_frente() -> dict[str, list[float]]:
    """
    Tiempo (µs) de quitar el primer elemento según estructura y tamaño.

    Complejidad:
        Tiempo: O(n) por tamaño, por construir cada estructura.
        Espacio: O(n).
    """
    res = {
        "ListaLotes": [],
        "ArregloDinamico": [],
        "list.pop(0)": [],
        "deque.popleft()": [],
    }
    for n in TAMANOS:
        lista = construir_lista(n)
        res["ListaLotes"].append(promedio(lambda: lista.despachar(1), 200) * 1e6)

        arreglo = ArregloDinamico(n)
        for i in range(n):
            arreglo.agregar(i)
        res["ArregloDinamico"].append(promedio(lambda: arreglo.eliminar(0), 20) * 1e6)

        nativa = list(range(n))
        res["list.pop(0)"].append(promedio(lambda: nativa.pop(0), 200) * 1e6)

        d = deque(range(n))
        res["deque.popleft()"].append(promedio(lambda: d.popleft(), 200) * 1e6)
    return res


def ciclo(estructura: Any, n: int, meter: str, sacar: str) -> None:
    """
    n inserciones seguidas de n extracciones.

    Complejidad:
        Tiempo: O(n) si cada operación es O(1).
        Espacio: O(n).
    """
    entrar, salir = getattr(estructura, meter), getattr(estructura, sacar)
    for i in range(n):
        entrar(i)
    for _ in range(n):
        salir()


def medir_colas() -> dict[str, list[float]]:
    """
    Tiempo (s) de n encolar + n desencolar según estructura.

    Complejidad:
        Tiempo: O(n) por tamaño medido (salvo list.pop(0), O(n²)).
        Espacio: O(n).
    """
    res = {"ColaEnlazada": [], "ColaCircular": [], "deque": [], "list.pop(0)": []}
    for n in TAMANOS:
        res["ColaEnlazada"].append(
            promedio(lambda: ciclo(ColaEnlazada(), n, "encolar", "desencolar"), 1)
        )
        res["ColaCircular"].append(
            promedio(lambda: ciclo(ColaCircular(n), n, "encolar", "desencolar"), 1)
        )
        res["deque"].append(promedio(lambda: ciclo(deque(), n, "append", "popleft"), 1))

        def con_lista() -> None:
            datos: list[int] = []
            for i in range(n):
                datos.append(i)
            for _ in range(n):
                datos.pop(0)

        res["list.pop(0)"].append(promedio(con_lista, 1))
    return res


def medir_fusion() -> dict[str, list[float | None]]:
    """
    Tiempo (ms) de fusión recursiva vs iterativa; None si hay RecursionError.

    Complejidad:
        Tiempo: O(total) por tamaño medido.
        Espacio: O(total).
    """
    res: dict[str, list[float | None]] = {"recursiva": [], "iterativa": []}
    for total in [100, 400, 900, 1400, 5000, 50000]:
        for nombre, clave in (
            ("fusionar_recursivo", "recursiva"),
            ("fusionar_iterativo", "iterativa"),
        ):
            a = construir_lista(total // 2, 2, 0, "a")
            b = construir_lista(total - total // 2, 2, 1, "b")
            inicio = time.perf_counter()
            try:
                getattr(a, nombre)(b)
                res[clave].append((time.perf_counter() - inicio) * 1e3)
            except RecursionError:
                res[clave].append(None)
    return res


def graficar(
    datos: dict[str, list[float | None]],
    xs: list[int],
    titulo: str,
    ylabel: str,
    archivo: str,
    log: bool = True,
) -> None:
    """
    Guarda una gráfica de líneas en la carpeta de salida.

    Complejidad:
        Tiempo: O(k·m) para k series de m puntos.
        Espacio: O(k·m).
    """
    plt.figure(figsize=(7, 4.2))
    for nombre, ys in datos.items():
        puntos = [(x, y) for x, y in zip(xs, ys, strict=True) if y is not None]
        plt.plot(
            [p[0] for p in puntos], [p[1] for p in puntos], marker="o", label=nombre
        )
    plt.xscale("log")
    if log:
        plt.yscale("log")
    plt.title(titulo)
    plt.xlabel("n")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(CARPETA / archivo, dpi=150)
    plt.close()


def main() -> None:
    """
    Ejecuta las mediciones y escribe las tres gráficas.

    Complejidad:
        Tiempo: dominado por list.pop(0) con n = 100.000.
        Espacio: O(n).
    """
    CARPETA.mkdir(parents=True, exist_ok=True)
    graficar(
        medir_frente(),
        TAMANOS,
        "Quitar el primer elemento",
        "µs por operación",
        "frente.png",
    )
    graficar(
        medir_colas(),
        TAMANOS,
        "Cola: n encolar + n desencolar",
        "segundos",
        "colas.png",
    )
    f = medir_fusion()
    graficar(
        f,
        [100, 400, 900, 1400, 5000, 50000],
        "Fusión de lotes (None = RecursionError)",
        "ms",
        "fusion.png",
    )
    print(f"Gráficas en {CARPETA}")


if __name__ == "__main__":
    main()
