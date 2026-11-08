from collections.abc import Iterator
from typing import Any


class ColaLlenaError(Exception):
    """Se intentó encolar en una cola circular que ya alcanzó su capacidad."""


class ColaCircular:
    """
    Cola FIFO estática sobre un arreglo de capacidad fija.

    Los índices del primer elemento y del siguiente hueco avanzan en círculo
    (módulo la capacidad), así que encolar y desencolar nunca desplazan
    elementos ni reservan memoria nueva.

    Complejidad:
        Espacio: O(c), con c la capacidad fija.
    """

    def __init__(self, capacidad: int) -> None:
        """
        Crea una cola vacía con la capacidad indicada.

        Lanza ValueError si la capacidad no es positiva.

        Complejidad:
            Tiempo: O(c).
            Espacio: O(c).
        """
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.capacidad = capacidad
        self.tamaño = 0
        self._inicio = 0
        self._datos = [None] * capacidad

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
        for i in range(self.tamaño):
            yield self._datos[(self._inicio + i) % self.capacidad]

    def esta_vacia(self) -> bool:
        """
        Indica si no hay elementos.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño == 0

    def esta_llena(self) -> bool:
        """
        Indica si se alcanzó la capacidad.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño == self.capacidad

    def encolar(self, elemento: Any) -> None:
        """
        Agrega un elemento al final. Lanza ColaLlenaError si no hay espacio.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self.esta_llena():
            raise ColaLlenaError("La cola está llena.")

        posicion = (self._inicio + self.tamaño) % self.capacidad
        self._datos[posicion] = elemento
        self.tamaño += 1

    def desencolar(self) -> Any:
        """
        Quita y devuelve el elemento más antiguo. Lanza IndexError si la
        cola está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")

        elemento = self._datos[self._inicio]
        self._datos[self._inicio] = None
        self._inicio = (self._inicio + 1) % self.capacidad
        self.tamaño -= 1

        return elemento

    def frente(self) -> Any:
        """
        Devuelve el elemento más antiguo sin quitarlo. Lanza IndexError si
        la cola está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")

        return self._datos[self._inicio]
