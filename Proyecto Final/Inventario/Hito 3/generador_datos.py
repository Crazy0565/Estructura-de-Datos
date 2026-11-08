"""
Generador reproducible de datos sintéticos a escala para el sistema de bodega.

Produce tres CSV compatibles con los cargadores del sistema:
    productos.csv  -> SistemaInventario.cargar_csv
    lotes.csv      -> SistemaInventario.cargar_lotes_csv   (entradas de mercancía)
    pedidos.csv    -> SistemaInventario.cargar_pedidos_csv (salidas)

Con los valores por defecto genera 10.000 referencias y 50.000 movimientos
(20.000 entradas de lotes + 30.000 pedidos). La misma semilla produce siempre
los mismos archivos, de modo que cualquier medición se puede repetir.

Este módulo es una herramienta de apoyo, no parte del núcleo: usa listas y
`random` de la biblioteca estándar solo para fabricar datos.

Uso: python generador_datos.py [--productos N] [--lotes N] [--pedidos N]
                               [--semilla N] [--salida CARPETA] [--desordenar]
"""

import argparse
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

CATEGORIAS = (
    "Alimentos",
    "Bebidas",
    "Lacteos",
    "Enlatados",
    "Dulces",
    "Aseo",
    "Granos",
    "Carnes frias",
)

COLUMNAS_PRODUCTOS = (
    "id",
    "nombre",
    "categoria",
    "cantidad",
    "tiempo_produccion",
    "fecha_produccion",
    "fecha_vencimiento",
    "precio",
    "pasillo",
    "estante",
)
COLUMNAS_LOTES = (
    "id_producto",
    "codigo_lote",
    "cantidad",
    "fecha_produccion",
    "fecha_vencimiento",
)
COLUMNAS_PEDIDOS = ("id_producto", "cantidad", "urgente")

INICIO = date(2026, 1, 1)
DIAS_DE_PRODUCCION = 300
PROPORCION_URGENTES = 0.10


def lado_de_la_bodega(productos: int) -> int:
    """
    Lado de la cuadrícula pasillo × estante necesaria para ubicar todos los
    productos sin repetir ubicación (la bodega es una matriz cuadrada).

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return math.ceil(math.sqrt(productos))


def _fecha(base: date, dias: int) -> str:
    """
    Devuelve la fecha ISO que queda `dias` días después de `base`.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return (base + timedelta(days=dias)).isoformat()


def generar(
    productos: int = 10_000,
    lotes: int = 20_000,
    pedidos: int = 30_000,
    semilla: int = 2026,
    desordenar: bool = False,
) -> tuple[list[list], list[list], list[list]]:
    """
    Fabrica las filas de los tres archivos. Lanza ValueError si `productos`
    no es positivo o si alguna cantidad es negativa.

    Los lotes y pedidos se reparten al azar entre los productos. Con
    `desordenar` las filas de productos salen en orden aleatorio (los ids
    siguen siendo 1..n), lo que obliga al sistema a usar búsqueda lineal.

    Complejidad:
        Tiempo: O(productos + lotes + pedidos).
        Espacio: O(productos + lotes + pedidos).
    """
    if productos <= 0:
        raise ValueError("Debe haber al menos un producto.")

    if lotes < 0 or pedidos < 0:
        raise ValueError("Las cantidades de lotes y pedidos no pueden ser negativas.")

    azar = random.Random(semilla)
    lado = lado_de_la_bodega(productos)
    filas_productos: list[list] = []

    for numero in range(productos):
        produccion = azar.randrange(DIAS_DE_PRODUCCION)
        vida_util = azar.randint(30, 720)
        filas_productos.append(
            [
                numero + 1,
                f"Producto {numero + 1:05d}",
                azar.choice(CATEGORIAS),
                azar.randint(0, 500),
                azar.randint(1, 10),
                _fecha(INICIO, produccion),
                _fecha(INICIO, produccion + vida_util),
                azar.randint(500, 50_000),
                numero // lado,
                numero % lado,
            ]
        )

    por_producto = [0] * (productos + 1)
    filas_lotes: list[list] = []

    for _ in range(lotes):
        id_producto = azar.randint(1, productos)
        por_producto[id_producto] += 1
        produccion = azar.randrange(DIAS_DE_PRODUCCION, DIAS_DE_PRODUCCION + 120)
        vida_util = azar.randint(30, 720)
        filas_lotes.append(
            [
                id_producto,
                f"{id_producto}-E{por_producto[id_producto]}",
                azar.randint(1, 300),
                _fecha(INICIO, produccion),
                _fecha(INICIO, produccion + vida_util),
            ]
        )

    filas_pedidos = [
        [
            azar.randint(1, productos),
            azar.randint(1, 30),
            1 if azar.random() < PROPORCION_URGENTES else 0,
        ]
        for _ in range(pedidos)
    ]

    if desordenar:
        azar.shuffle(filas_productos)

    return filas_productos, filas_lotes, filas_pedidos


def escribir(carpeta: Path, filas: list[list], columnas: tuple, nombre: str) -> Path:
    """
    Escribe un CSV con encabezado en la carpeta indicada y devuelve su ruta.

    Complejidad:
        Tiempo: O(filas).
        Espacio: O(1).
    """
    ruta = carpeta / nombre

    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(columnas)
        escritor.writerows(filas)

    return ruta


def generar_archivos(
    carpeta: str | Path = "datos",
    productos: int = 10_000,
    lotes: int = 20_000,
    pedidos: int = 30_000,
    semilla: int = 2026,
    desordenar: bool = False,
) -> dict[str, Path]:
    """
    Genera los tres CSV en la carpeta (que se crea si no existe) y devuelve
    un diccionario con sus rutas: productos, lotes y pedidos.

    Complejidad:
        Tiempo: O(productos + lotes + pedidos).
        Espacio: O(productos + lotes + pedidos).
    """
    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)
    f_productos, f_lotes, f_pedidos = generar(
        productos, lotes, pedidos, semilla, desordenar
    )

    return {
        "productos": escribir(
            destino, f_productos, COLUMNAS_PRODUCTOS, "productos.csv"
        ),
        "lotes": escribir(destino, f_lotes, COLUMNAS_LOTES, "lotes.csv"),
        "pedidos": escribir(destino, f_pedidos, COLUMNAS_PEDIDOS, "pedidos.csv"),
    }


def main() -> None:
    """
    Interfaz de línea de comandos del generador.

    Complejidad:
        Tiempo: la de generar_archivos.
        Espacio: la de generar_archivos.
    """
    analizador = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analizador.add_argument("--productos", type=int, default=10_000)
    analizador.add_argument("--lotes", type=int, default=20_000)
    analizador.add_argument("--pedidos", type=int, default=30_000)
    analizador.add_argument("--semilla", type=int, default=2026)
    analizador.add_argument("--salida", default="datos")
    analizador.add_argument(
        "--desordenar",
        action="store_true",
        help="filas de productos en orden aleatorio",
    )
    a = analizador.parse_args()
    rutas = generar_archivos(
        a.salida, a.productos, a.lotes, a.pedidos, a.semilla, a.desordenar
    )

    for nombre, ruta in rutas.items():
        print(f"{nombre}: {ruta}")

    print(f"Movimientos generados: {a.lotes + a.pedidos}")


if __name__ == "__main__":
    main()
