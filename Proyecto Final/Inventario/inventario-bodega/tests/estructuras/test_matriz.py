import pytest

from inventario.dominio.producto import Producto
from inventario.estructuras.matriz import MatrizBodega


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
        35,
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


def test_asignar_en_ubicacion_ocupada_se_rechaza():
    matriz = MatrizBodega()
    primero = crear_producto()
    segundo = crear_producto()

    matriz.asignar(3, 3, primero)

    with pytest.raises(ValueError):
        matriz.asignar(3, 3, segundo)

    assert matriz.obtener(3, 3) is primero


def test_reasignar_el_mismo_producto_no_falla():
    matriz = MatrizBodega()
    producto = crear_producto()

    matriz.asignar(3, 3, producto)
    matriz.asignar(3, 3, producto)

    assert matriz.obtener(3, 3) is producto


def test_ubicacion_se_puede_reutilizar_tras_eliminar():
    matriz = MatrizBodega()
    primero = crear_producto()
    segundo = crear_producto()

    matriz.asignar(3, 3, primero)
    matriz.eliminar(3, 3)
    matriz.asignar(3, 3, segundo)

    assert matriz.obtener(3, 3) is segundo
