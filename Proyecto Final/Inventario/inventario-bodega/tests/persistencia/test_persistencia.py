import sqlite3

import pytest

from inventario.dominio.pedido import DESPACHADO, RECHAZADO
from inventario.dominio.producto import Producto
from inventario.nucleo.sistema import SistemaInventario
from inventario.persistencia.repositorio_sqlite import RepositorioSQLite


def producto(id_, pasillo, estante, cantidad=10, vence="2027-01-01"):
    return Producto(
        id_,
        f"P{id_}",
        "cat",
        cantidad,
        2,
        "2026-01-01",
        vence,
        1500.5,
        pasillo,
        estante,
    )


def sistema_con_estado():
    s = SistemaInventario()
    s.agregar(producto(3, 0, 0))
    s.agregar(producto(1, 0, 1))
    s.agregar(producto(2, 1, 0, cantidad=0))
    s.registrar_lote(1, "A", 5, "2026-02-01", "2026-12-01")
    s.registrar_pedido(1, 4)
    s.registrar_pedido(1, 999)
    s.registrar_pedido(3, 1)
    s.despachar_siguiente()  # despachado
    s.despachar_siguiente()  # rechazado: stock insuficiente
    s.registrar_devolucion(3, 2, "2026-01-01", "2027-06-01")
    s.registrar_devolucion(1, 1, "2026-01-01", "2027-07-01")
    return s


def ida_y_vuelta(s, ruta=":memory:"):
    repo = RepositorioSQLite(ruta)
    repo.guardar(s)
    return repo, repo.cargar()


def test_base_vacia_da_sistema_vacio():
    repo = RepositorioSQLite(":memory:")
    s = repo.cargar()
    assert len(s.catalogo) == 0
    assert s.pedidos.esta_vacia()


def test_catalogo_conserva_orden_y_bandera():
    original = sistema_con_estado()
    _, nuevo = ida_y_vuelta(original)
    assert [nuevo.catalogo[i].id for i in range(3)] == [3, 1, 2]
    assert nuevo.ordenado_por_id is False
    assert nuevo.buscar_por_id(2).id == 2


def test_lotes_y_stock_se_recuperan():
    original = sistema_con_estado()
    _, nuevo = ida_y_vuelta(original)
    for id_ in (1, 2, 3):
        a, b = original.buscar_por_id(id_), nuevo.buscar_por_id(id_)
        assert [str(x) for x in a.lotes] == [str(x) for x in b.lotes]
        assert a.cantidad == b.cantidad
        assert a.fecha_vencimiento == b.fecha_vencimiento
    assert nuevo.buscar_por_id(2).cantidad == 0


def test_ubicaciones_se_recuperan():
    _, nuevo = ida_y_vuelta(sistema_con_estado())
    assert nuevo.consultar_ubicacion(0, 1).id == 1
    assert nuevo.consultar_ubicacion(1, 0).id == 2


def test_pedidos_pendientes_conservan_orden_y_contador():
    s = SistemaInventario()
    s.agregar(producto(1, 0, 0))
    s.registrar_pedido(1, 1)
    s.registrar_pedido(1, 2)
    _, nuevo = ida_y_vuelta(s)
    assert [p.numero for p in nuevo.pedidos] == [1, 2]
    assert nuevo.registrar_pedido(1, 3).numero == 3


def test_historial_conserva_estado_motivo_y_tomas():
    original = sistema_con_estado()
    _, nuevo = ida_y_vuelta(original)
    hist = list(nuevo.historial)
    assert [p.estado for p in hist] == [DESPACHADO, RECHAZADO]
    assert hist[0].tomas is not None and len(hist[0].tomas) >= 1
    assert hist[1].tomas is None
    assert hist[1].motivo == list(original.historial)[1].motivo


def test_pila_de_devoluciones_conserva_la_cima():
    original = sistema_con_estado()
    _, nuevo = ida_y_vuelta(original)
    assert [d.numero for d in nuevo.devoluciones] == [2, 1]
    deshecha = nuevo.deshacer_ultima_devolucion()
    assert deshecha.numero == 2
    assert nuevo.buscar_por_id(1).lotes.buscar("DEV-2") is None
    assert nuevo.registrar_devolucion(1, 1, "2026-01-01", "2027-08-01").numero == 3


def test_el_estado_recuperado_sigue_funcionando():
    _, nuevo = ida_y_vuelta(sistema_con_estado())
    assert nuevo.registrar_pedido(3, 1) is not None
    assert nuevo.despachar_siguiente().estado == DESPACHADO


def test_guardar_dos_veces_reemplaza_no_duplica():
    s = sistema_con_estado()
    repo, _ = ida_y_vuelta(s)
    repo.guardar(s)
    nuevo = repo.cargar()
    assert len(nuevo.catalogo) == 3


def test_persiste_en_archivo(tmp_path):
    ruta = str(tmp_path / "inv.db")
    repo = RepositorioSQLite(ruta)
    repo.guardar(sistema_con_estado())
    repo.cerrar()
    nuevo = RepositorioSQLite(ruta).cargar()
    assert len(nuevo.catalogo) == 3


def test_guardado_fallido_no_deja_la_base_a_medias():
    s = sistema_con_estado()
    repo, _ = ida_y_vuelta(s)
    s.catalogo[0].nombre = None  # viola NOT NULL en mitad del guardado
    with pytest.raises(sqlite3.IntegrityError):
        repo.guardar(s)
    assert len(repo.cargar().catalogo) == 3
