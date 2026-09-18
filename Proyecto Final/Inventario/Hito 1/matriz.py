class MatrizBodega:
    """Matriz escalable para almacenar las ubicaciones de la bodega."""

    def __init__(self, tamaño_inicial: int = 10):
        """Crea una matriz cuadrada inicial."""
        if tamaño_inicial <= 0:
            raise ValueError("El tamaño debe ser mayor que cero.")

        self.tamaño = tamaño_inicial
        self.datos = [
            [None for _ in range(self.tamaño)]
            for _ in range(self.tamaño)
        ]

    def asignar(self, fila: int, columna: int, producto) -> None:
        """
        Asigna un producto a una posición.

        Si la posición está fuera de la matriz, esta se amplía.

        Complejidad:
            O(1) normalmente.
            O(n²) cuando se redimensiona.
        """
        if fila < 0 or columna < 0:
            raise IndexError("La posición no puede ser negativa.")

        if fila >= self.tamaño or columna >= self.tamaño:
            nuevo_tamaño = max(fila + 1, columna + 1)
            self._ampliar(nuevo_tamaño)

        self.datos[fila][columna] = producto

    def obtener(self, fila: int, columna: int):
        """
        Obtiene un producto de una ubicación.

        Complejidad: O(1).
        """
        self._validar_posicion(fila, columna)
        return self.datos[fila][columna]

    def eliminar(self, fila: int, columna: int):
        """
        Elimina un producto de una ubicación.

        Complejidad: O(1).
        """
        self._validar_posicion(fila, columna)

        producto = self.datos[fila][columna]
        self.datos[fila][columna] = None

        return producto

    def _ampliar(self, nuevo_tamaño: int) -> None:
        """
        Amplía la matriz conservando los productos existentes.

        Complejidad: O(n²).
        """
        nueva_matriz = [
            [None for _ in range(nuevo_tamaño)]
            for _ in range(nuevo_tamaño)
        ]

        for i in range(self.tamaño):
            for j in range(self.tamaño):
                nueva_matriz[i][j] = self.datos[i][j]

        self.datos = nueva_matriz
        self.tamaño = nuevo_tamaño

    def _validar_posicion(self, fila: int, columna: int) -> None:
        """Verifica que la posición exista."""
        if (
            fila < 0
            or columna < 0
            or fila >= self.tamaño
            or columna >= self.tamaño
        ):
            raise IndexError("La posición está fuera de la matriz.")