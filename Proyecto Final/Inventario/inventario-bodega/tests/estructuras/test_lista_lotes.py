import random
from datetime import date, timedelta

import pytest

from inventario.dominio.lote import Lote
from inventario.estructuras.lista_lotes import LIMITE_RECURSION, ListaLotes


def crear_lote(codigo, cantidad=10, vence="2027-01-01"):
    return Lote(codigo, cantidad, "2026-01-01", vence)


def lista_con(*lotes):
    lista = ListaLotes()

    for lote in lotes:
        lista.insertar(lote)

    return lista


def codigos(lista):
    return [lote.codigo for lote in lista]


def detalle(tomas):
    return [tomas[i] for i in range(len(tomas))]


def fecha_numero(indice):
    return (date(2027, 1, 1) + timedelta(days=indice)).isoformat()


def lista_grande(prefijo, cantidad, desplazamiento):
    lista = ListaLotes()

    for i in range(cantidad):
        lista.insertar(
            crear_lote(f"{prefijo}{i}", 1, fecha_numero(2 * i + desplazamiento))
        )

    return lista


# ---------- lista vacía ----------


def test_lista_nueva_esta_vacia():
    lista = ListaLotes()

    assert len(lista) == 0
    assert lista.primero() is None
    assert lista.stock_total() == 0
    assert list(lista) == []


def test_operaciones_sobre_lista_vacia():
    lista = ListaLotes()

    assert lista.buscar("X") is None
    assert lista.eliminar_lote("X") is None

    with pytest.raises(ValueError):
        lista.despachar(1)


# ---------- insertar ----------


def test_insertar_un_lote():
    lista = lista_con(crear_lote("A", 7))

    assert len(lista) == 1
    assert lista.primero().codigo == "A"
    assert lista.stock_total() == 7


def test_insertar_mantiene_el_orden_por_vencimiento():
    lista = lista_con(
        crear_lote("tarde", vence="2027-12-01"),
        crear_lote("pronto", vence="2027-01-01"),
        crear_lote("medio", vence="2027-06-01"),
    )

    assert codigos(lista) == ["pronto", "medio", "tarde"]


def test_insertar_al_inicio_en_el_medio_y_al_final():
    lista = lista_con(
        crear_lote("b", vence="2027-02-01"),
        crear_lote("d", vence="2027-04-01"),
    )

    lista.insertar(crear_lote("a", vence="2027-01-01"))
    lista.insertar(crear_lote("c", vence="2027-03-01"))
    lista.insertar(crear_lote("e", vence="2027-05-01"))

    assert codigos(lista) == ["a", "b", "c", "d", "e"]
    assert len(lista) == 5


def test_vencimientos_iguales_conservan_el_orden_de_llegada():
    lista = lista_con(
        crear_lote("primero", vence="2027-01-01"),
        crear_lote("segundo", vence="2027-01-01"),
        crear_lote("tercero", vence="2027-01-01"),
    )

    assert codigos(lista) == ["primero", "segundo", "tercero"]


def test_insertar_codigo_repetido_se_rechaza_sin_cambiar_la_lista():
    lista = lista_con(crear_lote("A", 5))

    with pytest.raises(ValueError):
        lista.insertar(crear_lote("A", 99, "2026-06-01"))

    assert len(lista) == 1
    assert lista.stock_total() == 5


def test_stock_total_suma_todos_los_lotes():
    lista = lista_con(crear_lote("A", 5), crear_lote("B", 7), crear_lote("C", 3))

    assert lista.stock_total() == 15


# ---------- buscar ----------


def test_buscar_lote_por_codigo():
    lista = lista_con(crear_lote("A"), crear_lote("B"))

    assert lista.buscar("B").codigo == "B"
    assert lista.buscar("Z") is None


# ---------- despachar ----------


def test_despachar_parte_del_primer_lote():
    lista = lista_con(
        crear_lote("A", 10, "2027-01-01"),
        crear_lote("B", 10, "2027-02-01"),
    )

    tomas = lista.despachar(4)

    assert detalle(tomas) == [("A", 4)]
    assert lista.primero().cantidad == 6
    assert len(lista) == 2
    assert lista.stock_total() == 16


def test_despachar_un_lote_completo_lo_saca_de_la_lista():
    lista = lista_con(
        crear_lote("A", 10, "2027-01-01"),
        crear_lote("B", 10, "2027-02-01"),
    )

    tomas = lista.despachar(10)

    assert detalle(tomas) == [("A", 10)]
    assert codigos(lista) == ["B"]
    assert lista.stock_total() == 10


