import csv

import pytest

import generador_datos as gd
from sistema import SistemaInventario


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


@pytest.fixture
def rutas(tmp_path):
    return gd.generar_archivos(
        tmp_path, productos=60, lotes=120, pedidos=200, semilla=7
    )


def test_genera_las_cantidades_pedidas(rutas):
    assert len(leer(rutas["productos"])) == 60
    assert len(leer(rutas["lotes"])) == 120
    assert len(leer(rutas["pedidos"])) == 200


def test_encabezados_son_los_que_esperan_los_cargadores(rutas):
    assert tuple(leer(rutas["productos"])[0].keys()) == gd.COLUMNAS_PRODUCTOS
    assert tuple(leer(rutas["lotes"])[0].keys()) == gd.COLUMNAS_LOTES
    assert tuple(leer(rutas["pedidos"])[0].keys()) == gd.COLUMNAS_PEDIDOS


def test_misma_semilla_produce_archivos_identicos(tmp_path):
    a = gd.generar_archivos(tmp_path / "a", 40, 80, 100, semilla=3)
    b = gd.generar_archivos(tmp_path / "b", 40, 80, 100, semilla=3)
    for clave in a:
        assert a[clave].read_bytes() == b[clave].read_bytes()


def test_semillas_distintas_producen_datos_distintos(tmp_path):
    a = gd.generar_archivos(tmp_path / "a", 40, 80, 100, semilla=1)
    b = gd.generar_archivos(tmp_path / "b", 40, 80, 100, semilla=2)
    assert a["productos"].read_bytes() != b["productos"].read_bytes()


def test_ids_y_ubicaciones_no_se_repiten(rutas):
    filas = leer(rutas["productos"])
    assert len({f["id"] for f in filas}) == 60
    assert len({(f["pasillo"], f["estante"]) for f in filas}) == 60


def test_las_ubicaciones_caben_en_la_cuadricula(rutas):
    lado = gd.lado_de_la_bodega(60)
    for f in leer(rutas["productos"]):
        assert 0 <= int(f["pasillo"]) < lado and 0 <= int(f["estante"]) < lado


@pytest.mark.parametrize("n,lado", [(1, 1), (4, 2), (5, 3), (10_000, 100)])
def test_lado_de_la_bodega(n, lado):
    assert gd.lado_de_la_bodega(n) == lado


def test_fechas_validas_y_vencimiento_posterior(rutas):
    for nombre in ("productos", "lotes"):
        for f in leer(rutas[nombre]):
            assert f["fecha_produccion"] <= f["fecha_vencimiento"]
            assert len(f["fecha_produccion"]) == 10


def test_codigos_de_lote_unicos_por_producto(rutas):
    codigos = [f["codigo_lote"] for f in leer(rutas["lotes"])]
    assert len(codigos) == len(set(codigos))


def test_urgente_es_cero_o_uno_y_hay_de_ambos(tmp_path):
    rutas = gd.generar_archivos(tmp_path, 50, 10, 1000, semilla=5)
    valores = {f["urgente"] for f in leer(rutas["pedidos"])}
    assert valores == {"0", "1"}


def test_desordenar_cambia_el_orden_pero_no_los_ids(tmp_path):
    ordenado = gd.generar_archivos(tmp_path / "o", 80, 0, 0, semilla=9)
    revuelto = gd.generar_archivos(tmp_path / "r", 80, 0, 0, semilla=9, desordenar=True)
    ids_o = [int(f["id"]) for f in leer(ordenado["productos"])]
    ids_r = [int(f["id"]) for f in leer(revuelto["productos"])]
    assert ids_o == sorted(ids_o)
    assert ids_r != sorted(ids_r) and sorted(ids_r) == ids_o


def test_los_archivos_se_cargan_en_el_sistema_sin_errores(rutas):
    s = SistemaInventario()
    assert s.cargar_csv(str(rutas["productos"])) == 60
    assert s.cargar_lotes_csv(str(rutas["lotes"])) == 120
    assert s.cargar_pedidos_csv(str(rutas["pedidos"])) == 200


def test_productos_desordenados_se_cargan_y_usan_busqueda_lineal(tmp_path):
    r = gd.generar_archivos(tmp_path, 50, 0, 0, semilla=4, desordenar=True)
    s = SistemaInventario()
    s.cargar_csv(str(r["productos"]))
    assert s.ordenado_por_id is False
    assert s.buscar_por_id(25).id == 25


@pytest.mark.parametrize("args", [(0, 1, 1), (-5, 1, 1), (5, -1, 1), (5, 1, -1)])
def test_argumentos_invalidos_lanzan_error(args):
    with pytest.raises(ValueError):
        gd.generar(*args)


def test_crea_la_carpeta_de_salida_si_no_existe(tmp_path):
    destino = tmp_path / "no" / "existe"
    gd.generar_archivos(destino, 5, 5, 5)
    assert (destino / "productos.csv").exists()
