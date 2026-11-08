"""
Grafos propios, no dirigidos y ponderados, con dos representaciones que
ofrecen exactamente la misma interfaz:

    GrafoListaAdyacencia: cada nodo guarda una lista ligada de sus vecinos.
        Espacio O(V + E). Es la elegida para el plano de la bodega, un grafo
        disperso (cada punto toca como máximo 4 vecinos).
    GrafoMatrizAdyacencia: una matriz V x V de pesos. Espacio O(V²) aunque
        casi todas las celdas estén vacías; se conserva para poder medir el
        costo de memoria frente a la lista (ver medicion_grafo.py).

Los nodos son enteros de 0 a V-1. Los pesos son distancias (positivas).
"""

from collections.abc import Iterator

from arreglo import ArregloDinamico
from nodo import Nodo


def _validar_arista(grafo, u: int, v: int, peso: float) -> None:
    """
    Valida los datos de una arista. Lanza IndexError si un nodo no existe y
    ValueError si es un lazo (u == v) o el peso no es positivo.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    grafo._validar_nodo(u)
    grafo._validar_nodo(v)

    if u == v:
        raise ValueError("No se admiten lazos (una arista de un nodo a sí mismo).")

    if peso <= 0:
        raise ValueError("El peso de una arista debe ser positivo.")


class GrafoListaAdyacencia:
    """
    Grafo con listas de adyacencia ligadas.

    Complejidad:
        Espacio: O(V + E).
    """

    def __init__(self, nodos: int) -> None:
        """
        Crea un grafo con `nodos` nodos y sin aristas. Lanza ValueError si
        `nodos` no es positivo.

        Complejidad:
            Tiempo: O(V).
            Espacio: O(V).
        """
        if nodos <= 0:
            raise ValueError("El grafo debe tener al menos un nodo.")

        self._nodos = nodos
        self._aristas = 0
        self._cabezas = ArregloDinamico(nodos)

        for _ in range(nodos):
            self._cabezas.agregar(None)

    @property
    def numero_nodos(self) -> int:
        """
        Cantidad de nodos.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self._nodos

    @property
    def numero_aristas(self) -> int:
        """
        Cantidad de aristas (cada arista no dirigida cuenta una vez).

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self._aristas

    def agregar_arista(self, u: int, v: int, peso: float) -> None:
        """
        Conecta u con v en ambos sentidos. Lanza ValueError si la arista ya
        existe, es un lazo o el peso no es positivo, e IndexError si un nodo
        no existe.

        Complejidad:
            Tiempo: O(grado(u)) por la búsqueda de duplicado.
            Espacio: O(1).
        """
        _validar_arista(self, u, v, peso)

        if self.peso(u, v) is not None:
            raise ValueError(f"La arista {u}-{v} ya existe.")

        self._cabezas[u] = Nodo((v, peso), self._cabezas[u])
        self._cabezas[v] = Nodo((u, peso), self._cabezas[v])
        self._aristas += 1

    def peso(self, u: int, v: int) -> float | None:
        """
        Devuelve el peso de la arista u-v, o None si no existe.

        Complejidad:
            Tiempo: O(grado(u)).
            Espacio: O(1).
        """
        self._validar_nodo(u)
        self._validar_nodo(v)

        for vecino, peso in self.vecinos(u):
            if vecino == v:
                return peso

        return None

    def vecinos(self, u: int) -> Iterator[tuple[int, float]]:
        """
        Entrega los pares (vecino, peso) de un nodo.

        Complejidad:
            Tiempo: O(grado(u)).
            Espacio: O(1).
        """
        self._validar_nodo(u)
        actual = self._cabezas[u]

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def grado(self, u: int) -> int:
        """
        Cantidad de vecinos de un nodo.

        Complejidad:
            Tiempo: O(grado(u)).
            Espacio: O(1).
        """
        total = 0

        for _ in self.vecinos(u):
            total += 1

        return total

    def _validar_nodo(self, u: int) -> None:
        """
        Lanza IndexError si el nodo no existe.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if u < 0 or u >= self._nodos:
            raise IndexError(f"El nodo {u} no existe.")


class GrafoMatrizAdyacencia:
    """
    Grafo con matriz de adyacencia de pesos (None = sin arista).

    Complejidad:
        Espacio: O(V²).
    """

    def __init__(self, nodos: int) -> None:
        """
        Crea un grafo con `nodos` nodos y sin aristas. Lanza ValueError si
        `nodos` no es positivo.

        Complejidad:
            Tiempo: O(V²).
            Espacio: O(V²).
        """
        if nodos <= 0:
            raise ValueError("El grafo debe tener al menos un nodo.")

        self._nodos = nodos
        self._aristas = 0
        self._filas = ArregloDinamico(nodos)

        for _ in range(nodos):
            fila = ArregloDinamico(nodos)

            for _ in range(nodos):
                fila.agregar(None)

            self._filas.agregar(fila)

    @property
    def numero_nodos(self) -> int:
        """
        Cantidad de nodos.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self._nodos

    @property
    def numero_aristas(self) -> int:
        """
        Cantidad de aristas (cada arista no dirigida cuenta una vez).

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self._aristas

    def agregar_arista(self, u: int, v: int, peso: float) -> None:
        """
        Conecta u con v en ambos sentidos. Mismos errores que la versión con
        listas.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        _validar_arista(self, u, v, peso)

        if self._filas[u][v] is not None:
            raise ValueError(f"La arista {u}-{v} ya existe.")

        self._filas[u][v] = peso
        self._filas[v][u] = peso
        self._aristas += 1

    def peso(self, u: int, v: int) -> float | None:
        """
        Devuelve el peso de la arista u-v, o None si no existe.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._validar_nodo(u)
        self._validar_nodo(v)

        return self._filas[u][v]

    def vecinos(self, u: int) -> Iterator[tuple[int, float]]:
        """
        Entrega los pares (vecino, peso) de un nodo, recorriendo toda su fila.

        Complejidad:
            Tiempo: O(V).
            Espacio: O(1).
        """
        self._validar_nodo(u)
        fila = self._filas[u]

        for v in range(self._nodos):
            if fila[v] is not None:
                yield v, fila[v]

    def grado(self, u: int) -> int:
        """
        Cantidad de vecinos de un nodo.

        Complejidad:
            Tiempo: O(V).
            Espacio: O(1).
        """
        total = 0

        for _ in self.vecinos(u):
            total += 1

        return total

    def _validar_nodo(self, u: int) -> None:
        """
        Lanza IndexError si el nodo no existe.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if u < 0 or u >= self._nodos:
            raise IndexError(f"El nodo {u} no existe.")
