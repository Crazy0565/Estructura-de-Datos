class Producto:
    """Representa un producto almacenado en el inventario."""

    def __init__(
        self,
        id_producto: int,
        nombre: str,
        categoria: str,
        cantidad: int,
        tiempo_produccion: int,
        fecha_produccion: str,
        fecha_vencimiento: str,
        precio: float,
        pasillo: int,
        estante: int
    ):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad
        self.tiempo_produccion = tiempo_produccion
        self.fecha_produccion = fecha_produccion
        self.fecha_vencimiento = fecha_vencimiento
        self.precio = precio
        self.pasillo = pasillo
        self.estante = estante

    def __str__(self) -> str:
        """Devuelve una representación legible del producto."""
        return (
            f"ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio: ${self.precio}"
        )