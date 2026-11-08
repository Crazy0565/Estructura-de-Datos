"""Lote: tanda de unidades de un producto que comparten fecha de vencimiento."""

from datetime import date


def validar_fecha(fecha: str) -> None:
    """
    Verifica que una fecha tenga el formato estricto YYYY-MM-DD.

    El formato fijo permite comparar fechas como texto: el orden
    alfabético coincide con el orden cronológico.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    if (
        not isinstance(fecha, str)
        or len(fecha) != 10
        or fecha[4] != "-"
        or fecha[7] != "-"
    ):
        raise ValueError(f"Fecha inválida (use YYYY-MM-DD): {fecha!r}")

    try:
        date.fromisoformat(fecha)
    except ValueError:
        raise ValueError(f"Fecha inexistente: {fecha!r}") from None


class Lote:
    """
    Tanda de unidades de un producto que comparten fecha de vencimiento.

    Complejidad:
        Tiempo de creación: O(1).
        Espacio: O(1).
    """

    def __init__(
        self, codigo: str, cantidad: int, fecha_produccion: str, fecha_vencimiento: str
    ) -> None:
        """
        Crea un lote validando sus datos.

        Lanza ValueError si el código está vacío, la cantidad no es positiva,
        una fecha es inválida o el vencimiento es anterior a la producción.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código del lote no puede estar vacío.")

        if cantidad <= 0:
            raise ValueError("La cantidad del lote debe ser mayor que cero.")

        validar_fecha(fecha_produccion)
        validar_fecha(fecha_vencimiento)

        if fecha_vencimiento < fecha_produccion:
            raise ValueError("El vencimiento no puede ser anterior a la producción.")

        self.codigo = codigo.strip()
        self.cantidad = cantidad
        self.fecha_produccion = fecha_produccion
        self.fecha_vencimiento = fecha_vencimiento

    def __str__(self) -> str:
        """
        Devuelve una representación legible del lote.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return (
            f"Lote {self.codigo} | "
            f"Cantidad: {self.cantidad} | "
            f"Producido: {self.fecha_produccion} | "
            f"Vence: {self.fecha_vencimiento}"
        )
