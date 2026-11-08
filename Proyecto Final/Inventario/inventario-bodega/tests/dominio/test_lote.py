import pytest

from inventario.dominio.lote import Lote, validar_fecha


def crear_lote(**cambios):
    datos = {
        "codigo": "L-1",
        "cantidad": 10,
        "fecha_produccion": "2026-09-01",
        "fecha_vencimiento": "2027-09-01",
    }
    datos.update(cambios)
    return Lote(**datos)


def test_crear_lote_valido():
    lote = crear_lote()

    assert lote.codigo == "L-1"
    assert lote.cantidad == 10
    assert lote.fecha_produccion == "2026-09-01"
    assert lote.fecha_vencimiento == "2027-09-01"


def test_el_codigo_se_limpia_de_espacios():
    assert crear_lote(codigo="  L-7  ").codigo == "L-7"


@pytest.mark.parametrize("codigo", ["", "   "])
def test_codigo_vacio_se_rechaza(codigo):
    with pytest.raises(ValueError):
        crear_lote(codigo=codigo)


@pytest.mark.parametrize("cantidad", [0, -1, -100])
def test_cantidad_no_positiva_se_rechaza(cantidad):
    with pytest.raises(ValueError):
        crear_lote(cantidad=cantidad)


@pytest.mark.parametrize(
    "fecha",
    [
        "2027/01/01",
        "20270101",
        "2027-1-1",
        "27-01-01",
        "",
        "hoy",
        "2027-13-01",
        "2027-02-30",
    ],
)
def test_fechas_con_formato_invalido_se_rechazan(fecha):
    with pytest.raises(ValueError):
        crear_lote(fecha_vencimiento=fecha)

    with pytest.raises(ValueError):
        crear_lote(fecha_produccion=fecha, fecha_vencimiento="2030-01-01")


def test_vencimiento_anterior_a_la_produccion_se_rechaza():
    with pytest.raises(ValueError):
        crear_lote(fecha_produccion="2026-09-02", fecha_vencimiento="2026-09-01")


def test_vencimiento_el_mismo_dia_de_la_produccion_es_valido():
    lote = crear_lote(fecha_produccion="2026-09-01", fecha_vencimiento="2026-09-01")

    assert lote.fecha_vencimiento == "2026-09-01"


def test_fecha_bisiesta_valida():
    validar_fecha("2028-02-29")

    with pytest.raises(ValueError):
        validar_fecha("2027-02-29")


def test_str_incluye_codigo_cantidad_y_vencimiento():
    texto = str(crear_lote())

    assert "L-1" in texto
    assert "10" in texto
    assert "2027-09-01" in texto
