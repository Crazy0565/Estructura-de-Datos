"""
Plano de la bodega como grafo.

La bodega es una cuadrícula de `lado` pasillos x `lado` estantes (la misma
que usa la matriz de ubicaciones). Cada ubicación es un nodo, más un nodo
especial, el muelle de despacho (nodo 0), donde empieza y termina cada ruta.

Los caminos de la planta son:
    - a lo largo de cada pasillo, entre estantes contiguos (DIST_ESTANTE);
    - dos corredores transversales, uno al frente (estante 0) y otro al
      fondo (último estante), que unen pasillos contiguos (DIST_PASILLO);
    - el muelle, conectado a la ubicación (pasillo 0, estante 0) (DIST_MUELLE).

Para cambiar de pasillo hay que pasar por el frente o por el fondo, como en
una bodega real: por eso la ruta más corta entre dos estantes no es trivial.
"""

from inventario.grafos.grafo_bodega import GrafoListaAdyacencia

DIST_ESTANTE = 2
DIST_PASILLO = 4
DIST_MUELLE = 2
MUELLE = 0


class PlanoBodega:
    """
    Grafo de la planta: lado² ubicaciones + el muelle.

    Complejidad:
        Espacio: O(lado²) con lista de adyacencia (el grado máximo es 4).
    """

    def __init__(self, lado: int, fabrica: type = GrafoListaAdyacencia) -> None:
        """
        Construye el plano. `fabrica` es la clase de grafo a usar (lista o
        matriz de adyacencia). Lanza ValueError si `lado` no es positivo.

        Complejidad:
            Tiempo: O(lado²).
            Espacio: O(lado²).
        """
        if lado <= 0:
            raise ValueError("El lado de la bodega debe ser positivo.")

        self.lado = lado
        self.grafo = fabrica(lado * lado + 1)
        self.grafo.agregar_arista(MUELLE, self.nodo_de(0, 0), DIST_MUELLE)

        for pasillo in range(lado):
            for estante in range(lado - 1):
                self.grafo.agregar_arista(
                    self.nodo_de(pasillo, estante),
                    self.nodo_de(pasillo, estante + 1),
                    DIST_ESTANTE,
                )

        for pasillo in range(lado - 1):
            for estante in (0, lado - 1):
                self.grafo.agregar_arista(
                    self.nodo_de(pasillo, estante),
                    self.nodo_de(pasillo + 1, estante),
                    DIST_PASILLO,
                )

    def nodo_de(self, pasillo: int, estante: int) -> int:
        """
        Número de nodo de una ubicación. Lanza IndexError si queda fuera de
        la bodega.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if not (0 <= pasillo < self.lado and 0 <= estante < self.lado):
            raise IndexError("La ubicación está fuera de la bodega.")

        return pasillo * self.lado + estante + 1

    def ubicacion_de(self, nodo: int) -> tuple[int, int] | None:
        """
        Ubicación (pasillo, estante) de un nodo, o None si es el muelle.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if nodo == MUELLE:
            return None

        if not (0 < nodo <= self.lado * self.lado):
            raise IndexError(f"El nodo {nodo} no existe en el plano.")

        return divmod(nodo - 1, self.lado)
