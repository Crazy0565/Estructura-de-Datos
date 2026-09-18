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