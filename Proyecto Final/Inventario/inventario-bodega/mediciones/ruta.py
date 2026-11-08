"""
Medición de la Fase 4: ahorro de distancia de la ruta optimizada frente al
orden de llegada, en la bodega de 100 x 100 (criterio de éxito: >= 20 %).

Los pedidos son sintéticos y reproducibles (semilla fija): cada uno pide
productos en ubicaciones al azar. Uso: python -m mediciones.ruta
"""

import random
import time

from inventario.estructuras.arreglo import ArregloDinamico
from inventario.grafos.plano_bodega import PlanoBodega
from inventario.grafos.ruta_recoleccion import comparar_rutas

LADO = 100
PEDIDOS_POR_TAMANO = 100
TAMANOS = (3, 5, 10, 20)
SEMILLA = 2026


def medir() -> None:
    """
    Imprime, por tamaño de pedido, el ahorro medio, mínimo y el tiempo por ruta.

    Complejidad:
        Tiempo: O(pedidos · k (V + E) log V).
        Espacio: O(V + k²).
    """
    plano = PlanoBodega(LADO)
    azar = random.Random(SEMILLA)
    total = plano.grafo.numero_nodos
    print(
        f"Bodega {LADO}x{LADO} ({total} nodos), {PEDIDOS_POR_TAMANO} pedidos por tamaño\n"
    )
    print(
        f"{'ítems':>6}{'dist. llegada':>15}{'dist. óptima':>14}{'ahorro medio':>14}{'ahorro mín.':>13}{'ms/ruta':>9}"
    )

    for k in TAMANOS:
        suma_l = suma_o = 0
        minimo = 1.0
        inicio = time.perf_counter()

        for _ in range(PEDIDOS_POR_TAMANO):
            nodos = ArregloDinamico()
            for n in azar.sample(range(1, total), k):
                nodos.agregar(n)
            r = comparar_rutas(plano, nodos)
            suma_l += r.distancia_llegada
            suma_o += r.distancia_optima
            minimo = min(minimo, r.ahorro)

        ms = (time.perf_counter() - inicio) / PEDIDOS_POR_TAMANO * 1000
        n = PEDIDOS_POR_TAMANO
        ahorro = (suma_l - suma_o) / suma_l
        print(
            f"{k:>6}{suma_l / n:>15.0f}{suma_o / n:>14.0f}{ahorro:>13.1%}{minimo:>13.1%}{ms:>9.0f}"
        )


if __name__ == "__main__":
    medir()
