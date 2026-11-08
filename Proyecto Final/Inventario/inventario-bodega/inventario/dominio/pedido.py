"""Pedido de salida y sus estados (pendiente, despachado, rechazado)."""

from inventario.estructuras.arreglo import ArregloDinamico

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

    def __init__(
        self, numero: int, id_producto: int, cantidad: int, urgencia: int = 0
    ) -> None:
        """
        Crea un pedido pendiente. `urgencia` 0 es un pedido normal; de 1 a 9
        es urgente (más alto, más prioritario). Lanza ValueError si la
        cantidad no es positiva o la urgencia está fuera de rango.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if cantidad <= 0:
            raise ValueError("La cantidad del pedido debe ser mayor que cero.")

        if not 0 <= urgencia <= 9:
            raise ValueError("La urgencia debe estar entre 0 y 9.")

        self.numero = numero
        self.urgencia = urgencia
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
