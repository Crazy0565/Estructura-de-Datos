import random

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]
ordenada = sorted(aleatoria)
al_reves = ordenada[::-1]

# Bubble Sort

def burbuja(a):

    a = list(a)

    comparaciones = 0
    intercambios = 0

    n = len(a)

    for i in range(n - 1):

        for j in range(n - 1 - i):

            comparaciones += 1

            if a[j] > a[j + 1]:

                a[j], a[j + 1] = a[j + 1], a[j]

                intercambios += 1

    return a, comparaciones, intercambios
  
# Pruebas

print("=" * 60)
print("RETO 1 - BURBUJA CON CONTADOR")
print("=" * 60)

for nombre, datos in [
    ("Aleatoria", aleatoria),
    ("Ordenada", ordenada),
    ("Al revés", al_reves)
]:

    resultado, comparaciones, intercambios = burbuja(datos)

    assert resultado == ordenada

    print(f"\nEscenario: {nombre}")
    print(f"Comparaciones: {comparaciones:,}")
    print(f"Intercambios:  {intercambios:,}")


print("\nReto terminado correctamente.")
