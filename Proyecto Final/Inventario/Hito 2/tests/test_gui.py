import pytest

tk = pytest.importorskip("tkinter")

import gui
from persistencia import RepositorioSQLite
from sistema import SistemaInventario


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


def llenar(app, formulario, **valores):
    for clave, valor in valores.items():
        app.vars[formulario][clave].set(str(valor))


def alta(app, id_=1, pasillo=0, estante=0, cantidad=10):
    llenar(
        app,
        "producto",
        id=id_,
        nombre=f"P{id_}",
        categoria="cat",
        cantidad=cantidad,
        tiempo=2,
        fprod="2026-01-01",
        fvenc="2027-01-01",
        precio="1500.5",
        pasillo=pasillo,
        estante=estante,
    )
    return app.agregar_producto()


def test_agregar_producto_aparece_en_la_tabla(app):
    assert alta(app)
    assert len(app.tabla_catalogo.get_children()) == 1
    assert "agregado" in app.estado.get()


def test_dato_invalido_muestra_error_y_no_agrega(app):
    llenar(app, "producto", id="abc")
    assert not app.agregar_producto()
    assert app.estado.get().startswith("Error")
    assert len(app.sistema.catalogo) == 0


def test_id_repetido_y_ubicacion_ocupada_se_rechazan(app):
    alta(app, 1, 0, 0)
    assert not alta(app, 1, 1, 1)
    assert "Ya existe" in app.estado.get()
    assert not alta(app, 2, 0, 0)
    assert len(app.sistema.catalogo) == 1


def test_buscar_indica_el_tipo_de_busqueda(app):
    alta(app, 1, 0, 0)
    app.var_buscar.set("1")
    app.buscar_producto()
    assert "binaria" in app.estado.get()
    alta(app, 0, 0, 1)  # rompe el orden por ID
    app.var_buscar.set("1")
    app.buscar_producto()
    assert "lineal" in app.estado.get()


def test_ordenar_cambia_el_orden_de_la_tabla(app):
    alta(app, 3, 0, 0)
    alta(app, 1, 0, 1)
    app.var_orden.set("id")
    app.ordenar()
    ids = [
        app.tabla_catalogo.item(i, "values")[0]
        for i in app.tabla_catalogo.get_children()
    ]
    assert ids == ["1", "3"]


def test_eliminar_seleccionado(app):
    alta(app, 1, 0, 0)
    assert not app.eliminar_seleccionado()
    fila = app.tabla_catalogo.get_children()[0]
    app.tabla_catalogo.selection_set(fila)
    assert app.eliminar_seleccionado()
    assert len(app.sistema.catalogo) == 0


def test_lote_y_despacho_primero_vence_primero_sale(app):
    alta(app, 1, 0, 0, cantidad=10)  # lote 1-1 vence 2027-01-01
    llenar(
        app,
        "lote",
        id=1,
        codigo="A",
        cantidad=5,
        fprod="2026-01-01",
        fvenc="2026-06-01",
    )
    assert app.registrar_lote()
    assert len(app.tabla_lotes.get_children()) == 2
    app.var_despacho.set("7")
    assert app.despachar_unidades()
    assert "5 de A" in app.estado.get() and "2 de 1-1" in app.estado.get()


def test_despacho_sin_stock_suficiente_da_error(app):
    alta(app, 1, 0, 0, cantidad=2)
    llenar(app, "lote", id=1)
    app.var_despacho.set("50")
    assert not app.despachar_unidades()
    assert app.sistema.buscar_por_id(1).cantidad == 2


def test_pedidos_cola_e_historial(app):
    alta(app, 1, 0, 0, cantidad=10)
    llenar(app, "pedido", id=1, cantidad=4)
    app.registrar_pedido()
    llenar(app, "pedido", id=1, cantidad=99)
    app.registrar_pedido()
    assert len(app.tabla_pedidos.get_children()) == 2
    app.despachar_siguiente()
    app.despachar_siguiente()
    assert len(app.tabla_pedidos.get_children()) == 0
    estados = [
        app.tabla_historial.item(i, "values")[3]
        for i in app.tabla_historial.get_children()
    ]
    assert estados == ["despachado", "rechazado"]
    assert not app.despachar_siguiente()


def test_pedido_de_producto_inexistente(app):
    llenar(app, "pedido", id=9, cantidad=1)
    assert not app.registrar_pedido()


def test_devolucion_y_deshacer(app):
    alta(app, 1, 0, 0, cantidad=1)
    llenar(app, "devolucion", id=1, cantidad=3, fprod="2026-01-01", fvenc="2027-06-01")
    assert app.registrar_devolucion()
    assert app.sistema.buscar_por_id(1).cantidad == 4
    assert len(app.tabla_devoluciones.get_children()) == 1
    assert app.deshacer_devolucion()
    assert app.sistema.buscar_por_id(1).cantidad == 1
    assert not app.deshacer_devolucion()


def test_cargar_csv_y_guardado_en_la_base(app):
    from pathlib import Path

    carpeta = Path(gui.__file__).resolve().parent
    assert app.cargar_csv("productos", str(carpeta / "productos.csv"))
    assert app.cargar_csv("lotes", str(carpeta / "lotes.csv"))
    assert app.cargar_csv("pedidos", str(carpeta / "pedidos.csv"))
    assert len(app.tabla_catalogo.get_children()) == 5
    assert len(app.tabla_pedidos.get_children()) == 6
    assert len(app.repositorio.cargar().catalogo) == 5


def test_csv_inexistente_no_rompe_la_ventana(app):
    assert not app.cargar_csv("productos", "no_existe.csv")
    assert app.estado.get().startswith("Error")
