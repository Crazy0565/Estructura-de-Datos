import pytest

from agenda import Agenda


def test_agenda_vacia():
    agenda = Agenda()

    assert len(agenda) == 0
    assert agenda.nombres() == []


def test_agregar_contacto():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")

    assert len(agenda) == 1
    assert agenda.contiene("Carlos")


def test_orden_alfabetico():
    agenda = Agenda()

    agenda.agregar("Pedro", "3001111111")
    agenda.agregar("Ana", "3002222222")
    agenda.agregar("Carlos", "3003333333")

    assert agenda.nombres() == ["Ana", "Carlos", "Pedro"]


def test_contiene_contacto_inexistente():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")

    assert not agenda.contiene("Pedro")


def test_obtener_telefono():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")

    assert agenda.telefono_de("Carlos") == "3001234567"


def test_telefono_nombre_inexistente():
    agenda = Agenda()

    with pytest.raises(KeyError):
        agenda.telefono_de("Pedro")


def test_actualizar_telefono():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")
    agenda.agregar("Carlos", "3119999999")

    assert len(agenda) == 1
    assert agenda.telefono_de("Carlos") == "3119999999"


def test_eliminar_contacto():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")
    agenda.eliminar("Carlos")

    assert len(agenda) == 0
    assert not agenda.contiene("Carlos")


def test_eliminar_contacto_inexistente():
    agenda = Agenda()

    with pytest.raises(KeyError):
        agenda.eliminar("Pedro")


def test_nombre_vacio():
    agenda = Agenda()

    with pytest.raises(ValueError):
        agenda.agregar("", "3001234567")


def test_nombres_devuelve_una_lista_independiente():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")

    nombres = agenda.nombres()
    nombres.append("Pedro")

    assert agenda.nombres() == ["Carlos"]


def test_agregar_al_principio():
    agenda = Agenda()

    agenda.agregar("Carlos", "3001234567")
    agenda.agregar("Pedro", "3007654321")
    agenda.agregar("Ana", "3015555555")

    assert agenda.nombres() == ["Ana", "Carlos", "Pedro"]


def test_agregar_en_el_medio():
    agenda = Agenda()

    agenda.agregar("Ana", "3001234567")
    agenda.agregar("Pedro", "3007654321")
    agenda.agregar("Carlos", "3015555555")

    assert agenda.nombres() == ["Ana", "Carlos", "Pedro"]


def test_agregar_al_final():
    agenda = Agenda()

    agenda.agregar("Ana", "3001234567")
    agenda.agregar("Carlos", "3007654321")
    agenda.agregar("Pedro", "3015555555")

    assert agenda.nombres() == ["Ana", "Carlos", "Pedro"]
