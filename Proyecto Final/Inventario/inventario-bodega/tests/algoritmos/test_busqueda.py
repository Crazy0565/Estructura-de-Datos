from inventario.algoritmos.busqueda import busqueda_binaria, busqueda_lineal
from inventario.dominio.producto import Producto


def crear_productos():
    return [
        Producto(10, "A", "General", 10, 5, "2026-09-01", "2026-10-01", 1000, 1, 1),
        Producto(20, "B", "General", 20, 2, "2026-09-01", "2026-09-20", 2000, 1, 2),
        Producto(30, "C", "General", 30, 4, "2026-09-01", "2026-09-25", 3000, 1, 3),
    ]


def test_busqueda_lineal_encuentra():
    productos = crear_productos()

    resultado = busqueda_lineal(productos, 20, lambda p: p.id)

    assert resultado.id == 20


def test_busqueda_lineal_no_encuentra():
    productos = crear_productos()

    resultado = busqueda_lineal(productos, 99, lambda p: p.id)

    assert resultado is None


def test_busqueda_binaria_encuentra():
    productos = crear_productos()

    resultado = busqueda_binaria(productos, 20, lambda p: p.id)

    assert resultado.id == 20


def test_busqueda_binaria_no_encuentra():
    productos = crear_productos()

    resultado = busqueda_binaria(productos, 99, lambda p: p.id)

    assert resultado is None
