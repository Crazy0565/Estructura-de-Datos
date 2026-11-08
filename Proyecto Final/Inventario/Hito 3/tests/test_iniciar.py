from iniciar import preparar_base, resumen
from sistema import SistemaInventario


def test_arranque_crea_base_y_la_reutiliza(tmp_path):
    db, datos = str(tmp_path / "i.db"), str(tmp_path / "datos")
    primero = preparar_base(db, datos, productos=60, reiniciar=False)
    assert len(primero.catalogo) == 60
    assert primero.total_pendientes() == 180
    assert len(primero.urgentes) > 0  # la columna urgente del CSV se respeta
    segundo = preparar_base(db, datos, productos=999, reiniciar=False)
    assert len(segundo.catalogo) == 60  # reutiliza la base, no regenera
    assert "Productos: 60" in resumen(segundo)


def test_reiniciar_regenera(tmp_path):
    db, datos = str(tmp_path / "i.db"), str(tmp_path / "datos")
    preparar_base(db, datos, productos=20, reiniciar=False)
    nuevo = preparar_base(db, datos, productos=30, reiniciar=True)
    assert len(nuevo.catalogo) == 30


def test_pedidos_csv_urgentes(tmp_path):
    ruta = tmp_path / "p.csv"
    ruta.write_text("id_producto,cantidad,urgente\n1,1,0\n1,1,1\n", encoding="utf-8")
    s = SistemaInventario()
    from producto import Producto

    s.agregar(Producto(1, "A", "c", 1, 1, "2026-01-01", "2027-01-01", 1.0, 0, 0))
    assert s.cargar_pedidos_csv(str(ruta)) == 2
    assert len(s.urgentes) == 1 and len(s.pedidos) == 1
