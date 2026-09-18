import matplotlib.pyplot as plt


cantidades = [1000, 5000, 10000, 50000, 100000]

insercion = [
    0.000681,
    0.002720,
    0.005408,
    0.029080,
    0.081061
]

acceso = [
    0.000001200,
    0.000001600,
    0.000000900,
    0.000001100,
    0.000002200
]

lineal = [
    0.000038,
    0.000188,
    0.000395,
    0.002000,
    0.003892
]

binaria = [
    0.000003600,
    0.000004100,
    0.000004200,
    0.000006100,
    0.000007800
]

quick_sort = [
    0.000164,
    0.000799,
    0.001657,
    0.007957,
    0.018977
]

bubble_sort = [
    0.050138,
    1.446117,
    5.426820,
    None,
    None
]


# -----------------------------
# Inserción
# -----------------------------

plt.figure()
plt.plot(cantidades, insercion, marker="o")
plt.xlabel("Cantidad de productos")
plt.ylabel("Tiempo (segundos)")
plt.title("Tiempo de inserción")
plt.grid(True)
plt.savefig("grafica_insercion.png")
plt.show()


# -----------------------------
# Búsquedas
# -----------------------------

plt.figure()
plt.plot(cantidades, lineal, marker="o", label="Búsqueda lineal")
plt.plot(cantidades, binaria, marker="o", label="Búsqueda binaria")
plt.xlabel("Cantidad de productos")
plt.ylabel("Tiempo (segundos)")
plt.title("Comparación de búsquedas")
plt.legend()
plt.grid(True)
plt.savefig("grafica_busquedas.png")
plt.show()


# -----------------------------
# Ordenamientos
# -----------------------------

plt.figure()

bubble_x = cantidades[:3]
bubble_y = bubble_sort[:3]

plt.plot(bubble_x, bubble_y, marker="o", label="Bubble Sort")
plt.plot(cantidades, quick_sort, marker="o", label="QuickSort")

plt.xlabel("Cantidad de productos")
plt.ylabel("Tiempo (segundos)")
plt.title("Comparación de algoritmos de ordenamiento")
plt.legend()
plt.grid(True)
plt.savefig("grafica_ordenamientos.png")
plt.show()


# -----------------------------
# Acceso
# -----------------------------

plt.figure()
plt.plot(cantidades, acceso, marker="o")
plt.xlabel("Cantidad de productos")
plt.ylabel("Tiempo (segundos)")
plt.title("Tiempo de acceso al arreglo")
plt.grid(True)
plt.savefig("grafica_acceso.png")
plt.show()