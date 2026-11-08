import random

import pytest

from inventario.grafos.algoritmos_grafo import (
    INFINITO,
    bfs,
    camino_minimo,
    componentes_conexas,
    dfs,
    dijkstra,
)
from inventario.grafos.grafo_bodega import GrafoListaAdyacencia, GrafoMatrizAdyacencia

TIPOS = [GrafoListaAdyacencia, GrafoMatrizAdyacencia]


@pytest.fixture(params=TIPOS, ids=["lista", "matriz"])
def tipo(request):
    return request.param


def armar(tipo, n, aristas):
    g = tipo(n)
    for u, v, p in aristas:
        g.agregar_arista(u, v, p)
    return g


def lista_de(arreglo):
    return [arreglo[i] for i in range(len(arreglo))]


# Grafo clásico: el camino más corto de 0 a 4 es 0-2-1-3-4 con costo 8... ver abajo.
CLASICO = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]


def bellman_ford(n, aristas, origen):
    """Oráculo independiente: distancias mínimas por relajación repetida."""
    d = [INFINITO] * n
    d[origen] = 0
    for _ in range(n):
        for u, v, p in aristas:
            d[v] = min(d[v], d[u] + p)
            d[u] = min(d[u], d[v] + p)
    return d


class TestRecorridos:
    def test_bfs_visita_por_niveles(self, tipo):
        g = armar(
            tipo, 7, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (1, 4, 1), (2, 5, 1), (2, 6, 1)]
        )
        orden = list(bfs(g, 0))
        assert orden[0] == 0 and set(orden[1:3]) == {1, 2}
        assert set(orden[3:]) == {3, 4, 5, 6}

    def test_bfs_en_un_camino_sigue_el_camino(self, tipo):
        g = armar(tipo, 5, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)])
        assert list(bfs(g, 0)) == [0, 1, 2, 3, 4]
        assert next(bfs(g, 2)) == 2

    def test_dfs_visita_todo_lo_alcanzable_una_sola_vez(self, tipo):
        g = armar(tipo, 6, CLASICO)
        orden = list(dfs(g, 0))
        assert sorted(orden) == [0, 1, 2, 3, 4] and len(orden) == len(set(orden))

    def test_dfs_se_adentra_antes_de_retroceder(self, tipo):
        # estrella con un brazo largo: 0-1, 0-2, 2-3, 3-4
        g = armar(tipo, 5, [(0, 1, 1), (0, 2, 1), (2, 3, 1), (3, 4, 1)])
        orden = list(dfs(g, 0))
        i2 = orden.index(2)
        assert orden[i2 : i2 + 3] == [2, 3, 4]

    def test_los_recorridos_solo_alcanzan_la_componente_del_origen(self, tipo):
        g = armar(tipo, 6, [(0, 1, 1), (1, 2, 1), (3, 4, 1)])
        assert set(bfs(g, 0)) == {0, 1, 2} and set(dfs(g, 0)) == {0, 1, 2}
        assert list(bfs(g, 5)) == [5]

    def test_origen_inexistente(self, tipo):
        g = tipo(3)
        with pytest.raises(IndexError):
            list(bfs(g, 3))
        with pytest.raises(IndexError):
            list(dfs(g, -1))

    def test_grafo_de_un_solo_nodo(self, tipo):
        g = tipo(1)
        assert list(bfs(g, 0)) == [0] and list(dfs(g, 0)) == [0]

    def test_bfs_con_ciclos_no_se_repite(self, tipo):
        g = armar(tipo, 4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
        assert sorted(bfs(g, 0)) == [0, 1, 2, 3]

    def test_no_desborda_la_pila_en_un_camino_largo(self):
        n = 20000
        g = armar(GrafoListaAdyacencia, n, [(i, i + 1, 1) for i in range(n - 1)])
        assert len(list(dfs(g, 0))) == n and len(list(bfs(g, 0))) == n


class TestComponentes:
    def test_grafo_conexo_tiene_una_componente(self, tipo):
        cantidad, etiquetas = componentes_conexas(
            armar(tipo, 4, [(0, 1, 1), (1, 2, 1), (2, 3, 1)])
        )
        assert cantidad == 1 and lista_de(etiquetas) == [0, 0, 0, 0]

    def test_nodos_aislados_son_componentes_propias(self, tipo):
        cantidad, _ = componentes_conexas(tipo(5))
        assert cantidad == 5

    def test_varias_componentes(self, tipo):
        g = armar(tipo, 7, [(0, 1, 1), (1, 2, 1), (3, 4, 1), (5, 6, 1)])
        cantidad, etiquetas = componentes_conexas(g)
        e = lista_de(etiquetas)
        assert cantidad == 3 and e[0] == e[1] == e[2] and e[3] == e[4] and e[5] == e[6]
        assert len({e[0], e[3], e[5]}) == 3


class TestDijkstra:
    def test_distancias_del_grafo_clasico(self, tipo):
        distancia, _ = dijkstra(armar(tipo, 5, CLASICO), 0)
        assert lista_de(distancia) == [0, 3, 1, 4, 7]

    def test_camino_minimo_del_grafo_clasico(self, tipo):
        distancia, camino = camino_minimo(armar(tipo, 5, CLASICO), 0, 4)
        assert distancia == 7 and lista_de(camino) == [0, 2, 1, 3, 4]

    def test_camino_de_un_nodo_a_si_mismo(self, tipo):
        distancia, camino = camino_minimo(armar(tipo, 3, [(0, 1, 2)]), 1, 1)
        assert distancia == 0 and lista_de(camino) == [1]

    def test_sin_camino_devuelve_none_e_infinito(self, tipo):
        g = armar(tipo, 4, [(0, 1, 1), (2, 3, 1)])
        assert camino_minimo(g, 0, 3) is None
        distancia, previo = dijkstra(g, 0)
        assert distancia[3] == INFINITO and previo[3] == -1

    def test_preferir_dos_aristas_baratas_a_una_cara(self, tipo):
        g = armar(tipo, 3, [(0, 2, 10), (0, 1, 3), (1, 2, 3)])
        assert camino_minimo(g, 0, 2)[0] == 6

    def test_el_destino_detiene_la_busqueda_pero_da_el_mismo_resultado(self, tipo):
        g = armar(tipo, 5, CLASICO)
        completa, _ = dijkstra(g, 0)
        parcial, _ = dijkstra(g, 0, destino=3)
        assert parcial[3] == completa[3]

    def test_nodos_inexistentes(self, tipo):
        g = tipo(3)
        with pytest.raises(IndexError):
            dijkstra(g, 5)
        with pytest.raises(IndexError):
            camino_minimo(g, 0, 7)

    def test_el_camino_es_valido_y_suma_la_distancia(self, tipo):
        azar = random.Random(5)
        n = 30
        aristas, vistos = [], set()
        for _ in range(80):
            u, v = azar.sample(range(n), 2)
            if (min(u, v), max(u, v)) not in vistos:
                vistos.add((min(u, v), max(u, v)))
                aristas.append((u, v, azar.randint(1, 20)))
        g = armar(tipo, n, aristas)
        for destino in range(1, n):
            resultado = camino_minimo(g, 0, destino)
            if resultado is None:
                continue
            distancia, camino = resultado
            nodos = lista_de(camino)
            assert nodos[0] == 0 and nodos[-1] == destino
            assert (
                sum(g.peso(nodos[i], nodos[i + 1]) for i in range(len(nodos) - 1))
                == distancia
            )

    @pytest.mark.parametrize("semilla", range(8))
    def test_coincide_con_bellman_ford_en_grafos_aleatorios(self, tipo, semilla):
        azar = random.Random(semilla)
        n = azar.randint(5, 40)
        aristas, vistos = [], set()
        for _ in range(azar.randint(n, 3 * n)):
            u, v = azar.sample(range(n), 2)
            if (min(u, v), max(u, v)) not in vistos:
                vistos.add((min(u, v), max(u, v)))
                aristas.append((u, v, azar.randint(1, 50)))
        g = armar(tipo, n, aristas)
        distancia, _ = dijkstra(g, 0)
        assert lista_de(distancia) == bellman_ford(n, aristas, 0)
