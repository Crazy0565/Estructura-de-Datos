def bubble_sort(datos, clave):
    """
    Ordena los elementos utilizando Bubble Sort.

    Mejor caso: O(n)
    Caso promedio: O(n²)
    Peor caso: O(n²)
    """
    n = len(datos)

    for i in range(n):
        intercambio = False

        for j in range(0, n - i - 1):
            if clave(datos[j]) > clave(datos[j + 1]):
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                intercambio = True

        if not intercambio:
            break

    return datos


def quick_sort(datos, clave):
    """
    Ordena los elementos utilizando QuickSort.

    Caso promedio: O(n log n)
    Peor caso: O(n²)
    """
    if len(datos) <= 1:
        return datos

    pivote = datos[len(datos) // 2]
    valor_pivote = clave(pivote)

    menores = [
        elemento
        for elemento in datos
        if clave(elemento) < valor_pivote
    ]

    iguales = [
        elemento
        for elemento in datos
        if clave(elemento) == valor_pivote
    ]

    mayores = [
        elemento
        for elemento in datos
        if clave(elemento) > valor_pivote
    ]

    return (
        quick_sort(menores, clave)
        + iguales
        + quick_sort(mayores, clave)
    )