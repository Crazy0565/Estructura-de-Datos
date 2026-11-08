import generador_datos as gd
import medicion_escala as me
from sistema import SistemaInventario


def test_la_medicion_corre_con_datos_pequenos(tmp_path, capsys):
    gd.generar_archivos(tmp_path, productos=30, lotes=40, pedidos=50, semilla=1)
    me.main(str(tmp_path))
    salida = capsys.readouterr().out
    assert "Cargar productos" in salida
    assert "Despachar todos los pedidos" in salida


def test_despachar_todo_vacia_la_cola(tmp_path):
    rutas = gd.generar_archivos(tmp_path, productos=20, lotes=0, pedidos=25, semilla=2)
    s = SistemaInventario()
    s.cargar_csv(str(rutas["productos"]))
    s.cargar_pedidos_csv(str(rutas["pedidos"]))
    assert me.despachar_todo(s) == 25
    assert s.pedidos.esta_vacia()
