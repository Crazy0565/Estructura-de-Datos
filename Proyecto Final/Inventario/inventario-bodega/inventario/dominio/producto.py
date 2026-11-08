"""Producto del inventario; sus existencias viven en una lista ligada de lotes."""

from inventario.dominio.lote import Lote
from inventario.estructuras.lista_lotes import ListaLotes

SIN_VENCIMIENTO = "9999-12-31"


class Producto:
    """
    Representa un producto almacenado en el inventario.

    Sus existencias viven en una lista ligada de lotes ordenada por
    vencimiento. La cantidad total y el próximo vencimiento se derivan de
    esa lista, así que nunca quedan desincronizados.

    Complejidad:
        Tiempo de creación: O(1).
        Espacio: O(l), con l lotes.
    """

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
        estante: int,
    ) -> None:
        """
        Inicializa un producto. Si la cantidad es positiva, crea su lote
        inicial con las fechas indicadas; si es cero, queda sin existencias.

        Lanza ValueError si la cantidad es negativa o el lote inicial es
        inválido.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.tiempo_produccion = tiempo_produccion
        self.fecha_produccion = fecha_produccion
        self.precio = precio
        self.pasillo = pasillo
        self.estante = estante
        self.lotes = ListaLotes()

        if cantidad > 0:
            self.lotes.insertar(
                Lote(f"{id_producto}-1", cantidad, fecha_produccion, fecha_vencimiento)
            )

    @property
    def cantidad(self) -> int:
        """
        Unidades disponibles sumando todos los lotes.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.lotes.stock_total()

    @property
    def fecha_vencimiento(self) -> str:
        """
        Vencimiento del lote más próximo a vencer. Sin existencias devuelve
        SIN_VENCIMIENTO, para que esos productos ordenen al final.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        primero = self.lotes.primero()

        if primero is None:
            return SIN_VENCIMIENTO

        return primero.fecha_vencimiento

    def __str__(self) -> str:
        """
        Devuelve una representación legible del producto.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        primero = self.lotes.primero()
        vence = "sin existencias" if primero is None else primero.fecha_vencimiento

        return (
            f"ID: {self.id} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Cantidad: {self.cantidad} | "
            f"Vence: {vence} | "
            f"Precio: ${self.precio}"
        )
