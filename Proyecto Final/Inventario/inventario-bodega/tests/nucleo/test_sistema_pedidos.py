from pathlib import Path

import pytest

from inventario.dominio.pedido import DESPACHADO, PENDIENTE, RECHAZADO, Pedido
from inventario.dominio.producto import Producto
from inventario.nucleo.sistema import CAPACIDAD_HISTORIAL, SistemaInventario
from tests.rutas import EJEMPLO

RAIZ = Path(__file__).resolve().parent.parent
RUTA_PRODUCTOS = EJEMPLO / "productos.csv"
RUTA_LOTES = EJEMPLO / "lotes.csv"
RUTA_PEDIDOS = EJEMPLO / "pedidos.csv"


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


def numeros(cola):
    return [pedido.numero for pedido in cola]


def detalle(tomas):
    return [tomas[i] for i in range(len(tomas))]


# ---------- Pedido ----------


def test_pedido_nuevo_esta_pendiente():
    pedido = Pedido(1, 7, 25)

    assert pedido.estado == PENDIENTE
    assert pedido.tomas is None
    assert pedido.motivo == ""
    assert "Pedido #1" in str(pedido)


@pytest.mark.parametrize("cantidad", [0, -4])
def test_pedido_con_cantidad_no_positiva_se_rechaza(cantidad):
    with pytest.raises(ValueError):
        Pedido(1, 7, cantidad)


# ---------- registrar y despachar pedidos ----------


def test_registrar_pedido_lo_pone_al_final_de_la_cola():
    sistema = sistema_con_dos()

    primero = sistema.registrar_pedido(1, 10)
    segundo = sistema.registrar_pedido(2, 5)

    assert (primero.numero, segundo.numero) == (1, 2)
    assert numeros(sistema.pedidos) == [1, 2]
    assert primero.estado == PENDIENTE


def test_registrar_pedido_de_producto_inexistente_devuelve_none():
    sistema = sistema_con_dos()

    assert sistema.registrar_pedido(99, 5) is None
    assert len(sistema.pedidos) == 0


def test_registrar_pedido_con_cantidad_invalida_no_consume_numero():
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.registrar_pedido(1, 0)

    assert len(sistema.pedidos) == 0
    assert sistema.registrar_pedido(1, 5).numero == 1


def test_despachar_siguiente_atiende_en_orden_de_llegada():
    sistema = sistema_con_dos()
    sistema.registrar_pedido(2, 5)
    sistema.registrar_pedido(1, 10)

    primero = sistema.despachar_siguiente()
    segundo = sistema.despachar_siguiente()

    assert (primero.numero, segundo.numero) == (1, 2)
    assert primero.id_producto == 2
    assert len(sistema.pedidos) == 0


def test_despachar_siguiente_descuenta_primero_el_lote_que_vence_antes():
    sistema = sistema_con_dos()
    sistema.registrar_lote(1, "1-2", 30, "2026-10-01", "2027-02-01")
    sistema.registrar_pedido(1, 40)

    pedido = sistema.despachar_siguiente()

    assert pedido.estado == DESPACHADO
    assert detalle(pedido.tomas) == [("1-2", 30), ("1-1", 10)]
    assert sistema.buscar_por_id(1).cantidad == 90


def test_pedido_sin_stock_suficiente_se_rechaza_y_no_bloquea_la_cola():
    sistema = sistema_con_dos()
    sistema.registrar_pedido(2, 500)
    sistema.registrar_pedido(1, 10)

    rechazado = sistema.despachar_siguiente()
    atendido = sistema.despachar_siguiente()

    assert rechazado.estado == RECHAZADO
    assert "Stock insuficiente" in rechazado.motivo
    assert rechazado.tomas is None
    assert sistema.buscar_por_id(2).cantidad == 50
    assert atendido.estado == DESPACHADO


def test_pedido_de_un_producto_eliminado_se_rechaza():
    sistema = sistema_con_dos()
    sistema.registrar_pedido(2, 5)
    sistema.eliminar_por_id(2)

    pedido = sistema.despachar_siguiente()

    assert pedido.estado == RECHAZADO
    assert "ya no existe" in pedido.motivo


def test_despachar_siguiente_sin_pedidos_devuelve_none():
    assert SistemaInventario().despachar_siguiente() is None


