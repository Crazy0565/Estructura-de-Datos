import pytest

from arreglo import ArregloDinamico


def test_arreglo_inicia_vacio():
    arreglo = ArregloDinamico()

    assert len(arreglo) == 0
    assert arreglo.capacidad == 10


def test_agregar_elemento():
    arreglo = ArregloDinamico()

    arreglo.agregar("Producto")

    assert len(arreglo) == 1
    assert arreglo[0] == "Producto"


def test_acceso_por_indice():
    arreglo = ArregloDinamico()

    arreglo.agregar("A")
    arreglo.agregar("B")

    assert arreglo[0] == "A"
    assert arreglo[1] == "B"


def test_redimensionamiento():
    arreglo = ArregloDinamico(2)

    arreglo.agregar("A")
    arreglo.agregar("B")
    arreglo.agregar("C")

    assert len(arreglo) == 3
    assert arreglo.capacidad == 4
    assert arreglo[0] == "A"
    assert arreglo[2] == "C"


def test_indice_fuera_de_rango():
    arreglo = ArregloDinamico()

    with pytest.raises(IndexError):
        arreglo[0]


def test_capacidad_crece_correctamente():
    arreglo = ArregloDinamico(2)

    for i in range(10):
        arreglo.agregar(i)

    assert len(arreglo) == 10
    assert arreglo.capacidad == 16


def test_eliminar_en_el_medio_desplaza_elementos():
    arreglo = ArregloDinamico()

    for letra in "ABCD":
        arreglo.agregar(letra)

    eliminado = arreglo.eliminar(1)

    assert eliminado == "B"
    assert len(arreglo) == 3
    assert [arreglo[i] for i in range(3)] == ["A", "C", "D"]


def test_eliminar_primero_y_ultimo():
    arreglo = ArregloDinamico()

    for numero in range(3):
        arreglo.agregar(numero)

    assert arreglo.eliminar(0) == 0
    assert arreglo.eliminar(len(arreglo) - 1) == 2
    assert len(arreglo) == 1
    assert arreglo[0] == 1


def test_eliminar_unico_elemento_deja_el_arreglo_vacio():
    arreglo = ArregloDinamico()
    arreglo.agregar("solo")

    arreglo.eliminar(0)

    assert len(arreglo) == 0

    with pytest.raises(IndexError):
        arreglo[0]


def test_eliminar_indice_invalido():
    arreglo = ArregloDinamico()
    arreglo.agregar("A")

    with pytest.raises(IndexError):
        arreglo.eliminar(1)

    with pytest.raises(IndexError):
        arreglo.eliminar(-1)


def test_eliminar_en_arreglo_vacio():
    arreglo = ArregloDinamico()

    with pytest.raises(IndexError):
        arreglo.eliminar(0)


def test_se_puede_agregar_despues_de_eliminar():
    arreglo = ArregloDinamico(2)
    arreglo.agregar("A")
    arreglo.agregar("B")

    arreglo.eliminar(0)
    arreglo.agregar("C")
    arreglo.agregar("D")

    assert [arreglo[i] for i in range(len(arreglo))] == ["B", "C", "D"]
