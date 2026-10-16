class Devolucion:
    """
    Registro de unidades devueltas a un producto, que entraron como un lote
    nuevo. Guarda lo necesario para revertir la devolución.

    Complejidad:
        Tiempo de creación: O(1).
        Espacio: O(1).
    """

    def __init__(
        self, numero: int, id_producto: int, codigo_lote: str, cantidad: int
    ) -> None:
        """
        Crea el registro de una devolución.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.numero = numero
        self.id_producto = id_producto
        self.codigo_lote = codigo_lote
        self.cantidad = cantidad

    def __str__(self) -> str:
        """
        Devuelve una representación legible de la devolución.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return (
            f"Devolución #{self.numero} | Producto: {self.id_producto} | "
            f"Lote: {self.codigo_lote} | Cantidad: {self.cantidad}"
        )