def test_pedido_por_todo_el_stock_deja_el_producto_sin_existencias():
    sistema = sistema_con_dos()
    sistema.registrar_pedido(2, 50)

    pedido = sistema.despachar_siguiente()

    assert pedido.estado == DESPACHADO
    assert sistema.buscar_por_id(2).cantidad == 0


# ---------- historial (cola circular) ----------


def test_el_historial_guarda_los_pedidos_resueltos_en_orden():
    sistema = sistema_con_dos()

    for _ in range(3):
        sistema.registrar_pedido(1, 1)
        sistema.despachar_siguiente()

    assert numeros(sistema.historial) == [1, 2, 3]


def test_el_historial_descarta_el_mas_antiguo_cuando_se_llena():
    sistema = sistema_con_dos()
    total = CAPACIDAD_HISTORIAL + 3

    for _ in range(total):
        sistema.registrar_pedido(1, 1)
        sistema.despachar_siguiente()

    assert len(sistema.historial) == CAPACIDAD_HISTORIAL
    assert numeros(sistema.historial) == list(range(4, total + 1))


def test_el_historial_incluye_los_pedidos_rechazados():
    sistema = sistema_con_dos()
    sistema.registrar_pedido(1, 9999)

    sistema.despachar_siguiente()

    assert [pedido.estado for pedido in sistema.historial] == [RECHAZADO]


# ---------- cargar pedidos desde CSV ----------


def escribir_pedidos(ruta, filas, fin_de_linea="\n", codificacion="utf-8"):
    contenido = fin_de_linea.join(["id_producto,cantidad"] + filas) + fin_de_linea
    ruta.write_text(contenido, encoding=codificacion, newline="")


def test_cargar_los_pedidos_reales_del_proyecto():
    sistema = SistemaInventario()
    sistema.cargar_csv(str(RUTA_PRODUCTOS))
    sistema.cargar_lotes_csv(str(RUTA_LOTES))

    cargados = sistema.cargar_pedidos_csv(str(RUTA_PEDIDOS))

    resueltos = []
    while not sistema.pedidos.esta_vacia():
        resueltos.append(sistema.despachar_siguiente())

    assert cargados == 6
    assert [pedido.numero for pedido in resueltos] == [1, 2, 3, 4, 5, 6]
    assert [pedido.estado for pedido in resueltos] == [
        DESPACHADO,
        DESPACHADO,
        DESPACHADO,
        DESPACHADO,
        DESPACHADO,
        RECHAZADO,
    ]
    assert numeros(sistema.historial) == [2, 3, 4, 5, 6]


