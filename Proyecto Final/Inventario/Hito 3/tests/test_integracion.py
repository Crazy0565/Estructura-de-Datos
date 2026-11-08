import pytest

from cola_prioridad import ColaPrioridad
from pedido import DESPACHADO, Pedido
from persistencia import RepositorioSQLite
from producto import Producto
from sistema import SistemaInventario


def producto(id_, pasillo, estante, cantidad=10):
    return Producto(
        id_,
        f"P{id_}",
        "cat",
        cantidad,
        2,
        "2026-01-01",
        "2027-01-01",
        10.0,
        pasillo,
        estante,
    )


def sistema_base():
    s = SistemaInventario()
    for i in range(1, 7):
        s.agregar(producto(i, i % 3, i))
        s.registrar_lote(i, "L1", 100, "2026-01-01", "2027-01-01")
    return s


def numeros(arreglo):
    return [arreglo[i].numero for i in range(len(arreglo))]


def test_urgentes_salen_antes_y_por_urgencia():
    s = sistema_base()
    normal = s.registrar_pedido(1, 1)
    u1 = s.registrar_pedido(2, 1, urgencia=1)
    u3 = s.registrar_pedido(3, 1, urgencia=3)
    u1b = s.registrar_pedido(4, 1, urgencia=1)
    salida = [s.despachar_siguiente().numero for _ in range(4)]
    assert salida == [u3.numero, u1.numero, u1b.numero, normal.numero]


def test_total_y_siguientes_no_consumen():
    s = sistema_base()
    s.registrar_pedido(1, 1)
    s.registrar_pedido(2, 1, urgencia=2)
    s.registrar_pedido(3, 1)
    antes = s.total_pendientes()
    vista = s.siguientes_pedidos(2)
    assert numeros(vista) == [2, 1]
    assert s.total_pendientes() == antes == 3
    assert numeros(s.siguientes_pedidos(10)) == [2, 1, 3]


def test_urgencia_invalida():
    s = sistema_base()
    with pytest.raises(ValueError):
        s.registrar_pedido(1, 1, urgencia=10)
    with pytest.raises(ValueError):
        Pedido(1, 1, 1, urgencia=-1)


def test_en_orden_cola_prioridad_no_destructivo_y_estable():
    c = ColaPrioridad()
    for prioridad, dato in [(2, "a"), (1, "b"), (2, "c"), (1, "d")]:
        c.encolar(prioridad, dato)
    vista = c.en_orden()
    assert [vista[i] for i in range(len(vista))] == ["b", "d", "a", "c"]
    assert len(c) == 4
    c.encolar(1, "e")
    assert c.desencolar() == "b"
    assert len(c.en_orden(2)) == 2


def test_indice_avl_sincronizado():
    s = SistemaInventario()
    for i in (5, 3, 9, 1):
        s.agregar(producto(i, 0, i))
    assert not s.ordenado_por_id
    assert s.buscar_indexado(9).id == 9
    s.eliminar_por_id(9)
    assert s.buscar_indexado(9) is None
    assert len(s.indice) == 3


def test_despachar_ola_cumple_fefo_y_devuelve_ruta():
    s = sistema_base()
    s.registrar_lote(1, "L0", 5, "2026-01-01", "2026-06-01")  # vence antes
    for i in range(1, 6):
        s.registrar_pedido(i, 1 if i != 1 else 3)
    resueltos, ruta = s.despachar_ola(5)
    assert len(resueltos) == 5
    assert all(resueltos[i].estado == DESPACHADO for i in range(5))
    primero = resueltos[0].tomas[0]
    assert primero[0] == "L0" if isinstance(primero, tuple) else primero.codigo == "L0"
    assert ruta is not None
    assert ruta.distancia_optima <= ruta.distancia_llegada
    assert s.total_pendientes() == 0


def test_ruta_sin_pedidos_es_none():
    assert sistema_base().ruta_de_recoleccion(5) is None
    resueltos, ruta = sistema_base().despachar_ola(3)
    assert len(resueltos) == 0 and ruta is None


def test_plano_se_reconstruye_si_crece_la_bodega():
    s = SistemaInventario()
    s.agregar(producto(1, 0, 0))
    lado = s.plano().lado
    s.agregar(producto(2, 25, 25))
    assert s.plano().lado > lado


def test_persistencia_conserva_urgentes(tmp_path):
    s = sistema_base()
    s.registrar_pedido(1, 1)
    s.registrar_pedido(2, 1, urgencia=4)
    s.registrar_pedido(3, 1, urgencia=7)
    repo = RepositorioSQLite(str(tmp_path / "x.db"))
    repo.guardar(s)
    nuevo = repo.cargar()
    repo.cerrar()
    assert len(nuevo.urgentes) == 2 and len(nuevo.pedidos) == 1
    assert numeros(nuevo.siguientes_pedidos(3)) == [3, 2, 1]
