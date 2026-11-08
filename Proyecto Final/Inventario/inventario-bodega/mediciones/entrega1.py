"""Pruebas de complejidad de la Entrega 1 (reproducen docs/entrega1/resultados.md).

Mide inserción y acceso del arreglo dinámico, búsqueda lineal y binaria,
Bubble Sort y QuickSort, escalabilidad de la matriz, comparación con sorted()
y el benchmark de ArregloDinamico frente a list.

Uso: python -m mediciones.entrega1
"""

import random
import time
from collections.abc import Callable
from typing import Any

from inventario.algoritmos.busqueda import busqueda_binaria, busqueda_lineal
from inventario.algoritmos.ordenamiento import bubble_sort, quick_sort
from inventario.dominio.producto import Producto
from inventario.estructuras.arreglo import ArregloDinamico
from inventario.estructuras.matriz import MatrizBodega

CANTIDADES = [1000, 5000, 10000, 50000, 100000]
LIMITE_BUBBLE = 10000


def crear_producto(i: int) -> Producto:
    """
    Crea un producto sintético para las pruebas.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
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
        (i // 100) % 100,
    )


def probar_arreglo(cantidad: int) -> tuple[float, float, int, Any]:
    """
    Mide inserción y acceso en el arreglo dinámico.

    Complejidad:
        Tiempo: O(n) por las inserciones (O(1) amortizado cada una).
        Espacio: O(n).
    """
    arreglo = ArregloDinamico()

    inicio = time.perf_counter()

    for i in range(cantidad):
        arreglo.agregar(crear_producto(i))

    tiempo_insercion = time.perf_counter() - inicio

    inicio = time.perf_counter()
    producto = arreglo[cantidad // 2]
    tiempo_acceso = time.perf_counter() - inicio

    return tiempo_insercion, tiempo_acceso, arreglo.capacidad, producto


def probar_busquedas(productos: list[Producto]) -> tuple[float, float]:
    """
    Mide búsqueda lineal y binaria del último producto.

    Complejidad:
        Tiempo: O(n) la lineal y O(log n) la binaria.
        Espacio: O(1).
    """
    objetivo = productos[-1].id

    inicio = time.perf_counter()
    busqueda_lineal(productos, objetivo, lambda p: p.id)
    tiempo_lineal = time.perf_counter() - inicio

    inicio = time.perf_counter()
    busqueda_binaria(productos, objetivo, lambda p: p.id)
    tiempo_binaria = time.perf_counter() - inicio

    return tiempo_lineal, tiempo_binaria


def probar_matriz() -> None:
    """
    Mide el tiempo de creación de matrices de 10x10 hasta 100x100.

    Complejidad:
        Tiempo: O(n²) por matriz creada.
        Espacio: O(n²).
    """
    print("\n===== ESCALABILIDAD DE LA MATRIZ =====")

    for tamaño in range(10, 101, 10):
        inicio = time.perf_counter()
        MatrizBodega(tamaño)
        tiempo = time.perf_counter() - inicio

        print(
            f"{tamaño:>3}x{tamaño:<3} | "
            f"Ubicaciones: {tamaño * tamaño:>5} | "
            f"Creación: {tiempo:.8f} s"
        )


def probar_ordenamientos(productos: list[Producto]) -> tuple[float, float]:
    """
    Mide Bubble Sort y QuickSort sobre copias de la lista.

    Complejidad:
        Tiempo: O(n²) Bubble Sort y O(n log n) QuickSort en promedio.
        Espacio: O(n) por las copias.
    """
    inicio = time.perf_counter()
    bubble_sort(productos.copy(), lambda p: p.tiempo_produccion)
    tiempo_bubble = time.perf_counter() - inicio

    inicio = time.perf_counter()
    quick_sort(productos.copy(), lambda p: p.fecha_vencimiento)
    tiempo_quick = time.perf_counter() - inicio

    return tiempo_bubble, tiempo_quick


def probar_contra_sorted() -> bool:
    """
    Compara QuickSort con sorted() usando 1000 entradas aleatorias y verifica
    que ambos produzcan el mismo orden.

    Complejidad:
        Tiempo: O(n log n) en promedio.
        Espacio: O(n).
    """
    print("\n===== COMPARACIÓN CON sorted() =====")

    productos = [crear_producto(i) for i in range(1000)]
    random.shuffle(productos)

    def clave(p: Producto) -> int:
        return p.id

    inicio = time.perf_counter()
    resultado_quick = quick_sort(productos.copy(), clave)
    tiempo_quick = time.perf_counter() - inicio

    inicio = time.perf_counter()
    resultado_sorted = sorted(productos, key=clave)
    tiempo_sorted = time.perf_counter() - inicio

    orden_correcto = [p.id for p in resultado_quick] == [p.id for p in resultado_sorted]

    print("Entradas evaluadas: 1000")
    print(f"QuickSort:           {tiempo_quick:.8f} s")
    print(f"sorted():            {tiempo_sorted:.8f} s")
    print(f"Orden correcto:      {'SI' if orden_correcto else 'NO'}")

    return orden_correcto


def cronometrar(funcion: Callable[[], Any]) -> float:
    """
    Segundos que tarda en ejecutarse la función una vez.

    Complejidad:
        Tiempo: la de la función medida.
        Espacio: O(1).
    """
    inicio = time.perf_counter()
    funcion()
    return time.perf_counter() - inicio


def pruebas_de_complejidad() -> None:
    """
    Imprime, para cada cantidad, generación, inserción, acceso, búsquedas,
    capacidad final y ordenamientos (Bubble Sort se omite sobre 10.000).

    Complejidad:
        Tiempo: dominado por Bubble Sort, O(n²), hasta 10.000 elementos.
        Espacio: O(n).
    """
    print("===== PRUEBAS DE COMPLEJIDAD =====")

    for cantidad in CANTIDADES:
        print(f"\n--- {cantidad:,} PRODUCTOS ---")

        inicio = time.perf_counter()
        productos = [crear_producto(i) for i in range(cantidad)]
        tiempo_generacion = time.perf_counter() - inicio

        insercion, acceso, capacidad, _ = probar_arreglo(cantidad)
        lineal, binaria = probar_busquedas(productos)

        print(f"Generación:       {tiempo_generacion:.6f} s")
        print(f"Inserción:        {insercion:.6f} s")
        print(f"Acceso:           {acceso:.9f} s")
        print(f"Búsqueda lineal:  {lineal:.6f} s")
        print(f"Búsqueda binaria: {binaria:.9f} s")
        print(f"Capacidad final:  {capacidad}")

        if cantidad <= LIMITE_BUBBLE:
            bubble, quick = probar_ordenamientos(productos)
            print(f"Bubble Sort:      {bubble:.6f} s")
        else:
            print("Bubble Sort:      omitido (> 10.000)")
            quick = cronometrar(
                lambda productos=productos: quick_sort(
                    productos.copy(), lambda p: p.fecha_vencimiento
                )
            )

        print(f"QuickSort:        {quick:.6f} s")


def benchmark_lista_vs_arreglo() -> None:
    """
    Compara inserción y acceso de ArregloDinamico contra list de Python.

    Complejidad:
        Tiempo: O(n) por cantidad probada.
        Espacio: O(n).
    """
    print("\n===== BENCHMARK: ArregloDinamico VS list =====")

    for cantidad in CANTIDADES:
        productos = [crear_producto(i) for i in range(cantidad)]

        inicio = time.perf_counter()
        arreglo = ArregloDinamico()
        for producto in productos:
            arreglo.agregar(producto)
        tiempo_arreglo = time.perf_counter() - inicio

        inicio = time.perf_counter()
        lista: list[Producto] = []
        for producto in productos:
            lista.append(producto)
        tiempo_lista = time.perf_counter() - inicio

        indice = cantidad // 2

        inicio = time.perf_counter()
        arreglo[indice]
        acceso_arreglo = time.perf_counter() - inicio

        inicio = time.perf_counter()
        lista[indice]
        acceso_lista = time.perf_counter() - inicio

        print(f"\n--- {cantidad:,} elementos ---")
        print(f"Inserción ArregloDinamico: {tiempo_arreglo:.8f} s")
        print(f"Inserción list:            {tiempo_lista:.8f} s")
        print(f"Acceso ArregloDinamico:    {acceso_arreglo:.9f} s")
        print(f"Acceso list:               {acceso_lista:.9f} s")


def main() -> None:
    """
    Corre todas las pruebas de la Entrega 1.

    Complejidad:
        Tiempo: la suma de las pruebas anteriores.
        Espacio: O(n).
    """
    pruebas_de_complejidad()
    probar_matriz()
    probar_contra_sorted()
    benchmark_lista_vs_arreglo()


if __name__ == "__main__":
    main()
