import pytest

from producto import SIN_VENCIMIENTO, Producto


def crear_producto(cantidad=100, vence="2027-09-01"):
    return Producto(
        1, "Arroz Diana", "Alimentos", cantidad, 2, "2026-09-01", vence, 4500.0, 0, 0
    )


def test_producto_nuevo_tiene_un_lote_inicial():
    producto = crear_producto()

    assert len(producto.lotes) == 1
    assert producto.lotes.primero().codigo == "1-1"
    assert producto.cantidad == 100
    assert producto.fecha_vencimiento == "2027-09-01"


def test_producto_sin_cantidad_no_tiene_lotes():
    producto = crear_producto(cantidad=0)

    assert len(producto.lotes) == 0
    assert producto.cantidad == 0
    assert producto.fecha_vencimiento == SIN_VENCIMIENTO


def test_cantidad_negativa_se_rechaza():
    with pytest.raises(ValueError):
        crear_producto(cantidad=-5)


def test_fecha_de_vencimiento_invalida_se_rechaza():
    with pytest.raises(ValueError):
        crear_producto(vence="septiembre")


def test_vencimiento_anterior_a_la_produccion_se_rechaza():
    with pytest.raises(ValueError):
        crear_producto(vence="2026-08-01")


def test_cantidad_y_vencimiento_se_derivan_de_los_lotes():
    from lote import Lote

    producto = crear_producto()
    producto.lotes.insertar(Lote("1-2", 40, "2026-10-01", "2027-03-01"))

    assert producto.cantidad == 140
    assert producto.fecha_vencimiento == "2027-03-01"

    producto.lotes.despachar(40)

    assert producto.cantidad == 100
    assert producto.fecha_vencimiento == "2027-09-01"


def test_producto_agotado_pasa_a_vencer_al_final():
    producto = crear_producto(cantidad=10)

    producto.lotes.despachar(10)

    assert producto.cantidad == 0
    assert producto.fecha_vencimiento == SIN_VENCIMIENTO


def test_str_muestra_cantidad_total_y_proximo_vencimiento():
    producto = crear_producto()

    texto = str(producto)

    assert "Arroz Diana" in texto
    assert "Cantidad: 100" in texto
    assert "Vence: 2027-09-01" in texto


def test_str_de_producto_agotado():
    producto = crear_producto(cantidad=0)

    assert "sin existencias" in str(producto)
