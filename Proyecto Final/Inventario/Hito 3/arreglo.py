from typing import Any


class ArregloDinamico:
    """
    Implementa un arreglo dinámico con crecimiento automático.

    Complejidad:
        Tiempo: O(1) para acceso.
        Espacio: O(n), donde n es la capacidad del arreglo.
    """

    def __init__(self, capacidad_inicial: int = 10):
        """
        Inicializa el arreglo con la capacidad indicada.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(n).
        """
        if capacidad_inicial <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.capacidad = capacidad_inicial
        self.tamaño = 0
        self.datos = [None] * self.capacidad

    def __len__(self) -> int:
        """
        Devuelve la cantidad de elementos almacenados.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño

    def __getitem__(self, indice: int) -> Any:
        """
        Permite acceder a un elemento por su posición.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if indice < 0 or indice >= self.tamaño:
            raise IndexError("Índice fuera de rango.")

        return self.datos[indice]

    def __setitem__(self, indice: int, elemento: Any) -> None:
        """
        Reemplaza el elemento de una posición existente.

        No agrega elementos: el índice debe estar dentro del tamaño actual.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if indice < 0 or indice >= self.tamaño:
            raise IndexError("Índice fuera de rango.")

        self.datos[indice] = elemento

    def agregar(self, elemento: Any) -> None:
        """
        Agrega un elemento al final del arreglo.

        Complejidad:
            Tiempo: O(1) amortizado.
            Tiempo: O(n) cuando se redimensiona.
            Espacio: O(n) cuando se redimensiona.
        """
        if self.tamaño == self.capacidad:
            self._redimensionar()

        self.datos[self.tamaño] = elemento
        self.tamaño += 1

    def eliminar(self, indice: int) -> Any:
        """
        Elimina el elemento de una posición y lo devuelve.

        Desplaza una posición a la izquierda los elementos posteriores
        para no dejar huecos en el arreglo.

        Complejidad:
            Tiempo: O(n) por el desplazamiento.
            Espacio: O(1).
        """
        if indice < 0 or indice >= self.tamaño:
            raise IndexError("Índice fuera de rango.")

        eliminado = self.datos[indice]

        for i in range(indice, self.tamaño - 1):
            self.datos[i] = self.datos[i + 1]

        self.datos[self.tamaño - 1] = None
        self.tamaño -= 1

        return eliminado

    def _redimensionar(self) -> None:
        """
        Duplica la capacidad del arreglo y conserva sus elementos.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(n).
        """
        nueva_capacidad = self.capacidad * 2
        nuevos_datos = [None] * nueva_capacidad

        for i in range(self.tamaño):
            nuevos_datos[i] = self.datos[i]

        self.datos = nuevos_datos
        self.capacidad = nueva_capacidad
