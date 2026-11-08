"""Nodo de lista ligada, compartido por la lista de lotes, la pila y las colas enlazadas."""

from typing import Any, Optional


class Nodo:
    """
    Nodo de una lista ligada: guarda un dato y la referencia al siguiente.

    Complejidad:
        Tiempo de creación: O(1).
        Espacio: O(1).
    """

    def __init__(self, dato: Any, siguiente: Optional["Nodo"] = None) -> None:
        """
        Crea un nodo con su dato y, opcionalmente, su siguiente nodo.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.dato = dato
        self.siguiente = siguiente
