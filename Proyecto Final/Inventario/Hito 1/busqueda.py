def busqueda_lineal(datos, valor, clave):
    """
    Busca un elemento recorriendo el arreglo secuencialmente.

    Complejidad: O(n).
    """
    for elemento in datos:
        if clave(elemento) == valor:
            return elemento

    return None


def busqueda_binaria(datos, valor, clave):
    """
    Busca un elemento mediante búsqueda binaria.

    Los datos deben estar ordenados según la misma clave.

    Complejidad: O(log n).
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