def fusionar(izquierda, derecha):

    resultado = []

    i = 0
    j = 0

    comparaciones = 0

    while i < len(izquierda) and j < len(derecha):

        comparaciones += 1

        if izquierda[i] <= derecha[j]:

            resultado.append(izquierda[i])

            i += 1

        else:

            resultado.append(derecha[j])

            j += 1

# Agregar los elementos restantes.

    resultado.extend(izquierda[i:])

    resultado.extend(derecha[j:])

    return resultado, comparaciones

# Prueba solicitada

print("=" * 60)
print("RETO 1 - FUSIONAR")
print("=" * 60)

resultado, comparaciones = fusionar(
    [1, 4, 7],
    [2, 3, 9]
)

print("Resultado:", resultado)

print("Comparaciones:", comparaciones)

assert resultado == [1, 2, 3, 4, 7, 9]
assert comparaciones == 5

print("\nReto terminado correctamente.")
