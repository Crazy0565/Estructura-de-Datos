import sys
import time
from datetime import date, timedelta

from arreglo import ArregloDinamico
from lista_lotes import ListaLotes
from lote import Lote
from nodo import Nodo


def fecha(dia: int) -> str:
    """
    Devuelve una fecha ISO a partir de un desplazamiento en días.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return (date(2027, 1, 1) + timedelta(days=dia)).isoformat()


def construir_lista(
    n: int, paso: int = 1, desplazamiento: int = 0, prefijo: str = "L"
) -> ListaLotes:
    """
    Arma una lista de n lotes de una unidad ya ordenados, enlazando los
    nodos directamente para no pagar el O(n²) de insertar uno por uno.

    Complejidad:
        Tiempo: O(n).
        Espacio: O(n).
    """
    lista = ListaLotes()
    ultimo = None

    for i in range(n):
        nodo = Nodo(
            Lote(f"{prefijo}{i}", 1, "2026-01-01", fecha(paso * i + desplazamiento))
        )

        if ultimo is None:
            lista.cabeza = nodo
        else:
            ultimo.siguiente = nodo

        ultimo = nodo

    lista.tamaño = n
    lista._stock = n

    return lista


def promedio(funcion, repeticiones: int) -> float:
    """
    Devuelve el tiempo medio en segundos de ejecutar la función.

    Complejidad:
        Tiempo: O(r) ejecuciones de la función.
        Espacio: O(1).
    """
    inicio = time.perf_counter()

    for _ in range(repeticiones):
        funcion()

    return (time.perf_counter() - inicio) / repeticiones


def medir_quitar_del_frente() -> None:
    """
    Compara quitar el primer elemento en ListaLotes, ArregloDinamico y list.

    Complejidad:
        Tiempo: O(n) por tamaño medido, por construir cada estructura.
        Espacio: O(n).
    """
    print("== Quitar del frente (tiempo de una operación) ==")

    for n in [1000, 10000, 100000]:
        lista = construir_lista(n)
        t_lista = promedio(lambda: lista.despachar(1), 200)

        arreglo = ArregloDinamico(n)

        for i in range(n):
            arreglo.agregar(i)

        t_arreglo = promedio(lambda: arreglo.eliminar(0), 20)

        nativa = list(range(n))
        t_nativa = promedio(lambda: nativa.pop(0), 200)

        print(
            f"n={n:>7}  "
            f"ListaLotes.despachar(1)={t_lista * 1e6:9.2f} us   "
            f"ArregloDinamico.eliminar(0)={t_arreglo * 1e6:10.2f} us   "
            f"list.pop(0)={t_nativa * 1e6:8.2f} us"
        )


def medir_fusion() -> None:
    """
    Compara la fusión recursiva con la iterativa y busca el límite de la pila.

    Complejidad:
        Tiempo: O(n) por tamaño medido.
        Espacio: O(n).
    """
    print("\n== Fusión recursiva frente a iterativa ==")

    for total in [100, 400, 900, 1400, 5000, 50000]:
        mitad = total // 2
        resultados = []

        for nombre in ("fusionar_recursivo", "fusionar_iterativo"):
            a = construir_lista(mitad, 2, 0, "a")
            b = construir_lista(total - mitad, 2, 1, "b")
            inicio = time.perf_counter()

            try:
                getattr(a, nombre)(b)
                milisegundos = (time.perf_counter() - inicio) * 1e3
                resultados.append(f"{nombre}={milisegundos:8.3f} ms")
            except RecursionError:
                resultados.append(f"{nombre}=RecursionError")

        print(f"total={total:>6}  " + "   ".join(resultados))

    print(f"\nLímite de recursión de Python: {sys.getrecursionlimit()}")

    mayor = 0

    for total in range(100, 1100, 10):
        a = construir_lista(total // 2, 2, 0, "a")
        b = construir_lista(total - total // 2, 2, 1, "b")

        try:
            a.fusionar_recursivo(b)
            mayor = total
        except RecursionError:
            break

    print(f"Mayor total de lotes fusionado sin error por la recursiva: {mayor}")


if __name__ == "__main__":
    medir_quitar_del_frente()
    medir_fusion()
