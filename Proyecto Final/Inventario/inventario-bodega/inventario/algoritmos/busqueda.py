"""Búsqueda lineal y búsqueda binaria propias."""

from collections.abc import Callable, Iterable
from typing import Any


def busqueda_lineal(
    datos: Iterable[Any], valor: Any, clave: Callable[[Any], Any]
) -> Any | None:
    """
    Busca un elemento recorriendo los datos secuencialmente.

    Complejidad:
        Tiempo: O(n).
        Espacio: O(1).
    """
    for elemento in datos:
        if clave(elemento) == valor:
            return elemento

    return None


def busqueda_binaria(
    datos: list[Any], valor: Any, clave: Callable[[Any], Any]
) -> Any | None:
    """
    Busca un elemento mediante búsqueda binaria.

    Los datos deben estar ordenados según la misma clave.

    Complejidad:
        Tiempo: O(log n).
        Espacio: O(1).
    """
    izquierda = 0
    derecha = len(datos) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        valor_medio = clave(datos[medio])

        if valor_medio == valor:
            return datos[medio]

        if valor_medio < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None
