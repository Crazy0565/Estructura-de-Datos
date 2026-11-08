"""Ordenamientos propios: burbuja y QuickSort."""

from collections.abc import Callable
from typing import Any


def bubble_sort(datos: list[Any], clave: Callable[[Any], Any]) -> list[Any]:
    """
    Ordena los elementos utilizando Bubble Sort.

    Complejidad:
        Mejor caso: O(n) tiempo.
        Caso promedio: O(n²) tiempo.
        Peor caso: O(n²) tiempo.
        Espacio: O(1).
    """
    n = len(datos)

    for i in range(n):
        intercambio = False

        for j in range(n - i - 1):
            if clave(datos[j]) > clave(datos[j + 1]):
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                intercambio = True

        if not intercambio:
            break

    return datos


def quick_sort(datos: list[Any], clave: Callable[[Any], Any]) -> list[Any]:
    """
    Ordena los elementos utilizando QuickSort.

    Complejidad:
        Caso promedio: O(n log n) tiempo.
        Peor caso: O(n²) tiempo.
        Espacio: O(n) debido a las listas auxiliares y la recursión.
    """
    if len(datos) <= 1:
        return datos

    pivote = datos[len(datos) // 2]
    valor_pivote = clave(pivote)

    menores = [elemento for elemento in datos if clave(elemento) < valor_pivote]

    iguales = [elemento for elemento in datos if clave(elemento) == valor_pivote]

    mayores = [elemento for elemento in datos if clave(elemento) > valor_pivote]

    return quick_sort(menores, clave) + iguales + quick_sort(mayores, clave)
