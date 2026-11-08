import pytest

from algoritmos_grafo import camino_minimo, componentes_conexas, dijkstra
from grafo_bodega import GrafoMatrizAdyacencia
from plano_bodega import (
    DIST_ESTANTE,
    DIST_MUELLE,
    DIST_PASILLO,
    MUELLE,
    PlanoBodega,
)


def distancia_esperada(lado, p1, e1, p2, e2):
    """Fórmula cerrada: mismo pasillo directo; si no, por el frente o por el fondo."""
    if p1 == p2:
        return DIST_ESTANTE * abs(e1 - e2)
    cruce = DIST_PASILLO * abs(p1 - p2)
    frente = DIST_ESTANTE * (e1 + e2) + cruce
    fondo = DIST_ESTANTE * ((lado - 1 - e1) + (lado - 1 - e2)) + cruce
    return min(frente, fondo)


def test_cantidad_de_nodos_y_aristas():
    for lado in (1, 2, 5, 10):
        plano = PlanoBodega(lado)
        assert plano.grafo.numero_nodos == lado * lado + 1
        esperadas = 1 + lado * (lado - 1) + 2 * (lado - 1)
        assert plano.grafo.numero_aristas == esperadas


def test_lado_invalido():
    with pytest.raises(ValueError):
        PlanoBodega(0)


def test_nodo_de_y_ubicacion_de_son_inversas():
    plano = PlanoBodega(6)
    for p in range(6):
        for e in range(6):
            assert plano.ubicacion_de(plano.nodo_de(p, e)) == (p, e)
    assert plano.ubicacion_de(MUELLE) is None


def test_ubicaciones_fuera_de_la_bodega():
    plano = PlanoBodega(4)
    with pytest.raises(IndexError):
        plano.nodo_de(4, 0)
    with pytest.raises(IndexError):
        plano.nodo_de(0, -1)
    with pytest.raises(IndexError):
        plano.ubicacion_de(17)


def test_toda_la_planta_esta_conectada():
    cantidad, _ = componentes_conexas(PlanoBodega(8).grafo)
    assert cantidad == 1


def test_el_grado_maximo_es_cuatro():
    plano = PlanoBodega(7)
    assert max(plano.grafo.grado(n) for n in range(plano.grafo.numero_nodos)) <= 4


def test_distancia_del_muelle_a_cada_ubicacion():
    lado = 7
    plano = PlanoBodega(lado)
    distancia, _ = dijkstra(plano.grafo, MUELLE)
    for p in range(lado):
        for e in range(lado):
            esperada = DIST_MUELLE + distancia_esperada(lado, 0, 0, p, e)
            assert distancia[plano.nodo_de(p, e)] == esperada


@pytest.mark.parametrize(
    "a,b",
    [
        ((0, 0), (3, 5)),
        ((2, 1), (2, 6)),
        ((1, 5), (4, 5)),
        ((5, 0), (0, 5)),
        ((3, 3), (3, 3)),
    ],
)
def test_ruta_entre_dos_estantes_coincide_con_la_formula(a, b):
    lado = 8
    plano = PlanoBodega(lado)
    distancia, camino = camino_minimo(plano.grafo, plano.nodo_de(*a), plano.nodo_de(*b))
    assert distancia == distancia_esperada(lado, *a, *b)
    assert camino[0] == plano.nodo_de(*a) and camino[len(camino) - 1] == plano.nodo_de(
        *b
    )


def test_para_cambiar_de_pasillo_se_pasa_por_el_frente_o_el_fondo():
    lado = 6
    plano = PlanoBodega(lado)
    _, camino = camino_minimo(plano.grafo, plano.nodo_de(0, 3), plano.nodo_de(4, 3))
    visitadas = [plano.ubicacion_de(camino[i]) for i in range(len(camino))]
    estantes_en_el_cruce = {e for (p, e) in visitadas if p not in (0, 4)}
    assert estantes_en_el_cruce <= {0, lado - 1}


def test_funciona_igual_con_matriz_de_adyacencia():
    lista, matriz = PlanoBodega(5), PlanoBodega(5, fabrica=GrafoMatrizAdyacencia)
    a, _ = dijkstra(lista.grafo, MUELLE)
    b, _ = dijkstra(matriz.grafo, MUELLE)
    assert [a[i] for i in range(len(a))] == [b[i] for i in range(len(b))]


def test_plano_grande_se_resuelve_sin_errores():
    plano = PlanoBodega(100)
    distancia, _ = dijkstra(plano.grafo, MUELLE)
    assert distancia[plano.nodo_de(99, 99)] == DIST_MUELLE + distancia_esperada(
        100, 0, 0, 99, 99
    )