def test_cargar_pedidos_conserva_el_orden_del_archivo(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    escribir_pedidos(ruta, ["2,5", "1,10", "2,7"])
    sistema = sistema_con_dos()

    sistema.cargar_pedidos_csv(str(ruta))

    assert [(p.id_producto, p.cantidad) for p in sistema.pedidos] == [
        (2, 5),
        (1, 10),
        (2, 7),
    ]


def test_cargar_pedidos_con_bom_y_saltos_de_linea_windows(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    escribir_pedidos(ruta, ["1,10"], fin_de_linea="\r\n", codificacion="utf-8-sig")
    sistema = sistema_con_dos()

    assert sistema.cargar_pedidos_csv(str(ruta)) == 1


def test_cargar_pedidos_solo_con_encabezado(tmp_path):
    ruta = tmp_path / "pedidos.csv"
    escribir_pedidos(ruta, [])
    sistema = sistema_con_dos()

    assert sistema.cargar_pedidos_csv(str(ruta)) == 0
    assert len(sistema.pedidos) == 0


@pytest.mark.parametrize("fila_mala", ["99,5", "1,0", "1,-3", "1,muchos", "uno,5"])
def test_cargar_pedidos_con_una_fila_invalida_no_encola_nada(tmp_path, fila_mala):
    ruta = tmp_path / "pedidos.csv"
    escribir_pedidos(ruta, ["1,10", fila_mala])
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.cargar_pedidos_csv(str(ruta))

    assert len(sistema.pedidos) == 0


def test_cargar_pedidos_con_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        sistema_con_dos().cargar_pedidos_csv(str(tmp_path / "no_existe.csv"))


# ---------- devoluciones (pila) ----------


def test_registrar_devolucion_agrega_un_lote_y_apila_el_registro():
    sistema = sistema_con_dos()

    devolucion = sistema.registrar_devolucion(1, 12, "2026-09-01", "2027-03-01")

    producto = sistema.buscar_por_id(1)
    assert devolucion.codigo_lote == "DEV-1"
    assert producto.cantidad == 112
    assert producto.fecha_vencimiento == "2027-03-01"
    assert len(sistema.devoluciones) == 1
    assert "Devolución #1" in str(devolucion)


def test_registrar_devolucion_de_producto_inexistente_devuelve_none():
    sistema = sistema_con_dos()

    assert sistema.registrar_devolucion(99, 5, "2026-09-01", "2027-03-01") is None
    assert len(sistema.devoluciones) == 0


def test_registrar_devolucion_con_datos_invalidos_no_apila_nada():
    sistema = sistema_con_dos()

    with pytest.raises(ValueError):
        sistema.registrar_devolucion(1, 0, "2026-09-01", "2027-03-01")

    with pytest.raises(ValueError):
        sistema.registrar_devolucion(1, 5, "2026-09-01", "pronto")

    assert len(sistema.devoluciones) == 0
    assert sistema.buscar_por_id(1).cantidad == 100
    assert sistema.registrar_devolucion(1, 5, "2026-09-01", "2027-03-01").numero == 1


def test_deshacer_devolucion_retira_el_lote():
    sistema = sistema_con_dos()
    sistema.registrar_devolucion(1, 12, "2026-09-01", "2027-03-01")

    deshecha = sistema.deshacer_ultima_devolucion()

    producto = sistema.buscar_por_id(1)
    assert deshecha.numero == 1
    assert producto.cantidad == 100
    assert producto.lotes.buscar("DEV-1") is None
    assert len(sistema.devoluciones) == 0


def test_se_deshace_primero_la_ultima_devolucion():
    sistema = sistema_con_dos()
    sistema.registrar_devolucion(1, 5, "2026-09-01", "2027-03-01")
    sistema.registrar_devolucion(2, 7, "2026-09-01", "2027-03-01")

    primera = sistema.deshacer_ultima_devolucion()
    segunda = sistema.deshacer_ultima_devolucion()

    assert (primera.numero, segunda.numero) == (2, 1)
    assert sistema.buscar_por_id(2).cantidad == 50
    assert sistema.buscar_por_id(1).cantidad == 100


def test_deshacer_sin_devoluciones_devuelve_none():
    assert SistemaInventario().deshacer_ultima_devolucion() is None


def test_deshacer_devolucion_cuyo_lote_ya_se_despacho_por_completo():
    sistema = sistema_con_dos()
    sistema.registrar_devolucion(1, 12, "2026-09-01", "2026-12-01")
    sistema.despachar_producto(1, 12)

    with pytest.raises(ValueError):
        sistema.deshacer_ultima_devolucion()

    assert len(sistema.devoluciones) == 0
    assert sistema.buscar_por_id(1).cantidad == 100


def test_deshacer_devolucion_cuyo_lote_se_despacho_en_parte_retira_lo_que_quedaba():
    sistema = sistema_con_dos()
    sistema.registrar_devolucion(1, 12, "2026-09-01", "2026-12-01")
    sistema.despachar_producto(1, 5)

    sistema.deshacer_ultima_devolucion()

    assert sistema.buscar_por_id(1).cantidad == 100


def test_deshacer_devolucion_de_un_producto_eliminado():
    sistema = sistema_con_dos()
    sistema.registrar_devolucion(2, 5, "2026-09-01", "2027-03-01")
    sistema.eliminar_por_id(2)

    with pytest.raises(ValueError):
        sistema.deshacer_ultima_devolucion()

    assert len(sistema.devoluciones) == 0


def test_los_numeros_de_devolucion_no_se_reutilizan_al_deshacer():
    sistema = sistema_con_dos()
    sistema.registrar_devolucion(1, 5, "2026-09-01", "2027-03-01")
    sistema.deshacer_ultima_devolucion()

    nueva = sistema.registrar_devolucion(1, 5, "2026-09-01", "2027-03-01")

    assert nueva.numero == 2
    assert nueva.codigo_lote == "DEV-2"
