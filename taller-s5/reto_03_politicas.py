def simular_politica(n, politica):

    capacidad = 1
    tamano = 0
    copias = 0
    redim = 0

    for i in range(n):

        if tamano == capacidad:

            copias += tamano
            capacidad = politica(capacidad)
            redim += 1

        tamano += 1

    return copias, redim, capacidad

def politica_uno(capacidad):
    return capacidad + 1

def politica_diez(capacidad):
    return capacidad + 10

def politica_doble(capacidad):
    return capacidad * 2

# EJECUCIÓN DEL RETO 3

print("\n" + "=" * 65)
print("RETO 3 - LAS TRES POLÍTICAS")
print("=" * 65)

politicas = [
    ("capacidad + 1", politica_uno),
    ("capacidad + 10", politica_diez),
    ("capacidad × 2", politica_doble)
]

print(
    f"\n{'Política':<20}"
    f"{'Copias':>18}"
    f"{'Redim.':>12}"
    f"{'Copias/inserción':>20}"
)

print("-" * 70)

resultados_politicas = {}

for nombre, funcion in politicas:

    copias, redim, capacidad = simular_politica(100000, funcion)

    copias_por_insercion = copias / 100000

    resultados_politicas[nombre] = (
        copias,
        redim,
        capacidad,
        copias_por_insercion
    )

    print(
        f"{nombre:<20}"
        f"{copias:>18,}"
        f"{redim:>12,}"
        f"{copias_por_insercion:>20,.5f}"
    )

assert resultados_politicas["capacidad + 1"][0] == 4999950000
assert resultados_politicas["capacidad + 10"][0] == 499960000
assert resultados_politicas["capacidad × 2"][0] == 131071

print("\nReto terminado correctamente.")
