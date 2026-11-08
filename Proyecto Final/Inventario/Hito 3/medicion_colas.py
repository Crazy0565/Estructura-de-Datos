import time
from collections import deque

from cola_circular import ColaCircular
from cola_enlazada import ColaEnlazada
from pila import PilaEnlazada


def cronometrar(funcion) -> float:
    """
    Devuelve los segundos que tarda en ejecutarse la función.

    Complejidad:
        Tiempo: el de la función medida.
        Espacio: O(1).
    """
    inicio = time.perf_counter()
    funcion()

    return time.perf_counter() - inicio


def encolar_y_desencolar(cola, n: int, encolar: str, desencolar: str) -> None:
    """
    Encola n elementos y luego los desencola todos.

    Complejidad:
        Tiempo: O(n) si cada operación de la cola es O(1).
        Espacio: O(n).
    """
    agregar = getattr(cola, encolar)
    quitar = getattr(cola, desencolar)

    for i in range(n):
        agregar(i)

    for _ in range(n):
        quitar()


def medir_colas() -> None:
    """
    Compara ColaEnlazada, ColaCircular, deque y list.pop(0) con n encolados
    seguidos de n desencolados.

    Complejidad:
        Tiempo: O(n) por tamaño, salvo list.pop(0) que es O(n²).
        Espacio: O(n).
    """
    print("== n encolar + n desencolar (segundos) ==")

    for n in [1000, 10000, 100000]:
        t_enlazada = cronometrar(
            lambda: encolar_y_desencolar(ColaEnlazada(), n, "encolar", "desencolar")
        )
        t_circular = cronometrar(
            lambda: encolar_y_desencolar(ColaCircular(n), n, "encolar", "desencolar")
        )
        t_deque = cronometrar(
            lambda: encolar_y_desencolar(deque(), n, "append", "popleft")
        )

        lista = []
        t_lista = cronometrar(lambda: encolar_y_desencolar_lista(lista, n))

        print(
            f"n={n:>7}  ColaEnlazada={t_enlazada:8.4f}   ColaCircular={t_circular:8.4f}   "
            f"deque={t_deque:8.4f}   list.pop(0)={t_lista:8.4f}"
        )


def encolar_y_desencolar_lista(lista: list, n: int) -> None:
    """
    Usa una list como cola: append al final y pop(0) al frente.

    Complejidad:
        Tiempo: O(n²) por el desplazamiento de pop(0).
        Espacio: O(n).
    """
    for i in range(n):
        lista.append(i)

    for _ in range(n):
        lista.pop(0)


def medir_pila() -> None:
    """
    Compara PilaEnlazada con una list usada como pila (append y pop).

    Complejidad:
        Tiempo: O(n) por tamaño.
        Espacio: O(n).
    """
    print("\n== n apilar + n desapilar (segundos) ==")

    for n in [1000, 10000, 100000]:
        t_pila = cronometrar(
            lambda: encolar_y_desencolar(PilaEnlazada(), n, "apilar", "desapilar")
        )
        t_lista = cronometrar(lambda: encolar_y_desencolar([], n, "append", "pop"))

        print(f"n={n:>7}  PilaEnlazada={t_pila:8.4f}   list(append/pop)={t_lista:8.4f}")


if __name__ == "__main__":
    medir_colas()
    medir_pila()
