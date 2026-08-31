import random

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]
ordenada = sorted(aleatoria)
al_reves = ordenada[::-1]

# BURBUJA

def burbuja(a):

    a = list(a)

    comparaciones = 0

    n = len(a)

    for i in range(n - 1):

        hubo_cambio = False

        for j in range(n - 1 - i):

            comparaciones += 1

            if a[j] > a[j + 1]:

                a[j], a[j + 1] = a[j + 1], a[j]

                hubo_cambio = True

        if not hubo_cambio:
            break

    return a, comparaciones

# SELECCIÓN

def seleccion(a):

    a = list(a)

    comparaciones = 0

    n = len(a)

    for i in range(n - 1):

        menor = i

        for j in range(i + 1, n):

            comparaciones += 1

            if a[j] < a[menor]:
                menor = j

        if menor != i:

            a[i], a[menor] = a[menor], a[i]

    return a, comparaciones

# INSERCIÓN

def insercion(a):

    a = list(a)

    comparaciones = 0

    for i in range(1, len(a)):

        actual = a[i]

        j = i - 1

        while j >= 0:

            comparaciones += 1

            if a[j] > actual:

                a[j + 1] = a[j]

                j -= 1

            else:

                break

        a[j + 1] = actual

    return a, comparaciones

# Construcción de la tabla

escenarios = [
    ("Aleatoria", aleatoria),
    ("Ordenada", ordenada),
    ("Al revés", al_reves)
]

algoritmos = [
    ("Burbuja", burbuja),
    ("Selección", seleccion),
    ("Inserción", insercion)
]


print("=" * 70)
print("RETO 5 - TABLA DE NUEVE CASILLAS")
print("=" * 70)

print(
    f"\n{'Algoritmo':<15}"
    f"{'Aleatoria':>15}"
    f"{'Ordenada':>15}"
    f"{'Al revés':>15}"
)

print("-" * 60)


for nombre, funcion in algoritmos:

    resultados = []

    for _, datos in escenarios:

        resultado, comparaciones = funcion(datos)

        assert resultado == ordenada

        resultados.append(comparaciones)

    print(
        f"{nombre:<15}"
        f"{resultados[0]:>15,}"
        f"{resultados[1]:>15,}"
        f"{resultados[2]:>15,}"
    )


print("\nReto terminado correctamente.")


# ============================================================
# TABLA DE NUEVE CASILLAS
# ============================================================
#
#                    ALEATORIA    ORDENADA    AL REVÉS
#
# Burbuja             499149         999       499500
# Selección            499500      499500       499500
# Inserción            241994         999       499500
