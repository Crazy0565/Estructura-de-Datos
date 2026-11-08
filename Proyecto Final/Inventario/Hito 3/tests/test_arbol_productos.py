import math
import random

import pytest

from arbol_productos import ArbolAVL, ArbolBinarioBusqueda

TIPOS = [ArbolBinarioBusqueda, ArbolAVL]


def armar(tipo, claves):
    arbol = tipo()
    for c in claves:
        arbol.insertar(c, f"v{c}")
    return arbol


def claves(iterador):
    return [c for c, _ in iterador]


def verificar_avl(nodo):
    """Comprueba alturas guardadas y factor de equilibrio en todo el subárbol."""
    if nodo is None:
        return 0
    hi, hd = verificar_avl(nodo.izquierdo), verificar_avl(nodo.derecho)
    assert abs(hi - hd) <= 1
    assert nodo.altura == 1 + max(hi, hd)
    return nodo.altura


@pytest.mark.parametrize("tipo", TIPOS)
class TestComunes:
    def test_arbol_vacio(self, tipo):
        a = tipo()
        assert len(a) == 0 and a.esta_vacio() and a.altura() == 0
        assert a.buscar(1) is None and not a.contiene(1)
        assert claves(a.inorden()) == [] and claves(a.preorden()) == []
        assert claves(a.por_niveles()) == [] and claves(a.rango(0, 9)) == []
        assert a.eliminar(1) is None

    def test_minimo_y_maximo_en_vacio_lanzan_error(self, tipo):
        with pytest.raises(IndexError):
            tipo().minimo()
        with pytest.raises(IndexError):
            tipo().maximo()

    def test_insertar_y_buscar(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert len(a) == 7
        assert a.buscar(60) == "v60" and a.contiene(20)
        assert a.buscar(65) is None

    def test_clave_repetida_se_rechaza_y_no_cambia_el_tamaño(self, tipo):
        a = armar(tipo, [5, 3, 8])
        with pytest.raises(ValueError):
            a.insertar(3, "otro")
        assert len(a) == 3 and a.buscar(3) == "v3"

    def test_minimo_y_maximo(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 80])
        assert a.minimo() == (20, "v20") and a.maximo() == (80, "v80")

    def test_inorden_entrega_las_claves_ordenadas(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert claves(a.inorden()) == [20, 30, 40, 50, 60, 70, 80]
        assert claves(a) == [20, 30, 40, 50, 60, 70, 80]

    def test_por_niveles_en_un_arbol_perfecto(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert claves(a.por_niveles()) == [50, 30, 70, 20, 40, 60, 80]

    def test_preorden_en_un_arbol_perfecto(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert claves(a.preorden()) == [50, 30, 20, 40, 70, 60, 80]

    def test_rango_inclusivo(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert claves(a.rango(30, 60)) == [30, 40, 50, 60]
        assert claves(a.rango(31, 59)) == [40, 50]
        assert claves(a.rango(0, 10)) == []
        assert claves(a.rango(81, 99)) == []
        assert claves(a.rango(0, 999)) == [20, 30, 40, 50, 60, 70, 80]

    def test_eliminar_hoja(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40])
        assert a.eliminar(20) == "v20"
        assert claves(a) == [30, 40, 50, 70] and len(a) == 4

    def test_eliminar_nodo_con_un_hijo_izquierdo(self, tipo):
        a = armar(tipo, [50, 30, 70, 20])
        assert a.eliminar(30) == "v30"
        assert claves(a) == [20, 50, 70]

    def test_eliminar_nodo_con_un_hijo_derecho(self, tipo):
        a = armar(tipo, [50, 30, 70, 80])
        assert a.eliminar(70) == "v70"
        assert claves(a) == [30, 50, 80]

    def test_eliminar_nodo_con_dos_hijos(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert a.eliminar(30) == "v30"
        assert claves(a) == [20, 40, 50, 60, 70, 80] and len(a) == 6
        assert a.buscar(40) == "v40" and a.buscar(30) is None

    def test_eliminar_la_raiz_con_dos_hijos(self, tipo):
        a = armar(tipo, [50, 30, 70, 20, 40, 60, 80])
        assert a.eliminar(50) == "v50"
        assert claves(a) == [20, 30, 40, 60, 70, 80]
        assert a.buscar(60) == "v60"

    def test_eliminar_la_raiz_cuando_es_el_unico_nodo(self, tipo):
        a = armar(tipo, [7])
        assert a.eliminar(7) == "v7" and a.esta_vacio() and a.altura() == 0

    def test_eliminar_clave_inexistente_no_cambia_nada(self, tipo):
        a = armar(tipo, [5, 3, 8])
        assert a.eliminar(99) is None and len(a) == 3

    def test_vaciar_el_arbol_eliminando_todo(self, tipo):
        datos = list(range(1, 60))
        random.Random(1).shuffle(datos)
        a = armar(tipo, datos)
        random.Random(2).shuffle(datos)
        for c in datos:
            assert a.eliminar(c) == f"v{c}"
        assert a.esta_vacio() and claves(a) == []

    def test_aleatorio_coincide_con_un_modelo_de_referencia(self, tipo):
        azar = random.Random(42)
        a, modelo = tipo(), {}
        for _ in range(3000):
            c = azar.randint(1, 400)
            if azar.random() < 0.6:
                if c in modelo:
                    with pytest.raises(ValueError):
                        a.insertar(c, f"v{c}")
                else:
                    a.insertar(c, f"v{c}")
                    modelo[c] = f"v{c}"
            else:
                assert a.eliminar(c) == modelo.pop(c, None)
        assert claves(a) == sorted(modelo) and len(a) == len(modelo)
        assert claves(a.por_niveles()).__len__() == len(modelo)
        assert sorted(claves(a.preorden())) == sorted(modelo)

    def test_rango_coincide_con_el_modelo(self, tipo):
        azar = random.Random(7)
        datos = azar.sample(range(1, 1000), 200)
        a = armar(tipo, datos)
        for _ in range(100):
            d, h = sorted(azar.sample(range(1100), 2))
            esperado = sorted(c for c in datos if d <= c <= h)
            assert claves(a.rango(d, h)) == esperado


class TestSinBalanceo:
    def test_claves_ordenadas_degeneran_en_una_lista(self):
        a = armar(ArbolBinarioBusqueda, range(1, 201))
        assert a.altura() == 200

    def test_no_desborda_la_pila_con_claves_ordenadas(self):
        a = ArbolBinarioBusqueda()
        for c in range(1, 5001):
            a.insertar(c, c)
        assert a.buscar(5000) == 5000 and a.altura() == 5000
        assert len(claves(a.inorden())) == 5000
        assert a.eliminar(5000) == 5000 and a.eliminar(1) == 1

    def test_claves_mezcladas_dan_altura_logaritmica_aproximada(self):
        datos = list(range(1, 2001))
        random.Random(3).shuffle(datos)
        a = armar(ArbolBinarioBusqueda, datos)
        assert a.altura() < 40


class TestAVL:
    def test_rotacion_simple_a_la_derecha(self):
        a = armar(ArbolAVL, [30, 20, 10])
        assert claves(a.preorden()) == [20, 10, 30] and a.altura() == 2

    def test_rotacion_simple_a_la_izquierda(self):
        a = armar(ArbolAVL, [10, 20, 30])
        assert claves(a.preorden()) == [20, 10, 30]

    def test_rotacion_doble_izquierda_derecha(self):
        a = armar(ArbolAVL, [30, 10, 20])
        assert claves(a.preorden()) == [20, 10, 30]

    def test_rotacion_doble_derecha_izquierda(self):
        a = armar(ArbolAVL, [10, 30, 20])
        assert claves(a.preorden()) == [20, 10, 30]

    def test_claves_ordenadas_quedan_balanceadas(self):
        a = armar(ArbolAVL, range(1, 1024))
        assert a.altura() == 10
        verificar_avl(a._raiz)

    def test_cota_de_altura(self):
        n = 5000
        a = armar(ArbolAVL, range(1, n + 1))
        assert a.altura() <= 1.44 * math.log2(n + 2)

    def test_invariantes_tras_insertar_y_eliminar_al_azar(self):
        azar = random.Random(11)
        a = ArbolAVL()
        presentes = set()
        for paso in range(4000):
            c = azar.randint(1, 600)
            if c in presentes:
                a.eliminar(c)
                presentes.discard(c)
            else:
                a.insertar(c, c)
                presentes.add(c)
            if paso % 200 == 0:
                verificar_avl(a._raiz)
        verificar_avl(a._raiz)
        assert claves(a) == sorted(presentes)

    def test_eliminar_en_orden_mantiene_el_equilibrio(self):
        a = armar(ArbolAVL, range(1, 300))
        for c in range(1, 150):
            a.eliminar(c)
            verificar_avl(a._raiz)
        assert claves(a) == list(range(150, 300))

    def test_altura_es_constante_en_tiempo(self):
        a = armar(ArbolAVL, range(1, 100))
        assert a.altura() == a._raiz.altura
