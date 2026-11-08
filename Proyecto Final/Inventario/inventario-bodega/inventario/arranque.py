"""
Arranque del sistema completo con un solo comando.

    python iniciar.py                 # genera datos, los carga, abre la ventana
    python iniciar.py --sin-ventana   # lo mismo pero solo imprime un resumen
    python iniciar.py --productos 500 # un volumen menor para probar rápido
    python iniciar.py --consola       # menú de consola en vez de la ventana

Pasos (todos automáticos, ninguno manual):
    1. Si no existe la base SQLite (o se pide --reiniciar), genera los CSV
       sintéticos con semilla fija, los carga en el sistema y los guarda.
    2. Abre la base y muestra el estado.
    3. Abre la interfaz gráfica sobre esa base (salvo --sin-ventana).

Las estructuras de datos del núcleo son propias; SQLite solo guarda el estado
y la ventana es una capa delgada sobre SistemaInventario.
"""

import argparse
import time
from pathlib import Path

from inventario.generacion.generador_datos import generar_archivos
from inventario.nucleo.sistema import SistemaInventario
from inventario.persistencia.repositorio_sqlite import RepositorioSQLite

RUTA_DB = "inventario.db"
CARPETA_DATOS = "datos/generados"


def preparar_base(
    ruta_db: str, carpeta: str, productos: int, reiniciar: bool
) -> SistemaInventario:
    """
    Deja lista la base: la crea con datos sintéticos si no existe (o si se
    pide reiniciar) y devuelve el sistema cargado desde ella.

    Complejidad:
        Tiempo: O(n + L + p) al crearla (n productos, L lotes, p pedidos);
        O(n + L + p) al cargarla.
        Espacio: O(n + L + p).
    """
    existe = Path(ruta_db).exists()

    if existe and reiniciar:
        Path(ruta_db).unlink()
        existe = False

    repositorio = RepositorioSQLite(ruta_db)

    if not existe:
        rutas = generar_archivos(
            carpeta, productos, lotes=2 * productos, pedidos=3 * productos
        )
        sistema = SistemaInventario()
        sistema.cargar_csv(str(rutas["productos"]))
        sistema.cargar_lotes_csv(str(rutas["lotes"]))
        sistema.cargar_pedidos_csv(str(rutas["pedidos"]))
        repositorio.guardar(sistema)

    sistema = repositorio.cargar()
    repositorio.cerrar()

    return sistema


def resumen(sistema: SistemaInventario) -> str:
    """
    Texto con el estado del sistema recién cargado.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return (
        f"Productos: {len(sistema.catalogo)} | "
        f"Bodega: {sistema.bodega.tamaño}x{sistema.bodega.tamaño} | "
        f"Pedidos pendientes: {sistema.total_pendientes()} "
        f"({len(sistema.urgentes)} urgentes)"
    )


def main() -> None:
    """
    Lee los argumentos, prepara la base y abre la interfaz.

    Complejidad:
        Tiempo: la de preparar_base más la interfaz.
        Espacio: O(n + L + p).
    """
    ap = argparse.ArgumentParser(description="Arranca el sistema de inventario.")
    ap.add_argument("--productos", type=int, default=10_000)
    ap.add_argument("--db", default=RUTA_DB)
    ap.add_argument("--carpeta", default=CARPETA_DATOS)
    ap.add_argument("--reiniciar", action="store_true", help="regenera la base")
    ap.add_argument("--sin-ventana", action="store_true", help="solo imprime")
    ap.add_argument("--consola", action="store_true", help="abre el menú de consola")
    args = ap.parse_args()

    inicio = time.perf_counter()
    sistema = preparar_base(args.db, args.carpeta, args.productos, args.reiniciar)
    print(resumen(sistema))
    print(f"Listo en {time.perf_counter() - inicio:.1f} s (base: {args.db}).")

    if args.sin_ventana:
        return

    if args.consola:
        from inventario.interfaces import consola

        consola.RUTA_DB = args.db
        consola.main()
        return

    from inventario.interfaces import (
        gui,  # tkinter solo se importa si se abre la ventana
    )

    gui.RUTA_DB = args.db
    gui.main()


if __name__ == "__main__":
    main()
