import pytest

from matriz import MatrizBodega
from producto import Producto


def crear_producto():
    return Producto(
        54821,
        "Leche Entera",
        "Lácteos",
        120,
        2,
        "2026-09-01",
        "2026-10-01",
        4500.0,
        12,
        35
    )


def test_matriz_inicia_en_10x10():
    matriz = MatrizBodega()

    assert matriz.tamaño == 10
    assert len(matriz.datos) == 10
    assert len(matriz.datos[0]) == 10


def test_matriz_inicia_vacia():
    matriz = MatrizBodega()

    assert matriz.obtener(5, 5) is None


def test_asignar_producto():
    matriz = MatrizBodega()
    producto = crear_producto()

    matriz.asignar(5, 5, producto)

    assert matriz.obtener(5, 5) == producto


def test_eliminar_producto():
    matriz = MatrizBodega()
    producto = crear_producto()

    matriz.asignar(5, 5, producto)

    eliminado = matriz.eliminar(5, 5)

    assert eliminado == producto
    assert matriz.obtener(5, 5) is None


def test_matriz_se_amplia():
    matriz = MatrizBodega(10)
    producto = crear_producto()

    matriz.asignar(15, 15, producto)

    assert matriz.tamaño == 16
    assert matriz.obtener(15, 15) == producto


def test_ampliacion_conserva_productos():
    matriz = MatrizBodega(10)
    producto = crear_producto()

    matriz.asignar(5, 5, producto)
    matriz.asignar(20, 20, producto)

    assert matriz.tamaño == 21
    assert matriz.obtener(5, 5) == producto
    assert matriz.obtener(20, 20) == producto


def test_posicion_negativa():
    matriz = MatrizBodega()

    with pytest.raises(IndexError):
        matriz.obtener(-1, 5)


def test_eliminar_fuera_de_rango():
    matriz = MatrizBodega()

    with pytest.raises(IndexError):
        matriz.eliminar(20, 20)