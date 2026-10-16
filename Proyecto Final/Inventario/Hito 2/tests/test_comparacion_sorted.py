import random

from ordenamiento import quick_sort
from producto import Producto


def crear_productos_aleatorios(cantidad):
    """Crea productos con IDs en orden aleatorio."""
    ids = list(range(cantidad))
    random.Random(42).shuffle(ids)

    return [
        Producto(
            id_producto,
            f"Producto {id_producto}",
            "General",
            100,
            2,
            "2026-09-01",
            "2026-12-01",
            4500.0,
            0,
            0,
        )
        for id_producto in ids
    ]


def test_quick_sort_vs_sorted_1000_entradas_aleatorias():
    """
    Verifica que QuickSort produzca el mismo orden que sorted().

    Se utilizan 1000 entradas aleatorias.

    Complejidad:
        Tiempo: O(n log n) promedio para QuickSort y O(n log n) para sorted().
        Espacio: O(n) para QuickSort en esta implementación y O(n) para sorted().
    """
    productos = crear_productos_aleatorios(1000)

    resultado_quick = quick_sort(productos.copy(), lambda p: p.id)

    resultado_sorted = sorted(productos, key=lambda p: p.id)

    ids_quick = [producto.id for producto in resultado_quick]
    ids_sorted = [producto.id for producto in resultado_sorted]

    assert ids_quick == ids_sorted
