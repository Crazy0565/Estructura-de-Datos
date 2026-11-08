import itertools
import random

from arreglo import ArregloDinamico
from plano_bodega import PlanoBodega
from ruta_recoleccion import (
    comparar_rutas,
    distancia_de_ruta,
    matriz_de_distancias,
    mejorar_2opt,
    orden_de_llegada,
    vecino_mas_cercano,
)


def arr(*valores):
    a = ArregloDinamico()
    for v in valores:
        a.agregar(v)
    return a


def nodos_al_azar(plano, k, semilla):
    rnd = random.Random(semilla)
    total = plano.grafo.numero_nodos
    return arr(*rnd.sample(range(1, total), k))


def test_un_solo_destino_ida_y_vuelta():
    plano = PlanoBodega(4)
    r = comparar_rutas(plano, arr(plano.nodo_de(0, 0)))
    assert r.distancia_llegada == r.distancia_optima == 2 * 2
    assert r.ahorro == 0.0


def test_pedido_vacio():
    r = comparar_rutas(PlanoBodega(3), arr())
    assert r.distancia_llegada == 0
    assert r.ahorro == 0.0


def test_orden_es_permutacion():
    plano = PlanoBodega(8)
    r = comparar_rutas(plano, nodos_al_azar(plano, 9, 1))
    assert sorted(r.orden_optimo[i] for i in range(len(r.orden_optimo))) == list(
        range(1, 10)
    )


def test_optima_nunca_peor_que_llegada_y_cercana_al_optimo_exacto():
    plano = PlanoBodega(6)
    for semilla in range(15):
        nodos = nodos_al_azar(plano, 6, semilla)
        r = comparar_rutas(plano, nodos)
        matriz = matriz_de_distancias(plano, r.paradas)
        exacto = min(
            distancia_de_ruta(matriz, arr(*p))
            for p in itertools.permutations(range(1, 7))
        )
        assert (
            r.distancia_optima <= r.distancia_llegada + 0
        )  # heurística no empeora vs. llegada típica
        assert exacto <= r.distancia_optima <= exacto * 1.25


def test_2opt_no_empeora():
    plano = PlanoBodega(7)
    nodos = nodos_al_azar(plano, 8, 3)
    r = comparar_rutas(plano, nodos)
    matriz = matriz_de_distancias(plano, r.paradas)
    base = vecino_mas_cercano(matriz)
    antes = distancia_de_ruta(matriz, base)
    despues = distancia_de_ruta(matriz, mejorar_2opt(matriz, base))
    assert despues <= antes


def test_distancia_calculada_a_mano():
    plano = PlanoBodega(3)
    a, b, c = plano.nodo_de(0, 2), plano.nodo_de(0, 0), plano.nodo_de(0, 1)
    r = comparar_rutas(plano, arr(a, b, c))
    # llegada: muelle->e2=6, e2->e0=4, e0->e1=2, e1->muelle=4  => 16
    assert r.distancia_llegada == 16
    # óptima: muelle->e0=2, e0->e1=2, e1->e2=2, e2->muelle=6 => 12
    assert r.distancia_optima == 12
    assert r.ahorro == 0.25
    assert orden_de_llegada(4)[0] == 1
