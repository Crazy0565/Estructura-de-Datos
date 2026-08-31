import time


def recorrer(datos, paso):

    t0 = time.perf_counter()
    total = 0

    for i in range(0, len(datos), paso):
        total += datos[i]

    dt = time.perf_counter() - t0

    return dt / (len(datos) / paso) * 1e9, total

# EJECUCIÓN DEL RETO 9

print("\n" + "=" * 65)
print("RETO 9 - LOCALIDAD")
print("=" * 65)

N = 4_000_000
datos = list(range(N))

for paso in (1, 16, 1024):

    tiempo, total = recorrer(datos, paso)

    print(
        f"Paso {paso:<4} | "
        f"{tiempo:.2f} ns por elemento"
    )
