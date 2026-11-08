import pytest

from inventario.grafos.grafo_bodega import GrafoListaAdyacencia, GrafoMatrizAdyacencia

TIPOS = [GrafoListaAdyacencia, GrafoMatrizAdyacencia]


@pytest.fixture(params=TIPOS, ids=["lista", "matriz"])
def tipo(request):
    return request.param


def vecinos(g, u):
    return sorted(g.vecinos(u))


def test_grafo_nuevo_no_tiene_aristas(tipo):
    g = tipo(4)
    assert g.numero_nodos == 4 and g.numero_aristas == 0
    assert vecinos(g, 0) == [] and g.grado(0) == 0


@pytest.mark.parametrize("n", [0, -3])
def test_cantidad_de_nodos_invalida(tipo, n):
    with pytest.raises(ValueError):
        tipo(n)


def test_arista_es_no_dirigida(tipo):
    g = tipo(3)
    g.agregar_arista(0, 2, 5)
    assert g.peso(0, 2) == 5 and g.peso(2, 0) == 5
    assert vecinos(g, 0) == [(2, 5)] and vecinos(g, 2) == [(0, 5)]
    assert g.numero_aristas == 1


def test_peso_de_una_arista_inexistente_es_none(tipo):
    g = tipo(3)
    g.agregar_arista(0, 1, 1)
    assert g.peso(1, 2) is None


def test_varias_aristas_y_grados(tipo):
    g = tipo(4)
    for u, v, p in [(0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 2, 4)]:
        g.agregar_arista(u, v, p)
    assert g.numero_aristas == 4
    assert g.grado(0) == 3 and g.grado(1) == 2 and g.grado(3) == 1
    assert vecinos(g, 0) == [(1, 1), (2, 2), (3, 3)]


def test_arista_repetida_se_rechaza_en_cualquier_sentido(tipo):
    g = tipo(3)
    g.agregar_arista(0, 1, 1)
    with pytest.raises(ValueError):
        g.agregar_arista(0, 1, 9)
    with pytest.raises(ValueError):
        g.agregar_arista(1, 0, 9)
    assert g.numero_aristas == 1 and g.peso(0, 1) == 1


def test_lazo_se_rechaza(tipo):
    with pytest.raises(ValueError):
        tipo(3).agregar_arista(1, 1, 2)


@pytest.mark.parametrize("peso", [0, -1, -0.5])
def test_peso_no_positivo_se_rechaza(tipo, peso):
    with pytest.raises(ValueError):
        tipo(3).agregar_arista(0, 1, peso)


@pytest.mark.parametrize("u,v", [(-1, 0), (0, 3), (5, 1), (0, -2)])
def test_nodo_inexistente_lanza_indexerror(tipo, u, v):
    with pytest.raises(IndexError):
        tipo(3).agregar_arista(u, v, 1)


def test_consultas_con_nodo_inexistente_lanzan_indexerror(tipo):
    g = tipo(2)
    with pytest.raises(IndexError):
        list(g.vecinos(2))
    with pytest.raises(IndexError):
        g.peso(0, 9)
    with pytest.raises(IndexError):
        g.grado(-1)


def test_pesos_decimales(tipo):
    g = tipo(2)
    g.agregar_arista(0, 1, 2.5)
    assert g.peso(0, 1) == 2.5


def test_ambas_representaciones_dan_lo_mismo():
    aristas = [(0, 1, 3), (1, 2, 1), (0, 3, 7), (3, 4, 2), (2, 4, 9), (1, 4, 5)]
    lista, matriz = GrafoListaAdyacencia(5), GrafoMatrizAdyacencia(5)
    for u, v, p in aristas:
        lista.agregar_arista(u, v, p)
        matriz.agregar_arista(u, v, p)
    assert lista.numero_aristas == matriz.numero_aristas
    for u in range(5):
        assert vecinos(lista, u) == vecinos(matriz, u)
        assert lista.grado(u) == matriz.grado(u)
        for v in range(5):
            assert lista.peso(u, v) == matriz.peso(u, v)
