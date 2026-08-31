import sys
import array
import time

# EJECUCIÓN DEL RETO 10

print("\n" + "=" * 65)
print("RETO 10 - MEMORIA")
print("=" * 65)

n = 1_000_000

lista = list(range(n))
arr = array.array("q", range(n))

# La lista guarda direcciones: hay que sumar el peso
# de cada entero por separado.
peso_lista = (
    sys.getsizeof(lista)
    + sum(sys.getsizeof(i) for i in lista)
)

memoria_lista = peso_lista / 1024 / 1024
memoria_array = sys.getsizeof(arr) / 1024 / 1024

print("lista ", round(memoria_lista, 1), "MB")
print("array ", round(memoria_array, 1), "MB")

tiempo_lista = None
tiempo_array = None

t0 = time.perf_counter()
sum(lista)
tiempo_lista = time.perf_counter() - t0

t0 = time.perf_counter()
sum(arr)
tiempo_array = time.perf_counter() - t0

print("sum(lista):", tiempo_lista)
print("sum(array):", tiempo_array)
