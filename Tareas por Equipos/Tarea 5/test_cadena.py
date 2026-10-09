from cadena import Cadena, Doble


def crear_cadena(datos):
    cadena = Cadena()
    for dato in datos:
        cadena.agregar(dato)
    return cadena


def crear_doble(datos):
    cadena = Doble()
    for dato in datos:
        cadena.agregar(dato)
    return cadena


def test_cadena_agregar_y_lista():
    assert crear_cadena([1, 2, 3]).a_lista() == [1, 2, 3]


def test_cadena_vacia_es_caso_borde():
    cadena = Cadena()
    assert len(cadena) == 0
    assert cadena.a_lista() == []
    assert cadena.medio() is None


def test_medio_cantidad_impar():
    cadena = crear_cadena([10, 20, 30, 40, 50])
    assert cadena.medio() == 30
    assert cadena.medio_dos_pasadas() == 30


def test_medio_par_toma_el_primero_central():
    cadena = crear_cadena([10, 20, 30, 40])
    assert cadena.medio() == 20
    assert cadena.medio_dos_pasadas() == 20


def test_invertir_cadena_y_agregar_despues():
    cadena = crear_cadena([1, 2, 3])
    cadena.invertir()
    cadena.agregar(4)
    assert cadena.a_lista() == [3, 2, 1, 4]


def test_doble_agregar_y_reversa():
    cadena = crear_doble(["a", "b", "c"])
    assert cadena.a_lista() == ["a", "b", "c"]
    assert cadena.a_lista_al_reves() == ["c", "b", "a"]


def test_doble_invertir():
    cadena = crear_doble([1, 2, 3])
    cadena.invertir()
    assert cadena.a_lista() == [3, 2, 1]
    assert cadena.a_lista_al_reves() == [1, 2, 3]


def test_doble_vacia_es_caso_borde():
    cadena = Doble()
    assert len(cadena) == 0
    assert cadena.a_lista_al_reves() == []


def test_doble_agregar_despues_de_invertir():
    cadena = crear_doble([1, 2])
    cadena.invertir()
    cadena.agregar(3)
    assert cadena.a_lista() == [2, 1, 3]


def test_un_elemento():
    cadena = crear_cadena([99])
    assert cadena.medio() == 99
    assert cadena.medio_dos_pasadas() == 99
