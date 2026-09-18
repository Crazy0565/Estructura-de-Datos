import pytest
from matriz import Matriz


def test_matriz_se_crea_con_ceros():
    matriz = Matriz(2, 3)

    assert matriz.filas() == 2
    assert matriz.columnas() == 3
    assert matriz.obtener(0, 0) == 0
    assert matriz.obtener(1, 2) == 0


def test_asignar_y_obtener():
    matriz = Matriz(2, 3)

    matriz.asignar(0, 0, 10)
    matriz.asignar(0, 2, 30)
    matriz.asignar(1, 1, 50)

    assert matriz.obtener(0, 0) == 10
    assert matriz.obtener(0, 2) == 30
    assert matriz.obtener(1, 1) == 50


def test_suma():
    matriz = Matriz(2, 3)

    matriz.asignar(0, 0, 1)
    matriz.asignar(0, 1, 2)
    matriz.asignar(0, 2, 3)
    matriz.asignar(1, 0, 4)
    matriz.asignar(1, 1, 5)
    matriz.asignar(1, 2, 6)

    assert matriz.suma() == 21


def test_matriz_de_una_sola_celda():
    matriz = Matriz(1, 1)

    assert matriz.filas() == 1
    assert matriz.columnas() == 1
    assert matriz.obtener(0, 0) == 0

    matriz.asignar(0, 0, 99)

    assert matriz.obtener(0, 0) == 99
    assert matriz.suma() == 99


@pytest.mark.parametrize(
    "filas,columnas",
    [
        (0, 3),
        (3, 0),
        (-1, 3),
        (3, -1),
    ],
)
def test_dimensiones_no_positivas_lanzan_value_error(filas, columnas):
    with pytest.raises(ValueError):
        Matriz(filas, columnas)


@pytest.mark.parametrize(
    "i,j",
    [
        (-1, 0),
        (0, -1),
        (2, 0),
        (0, 3),
    ],
)
def test_coordenadas_fuera_de_rango_lanzan_index_error(i, j):
    matriz = Matriz(2, 3)

    with pytest.raises(IndexError):
        matriz.obtener(i, j)


def test_asignar_fuera_de_rango_lanza_index_error():
    matriz = Matriz(2, 3)

    with pytest.raises(IndexError):
        matriz.asignar(2, 0, 10)
