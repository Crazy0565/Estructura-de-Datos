from typing import Any


class MatrizBodega:
    """
    Representa una matriz cuadrada escalable para las ubicaciones
    de productos dentro de la bodega.

    Complejidad:
        Acceso y modificación normal: O(1).
        Redimensionamiento: O(n²).
    """

    def __init__(self, tamaño_inicial: int = 10):
        """
        Crea una matriz cuadrada inicial.

        Complejidad:
            Tiempo: O(n²).
            Espacio: O(n²).
        """
        if tamaño_inicial <= 0:
            raise ValueError("El tamaño debe ser mayor que cero.")

        self.tamaño = tamaño_inicial
        self.datos = [[None for _ in range(self.tamaño)] for _ in range(self.tamaño)]

    def asignar(self, fila: int, columna: int, producto: Any) -> None:
        """
        Asigna un producto a una posición.

        Si la posición está fuera de la matriz, esta se amplía. Si ya hay
        otro producto en esa ubicación, se rechaza la asignación en vez de
        sobrescribirlo en silencio.

        Complejidad:
            Tiempo: O(1) normalmente.
            Tiempo: O(n²) cuando se redimensiona.
            Espacio: O(n²) cuando se redimensiona.
        """
        if fila < 0 or columna < 0:
            raise IndexError("La posición no puede ser negativa.")

        if fila >= self.tamaño or columna >= self.tamaño:
            nuevo_tamaño = max(fila + 1, columna + 1)
            self._ampliar(nuevo_tamaño)

        ocupante = self.datos[fila][columna]

        if ocupante is not None and ocupante is not producto:
            raise ValueError("La ubicación ya está ocupada por otro producto.")

        self.datos[fila][columna] = producto

    def obtener(self, fila: int, columna: int) -> Any:
        """
        Obtiene el producto ubicado en una posición.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._validar_posicion(fila, columna)
        return self.datos[fila][columna]

    def eliminar(self, fila: int, columna: int) -> Any:
        """
        Elimina el producto de una ubicación y devuelve el producto eliminado.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._validar_posicion(fila, columna)

        producto = self.datos[fila][columna]
        self.datos[fila][columna] = None

        return producto

    def _ampliar(self, nuevo_tamaño: int) -> None:
        """
        Amplía la matriz conservando los productos existentes.

        Complejidad:
            Tiempo: O(n²).
            Espacio: O(n²).
        """
        nueva_matriz = [
            [None for _ in range(nuevo_tamaño)] for _ in range(nuevo_tamaño)
        ]

        for i in range(self.tamaño):
            for j in range(self.tamaño):
                nueva_matriz[i][j] = self.datos[i][j]

        self.datos = nueva_matriz
        self.tamaño = nuevo_tamaño

    def _validar_posicion(self, fila: int, columna: int) -> None:
        """
        Verifica que una posición se encuentre dentro de la matriz.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if fila < 0 or columna < 0 or fila >= self.tamaño or columna >= self.tamaño:
            raise IndexError("La posición está fuera de la matriz.")
