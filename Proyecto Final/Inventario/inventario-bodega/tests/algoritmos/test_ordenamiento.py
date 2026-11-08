from inventario.algoritmos.ordenamiento import bubble_sort, quick_sort
from inventario.dominio.producto import Producto


def crear_productos():
    return [
        Producto(1, "A", "General", 10, 5, "2026-09-01", "2026-10-01", 1000, 1, 1),
        Producto(2, "B", "General", 20, 2, "2026-09-01", "2026-09-20", 2000, 1, 2),
        Producto(3, "C", "General", 30, 4, "2026-09-01", "2026-09-25", 3000, 1, 3),
    ]


def test_bubble_sort():
    productos = crear_productos()

    resultado = bubble_sort(productos, lambda p: p.tiempo_produccion)

    assert [p.tiempo_produccion for p in resultado] == [2, 4, 5]


def test_quick_sort():
    productos = crear_productos()

    resultado = quick_sort(productos, lambda p: p.fecha_vencimiento)

    assert [p.fecha_vencimiento for p in resultado] == [
        "2026-09-20",
        "2026-09-25",
        "2026-10-01",
    ]


def test_bubble_sort_vacio():
    assert bubble_sort([], lambda p: p.id) == []


def test_quick_sort_vacio():
    assert quick_sort([], lambda p: p.id) == []


def test_bubble_sort_por_id():
    productos = crear_productos()[::-1]

    resultado = bubble_sort(productos, lambda p: p.id)

    assert [p.id for p in resultado] == [1, 2, 3]
