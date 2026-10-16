from pathlib import Path

import pytest

from producto import Producto
from sistema import SistemaInventario

RUTA_PRODUCTOS = Path(__file__).resolve().parent.parent / "productos.csv"

ENCABEZADO = (
    "id,nombre,categoria,cantidad,tiempo_produccion,"
    "fecha_produccion,fecha_vencimiento,precio,pasillo,estante"
)


def crear_producto(
    id_producto,
    pasillo=0,
    estante=0,
    nombre="Producto",
    vencimiento="2027-01-01",
    tiempo=1,
):
    return Producto(
        id_producto,
        nombre,
        "General",
        10,
        tiempo,
        "2026-09-01",
        vencimiento,
        1000.0,
        pasillo,
        estante,
    )


def ids_del_catalogo(sistema):
    return [sistema.catalogo[i].id for i in range(len(sistema.catalogo))]


def sistema_con_tres():
    sistema = SistemaInventario()
    sistema.agregar(crear_producto(1, 0, 0))
    sistema.agregar(crear_producto(2, 0, 1))
    sistema.agregar(crear_producto(3, 0, 2))
    return sistema


# ---------- agregar y ubicaciones ----------


def test_sistema_inicia_vacio():
    sistema = SistemaInventario()

    assert len(sistema.catalogo) == 0
    assert sistema.ordenado_por_id is True
    assert sistema.buscar_por_id(1) is None


def test_agregar_registra_en_catalogo_y_bodega():
    sistema = SistemaInventario()
    producto = crear_producto(7, 3, 4)

    sistema.agregar(producto)

    assert len(sistema.catalogo) == 1
    assert sistema.consultar_ubicacion(3, 4) is producto


def test_agregar_en_ubicacion_ocupada_no_cambia_el_catalogo():
    sistema = SistemaInventario()
    sistema.agregar(crear_producto(1, 2, 2))

    with pytest.raises(ValueError):
        sistema.agregar(crear_producto(2, 2, 2))

    assert ids_del_catalogo(sistema) == [1]


def test_agregar_con_ubicacion_negativa_no_cambia_el_catalogo():
    sistema = SistemaInventario()

    with pytest.raises(IndexError):
        sistema.agregar(crear_producto(1, -1, 0))

    assert len(sistema.catalogo) == 0


def test_agregar_en_ubicacion_lejana_amplia_la_bodega():
    sistema = SistemaInventario()

    sistema.agregar(crear_producto(1, 25, 30))

    assert sistema.bodega.tamaño == 31
    assert sistema.consultar_ubicacion(25, 30).id == 1


def test_consultar_ubicacion_libre_y_fuera_de_rango():
    sistema = SistemaInventario()

    assert sistema.consultar_ubicacion(5, 5) is None

    with pytest.raises(IndexError):
        sistema.consultar_ubicacion(50, 50)


def test_ubicaciones_libres():
    sistema = SistemaInventario()

    assert sistema.ubicaciones_libres() == 100

    sistema.agregar(crear_producto(1, 0, 0))
    sistema.agregar(crear_producto(2, 0, 1))

    assert sistema.ubicaciones_libres() == 98


# ---------- búsqueda ----------


def test_buscar_por_id_encuentra_y_no_encuentra():
    sistema = sistema_con_tres()

    assert sistema.buscar_por_id(2).id == 2
    assert sistema.buscar_por_id(99) is None


def test_ids_crecientes_mantienen_el_catalogo_ordenado():
    sistema = sistema_con_tres()

    assert sistema.ordenado_por_id is True


def test_agregar_id_menor_pierde_el_orden_pero_la_busqueda_funciona():
    sistema = sistema_con_tres()

    sistema.agregar(crear_producto(0, 1, 0))

    assert sistema.ordenado_por_id is False
    assert sistema.buscar_por_id(0).id == 0
    assert sistema.buscar_por_id(3).id == 3


def test_buscar_en_catalogo_de_un_solo_producto():
    sistema = SistemaInventario()
    sistema.agregar(crear_producto(5, 0, 0))

    assert sistema.buscar_por_id(5).id == 5
    assert sistema.buscar_por_id(6) is None


# ---------- eliminar ----------


def test_eliminar_por_id_quita_del_catalogo_y_libera_la_ubicacion():
    sistema = sistema_con_tres()

    eliminado = sistema.eliminar_por_id(2)

    assert eliminado.id == 2
    assert ids_del_catalogo(sistema) == [1, 3]
    assert sistema.consultar_ubicacion(0, 1) is None
    assert sistema.buscar_por_id(2) is None


def test_eliminar_id_inexistente_devuelve_none():
    sistema = sistema_con_tres()

    assert sistema.eliminar_por_id(99) is None
    assert ids_del_catalogo(sistema) == [1, 2, 3]


def test_eliminar_primero_y_ultimo_conserva_el_orden():
    sistema = sistema_con_tres()

    sistema.eliminar_por_id(1)
    sistema.eliminar_por_id(3)

    assert ids_del_catalogo(sistema) == [2]
    assert sistema.ordenado_por_id is True


def test_eliminar_en_catalogo_desordenado():
    sistema = SistemaInventario()
    sistema.agregar(crear_producto(5, 0, 0))
    sistema.agregar(crear_producto(2, 0, 1))
    sistema.agregar(crear_producto(9, 0, 2))

    assert sistema.ordenado_por_id is False

    sistema.eliminar_por_id(2)

    assert ids_del_catalogo(sistema) == [5, 9]


def test_ubicacion_liberada_se_puede_reutilizar():
    sistema = sistema_con_tres()

    sistema.eliminar_por_id(2)
    sistema.agregar(crear_producto(10, 0, 1))

    assert sistema.consultar_ubicacion(0, 1).id == 10