def test_despachar_cruza_varios_lotes_empezando_por_el_que_vence_antes():
    lista = lista_con(
        crear_lote("tarde", 10, "2027-12-01"),
        crear_lote("pronto", 5, "2027-01-01"),
        crear_lote("medio", 8, "2027-06-01"),
    )

    tomas = lista.despachar(15)

    assert detalle(tomas) == [("pronto", 5), ("medio", 8), ("tarde", 2)]
    assert codigos(lista) == ["tarde"]
    assert lista.primero().cantidad == 8
    assert lista.stock_total() == 8


def test_despachar_todo_el_stock_deja_la_lista_vacia():
    lista = lista_con(crear_lote("A", 4), crear_lote("B", 6, "2027-02-01"))

    lista.despachar(10)

    assert len(lista) == 0
    assert lista.primero() is None
    assert lista.stock_total() == 0


def test_despachar_mas_del_stock_no_cambia_nada():
    lista = lista_con(crear_lote("A", 4), crear_lote("B", 6, "2027-02-01"))

    with pytest.raises(ValueError):
        lista.despachar(11)

    assert codigos(lista) == ["A", "B"]
    assert lista.stock_total() == 10
    assert lista.primero().cantidad == 4


@pytest.mark.parametrize("cantidad", [0, -3])
def test_despachar_cantidad_no_positiva(cantidad):
    lista = lista_con(crear_lote("A", 4))

    with pytest.raises(ValueError):
        lista.despachar(cantidad)

    assert lista.stock_total() == 4


def test_se_puede_insertar_despues_de_vaciar_la_lista():
    lista = lista_con(crear_lote("A", 4))
    lista.despachar(4)

    lista.insertar(crear_lote("B", 9))

    assert codigos(lista) == ["B"]
    assert lista.stock_total() == 9


# ---------- eliminar ----------


def test_eliminar_primero_medio_y_ultimo():
    lista = lista_con(
        crear_lote("a", 1, "2027-01-01"),
        crear_lote("b", 2, "2027-02-01"),
        crear_lote("c", 4, "2027-03-01"),
        crear_lote("d", 8, "2027-04-01"),
    )

    assert lista.eliminar_lote("a").codigo == "a"
    assert lista.eliminar_lote("c").codigo == "c"
    assert lista.eliminar_lote("d").codigo == "d"

    assert codigos(lista) == ["b"]
    assert len(lista) == 1
    assert lista.stock_total() == 2


def test_eliminar_lote_inexistente_no_cambia_nada():
    lista = lista_con(crear_lote("a", 3))

    assert lista.eliminar_lote("z") is None
    assert len(lista) == 1
    assert lista.stock_total() == 3


def test_eliminar_el_unico_lote():
    lista = lista_con(crear_lote("a", 3))

    lista.eliminar_lote("a")

    assert len(lista) == 0
    assert lista.primero() is None
    assert lista.stock_total() == 0


# ---------- fusionar ----------


@pytest.mark.parametrize(
    "metodo", ["fusionar", "fusionar_recursivo", "fusionar_iterativo"]
)
def test_fusionar_intercala_por_vencimiento(metodo):
    a = lista_con(
        crear_lote("a1", 1, "2027-01-01"),
        crear_lote("a2", 2, "2027-03-01"),
        crear_lote("a3", 4, "2027-05-01"),
    )
    b = lista_con(
        crear_lote("b1", 8, "2027-02-01"),
        crear_lote("b2", 16, "2027-04-01"),
    )

    getattr(a, metodo)(b)

    assert codigos(a) == ["a1", "b1", "a2", "b2", "a3"]
    assert len(a) == 5
    assert a.stock_total() == 31


@pytest.mark.parametrize("metodo", ["fusionar_recursivo", "fusionar_iterativo"])
def test_fusionar_deja_vacia_la_otra_lista(metodo):
    a = lista_con(crear_lote("a1"))
    b = lista_con(crear_lote("b1", 5, "2027-02-01"))

    getattr(a, metodo)(b)

    assert len(b) == 0
    assert b.primero() is None
    assert b.stock_total() == 0
    assert list(b) == []


@pytest.mark.parametrize("metodo", ["fusionar_recursivo", "fusionar_iterativo"])
def test_fusionar_con_una_lista_vacia(metodo):
    llena = lista_con(crear_lote("a1", 3), crear_lote("a2", 4, "2027-02-01"))

    destino = ListaLotes()
    getattr(destino, metodo)(llena)
    assert codigos(destino) == ["a1", "a2"]
    assert destino.stock_total() == 7

    vacia = ListaLotes()
    getattr(destino, metodo)(vacia)
    assert codigos(destino) == ["a1", "a2"]
    assert destino.stock_total() == 7


@pytest.mark.parametrize("metodo", ["fusionar_recursivo", "fusionar_iterativo"])
def test_fusionar_dos_listas_vacias(metodo):
    a = ListaLotes()

    getattr(a, metodo)(ListaLotes())

    assert len(a) == 0
    assert a.primero() is None


