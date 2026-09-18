import time

from producto import Producto
from arreglo import ArregloDinamico
from matriz import MatrizBodega
from ordenamiento import bubble_sort, quick_sort
from busqueda import busqueda_lineal, busqueda_binaria


def crear_producto(i):
    """Crea un producto para las pruebas."""
    return Producto(
        i,
        f"Producto {i}",
        "General",
        100,
        (i % 10) + 1,
        "2026-09-01",
        "2026-12-01",
        4500.0,
        i % 100,
        (i // 100) % 100
    )


def probar_arreglo(cantidad):
    """Mide inserción y acceso en el arreglo dinámico."""
    arreglo = ArregloDinamico()

    inicio = time.perf_counter()

    for i in range(cantidad):
        arreglo.agregar(crear_producto(i))

    tiempo_insercion = time.perf_counter() - inicio

    inicio = time.perf_counter()
    producto = arreglo[cantidad // 2]
    tiempo_acceso = time.perf_counter() - inicio

    return tiempo_insercion, tiempo_acceso, arreglo.capacidad, producto


def probar_busquedas(productos):
    """Mide búsqueda lineal y binaria."""
    objetivo = productos[-1].id

    inicio = time.perf_counter()
    busqueda_lineal(productos, objetivo, lambda p: p.id)
    tiempo_lineal = time.perf_counter() - inicio

    inicio = time.perf_counter()
    busqueda_binaria(productos, objetivo, lambda p: p.id)
    tiempo_binaria = time.perf_counter() - inicio

    return tiempo_lineal, tiempo_binaria


def probar_matriz():
    """Mide el crecimiento de la matriz."""
    print("\n===== ESCALABILIDAD DE LA MATRIZ =====")

    for tamaño in range(10, 101, 10):
        inicio = time.perf_counter()

        matriz = MatrizBodega(tamaño)

        tiempo = time.perf_counter() - inicio

        ubicaciones = tamaño * tamaño

        print(
            f"{tamaño:>3}x{tamaño:<3} | "
            f"Ubicaciones: {ubicaciones:>5} | "
            f"Creación: {tiempo:.8f} s"
        )


def probar_ordenamientos(productos):
    """Mide Bubble Sort y QuickSort."""
    inicio = time.perf_counter()

    copia_bubble = productos.copy()
    bubble_sort(copia_bubble, lambda p: p.tiempo_produccion)

    tiempo_bubble = time.perf_counter() - inicio

    inicio = time.perf_counter()

    copia_quick = productos.copy()
    quick_sort(copia_quick, lambda p: p.fecha_vencimiento)

    tiempo_quick = time.perf_counter() - inicio

    return tiempo_bubble, tiempo_quick


if __name__ == "__main__":

    cantidades = [1000, 5000, 10000, 50000, 100000]

    print("===== PRUEBAS DE COMPLEJIDAD =====")

    for cantidad in cantidades:

        print(f"\n--- {cantidad:,} PRODUCTOS ---")

        inicio = time.perf_counter()
        productos = [crear_producto(i) for i in range(cantidad)]
        tiempo_generacion = time.perf_counter() - inicio

        insercion, acceso, capacidad, producto = probar_arreglo(cantidad)

        lineal, binaria = probar_busquedas(productos)

        print(f"Generación:       {tiempo_generacion:.6f} s")
        print(f"Inserción:        {insercion:.6f} s")
        print(f"Acceso:           {acceso:.9f} s")
        print(f"Búsqueda lineal:  {lineal:.6f} s")
        print(f"Búsqueda binaria: {binaria:.9f} s")
        print(f"Capacidad final:  {capacidad}")

        # Bubble Sort puede tardar demasiado con cantidades grandes.
        if cantidad <= 10000:
            bubble, quick = probar_ordenamientos(productos)

            print(f"Bubble Sort:      {bubble:.6f} s")
            print(f"QuickSort:        {quick:.6f} s")
        else:
            print("Bubble Sort:      omitido (> 10.000)")
            
            inicio = time.perf_counter()
            copia = productos.copy()
            quick_sort(copia, lambda p: p.fecha_vencimiento)
            quick = time.perf_counter() - inicio

            print(f"QuickSort:        {quick:.6f} s")

    probar_matriz()