def test_eliminar_en_sistema_vacio():
    sistema = SistemaInventario()

    assert sistema.eliminar_por_id(1) is None


# ---------- ordenar ----------


def sistema_para_ordenar():
    sistema = SistemaInventario()
    sistema.agregar(crear_producto(3, 0, 0, "Cafe", "2027-03-01", 3))
    sistema.agregar(crear_producto(1, 0, 1, "Leche", "2026-10-05", 1))
    sistema.agregar(crear_producto(2, 0, 2, "Arroz", "2027-09-01", 2))
    return sistema


def test_ordenar_por_vencimiento():
    sistema = sistema_para_ordenar()

    sistema.ordenar("vencimiento")

    assert ids_del_catalogo(sistema) == [1, 3, 2]
    assert sistema.ordenado_por_id is False


def test_ordenar_por_nombre():
    sistema = sistema_para_ordenar()

    sistema.ordenar("nombre")

    assert ids_del_catalogo(sistema) == [2, 3, 1]


def test_ordenar_por_tiempo_de_produccion():
    sistema = sistema_para_ordenar()

    sistema.ordenar("tiempo_produccion")

    assert ids_del_catalogo(sistema) == [1, 2, 3]


def test_ordenar_por_id_habilita_la_busqueda_binaria():
    sistema = sistema_para_ordenar()
    assert sistema.ordenado_por_id is False

    sistema.ordenar("id")

    assert ids_del_catalogo(sistema) == [1, 2, 3]
    assert sistema.ordenado_por_id is True
    assert sistema.buscar_por_id(2).nombre == "Arroz"


def test_ordenar_no_pierde_la_ubicacion_de_los_productos():
    sistema = sistema_para_ordenar()

    sistema.ordenar("nombre")

    assert sistema.consultar_ubicacion(0, 0).nombre == "Cafe"
    assert len(sistema.catalogo) == 3


def test_ordenar_catalogo_vacio_y_de_un_elemento():
    vacio = SistemaInventario()
    vacio.ordenar("nombre")
    assert len(vacio.catalogo) == 0

    uno = SistemaInventario()
    uno.agregar(crear_producto(1, 0, 0))
    uno.ordenar("vencimiento")
    assert ids_del_catalogo(uno) == [1]


def test_ordenar_con_criterio_desconocido():
    sistema = sistema_para_ordenar()

    with pytest.raises(ValueError):
        sistema.ordenar("color")


def test_ordenar_mil_productos_aleatorios_coincide_con_sorted():
    import random

    generador = random.Random(42)
    ids = list(range(1000))
    generador.shuffle(ids)

    sistema = SistemaInventario()

    for i, id_producto in enumerate(ids):
        sistema.agregar(crear_producto(id_producto, i % 40, i // 40))

    sistema.ordenar("id")

    assert ids_del_catalogo(sistema) == sorted(ids)
    assert sistema.buscar_por_id(777).id == 777


# ---------- carga desde CSV ----------


def escribir_csv(ruta, filas, fin_de_linea="\n", con_bom=False):
    contenido = fin_de_linea.join([ENCABEZADO] + filas) + fin_de_linea
    codificacion = "utf-8-sig" if con_bom else "utf-8"
    ruta.write_text(contenido, encoding=codificacion, newline="")


def test_cargar_el_csv_real_del_proyecto():
    sistema = SistemaInventario()

    cantidad = sistema.cargar_csv(str(RUTA_PRODUCTOS))

    assert cantidad == len(sistema.catalogo)
    assert cantidad >= 5
    assert sistema.buscar_por_id(1).nombre == "Arroz Diana"


def test_cargar_csv_con_bom_y_saltos_de_linea_windows(tmp_path):
    ruta = tmp_path / "productos.csv"
    escribir_csv(
        ruta,
        ["1,Arroz,Alimentos,10,2,2026-09-01,2027-09-01,4500,0,0"],
        fin_de_linea="\r\n",
        con_bom=True,
    )
    sistema = SistemaInventario()

    assert sistema.cargar_csv(str(ruta)) == 1
    assert sistema.buscar_por_id(1).precio == 4500.0


def test_cargar_csv_solo_con_encabezado(tmp_path):
    ruta = tmp_path / "vacio.csv"
    escribir_csv(ruta, [])
    sistema = SistemaInventario()

    assert sistema.cargar_csv(str(ruta)) == 0
    assert len(sistema.catalogo) == 0


def test_cargar_dos_veces_el_mismo_csv_no_duplica_productos(tmp_path):
    ruta = tmp_path / "productos.csv"
    escribir_csv(ruta, ["1,Arroz,Alimentos,10,2,2026-09-01,2027-09-01,4500,0,0"])
    sistema = SistemaInventario()
    sistema.cargar_csv(str(ruta))

    with pytest.raises(ValueError):
        sistema.cargar_csv(str(ruta))

    assert len(sistema.catalogo) == 1


def test_cargar_csv_inexistente(tmp_path):
    sistema = SistemaInventario()

    with pytest.raises(FileNotFoundError):
        sistema.cargar_csv(str(tmp_path / "no_existe.csv"))


def test_cargar_csv_con_numero_invalido(tmp_path):
    ruta = tmp_path / "malo.csv"
    escribir_csv(ruta, ["1,Arroz,Alimentos,diez,2,2026-09-01,2027-09-01,4500,0,0"])
    sistema = SistemaInventario()

    with pytest.raises(ValueError):
        sistema.cargar_csv(str(ruta))

    assert len(sistema.catalogo) == 0
