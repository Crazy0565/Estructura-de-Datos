"""
Cola de prioridad propia sobre un montículo binario mínimo.

El elemento con el número de prioridad MÁS BAJO sale primero (0 = lo más
urgente). Ante prioridades iguales sale primero el que llegó antes (orden
estable, gracias a un número de llegada), de modo que la cola de pedidos
urgentes respeta el orden de llegada dentro de cada nivel.

El montículo vive en un `ArregloDinamico` propio: el hijo izquierdo del nodo
i está en 2i+1, el derecho en 2i+2 y el padre en (i-1)//2.
"""

from typing import Any

from inventario.estructuras.arreglo import ArregloDinamico


class ColaPrioridad:
    """
    Cola de prioridad (montículo mínimo) con salida estable.

    Complejidad:
        Espacio: O(n).
    """

    def __init__(self) -> None:
        """
        Crea una cola vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._monticulo = ArregloDinamico()
        self._llegadas = 0

    def __len__(self) -> int:
        """
        Devuelve la cantidad de elementos en espera.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return len(self._monticulo)

    def esta_vacia(self) -> bool:
        """
        Indica si no hay elementos.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return len(self._monticulo) == 0

    def encolar(self, prioridad: float, dato: Any) -> None:
        """
        Agrega un elemento con su prioridad (menor número = más urgente).

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(1) amortizado.
        """
        self._monticulo.agregar((prioridad, self._llegadas, dato))
        self._llegadas += 1
        self._subir(len(self._monticulo) - 1)

    def frente(self) -> Any:
        """
        Devuelve el elemento que saldría primero, sin quitarlo. Lanza
        IndexError si la cola está vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía.")

        return self._monticulo[0][2]

    def desencolar(self) -> Any:
        """
        Quita y devuelve el elemento más urgente. Lanza IndexError si la
        cola está vacía.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(1).
        """
        return self.desencolar_con_prioridad()[1]

    def desencolar_con_prioridad(self) -> tuple[float, Any]:
        """
        Quita el elemento más urgente y devuelve (prioridad, dato). Lanza
        IndexError si la cola está vacía.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(1).
        """
        if self.esta_vacia():
            raise IndexError("La cola de prioridad está vacía.")

        raiz = self._monticulo[0]
        ultimo = self._monticulo.eliminar(len(self._monticulo) - 1)

        if len(self._monticulo) > 0:
            self._monticulo[0] = ultimo
            self._bajar(0)

        return raiz[0], raiz[2]

    def _antes(self, i: int, j: int) -> bool:
        """
        Indica si la entrada i debe salir antes que la j: menor prioridad,
        y a igual prioridad, la que llegó antes.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        a, b = self._monticulo[i], self._monticulo[j]

        if a[0] != b[0]:
            return a[0] < b[0]

        return a[1] < b[1]

    def _intercambiar(self, i: int, j: int) -> None:
        """
        Intercambia dos entradas del montículo.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        temporal = self._monticulo[i]
        self._monticulo[i] = self._monticulo[j]
        self._monticulo[j] = temporal

    def _subir(self, indice: int) -> None:
        """
        Sube una entrada mientras deba salir antes que su padre.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(1).
        """
        while indice > 0:
            padre = (indice - 1) // 2

            if not self._antes(indice, padre):
                return

            self._intercambiar(indice, padre)
            indice = padre

    def _bajar(self, indice: int) -> None:
        """
        Baja una entrada intercambiándola con su hijo más urgente mientras
        alguno deba salir antes que ella.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(1).
        """
        total = len(self._monticulo)

        while True:
            izquierdo = 2 * indice + 1
            derecho = izquierdo + 1
            primero = indice

            if izquierdo < total and self._antes(izquierdo, primero):
                primero = izquierdo

            if derecho < total and self._antes(derecho, primero):
                primero = derecho

            if primero == indice:
                return

            self._intercambiar(indice, primero)
            indice = primero

    def en_orden(self, maximo: int | None = None) -> ArregloDinamico:
        """
        Devuelve los datos en el orden en que saldrían, sin sacarlos de la cola
        (hasta `maximo` si se indica). Trabaja sobre una copia del montículo.

        Complejidad:
            Tiempo: O(n + m log n) para m datos pedidos.
            Espacio: O(n) por la copia.
        """
        copia = ColaPrioridad()

        for i in range(len(self._monticulo)):
            copia._monticulo.agregar(self._monticulo[i])

        copia._llegadas = self._llegadas
        resultado = ArregloDinamico()

        while not copia.esta_vacia() and (maximo is None or len(resultado) < maximo):
            resultado.agregar(copia.desencolar())

        return resultado
