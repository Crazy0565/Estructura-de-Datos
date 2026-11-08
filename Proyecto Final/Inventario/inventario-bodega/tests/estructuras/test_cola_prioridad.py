import heapq
import random

import pytest

from inventario.estructuras.cola_prioridad import ColaPrioridad


def vaciar(cola):
    salida = []
    while not cola.esta_vacia():
        salida.append(cola.desencolar())
    return salida


def test_cola_nueva_esta_vacia():
    cola = ColaPrioridad()
    assert cola.esta_vacia() and len(cola) == 0


def test_desencolar_y_frente_en_cola_vacia_lanzan_error():
    cola = ColaPrioridad()
    with pytest.raises(IndexError):
        cola.desencolar()
    with pytest.raises(IndexError):
        cola.frente()
    with pytest.raises(IndexError):
        cola.desencolar_con_prioridad()


def test_sale_primero_el_de_menor_numero():
    cola = ColaPrioridad()
    for prioridad, dato in [(5, "e"), (1, "a"), (3, "c"), (2, "b"), (4, "d")]:
        cola.encolar(prioridad, dato)
    assert len(cola) == 5
    assert vaciar(cola) == ["a", "b", "c", "d", "e"]


def test_frente_no_quita_el_elemento():
    cola = ColaPrioridad()
    cola.encolar(2, "x")
    cola.encolar(1, "y")
    assert cola.frente() == "y" and len(cola) == 2


def test_prioridades_iguales_salen_en_orden_de_llegada():
    cola = ColaPrioridad()
    for i in range(20):
        cola.encolar(1, f"n{i}")
    assert vaciar(cola) == [f"n{i}" for i in range(20)]


def test_urgentes_pasan_adelante_pero_cada_nivel_conserva_su_orden():
    cola = ColaPrioridad()
    for nombre, prioridad in [("a", 1), ("b", 0), ("c", 1), ("d", 0), ("e", 1)]:
        cola.encolar(prioridad, nombre)
    assert vaciar(cola) == ["b", "d", "a", "c", "e"]


def test_desencolar_con_prioridad_devuelve_ambos():
    cola = ColaPrioridad()
    cola.encolar(7.5, "x")
    assert cola.desencolar_con_prioridad() == (7.5, "x")


def test_acepta_prioridades_decimales_y_negativas():
    cola = ColaPrioridad()
    for p, d in [(0.5, "b"), (-2, "a"), (3.25, "c")]:
        cola.encolar(p, d)
    assert vaciar(cola) == ["a", "b", "c"]


def test_intercalar_encolar_y_desencolar():
    cola = ColaPrioridad()
    cola.encolar(3, "c")
    cola.encolar(1, "a")
    assert cola.desencolar() == "a"
    cola.encolar(2, "b")
    assert vaciar(cola) == ["b", "c"]


def test_un_solo_elemento():
    cola = ColaPrioridad()
    cola.encolar(1, "solo")
    assert cola.desencolar() == "solo" and cola.esta_vacia()


def test_crece_mas_alla_de_la_capacidad_inicial():
    cola = ColaPrioridad()
    for i in range(500, 0, -1):
        cola.encolar(i, i)
    assert vaciar(cola) == list(range(1, 501))


@pytest.mark.parametrize("semilla", [1, 2, 3, 4, 5])
def test_aleatorio_coincide_con_heapq_de_referencia(semilla):
    azar = random.Random(semilla)
    cola, referencia, llegada = ColaPrioridad(), [], 0
    for _ in range(2000):
        if referencia and azar.random() < 0.4:
            assert cola.desencolar() == heapq.heappop(referencia)[2]
        else:
            p = azar.randint(0, 20)
            cola.encolar(p, llegada)
            heapq.heappush(referencia, (p, llegada, llegada))
            llegada += 1
    assert len(cola) == len(referencia)
    while referencia:
        assert cola.desencolar() == heapq.heappop(referencia)[2]
