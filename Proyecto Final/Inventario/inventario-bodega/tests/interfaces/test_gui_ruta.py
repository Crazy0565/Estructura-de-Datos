import pytest

tk = pytest.importorskip("tkinter")

from inventario.interfaces import gui
from inventario.nucleo.sistema import SistemaInventario
from inventario.persistencia.repositorio_sqlite import RepositorioSQLite
from tests.interfaces.test_gui import alta, llenar


@pytest.fixture
def app():
    try:
        ventana = gui.AplicacionInventario(
            SistemaInventario(), RepositorioSQLite(":memory:")
        )
    except tk.TclError:
        pytest.skip("No hay pantalla disponible para tkinter")
    yield ventana
    ventana.destroy()


def preparar(app):
    for i, (pasillo, estante) in enumerate([(0, 5), (3, 1), (0, 1), (3, 5)], start=1):
        assert alta(app, id_=i, pasillo=pasillo, estante=estante)
        app.sistema.registrar_lote(i, "L", 50, "2026-01-01", "2027-01-01")


def test_pedido_urgente_aparece_primero(app):
    preparar(app)
    llenar(app, "pedido", id=1, cantidad=1, urgencia="")
    app.registrar_pedido()
    llenar(app, "pedido", id=2, cantidad=1, urgencia=5)
    app.registrar_pedido()
    filas = [
        app.tabla_pedidos.item(i, "values") for i in app.tabla_pedidos.get_children()
    ]
    assert [f[0] for f in filas] == ["2", "1"]
    assert filas[0][3] == "5"


def test_calcular_ruta_muestra_resumen_sin_despachar(app):
    preparar(app)
    for i in range(1, 5):
        app.sistema.registrar_pedido(i, 1)
    llenar(app, "ruta", cantidad=4)
    assert app.calcular_ruta()
    assert "Ahorro" in app.resumen_ruta.get()
    assert len(app.tabla_ruta.get_children()) == 4
    assert app.sistema.total_pendientes() == 4


def test_despachar_ola_consume_pedidos(app):
    preparar(app)
    for i in range(1, 5):
        app.sistema.registrar_pedido(i, 1)
    llenar(app, "ruta", cantidad=3)
    assert app.despachar_ola()
    assert app.sistema.total_pendientes() == 1


def test_ola_sin_pedidos_da_error(app):
    assert not app.despachar_ola()
    assert app.estado.get().startswith("Error")
