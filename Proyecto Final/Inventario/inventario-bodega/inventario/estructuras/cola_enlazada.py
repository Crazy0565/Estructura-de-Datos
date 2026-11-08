"""Cola enlazada propia (versión dinámica, sobre nodos)."""

from collections.abc import Iterator
from typing import Any

from inventario.estructuras.nodo import Nodo


class ColaEnlazada:
    """
    Cola FIFO dinámica sobre nodos enlazados, con punteros al primero y al
    último para que encolar y desencolar no recorran nada.

    No tiene tope: crece mientras haya memoria.

    Complejidad:
        Espacio: O(n), un nodo por elemento.
    """

    def __init__(self) -> None:
        """
        Crea una cola vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._primero: Nodo | None = None
        self._ultimo: Nodo | None = None
        self.tamaño = 0

    def __len__(self) -> int:
        """
        Devuelve la cantidad de elementos en espera.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño

    def __iter__(self) -> Iterator[Any]:
        """
        Recorre los elementos del más antiguo al más reciente sin sacarlos.

        Complejidad:
            Tiempo: O(n) el recorrido completo.
            Espacio: O(1).
        """
        actual = self._primero

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def esta_vacia(self) -> bool:
        """
        Indica si no hay elementos.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño == 0

    def encolar(self, elemento: Any) -> None:
        """
        Agrega un elemento al final de la cola.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        nodo = Nodo(elemento)

        if self._ultimo is None:
            self._primero = nodo
        else:
            self._ultimo.siguiente = nodo

        self._ultimo = nodo
        self.tamaño += 1

    def desencolar(self) -> Any:
        """
        Quita y devuelve el elemento más antiguo. Lanza IndexError si la
        cola está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self._primero is None:
            raise IndexError("La cola está vacía.")

        nodo = self._primero
        self._primero = nodo.siguiente

        if self._primero is None:
            self._ultimo = None

        self.tamaño -= 1

        return nodo.dato

    def frente(self) -> Any:
        """
        Devuelve el elemento más antiguo sin quitarlo. Lanza IndexError si
        la cola está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self._primero is None:
            raise IndexError("La cola está vacía.")

        return self._primero.dato
