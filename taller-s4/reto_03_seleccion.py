import random

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]
ordenada = sorted(aleatoria)
al_reves = ordenada[::-1]

# Selection Sort

def seleccion(a):

    a = list(a)

    comparaciones = 0
    intercambios = 0

    n = len(a)

    for i in range(n - 1):

        menor = i

        for j in range(i + 1, n):

            comparaciones += 1

            if a[j] < a[menor]:

                menor = j

 # El intercambio se realiza una sola vez después de buscar el menor.

        if menor != i:

            a[i], a[menor] = a[menor], a[i]

            intercambios += 1

    return a, comparaciones, intercambios

# Pruebas

print("=" * 60)
print("RETO 3 - SELECCIÓN")
print("=" * 60)


for nombre, datos in [
    ("Aleatoria", aleatoria),
    ("Ordenada", ordenada),
    ("Al revés", al_reves)
]:

    resultado, comparaciones, intercambios = seleccion(datos)

    assert resultado == ordenada

    print(f"\nEscenario: {nombre}")
    print(f"Comparaciones: {comparaciones:,}")
    print(f"Intercambios:  {intercambios:,}")

# Selection Sort realiza 499500 comparaciones en los tres escenarios.

assert seleccion(aleatoria)[1] == 499500
assert seleccion(ordenada)[1] == 499500
assert seleccion(al_reves)[1] == 499500

print("\nReto terminado correctamente.")
