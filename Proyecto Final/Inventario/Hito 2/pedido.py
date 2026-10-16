from arreglo import ArregloDinamico

PENDIENTE = "pendiente"
DESPACHADO = "despachado"
RECHAZADO = "rechazado"


class Pedido:
    """
    Solicitud de despacho de unidades de un producto.

    Nace pendiente. Al procesarse pasa a despachado (con el detalle de
    lotes usados) o a rechazado (con el motivo).

    Complejidad:
        Tiempo de creación: O(1).
        Espacio: O(1) sin contar el detalle del despacho.
    """

    def __init__(self, numero: int, id_producto: int, cantidad: int) -> None:
        """
        Crea un pedido pendiente. Lanza ValueError si la cantidad no es
        positiva.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if cantidad <= 0:
            raise ValueError("La cantidad del pedido debe ser mayor que cero.")

        self.numero = numero
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.estado = PENDIENTE
        self.tomas: ArregloDinamico | None = None
        self.motivo = ""

    def __str__(self) -> str:
        """
        Devuelve una representación legible del pedido.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        texto = (
            f"Pedido #{self.numero} | Producto: {self.id_producto} | "
            f"Cantidad: {self.cantidad} | Estado: {self.estado}"
        )

        if self.estado == RECHAZADO:
            texto += f" ({self.motivo})"

        return texto
