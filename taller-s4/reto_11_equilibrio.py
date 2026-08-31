import math

# Punto de equilibrio

def equilibrio(n):

    # Costo aproximado de ordenar
  
    costo_ordenar = n * math.log2(n)

    k = 1

    while True:

# Costo de hacer k búsquedas lineales
      
        sin_ordenar = k * n / 2

# Costo de ordenar + k búsquedas binarias
        con_orden = (
            costo_ordenar
            + k * math.log2(n)
        )

# Si ordenar ya resulta más barato, encontramos el punto de equilibrio.

        if con_orden < sin_ordenar:

           return k

        k += 1

# PRUEBAS

print("=" * 60)
print("RETO 5 - PUNTO DE EQUILIBRIO")
print("=" * 60)

resultado_1000 = equilibrio(1000)

resultado_1000000 = equilibrio(1000000)

print(
    "\nequilibrio(1000):",
    resultado_1000
)

print(
    "equilibrio(1000000):",
    resultado_1000000
)

# Comprobación solicitada por la guía.

assert resultado_1000000 == 40

print("\nReto terminado correctamente.")
