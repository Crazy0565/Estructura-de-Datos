import random
import sys

sys.setrecursionlimit(5000)

# Preparación de datos

random.seed(11)

N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]

ordenada = sorted(aleatoria)

# QuickSort

def rapida(a, modo="medio"):

    if len(a) <= 1:

        return list(a), 0

 # Selección del pivote

    if modo == "medio":

        indice_pivote = len(a) // 2

    elif modo == "ultimo":

        indice_pivote = len(a) - 1

    else:

        raise ValueError(
            "El modo debe ser 'medio' o 'ultimo'"
        )

    pivote = a[indice_pivote]

    menores = []

    mayores = []

    comparaciones = 0

  # Partición

    for i in range(len(a)):

        if i == indice_pivote:

            continue

        comparaciones += 1

        if a[i] < pivote:

            menores.append(a[i])

        else:

            mayores.append(a[i])

  # Recursión

    izquierda, c1 = rapida(
        menores,
        modo
    )

    derecha, c2 = rapida(
        mayores,
        modo
    )

    resultado = (
        izquierda
        + [pivote]
        + derecha
    )

    total = (
        comparaciones
        + c1
        + c2
    )

    return resultado, total

# Caso 1
# Pivote medio + lista aleatoria

resultado_1, comp_1 = rapida(
    aleatoria,
    "medio"
)

assert resultado_1 == ordenada

# Caso 2
# Pivote último + lista aleatoria

resultado_2, comp_2 = rapida(
    aleatoria,
    "ultimo"
)

assert resultado_2 == ordenada

# Caso 3
# Pivote medio + lista ordenada

resultado_3, comp_3 = rapida(
    ordenada,
    "medio"
)

assert resultado_3 == ordenada

# Caso 4
# Pivote último + lista ordenada

resultado_4, comp_4 = rapida(
    ordenada,
    "ultimo"
)

assert resultado_4 == ordenada

# Resultados

print("=" * 70)
print("RETO 3 - RÁPIDA / QUICKSORT")
print("=" * 70)

print(
    f"\nPivote medio  | Aleatoria: "
    f"{comp_1:,}"
)

print(
    f"Pivote último | Aleatoria: "
    f"{comp_2:,}"
)

print(
    f"Pivote medio  | Ordenada: "
    f"{comp_3:,}"
)

print(
    f"Pivote último | Ordenada: "
    f"{comp_4:,}"
)

print("\nReto terminado correctamente.")
