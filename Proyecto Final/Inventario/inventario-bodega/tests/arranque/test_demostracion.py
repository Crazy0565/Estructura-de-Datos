from inventario.demostracion import (
    cargar_sistema,
    cumple_fefo,
    despachar_verificado,
    medir_rutas,
)
from inventario.estructuras.arreglo import ArregloDinamico
from inventario.estructuras.lista_lotes import ListaLotes

FOTO = [("A", 5, "2026-03-01"), ("B", 5, "2026-06-01"), ("C", 5, "2026-09-01")]


def test_verificador_acepta_fefo_correcto():
    assert cumple_fefo(FOTO, [("A", 5), ("B", 2)], 7)
    assert cumple_fefo(FOTO, [("A", 3)], 3)


def test_verificador_rechaza_violaciones():
    assert not cumple_fefo(FOTO, [("B", 3)], 3)  # saltó el que vence antes
    assert not cumple_fefo(FOTO, [("A", 3), ("B", 2)], 5)  # A no se vació
    assert not cumple_fefo(FOTO, [("A", 5), ("B", 2)], 8)  # no suma lo pedido
    assert not cumple_fefo(FOTO, [("A", 6)], 6)  # más de lo que tenía
    assert not cumple_fefo(FOTO, [("Z", 1)], 1)  # lote inexistente


def test_demostracion_pequena_cumple_y_detecta_sabotaje(tmp_path, monkeypatch):
    sistema = cargar_sistema(str(tmp_path), 80)
    ok = {"despachados": 0, "rechazados": 0, "violaciones": 0}
    medir_rutas(sistema, 1, ok)

    while sistema.total_pendientes() > 0:
        despachar_verificado(sistema, ok)

    assert ok["despachados"] > 0 and ok["violaciones"] == 0

    # Sabotaje: un despacho que toma del lote que vence DE ÚLTIMO debe detectarse.
    def despachar_mal(self, cantidad):
        lotes = [lote for lote in self]
        lote = lotes[-1]
        lote.cantidad -= cantidad
        tomas = ArregloDinamico()
        tomas.agregar((lote.codigo, cantidad))
        return tomas

    monkeypatch.setattr(ListaLotes, "despachar", despachar_mal)
    malo = cargar_sistema(str(tmp_path), 80)
    res = {"despachados": 0, "rechazados": 0, "violaciones": 0}

    for _ in range(20):
        despachar_verificado(malo, res)

    assert res["violaciones"] > 0
