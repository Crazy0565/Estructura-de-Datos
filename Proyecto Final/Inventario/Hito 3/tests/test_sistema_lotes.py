from datetime import date, timedelta
from pathlib import Path

import pytest

from producto import SIN_VENCIMIENTO, Producto
from sistema import SistemaInventario

RUTA_PRODUCTOS = Path(__file__).resolve().parent.parent / "productos.csv"
RUTA_LOTES = Path(__file__).resolve().parent.parent / "lotes.csv"

ENCABEZADO_LOTES = "id_producto,codigo_lote,cantidad,fecha_produccion,fecha_vencimiento"


def crear_producto(id_producto, pasillo, estante, cantidad=100, vence="2027-09-01"):
    return Producto(
        id_producto,
        f"Producto {id_producto}",
        "General",
        cantidad,
        1,
        "2026-09-01",
        vence,
        1000.0,
        pasillo,
        estante,
    )


def sistema_con_dos():
    sistema = SistemaInventario()
    sistema.agregar(crear_producto(1, 0, 0, 100, "2027-09-01"))
    sistema.agregar(crear_producto(2, 0, 1, 50, "2027-01-01"))
    return sistema


def escribir_lotes(ruta, filas, fin_de_linea="\n", codificacion="utf-8"):
    contenido = fin_de_linea.join([ENCABEZADO_LOTES] + filas) + fin_de_linea
    ruta.write_text(contenido, encoding=codificacion, newline="")


def codigos_de(producto):
    return [lote.codigo for lote in producto.lotes]


# ---------- registrar lote ----------


def test_registrar_lote_actualiza_cantidad_y_vencimiento():
    sistema = sistema_con_dos()

    lote = sistema.registrar_lote(1, "1-2", 30, "2026-10-01", "2027-02-01")

    producto = sistema.buscar_por_id(1)
    assert lote.codigo == "1-2"
    assert producto.cantidad == 130
    assert producto.fecha_vencimiento == "2027-02-01"
    assert codigos_de(producto) == ["1-2", "1-1"]


def test_registrar_lote_en_producto_inexistente_devuelve_none():
    sistema = sistema_con_dos()

    assert sistema.registrar_lote(99, "X", 5, "2026-10-01", "2027-02-01") is None


def test_registrar_lote_con_codigo_repetido_se_rechaza():
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.registrar_lote(1, "1-1", 5, "2026-10-01", "2027-02-01")

    assert sistema.buscar_por_id(1).cantidad == 100


def test_registrar_lote_con_datos_invalidos_se_rechaza():
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.registrar_lote(1, "1-2", 0, "2026-10-01", "2027-02-01")

    with pytest.raises(ValueError):
        sistema.registrar_lote(1, "1-2", 5, "2026-10-01", "mañana")

    assert len(sistema.buscar_por_id(1).lotes) == 1


# ---------- despachar ----------


def test_despachar_toma_primero_el_lote_que_vence_antes():
    sistema = sistema_con_dos()
    sistema.registrar_lote(1, "1-2", 30, "2026-10-01", "2027-02-01")

    tomas = sistema.despachar_producto(1, 40)

    assert [tomas[i] for i in range(len(tomas))] == [("1-2", 30), ("1-1", 10)]
    assert sistema.buscar_por_id(1).cantidad == 90


def test_despachar_producto_inexistente_devuelve_none():
    sistema = sistema_con_dos()

    assert sistema.despachar_producto(99, 1) is None


def test_despachar_mas_del_stock_no_cambia_el_stock():
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.despachar_producto(2, 51)

    assert sistema.buscar_por_id(2).cantidad == 50


def test_producto_agotado_queda_al_final_al_ordenar_por_vencimiento():
    sistema = sistema_con_dos()
    sistema.despachar_producto(2, 50)

    sistema.ordenar("vencimiento")

    assert sistema.catalogo[0].id == 1
    assert sistema.catalogo[1].fecha_vencimiento == SIN_VENCIMIENTO


def test_ordenar_por_vencimiento_usa_el_lote_mas_proximo():
    sistema = sistema_con_dos()
    sistema.registrar_lote(1, "1-2", 30, "2026-10-01", "2026-12-01")

    sistema.ordenar("vencimiento")

    assert sistema.catalogo[0].id == 1


# ---------- cargar lotes desde CSV ----------


def test_cargar_los_lotes_reales_del_proyecto():
    sistema = SistemaInventario()
    sistema.cargar_csv(str(RUTA_PRODUCTOS))

    cargados = sistema.cargar_lotes_csv(str(RUTA_LOTES))

    arroz = sistema.buscar_por_id(1)
    chocolate = sistema.buscar_por_id(5)
    assert cargados == 8
    assert codigos_de(arroz) == ["1-2", "1-1", "1-3"]
    assert arroz.cantidad == 200
    assert codigos_de(chocolate) == ["5-2", "5-1", "5-3"]
    assert chocolate.cantidad == 195


