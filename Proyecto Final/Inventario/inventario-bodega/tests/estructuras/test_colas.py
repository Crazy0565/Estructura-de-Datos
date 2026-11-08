import random
from collections import deque

import pytest

from inventario.estructuras.cola_circular import ColaCircular, ColaLlenaError
from inventario.estructuras.cola_enlazada import ColaEnlazada

FABRICAS = [
    pytest.param(ColaEnlazada, id="enlazada"),
    pytest.param(lambda: ColaCircular(100), id="circular"),
]


def contenido(cola):
    return list(cola)


# ---------- comportamiento común a las dos variantes ----------


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_cola_nueva_esta_vacia(fabrica):
    cola = fabrica()

    assert len(cola) == 0
    assert cola.esta_vacia()
    assert contenido(cola) == []


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_desencolar_y_frente_en_cola_vacia(fabrica):
    cola = fabrica()

    with pytest.raises(IndexError):
        cola.desencolar()

    with pytest.raises(IndexError):
        cola.frente()


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_sale_primero_el_que_llego_primero(fabrica):
    cola = fabrica()

    for numero in range(1, 6):
        cola.encolar(numero)

    assert [cola.desencolar() for _ in range(5)] == [1, 2, 3, 4, 5]
    assert cola.esta_vacia()


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_frente_no_quita_el_elemento(fabrica):
    cola = fabrica()
    cola.encolar("A")
    cola.encolar("B")

    assert cola.frente() == "A"
    assert cola.frente() == "A"
    assert len(cola) == 2


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_cola_de_un_solo_elemento(fabrica):
    cola = fabrica()

    cola.encolar("solo")

    assert len(cola) == 1
    assert cola.desencolar() == "solo"
    assert cola.esta_vacia()


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_se_puede_reutilizar_despues_de_vaciarse(fabrica):
    cola = fabrica()
    cola.encolar(1)
    cola.encolar(2)
    cola.desencolar()
    cola.desencolar()

    cola.encolar(3)
    cola.encolar(4)

    assert contenido(cola) == [3, 4]
    assert cola.desencolar() == 3
    assert cola.desencolar() == 4


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_encolar_y_desencolar_intercalados(fabrica):
    cola = fabrica()

    cola.encolar("a")
    cola.encolar("b")
    assert cola.desencolar() == "a"
    cola.encolar("c")
    assert cola.desencolar() == "b"
    assert cola.desencolar() == "c"
    assert cola.esta_vacia()


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_recorrer_no_consume_la_cola(fabrica):
    cola = fabrica()

    for letra in "xyz":
        cola.encolar(letra)

    assert contenido(cola) == ["x", "y", "z"]
    assert contenido(cola) == ["x", "y", "z"]
    assert len(cola) == 3


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_none_es_un_elemento_valido(fabrica):
    cola = fabrica()

    cola.encolar(None)
    cola.encolar(0)

    assert len(cola) == 2
    assert cola.desencolar() is None
    assert cola.desencolar() == 0


@pytest.mark.parametrize("fabrica", FABRICAS)
def test_coincide_con_collections_deque_en_operaciones_aleatorias(fabrica):
    generador = random.Random(11)
    cola = fabrica()
    referencia = deque()

    for paso in range(3000):
        if referencia and (len(referencia) >= 90 or generador.random() < 0.45):
            assert cola.desencolar() == referencia.popleft()
        else:
            cola.encolar(paso)
            referencia.append(paso)

        assert len(cola) == len(referencia)

        if referencia:
            assert cola.frente() == referencia[0]

    assert contenido(cola) == list(referencia)


# ---------- cola circular ----------


@pytest.mark.parametrize("capacidad", [0, -1, -50])
def test_capacidad_invalida(capacidad):
    with pytest.raises(ValueError):
        ColaCircular(capacidad)


def test_cola_circular_se_llena_y_rechaza_mas_elementos():
    cola = ColaCircular(3)

    for letra in "abc":
        cola.encolar(letra)

    assert cola.esta_llena()

    with pytest.raises(ColaLlenaError):
        cola.encolar("d")

    assert contenido(cola) == ["a", "b", "c"]
    assert len(cola) == 3


def test_cola_circular_reutiliza_los_espacios_liberados():
    cola = ColaCircular(3)

    for letra in "abc":
        cola.encolar(letra)

    assert cola.desencolar() == "a"
    cola.encolar("d")

    assert cola.esta_llena()
    assert contenido(cola) == ["b", "c", "d"]
    assert [cola.desencolar() for _ in range(3)] == ["b", "c", "d"]


def test_cola_circular_de_capacidad_uno():
    cola = ColaCircular(1)

    cola.encolar("A")

    assert cola.esta_llena()

    with pytest.raises(ColaLlenaError):
        cola.encolar("B")

    assert cola.desencolar() == "A"

    cola.encolar("C")
    assert cola.frente() == "C"


def test_cola_circular_mantiene_el_orden_tras_muchas_vueltas():
    cola = ColaCircular(4)
    esperado = deque()

    for numero in range(1000):
        if cola.esta_llena():
            assert cola.desencolar() == esperado.popleft()

        cola.encolar(numero)
        esperado.append(numero)

    assert contenido(cola) == list(esperado)
    assert len(cola) == 4


def test_cola_circular_como_historial_descarta_el_mas_antiguo():
    cola = ColaCircular(3)

    for numero in range(1, 6):
        if cola.esta_llena():
            cola.desencolar()

        cola.encolar(numero)

    assert contenido(cola) == [3, 4, 5]


def test_cola_circular_vacia_no_esta_llena_y_llena_no_esta_vacia():
    cola = ColaCircular(2)

    assert not cola.esta_llena()

    cola.encolar(1)
    cola.encolar(2)

    assert cola.esta_llena()
    assert not cola.esta_vacia()


# ---------- cola enlazada ----------


def test_cola_enlazada_no_tiene_tope():
    cola = ColaEnlazada()

    for numero in range(20000):
        cola.encolar(numero)

    assert len(cola) == 20000
    assert cola.desencolar() == 0
    assert cola.frente() == 1


def test_cola_enlazada_actualiza_el_ultimo_al_vaciarse():
    cola = ColaEnlazada()
    cola.encolar("A")
    cola.desencolar()

    cola.encolar("B")
    cola.encolar("C")

    assert contenido(cola) == ["B", "C"]
