import random

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]
ordenada = sorted(aleatoria)

# BURBUJA

def burbuja(a):

    a = list(a)

    comparaciones = 0
    movimientos = 0

    for i in range(len(a) - 1):

        hubo_cambio = False

        for j in range(len(a) - 1 - i):

            comparaciones += 1

            if a[j] > a[j + 1]:

                a[j], a[j + 1] = a[j + 1], a[j]

                movimientos += 1

                hubo_cambio = True

        if not hubo_cambio:
            break

    return a, comparaciones, movimientos

# SELECCIÓN

def seleccion(a):

    a = list(a)

    comparaciones = 0
    movimientos = 0

    for i in range(len(a) - 1):

        menor = i

        for j in range(i + 1, len(a)):

            comparaciones += 1

            if a[j] < a[menor]:
                menor = j

        if menor != i:

            a[i], a[menor] = a[menor], a[i]

            movimientos += 1

    return a, comparaciones, movimientos

# INSERCIÓN

def insercion(a):

    a = list(a)

    comparaciones = 0
    movimientos = 0

    for i in range(1, len(a)):

        actual = a[i]

        j = i - 1

        while j >= 0:

            comparaciones += 1

            if a[j] > actual:

                a[j + 1] = a[j]

                movimientos += 1

                j -= 1

            else:

                break

        a[j + 1] = actual

        movimientos += 1

    return a, comparaciones, movimientos

# Comparación

print("=" * 70)
print("RETO 6 - COMPARAR NO ES LO MISMO QUE MOVER")
print("=" * 70)

algoritmos = [
    ("Burbuja", burbuja),
    ("Selección", seleccion),
    ("Inserción", insercion)
]

for nombre, funcion in algoritmos:

    resultado, comparaciones, movimientos = funcion(aleatoria)

    assert resultado == ordenada

    print(f"\n{nombre}")
    print(f"Comparaciones: {comparaciones:,}")
    print(f"Movimientos:   {movimientos:,}")

print("\nReto terminado correctamente.")