def test_cargar_lotes_deja_cada_lista_ordenada_por_vencimiento():
    sistema = SistemaInventario()
    sistema.cargar_csv(str(RUTA_PRODUCTOS))
    sistema.cargar_lotes_csv(str(RUTA_LOTES))

    for i in range(len(sistema.catalogo)):
        fechas = [lote.fecha_vencimiento for lote in sistema.catalogo[i].lotes]
        assert fechas == sorted(fechas)


def test_cargar_lotes_con_bom_y_saltos_de_linea_windows(tmp_path):
    ruta = tmp_path / "lotes.csv"
    escribir_lotes(
        ruta,
        ["1,1-2,30,2026-10-01,2027-02-01"],
        fin_de_linea="\r\n",
        codificacion="utf-8-sig",
    )
    sistema = sistema_con_dos()

    assert sistema.cargar_lotes_csv(str(ruta)) == 1
    assert sistema.buscar_por_id(1).cantidad == 130


def test_cargar_lotes_solo_con_encabezado(tmp_path):
    ruta = tmp_path / "lotes.csv"
    escribir_lotes(ruta, [])
    sistema = sistema_con_dos()

    assert sistema.cargar_lotes_csv(str(ruta)) == 0
    assert sistema.buscar_por_id(1).cantidad == 100


def test_cargar_lotes_con_producto_inexistente_no_aplica_nada(tmp_path):
    ruta = tmp_path / "lotes.csv"
    escribir_lotes(
        ruta, ["1,1-2,30,2026-10-01,2027-02-01", "99,99-1,5,2026-10-01,2027-02-01"]
    )
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.cargar_lotes_csv(str(ruta))

    assert sistema.buscar_por_id(1).cantidad == 100
    assert len(sistema.buscar_por_id(1).lotes) == 1


def test_cargar_lotes_con_codigo_ya_existente_no_aplica_nada(tmp_path):
    ruta = tmp_path / "lotes.csv"
    escribir_lotes(
        ruta, ["2,2-2,5,2026-10-01,2027-02-01", "1,1-1,30,2026-10-01,2027-02-01"]
    )
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.cargar_lotes_csv(str(ruta))

    assert len(sistema.buscar_por_id(2).lotes) == 1
    assert sistema.buscar_por_id(1).cantidad == 100


def test_cargar_lotes_con_codigo_repetido_dentro_del_archivo(tmp_path):
    ruta = tmp_path / "lotes.csv"
    escribir_lotes(
        ruta, ["1,1-2,30,2026-10-01,2027-02-01", "1,1-2,10,2026-10-01,2027-03-01"]
    )
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.cargar_lotes_csv(str(ruta))

    assert len(sistema.buscar_por_id(1).lotes) == 1


def test_cargar_lotes_con_numero_invalido_no_aplica_nada(tmp_path):
    ruta = tmp_path / "lotes.csv"
    escribir_lotes(
        ruta, ["1,1-2,30,2026-10-01,2027-02-01", "1,1-3,muchos,2026-10-01,2027-03-01"]
    )
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.cargar_lotes_csv(str(ruta))

    assert len(sistema.buscar_por_id(1).lotes) == 1


def test_cargar_lotes_con_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        sistema_con_dos().cargar_lotes_csv(str(tmp_path / "no_existe.csv"))


def test_cargar_dos_veces_el_mismo_archivo_no_duplica_lotes():
    sistema = SistemaInventario()
    sistema.cargar_csv(str(RUTA_PRODUCTOS))
    sistema.cargar_lotes_csv(str(RUTA_LOTES))

    with pytest.raises(ValueError):
        sistema.cargar_lotes_csv(str(RUTA_LOTES))

    assert sistema.buscar_por_id(1).cantidad == 200


def test_un_embarque_grande_usa_la_fusion_iterativa_y_queda_ordenado(tmp_path):
    ruta = tmp_path / "lotes.csv"
    base = date(2027, 6, 1)
    filas = [
        f"1,E{i},1,2026-10-01,{(base + timedelta(days=(i * 7) % 900)).isoformat()}"
        for i in range(700)
    ]
    escribir_lotes(ruta, filas)
    sistema = sistema_con_dos()

    cargados = sistema.cargar_lotes_csv(str(ruta))

    producto = sistema.buscar_por_id(1)
    fechas = [lote.fecha_vencimiento for lote in producto.lotes]
    assert cargados == 700
    assert len(producto.lotes) == 701
    assert fechas == sorted(fechas)
    assert producto.cantidad == 800
