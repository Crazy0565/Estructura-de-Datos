class Matriz:
    """Representa una matriz almacenada en una única lista plana."""

    def __init__(self, filas: int, columnas: int) -> None:
        """Crea una matriz de filas x columnas llena de ceros.

        Raises:
            ValueError: Si filas o columnas no son positivas.

        Complejidad: O(f · c)
        """
        if filas <= 0 or columnas <= 0:
            raise ValueError("Las filas y columnas deben ser positivas.")

        self._filas = filas
        self._columnas = columnas
        self._datos = [0] * (filas * columnas)

    def _posicion(self, i: int, j: int) -> int:
        """Convierte una coordenada de matriz en una posición de la lista plana.

        Complejidad: O(1)
        """
        return i * self._columnas + j

    def _validar_indices(self, i: int, j: int) -> None:
        """Verifica que una coordenada pertenezca a la matriz.

        Raises:
            IndexError: Si la coordenada está fuera de la matriz.

        Complejidad: O(1)
        """
        if i < 0 or i >= self._filas or j < 0 or j >= self._columnas:
            raise IndexError("La posición está fuera de la matriz.")

    def filas(self) -> int:
        """Devuelve la cantidad de filas de la matriz.

        Complejidad: O(1)
        """
        return self._filas

    def columnas(self) -> int:
        """Devuelve la cantidad de columnas de la matriz.

        Complejidad: O(1)
        """
        return self._columnas

    def obtener(self, i: int, j: int) -> int:
        """Devuelve el valor almacenado en la celda (i, j).

        Raises:
            IndexError: Si la coordenada está fuera de la matriz.

        Complejidad: O(1)
        """
        self._validar_indices(i, j)
        return self._datos[self._posicion(i, j)]

    def asignar(self, i: int, j: int, valor: int) -> None:
        """Asigna valor a la celda (i, j).

        Raises:
            IndexError: Si la coordenada está fuera de la matriz.

        Complejidad: O(1)
        """
        self._validar_indices(i, j)
        self._datos[self._posicion(i, j)] = valor

    def suma(self) -> int:
        """Devuelve la suma de todos los valores de la matriz.

        Complejidad: O(f · c)
        """
        return sum(self._datos)
