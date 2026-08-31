import sys

def capacidades_python():

    base = sys.getsizeof([])
    lista = []
    previa = None
    secuencia = []

    for i in range(200):

        capacidad = (sys.getsizeof(lista) - base) // 8

        if capacidad != previa:

            secuencia.append((i, capacidad))
            previa = capacidad

        lista.append(i)

    return secuencia

# EJECUCIÓN DEL RETO 5

print("\n" + "=" * 65)
print("RETO 5 - CAPACIDAD REAL DE PYTHON")
print("=" * 65)

secuencia = capacidades_python()

for posicion, capacidad in secuencia:
    print(posicion, capacidad)

print("\nPython crece de forma proporcional, no duplicando exactamente.")

print("\nReto terminado correctamente.")
