"""
Mediciones de la Fase 3: grafo del plano de la bodega y cola de prioridad.

1. Memoria: lista de adyacencia frente a matriz de adyacencia (tracemalloc).
2. Tiempo: Dijkstra con cada representación y con el plano completo.
3. Cola de prioridad propia frente a `heapq` (referencia de la biblioteca
   estándar) y frente a buscar el mínimo recorriendo una lista.

Uso: python -m mediciones.grafo
"""

import heapq
import random
import time
import tracemalloc
from collections.abc import Callable
from typing import Any

from inventario.estructuras.cola_prioridad import ColaPrioridad
from inventario.grafos.algoritmos_grafo import dijkstra
from inventario.grafos.grafo_bodega import GrafoListaAdyacencia, GrafoMatrizAdyacencia
from inventario.grafos.plano_bodega import MUELLE, PlanoBodega

LADOS_MEMORIA = (5, 10, 20, 30, 40, 50)
BYTES_POR_CELDA = 8


def segundos(funcion: Callable[[], Any]) -> float:
    """
    Tiempo en segundos de ejecutar la función una vez.

    Complejidad:
        Tiempo: la de la función medida.
        Espacio: O(1).
    """
    inicio = time.perf_counter()
    funcion()
    return time.perf_counter() - inicio


def bytes_de(lado: int, fabrica: type) -> int:
    """
    Memoria (bytes) que ocupa el plano de un lado dado con una representación.

    Complejidad:
        Tiempo: O(lado²) (O(lado⁴) con matriz).
        Espacio: la del grafo medido.
    """
    tracemalloc.start()
    antes = tracemalloc.get_traced_memory()[0]
    plano = PlanoBodega(lado, fabrica)
    despues = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    del plano

    return despues - antes


def medir_memoria() -> None:
    """
    Imprime la memoria de ambas representaciones y la proyección al plano
    de 100 x 100 (10.001 nodos) de la guía.

    Complejidad:
        Tiempo: dominado por construir la matriz más grande medida.
        Espacio: O(V²) transitorio.
    """
    print("== 1. Memoria del plano: lista frente a matriz de adyacencia ==")
    print(
        f"{'lado':>5}{'nodos':>8}{'aristas':>9}{'lista (KB)':>13}{'matriz (KB)':>14}{'matriz/lista':>14}"
    )
    ultimo = None

    for lado in LADOS_MEMORIA:
        nodos = lado * lado + 1
        aristas = PlanoBodega(lado).grafo.numero_aristas
        lista = bytes_de(lado, GrafoListaAdyacencia)
        matriz = bytes_de(lado, GrafoMatrizAdyacencia)
        ultimo = (nodos, matriz)
        print(
            f"{lado:>5}{nodos:>8}{aristas:>9}{lista / 1024:>13.0f}{matriz / 1024:>14.0f}{matriz / lista:>14.1f}"
        )

    lista_100 = bytes_de(100, GrafoListaAdyacencia)
    nodos_100 = 100 * 100 + 1
    matriz_100 = ultimo[1] * (nodos_100 / ultimo[0]) ** 2
    teorica = nodos_100**2 * BYTES_POR_CELDA
    print(f"\nPlano 100 x 100 ({nodos_100:,} nodos):".replace(",", "."))
    print(f"  lista de adyacencia (medida):     {lista_100 / 1024 / 1024:8.1f} MB")
    print(
        f"  matriz de adyacencia (proyectada): {matriz_100 / 1024 / 1024:8.0f} MB  (mínimo teórico {teorica / 1024 / 1024:.0f} MB)"
    )


def medir_dijkstra() -> None:
    """
    Compara Dijkstra con cada representación y sobre el plano completo.

    Complejidad:
        Tiempo: dominado por Dijkstra sobre la matriz más grande.
        Espacio: O(V²) transitorio.
    """
    print("\n== 2. Dijkstra desde el muelle ==")
    print(f"{'lado':>5}{'nodos':>8}{'lista (ms)':>13}{'matriz (ms)':>14}")

    for lado in (10, 20, 30):
        lista, matriz = PlanoBodega(lado), PlanoBodega(lado, GrafoMatrizAdyacencia)
        t_lista = segundos(lambda lista=lista: dijkstra(lista.grafo, MUELLE))
        t_matriz = segundos(lambda matriz=matriz: dijkstra(matriz.grafo, MUELLE))
        print(
            f"{lado:>5}{lado * lado + 1:>8}{t_lista * 1e3:>13.1f}{t_matriz * 1e3:>14.1f}"
        )

    plano = PlanoBodega(100)
    t = segundos(lambda: dijkstra(plano.grafo, MUELLE))
    print(
        f"\nPlano completo 100 x 100 con lista: {t * 1e3:.0f} ms (todas las ubicaciones)"
    )


def con_monticulo_propio(prioridades: list[int]) -> None:
    """
    n encolar seguidos de n desencolar en la cola de prioridad propia.

    Complejidad:
        Tiempo: O(n log n).
        Espacio: O(n).
    """
    cola = ColaPrioridad()

    for p in prioridades:
        cola.encolar(p, p)

    while not cola.esta_vacia():
        cola.desencolar()


def con_heapq(prioridades: list[int]) -> None:
    """
    n encolar seguidos de n desencolar con heapq (referencia).

    Complejidad:
        Tiempo: O(n log n).
        Espacio: O(n).
    """
    monticulo: list[int] = []

    for p in prioridades:
        heapq.heappush(monticulo, p)

    while monticulo:
        heapq.heappop(monticulo)


def con_busqueda_lineal(prioridades: list[int]) -> None:
    """
    n encolar y n desencolar buscando el mínimo recorriendo toda la lista.

    Complejidad:
        Tiempo: O(n²).
        Espacio: O(n).
    """
    datos = list(prioridades)

    while datos:
        menor = 0

        for i in range(1, len(datos)):
            if datos[i] < datos[menor]:
                menor = i

        datos[menor] = datos[-1]
        datos.pop()


def medir_cola() -> None:
    """
    Compara las tres formas de sacar siempre el elemento más urgente.

    Complejidad:
        Tiempo: dominado por la búsqueda lineal con el n mayor.
        Espacio: O(n).
    """
    print("\n== 3. Cola de prioridad: n encolar + n desencolar (segundos) ==")
    print(f"{'n':>8}{'montículo propio':>18}{'heapq (ref.)':>14}{'lista lineal':>14}")

    for n in (1_000, 5_000, 20_000):
        datos = random.Random(n).sample(range(10 * n), n)
        t_propio = segundos(lambda datos=datos: con_monticulo_propio(datos))
        t_heapq = segundos(lambda datos=datos: con_heapq(datos))
        lineal = (
            segundos(lambda datos=datos: con_busqueda_lineal(datos))
            if n <= 5_000
            else None
        )
        texto = f"{lineal:>14.4f}" if lineal is not None else f"{'(omitida)':>14}"
        print(f"{n:>8}{t_propio:>18.4f}{t_heapq:>14.4f}{texto}")


def main() -> None:
    """
    Corre las tres mediciones.

    Complejidad:
        Tiempo: la suma de las mediciones.
        Espacio: O(V²) transitorio.
    """
    medir_memoria()
    medir_dijkstra()
    medir_cola()


if __name__ == "__main__":
    main()
