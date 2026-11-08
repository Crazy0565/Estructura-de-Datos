import pytest

from inventario.interfaces import consola
from inventario.nucleo.sistema import SistemaInventario
from tests.rutas import EJEMPLO, RAIZ


def simular_entradas(monkeypatch, respuestas):
    iterador = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda _mensaje="": next(iterador))


@pytest.fixture(autouse=True)
def base_temporal(monkeypatch, tmp_path):
    monkeypatch.setattr(consola, "RUTA_DB", str(tmp_path / "inventario.db"))


def test_leer_entero_repite_hasta_recibir_un_numero(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["abc", "", "42"])

    assert consola.leer_entero("N: ") == 42
    assert capsys.readouterr().out.count("número entero") == 2


def test_leer_decimal_repite_hasta_recibir_un_numero(monkeypatch):
    simular_entradas(monkeypatch, ["x", "12.5"])

    assert consola.leer_decimal("P: ") == 12.5


def test_agregar_producto_por_consola(monkeypatch, capsys):
    simular_entradas(
        monkeypatch,
        [
            "7",
            "Arroz",
            "Alimentos",
            "10",
            "2",
            "2026-09-01",
            "2027-09-01",
            "4500",
            "1",
            "2",
        ],
    )
    sistema = SistemaInventario()

    consola.agregar_producto(sistema)

    assert sistema.buscar_por_id(7).nombre == "Arroz"
    assert "agregado correctamente" in capsys.readouterr().out


def test_agregar_en_ubicacion_ocupada_muestra_el_error(monkeypatch, capsys):
    datos = [
        "Arroz",
        "Alimentos",
        "10",
        "2",
        "2026-09-01",
        "2027-09-01",
        "4500",
        "1",
        "2",
    ]
    simular_entradas(monkeypatch, ["7"] + datos + ["8"] + datos)
    sistema = SistemaInventario()

    consola.agregar_producto(sistema)
    consola.agregar_producto(sistema)

    assert len(sistema.catalogo) == 1
    assert "No se pudo agregar" in capsys.readouterr().out


def test_consultar_ubicacion_fuera_de_la_bodega_no_se_cae(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["99", "99"])

    consola.consultar_ubicacion(SistemaInventario())

    assert "fuera de la bodega" in capsys.readouterr().out


