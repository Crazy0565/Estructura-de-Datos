import random

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]
ordenada = sorted(aleatoria)
al_reves = ordenada[::-1]

# Insertion Sort

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

# Pruebas

print("=" * 60)
print("RETO 4 - INSERCIÓN")
print("=" * 60)


for nombre, datos in [
    ("Aleatoria", aleatoria),
    ("Ordenada", ordenada),
    ("Al revés", al_reves)
]:

    resultado, comparaciones, movimientos = insercion(datos)

    assert resultado == ordenada

    print(f"\nEscenario: {nombre}")
    print(f"Comparaciones: {comparaciones:,}")
    print(f"Movimientos:   {movimientos:,}")

# Comprobación del caso aleatorio

assert insercion(aleatoria)[1] == 241994

print("\nReto terminado correctamente.")
