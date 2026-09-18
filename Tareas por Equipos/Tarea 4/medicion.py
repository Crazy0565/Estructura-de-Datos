# -*- coding: utf-8 -*-

import platform
import random
import sys
import timeit

from matriz import Matriz


random.seed(11)


def crear_matriz(lado: int) -> Matriz:
    matriz = Matriz(lado, lado)

    for i in range(lado):
        for j in range(lado):
            matriz.asignar(i, j, random.randint(0, 9))

    return matriz


def medir_suma(matriz: Matriz) -> float:
    tiempos = timeit.repeat(
        stmt=matriz.suma,
        repeat=5,
        number=1,
    )

    return min(tiempos)


def main() -> None:
    resultados = []
    tiempo_anterior = None

    for lado in (250, 500, 1000):
        matriz = crear_matriz(lado)

        tiempo = medir_suma(matriz)
        celdas = lado * lado

        if tiempo_anterior is None:
            factor = None
        else:
            factor = tiempo / tiempo_anterior

        resultados.append((lado, celdas, tiempo, factor))
        tiempo_anterior = tiempo

    print("MEDICION DE suma()")
    print("-" * 55)
    print(f"{'Lado':<10}{'Celdas':<15}{'Tiempo (s)':<15}{'Factor':<10}")
    print("-" * 55)

    for lado, celdas, tiempo, factor in resultados:
        factor_texto = "-" if factor is None else f"{factor:.2f}"
        print(f"{lado:<10}{celdas:<15}{tiempo:<15.6f}{factor_texto:<10}")

    print("-" * 55)
    print(f"Python: {sys.version.split()[0]}")
    print(f"Sistema: {platform.platform()}")


if __name__ == "__main__":
    main()