def test_cargar_datos_sin_archivo_muestra_mensaje(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    consola.cargar_datos(SistemaInventario())

    assert "No se encontró" in capsys.readouterr().out


def test_recorrido_completo_del_menu(monkeypatch, capsys):
    monkeypatch.chdir(RAIZ)
    simular_entradas(
        monkeypatch, ["6", "5", "2", "3", "4", "0", "0", "3", "1", "8", "x", "0"]
    )

    consola.main()

    salida = capsys.readouterr().out

    assert "Se cargaron" in salida
    assert "Producto encontrado (búsqueda binaria)" in salida
    assert "Producto ubicado" in salida
    assert "Producto eliminado correctamente" in salida
    assert "Opción inválida." in salida
    assert "Saliendo del sistema..." in salida


def entrar_a_la_carpeta_del_proyecto(monkeypatch):
    monkeypatch.chdir(RAIZ)


def test_recorrido_de_lotes_por_el_menu(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    simular_entradas(
        monkeypatch, ["6", "12", "10", "1", "11", "1", "130", "10", "1", "0"]
    )

    consola.main()

    salida = capsys.readouterr().out

    assert "Se cargaron 8 lotes correctamente." in salida
    assert "Total disponible: 200 unidades" in salida
    assert "60 unidades del lote 1-2" in salida
    assert "70 unidades del lote 1-1" in salida
    assert "Total disponible: 70 unidades" in salida


def test_registrar_lote_por_consola(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    sistema = SistemaInventario()
    sistema.cargar_csv(str(EJEMPLO / "productos.csv"))
    simular_entradas(monkeypatch, ["1", "L-9", "25", "2026-10-01", "2027-01-01"])

    consola.registrar_lote(sistema)

    assert sistema.buscar_por_id(1).cantidad == 125
    assert "Lote registrado correctamente." in capsys.readouterr().out


def test_registrar_lote_invalido_muestra_el_error(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    sistema = SistemaInventario()
    sistema.cargar_csv(str(EJEMPLO / "productos.csv"))
    simular_entradas(monkeypatch, ["1", "L-9", "25", "2026-10-01", "pronto"])

    consola.registrar_lote(sistema)

    assert sistema.buscar_por_id(1).cantidad == 100
    assert "No se pudo registrar el lote" in capsys.readouterr().out


def test_registrar_lote_en_producto_inexistente(monkeypatch, capsys):
    sistema = SistemaInventario()
    simular_entradas(monkeypatch, ["99", "L-9", "25", "2026-10-01", "2027-01-01"])

    consola.registrar_lote(sistema)

    assert "Producto no encontrado." in capsys.readouterr().out


def test_ver_lotes_de_producto_inexistente_o_sin_lotes(monkeypatch, capsys):
    sistema = SistemaInventario()
    simular_entradas(monkeypatch, ["99"])
    consola.ver_lotes(sistema)
    assert "Producto no encontrado." in capsys.readouterr().out

    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    sistema.cargar_csv(str(EJEMPLO / "productos.csv"))
    sistema.despachar_producto(1, 100)
    simular_entradas(monkeypatch, ["1"])
    consola.ver_lotes(sistema)
    assert "Sin lotes." in capsys.readouterr().out


def test_despachar_mas_del_stock_muestra_el_error(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    sistema = SistemaInventario()
    sistema.cargar_csv(str(EJEMPLO / "productos.csv"))
    simular_entradas(monkeypatch, ["1", "1000"])

    consola.despachar_unidades(sistema)

    assert "No se pudo despachar" in capsys.readouterr().out
    assert sistema.buscar_por_id(1).cantidad == 100


def test_despachar_producto_inexistente(monkeypatch, capsys):
    simular_entradas(monkeypatch, ["99", "5"])

    consola.despachar_unidades(SistemaInventario())

    assert "Producto no encontrado." in capsys.readouterr().out


def test_cargar_lotes_sin_archivo_muestra_mensaje(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    consola.cargar_lotes(SistemaInventario())

    assert "No se encontró" in capsys.readouterr().out


def test_cargar_lotes_dos_veces_muestra_el_error(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    sistema = SistemaInventario()
    sistema.cargar_csv(str(EJEMPLO / "productos.csv"))

    consola.cargar_lotes(sistema)
    consola.cargar_lotes(sistema)

    salida = capsys.readouterr().out
    assert "Se cargaron 8 lotes correctamente." in salida
    assert "No se pudo cargar el archivo" in salida


def test_agregar_producto_con_fecha_invalida_no_se_cae(monkeypatch, capsys):
    simular_entradas(
        monkeypatch,
        [
            "7",
            "Arroz",
            "Alimentos",
            "10",
            "2",
            "2026-09-01",
            "no-es-fecha",
            "4500",
            "1",
            "2",
        ],
    )
    sistema = SistemaInventario()

    consola.agregar_producto(sistema)

    assert len(sistema.catalogo) == 0
    assert "No se pudo agregar" in capsys.readouterr().out


def sistema_con_datos_reales(monkeypatch):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    sistema = SistemaInventario()
    sistema.cargar_csv(str(EJEMPLO / "productos.csv"))
    sistema.cargar_lotes_csv(str(EJEMPLO / "lotes.csv"))
    return sistema


def test_recorrido_de_pedidos_por_el_menu(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    simular_entradas(monkeypatch, ["6", "12", "17", "15"] + ["14"] * 7 + ["16", "0"])

    consola.main()

    salida = capsys.readouterr().out

    assert "Se cargaron 6 pedidos correctamente." in salida
    assert "Pedidos pendientes (el primero se atiende antes):" in salida
    assert "60 unidades del lote 1-2" in salida
    assert "Estado: rechazado (Stock insuficiente: hay 50 y se piden 70.)" in salida
    assert "No hay pedidos pendientes." in salida
    assert "Últimos despachos (máximo 5):" in salida


def test_recorrido_de_devoluciones_por_el_menu(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    simular_entradas(
        monkeypatch,
        ["6", "18", "1", "20", "2026-10-01", "2027-05-01", "10", "1", "19", "19", "0"],
    )

    consola.main()

    salida = capsys.readouterr().out

    assert "Devolución #1 registrada como lote DEV-1." in salida
    assert "Lote DEV-1 | Cantidad: 20" in salida
    assert "Devolución #1 revertida (lote DEV-1 retirado)." in salida
    assert "No hay devoluciones para deshacer." in salida


def test_registrar_pedido_por_consola(monkeypatch, capsys):
    sistema = sistema_con_datos_reales(monkeypatch)
    simular_entradas(monkeypatch, ["1", "10"])

    consola.registrar_pedido(sistema)

    assert len(sistema.pedidos) == 1
    assert "Pedido #1 registrado. En espera: 1." in capsys.readouterr().out


def test_registrar_pedido_invalido_o_de_producto_inexistente(monkeypatch, capsys):
    sistema = sistema_con_datos_reales(monkeypatch)

    simular_entradas(monkeypatch, ["1", "0"])
    consola.registrar_pedido(sistema)
    assert "No se pudo registrar el pedido" in capsys.readouterr().out

    simular_entradas(monkeypatch, ["99", "5"])
    consola.registrar_pedido(sistema)
    assert "Producto no encontrado." in capsys.readouterr().out

    assert len(sistema.pedidos) == 0


def test_despachar_siguiente_sin_pedidos(monkeypatch, capsys):
    consola.despachar_siguiente_pedido(SistemaInventario())

    assert "No hay pedidos pendientes." in capsys.readouterr().out


def test_ver_pedidos_e_historial_vacios(capsys):
    sistema = SistemaInventario()

    consola.ver_pedidos(sistema)
    consola.ver_historial(sistema)

    salida = capsys.readouterr().out
    assert "No hay pedidos pendientes." in salida
    assert "Todavía no hay despachos." in salida


def test_cargar_pedidos_sin_archivo_muestra_mensaje(monkeypatch, capsys, tmp_path):
    monkeypatch.chdir(tmp_path)

    consola.cargar_pedidos(SistemaInventario())

    assert "No se encontró" in capsys.readouterr().out


def test_cargar_pedidos_con_producto_inexistente_muestra_el_error(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)

    consola.cargar_pedidos(SistemaInventario())

    assert "No se pudo cargar el archivo" in capsys.readouterr().out


def test_registrar_devolucion_invalida_o_de_producto_inexistente(monkeypatch, capsys):
    sistema = sistema_con_datos_reales(monkeypatch)

    simular_entradas(monkeypatch, ["1", "5", "2026-10-01", "no-es-fecha"])
    consola.registrar_devolucion(sistema)
    assert "No se pudo registrar la devolución" in capsys.readouterr().out

    simular_entradas(monkeypatch, ["99", "5", "2026-10-01", "2027-01-01"])
    consola.registrar_devolucion(sistema)
    assert "Producto no encontrado." in capsys.readouterr().out

    assert len(sistema.devoluciones) == 0


def test_deshacer_devolucion_ya_despachada_muestra_el_error(monkeypatch, capsys):
    sistema = sistema_con_datos_reales(monkeypatch)
    sistema.registrar_devolucion(1, 5, "2026-10-01", "2026-12-01")
    sistema.despachar_producto(1, 5)

    consola.deshacer_devolucion(sistema)

    assert "No se pudo revertir" in capsys.readouterr().out


def test_la_informacion_incluye_pedidos_y_devoluciones(capsys):
    sistema = SistemaInventario()

    consola.mostrar_informacion(sistema)

    salida = capsys.readouterr().out
    assert "Pedidos pendientes: 0" in salida
    assert "Devoluciones que se pueden revertir: 0" in salida


def test_los_datos_sobreviven_entre_ejecuciones(monkeypatch, capsys):
    entrar_a_la_carpeta_del_proyecto(monkeypatch)
    simular_entradas(monkeypatch, ["6", "0"])
    consola.main()
    capsys.readouterr()

    simular_entradas(monkeypatch, ["8", "0"])
    consola.main()

    salida = capsys.readouterr().out

    assert "Se recuperaron 5 productos" in salida
    assert "Arroz Diana" in salida
