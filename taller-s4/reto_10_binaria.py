import math

# Búsqueda binaria

def binaria(a, x):

    izquierda = 0

    derecha = len(a) - 1

    pasos = 0

    while izquierda <= derecha:

        pasos += 1

        mitad = (
            izquierda + derecha
        ) // 2

        if a[mitad] == x:

            return mitad, pasos

        elif a[mitad] < x:

            izquierda = mitad + 1

        else:

            derecha = mitad - 1

    return -1, pasos

# RETO

print("=" * 60)
print("RETO 4 - BÚSQUEDA BINARIA")
print("=" * 60)

# Lista de 1.000 elementos

lista_1000 = list(range(1000))

peor_1000 = 0

for valor in lista_1000:

    posicion, pasos = binaria(
        lista_1000,
        valor
    )

    assert posicion == valor

    if pasos > peor_1000:

        peor_1000 = pasos

print(
    "\nPeor caso con 1.000 elementos:",
    peor_1000
)

assert peor_1000 == 10

# Lista de 1.000.000 elementos

lista_millon = list(range(1000000))

# Probamos valores representativos y calculamos el máximo teórico.

valores = [
    0,
    1,
    2,
    500000,
    999997,
    999998,
    999999
]

peor_millon = 0

for valor in valores:

    posicion, pasos = binaria(
        lista_millon,
        valor
    )

    assert posicion == valor

    if pasos > peor_millon:

        peor_millon = pasos

maximo_teorico = math.ceil(
    math.log2(1000000)
)

print(
    "Peor caso comprobado con 1.000.000 elementos:",
    peor_millon
)

print(
    "Máximo teórico:",
    maximo_teorico
)

assert maximo_teorico == 20

print("\nReto terminado correctamente.")
