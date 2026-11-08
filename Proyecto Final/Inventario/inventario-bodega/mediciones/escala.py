"""
Mide cómo responde el sistema ya construido (Hito 2) con datos a escala.

Carga los CSV generados por inventario/generacion/generador_datos.py y cronometra cada etapa:
carga de productos, carga de lotes, carga de pedidos y despacho de todos los
pedidos. No modifica el sistema: solo lo observa. Sirve de línea base antes de
agregar árboles, grafos y rutas.

Uso: python -m mediciones.escala [CARPETA]   (por defecto: datos/generados)
"""

import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from inventario.nucleo.sistema import SistemaInventario


def cronometrar(descripcion: str, funcion: Callable[[], Any]) -> float:
    """
    Ejecuta la función, imprime su duración y devuelve los segundos.

    Complejidad:
        Tiempo: la de la función medida.
        Espacio: O(1).
    """
    inicio = time.perf_counter()
    resultado = funcion()
    segundos = time.perf_counter() - inicio
    print(f"{descripcion:<42} {segundos:9.3f} s   (resultado: {resultado})")
    return segundos


def despachar_todo(sistema: SistemaInventario) -> int:
    """
    Despacha todos los pedidos pendientes y devuelve cuántos se resolvieron.

    Complejidad:
        Tiempo: O(p · (log n + k)) para p pedidos.
        Espacio: O(1) extra (el historial guarda solo los últimos 5).
    """
    resueltos = 0

    while sistema.despachar_siguiente() is not None:
        resueltos += 1

    return resueltos


def main(carpeta: str = "datos/generados") -> None:
    """
    Corre la medición completa sobre la carpeta de datos indicada.

    Complejidad:
        Tiempo: la suma de las etapas medidas.
        Espacio: O(n + L + p).
    """
    base = Path(carpeta)
    sistema = SistemaInventario()
    print(f"== Medición a escala con {base} ==")
    cronometrar(
        "Cargar productos", lambda: sistema.cargar_csv(str(base / "productos.csv"))
    )
    print(
        f"   ordenado por id: {sistema.ordenado_por_id}, bodega {sistema.bodega.tamaño}x{sistema.bodega.tamaño}"
    )
    cronometrar(
        "Cargar lotes (entradas)",
        lambda: sistema.cargar_lotes_csv(str(base / "lotes.csv")),
    )
    cronometrar(
        "Cargar pedidos (salidas)",
        lambda: sistema.cargar_pedidos_csv(str(base / "pedidos.csv")),
    )
    cronometrar("Despachar todos los pedidos", lambda: despachar_todo(sistema))
    cronometrar(
        "1.000 búsquedas por id",
        lambda: sum(
            1 for i in range(1, 1001) if sistema.buscar_por_id(i * 7 % 10000 + 1)
        ),
    )
    cronometrar(
        "Ordenar por vencimiento (QuickSort)", lambda: sistema.ordenar("vencimiento")
    )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "datos/generados")
