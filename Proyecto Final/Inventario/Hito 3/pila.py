from collections.abc import Iterator
from typing import Any

from nodo import Nodo


class PilaEnlazada:
    """
    Pila LIFO dinámica sobre nodos enlazados: el último elemento apilado es
    el primero en salir.

    Complejidad:
        Espacio: O(n), un nodo por elemento.
    """

    def __init__(self) -> None:
        """
        Crea una pila vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._tope: Nodo | None = None
        self.tamaño = 0

    def __len__(self) -> int:
        """
        Devuelve la cantidad de elementos apilados.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño

    def __iter__(self) -> Iterator[Any]:
        """
        Recorre los elementos de la cima hacia el fondo sin sacarlos.

        Complejidad:
            Tiempo: O(n) el recorrido completo.
            Espacio: O(1).
        """
        actual = self._tope

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

    def apilar(self, elemento: Any) -> None:
        """
        Coloca un elemento en la cima.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._tope = Nodo(elemento, self._tope)
        self.tamaño += 1

    def desapilar(self) -> Any:
        """
        Quita y devuelve el elemento de la cima. Lanza IndexError si la pila
        está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self._tope is None:
            raise IndexError("La pila está vacía.")

        nodo = self._tope
        self._tope = nodo.siguiente
        self.tamaño -= 1

        return nodo.dato

    def cima(self) -> Any:
        """
        Devuelve el elemento de la cima sin quitarlo. Lanza IndexError si la
        pila está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self._tope is None:
            raise IndexError("La pila está vacía.")

        return self._tope.dato
