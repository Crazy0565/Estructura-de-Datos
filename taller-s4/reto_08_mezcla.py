import random

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]

ordenada = sorted(aleatoria)

# Fusión

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

    resultado.extend(izquierda[i:])

    resultado.extend(derecha[j:])

    return resultado, comparaciones

# Merge Sort

def mezcla(a):

    if len(a) <= 1:

        return list(a), 0

    mitad = len(a) // 2

    izquierda, comparaciones_izquierda = mezcla(
        a[:mitad]
    )

    derecha, comparaciones_derecha = mezcla(
        a[mitad:]
    )

    resultado, comparaciones_fusion = fusionar(
        izquierda,
        derecha
    )

    total = (
        comparaciones_izquierda
        + comparaciones_derecha
        + comparaciones_fusion
    )

    return resultado, total

# Prueba

print("=" * 60)
print("RETO 2 - MEZCLA")
print("=" * 60)

resultado, comparaciones = mezcla(aleatoria)

assert resultado == ordenada
assert comparaciones == 8720

print("Comparaciones:", comparaciones)
print("\nReto terminado correctamente.")
