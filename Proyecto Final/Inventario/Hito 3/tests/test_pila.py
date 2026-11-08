import random

import pytest

from pila import PilaEnlazada


def test_pila_nueva_esta_vacia():
    pila = PilaEnlazada()

    assert len(pila) == 0
    assert pila.esta_vacia()
    assert list(pila) == []


def test_desapilar_y_cima_en_pila_vacia():
    pila = PilaEnlazada()

    with pytest.raises(IndexError):
        pila.desapilar()

    with pytest.raises(IndexError):
        pila.cima()


def test_sale_primero_el_ultimo_que_entro():
    pila = PilaEnlazada()

    for numero in range(1, 6):
        pila.apilar(numero)

    assert [pila.desapilar() for _ in range(5)] == [5, 4, 3, 2, 1]
    assert pila.esta_vacia()


def test_cima_no_quita_el_elemento():
    pila = PilaEnlazada()
    pila.apilar("A")
    pila.apilar("B")

    assert pila.cima() == "B"
    assert pila.cima() == "B"
    assert len(pila) == 2


def test_pila_de_un_solo_elemento():
    pila = PilaEnlazada()

    pila.apilar("solo")

    assert pila.desapilar() == "solo"
    assert pila.esta_vacia()


def test_recorrer_va_de_la_cima_al_fondo_sin_consumir():
    pila = PilaEnlazada()

    for letra in "xyz":
        pila.apilar(letra)

    assert list(pila) == ["z", "y", "x"]
    assert list(pila) == ["z", "y", "x"]
    assert len(pila) == 3


def test_se_puede_reutilizar_despues_de_vaciarse():
    pila = PilaEnlazada()
    pila.apilar(1)
    pila.desapilar()

    pila.apilar(2)
    pila.apilar(3)

    assert list(pila) == [3, 2]


def test_apilar_y_desapilar_intercalados():
    pila = PilaEnlazada()

    pila.apilar("a")
    pila.apilar("b")
    assert pila.desapilar() == "b"
    pila.apilar("c")
    assert pila.desapilar() == "c"
    assert pila.desapilar() == "a"
    assert pila.esta_vacia()


def test_none_es_un_elemento_valido():
    pila = PilaEnlazada()

    pila.apilar(None)

    assert len(pila) == 1
    assert pila.desapilar() is None


def test_pila_sin_tope_acepta_muchos_elementos():
    pila = PilaEnlazada()

    for numero in range(20000):
        pila.apilar(numero)

    assert len(pila) == 20000
    assert pila.desapilar() == 19999


def test_coincide_con_una_lista_usada_como_pila_en_operaciones_aleatorias():
    generador = random.Random(5)
    pila = PilaEnlazada()
    referencia = []

    for paso in range(3000):
        if referencia and generador.random() < 0.45:
            assert pila.desapilar() == referencia.pop()
        else:
            pila.apilar(paso)
            referencia.append(paso)

        assert len(pila) == len(referencia)

        if referencia:
            assert pila.cima() == referencia[-1]

    assert list(pila) == referencia[::-1]