@pytest.mark.parametrize("metodo", ["fusionar_recursivo", "fusionar_iterativo"])
def test_fusionar_con_vencimientos_iguales_pone_primero_a_la_lista_propia(metodo):
    a = lista_con(crear_lote("a1", vence="2027-01-01"))
    b = lista_con(crear_lote("b1", vence="2027-01-01"))

    getattr(a, metodo)(b)

    assert codigos(a) == ["a1", "b1"]


@pytest.mark.parametrize("metodo", ["fusionar_recursivo", "fusionar_iterativo"])
def test_fusionar_listas_con_todos_los_lotes_de_una_antes_que_los_de_la_otra(metodo):
    a = lista_con(
        crear_lote("a1", vence="2027-01-01"), crear_lote("a2", vence="2027-02-01")
    )
    b = lista_con(
        crear_lote("b1", vence="2027-05-01"), crear_lote("b2", vence="2027-06-01")
    )

    getattr(b, metodo)(a)

    assert codigos(b) == ["a1", "a2", "b1", "b2"]


@pytest.mark.parametrize("metodo", ["fusionar_recursivo", "fusionar_iterativo"])
def test_fusionar_una_lista_consigo_misma_se_rechaza(metodo):
    a = lista_con(crear_lote("a1"))

    with pytest.raises(ValueError):
        getattr(a, metodo)(a)

    assert codigos(a) == ["a1"]


def test_la_version_recursiva_y_la_iterativa_dan_el_mismo_resultado():
    generador = random.Random(7)
    fechas = ["2027-01-01", "2027-01-02", "2027-01-03", "2027-01-04"]

    for intento in range(200):

        def armar(prefijo):
            lista = ListaLotes()

            for i in range(generador.randint(0, 12)):
                lista.insertar(
                    crear_lote(
                        f"{prefijo}{i}",
                        generador.randint(1, 9),
                        generador.choice(fechas),
                    )
                )

            return lista

        base_a, base_b = armar("a"), armar("b")
        esperado = [
            lote.codigo
            for lote in sorted(
                list(base_a) + list(base_b), key=lambda lote: lote.fecha_vencimiento
            )
        ]
        stock_esperado = base_a.stock_total() + base_b.stock_total()
        tamaño_esperado = len(base_a) + len(base_b)

        a1, b1 = armar_copia(base_a), armar_copia(base_b)
        a2, b2 = armar_copia(base_a), armar_copia(base_b)

        a1.fusionar_recursivo(b1)
        a2.fusionar_iterativo(b2)

        assert codigos(a1) == esperado, f"intento {intento}"
        assert codigos(a2) == esperado, f"intento {intento}"
        assert len(a1) == len(a2) == tamaño_esperado
        assert a1.stock_total() == a2.stock_total() == stock_esperado


def armar_copia(lista):
    copia = ListaLotes()

    for lote in lista:
        copia.insertar(
            Lote(
                lote.codigo,
                lote.cantidad,
                lote.fecha_produccion,
                lote.fecha_vencimiento,
            )
        )

    return copia


# ---------- límite de recursión ----------


def test_la_fusion_recursiva_desborda_la_pila_con_listas_muy_grandes():
    a = lista_grande("a", 700, 0)
    b = lista_grande("b", 700, 1)

    with pytest.raises(RecursionError):
        a.fusionar_recursivo(b)

    assert len(a) == 700
    assert len(b) == 700
    assert a.stock_total() == 700
    assert b.stock_total() == 700


def test_la_fusion_iterativa_soporta_listas_muy_grandes():
    a = lista_grande("a", 700, 0)
    b = lista_grande("b", 700, 1)

    a.fusionar_iterativo(b)

    fechas = [lote.fecha_vencimiento for lote in a]
    assert len(a) == 1400
    assert fechas == sorted(fechas)
    assert len(b) == 0


def test_fusionar_elige_iterativa_cuando_superan_el_limite():
    a = lista_grande("a", 700, 0)
    b = lista_grande("b", 700, 1)

    a.fusionar(b)

    assert len(a) == 1400
    assert 1400 > LIMITE_RECURSION


def test_fusionar_usa_la_recursiva_con_listas_pequenas(monkeypatch):
    llamadas = []
    original = ListaLotes.fusionar_recursivo

    def espia(self, otra):
        llamadas.append("recursivo")
        original(self, otra)

    monkeypatch.setattr(ListaLotes, "fusionar_recursivo", espia)

    a = lista_con(crear_lote("a1"))
    b = lista_con(crear_lote("b1", vence="2027-02-01"))
    a.fusionar(b)

    assert llamadas == ["recursivo"]
    assert codigos(a) == ["a1", "b1"]


def test_el_limite_de_recursion_deja_margen_con_la_pila_de_python():
    import sys

    assert LIMITE_RECURSION < sys.getrecursionlimit() // 1.5
