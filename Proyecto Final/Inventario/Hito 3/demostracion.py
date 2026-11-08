"""
Demostración reproducible del criterio de éxito del proyecto.

    python demostracion.py              # 10.000 productos, 20 olas por tamaño
    python demostracion.py --rapido     # versión pequeña (segundos)

Con datos sintéticos de semilla fija, comprueba dos cosas:

    1. FEFO: cada pedido despachado toma primero los lotes que vencen antes.
       Se verifica con un verificador independiente, escrito aparte del código
       del despacho, sobre una foto de los lotes tomada ANTES de cada
       despacho. Criterio: 100 % de los casos.

    2. Ruta de recolección: la ruta optimizada recorre al menos 20 % menos
       distancia que atender las ubicaciones en orden de llegada. Se mide en
       olas reales (los próximos k pedidos de la cola) de varios tamaños.

Escribe en la carpeta `resultados/`: resumen.txt, rutas.csv y
ahorro_rutas.png. Si un criterio no se cumple, lo dice en el resumen.
"""

import argparse
import csv
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from generador_datos import generar_archivos
from pedido import DESPACHADO
from sistema import SistemaInventario

SEMILLA = 2026
TAMANOS_OLA = (3, 5, 10, 20)
TAMANO_TIPICO = 10
META_AHORRO = 0.20


def cargar_sistema(carpeta: str, productos: int) -> SistemaInventario:
    """
    Genera los CSV sintéticos (productos en orden aleatorio, lotes en
    desorden) y los carga en un sistema nuevo.

    Complejidad:
        Tiempo: O(n + L + p) para n productos, L lotes y p pedidos.
        Espacio: O(n + L + p).
    """
    rutas = generar_archivos(
        carpeta, productos, lotes=2 * productos, pedidos=3 * productos,
        semilla=SEMILLA, desordenar=True,
    )  # fmt: skip
    sistema = SistemaInventario()
    sistema.cargar_csv(str(rutas["productos"]))
    sistema.cargar_lotes_csv(str(rutas["lotes"]))
    sistema.cargar_pedidos_csv(str(rutas["pedidos"]))

    return sistema


def foto_de_lotes(sistema: SistemaInventario, id_producto: int) -> list[tuple]:
    """
    Copia (código, cantidad, vencimiento) de los lotes de un producto.

    Complejidad:
        Tiempo: O(l) con l lotes del producto.
        Espacio: O(l).
    """
    producto = sistema.buscar_indexado(id_producto)

    return [(l.codigo, l.cantidad, l.fecha_vencimiento) for l in producto.lotes]


def cumple_fefo(foto: list[tuple], tomas: list[tuple], cantidad: int) -> bool:
    """
    Verificador independiente de FEFO. Un despacho es correcto si:
      - lo tomado suma exactamente lo pedido;
      - nunca se toma más de lo que tenía un lote;
      - todo lote tomado salvo el último se vació por completo;
      - ningún lote que NO se tocó vence antes que uno que sí se tocó.

    Complejidad:
        Tiempo: O(l + t) con l lotes en la foto y t tomas.
        Espacio: O(l).
    """
    if sum(c for _, c in tomas) != cantidad:
        return False

    existencias = {codigo: (cant, venc) for codigo, cant, venc in foto}
    ultimo_venc = ""

    for i, (codigo, tomado) in enumerate(tomas):
        if codigo not in existencias or tomado > existencias[codigo][0] or tomado <= 0:
            return False

        if i < len(tomas) - 1 and tomado != existencias[codigo][0]:
            return False

        ultimo_venc = max(ultimo_venc, existencias[codigo][1])

    tocados = {codigo for codigo, _ in tomas}

    return all(venc >= ultimo_venc for codigo, (cant, venc) in existencias.items()
               if codigo not in tocados and cant > 0)  # fmt: skip


def despachar_verificado(sistema: SistemaInventario, resultados: dict) -> None:
    """
    Despacha el siguiente pedido y verifica FEFO si se despachó.

    Complejidad:
        Tiempo: la del despacho más O(l) de la verificación.
        Espacio: O(l).
    """
    siguiente = sistema.siguientes_pedidos(1)[0]
    foto = foto_de_lotes(sistema, siguiente.id_producto)
    pedido = sistema.despachar_siguiente()

    if pedido.estado != DESPACHADO:
        resultados["rechazados"] += 1
        return

    tomas = [pedido.tomas[i] for i in range(len(pedido.tomas))]
    resultados["despachados"] += 1

    if not cumple_fefo(foto, tomas, pedido.cantidad):
        resultados["violaciones"] += 1


def medir_rutas(sistema: SistemaInventario, olas: int, resultados: dict) -> list[dict]:
    """
    Para cada tamaño de ola, toma `olas` olas consecutivas de la cola real,
    calcula su ruta (llegada frente a optimizada) y despacha los pedidos con
    verificación de FEFO.

    Complejidad:
        Tiempo: O(olas · k (V + E) log V) por tamaño de ola k.
        Espacio: O(V + k²).
    """
    filas = []

    for k in TAMANOS_OLA:
        llegada = optima = 0
        peor = 1.0

        for _ in range(olas):
            ruta = sistema.ruta_de_recoleccion(k)

            if ruta is not None:
                llegada += ruta.distancia_llegada
                optima += ruta.distancia_optima
                peor = min(peor, ruta.ahorro)

            for _ in range(k):
                despachar_verificado(sistema, resultados)

        ahorro = (llegada - optima) / llegada if llegada else 0.0
        filas.append({"pedidos_por_ola": k, "olas": olas, "distancia_llegada": llegada,
                      "distancia_optima": optima, "ahorro": ahorro, "ahorro_minimo": peor})  # fmt: skip

    return filas


def graficar(filas: list[dict], destino: Path) -> None:
    """
    Gráfica del ahorro por tamaño de ola con la meta del 20 %.

    Complejidad:
        Tiempo: O(f) con f filas.
        Espacio: O(f).
    """
    etiquetas = [str(f["pedidos_por_ola"]) for f in filas]
    ahorros = [100 * f["ahorro"] for f in filas]
    minimos = [100 * f["ahorro_minimo"] for f in filas]
    colores = ["#2a7f62" if a >= 100 * META_AHORRO else "#b5502d" for a in ahorros]

    fig, ax = plt.subplots(figsize=(6.5, 4), dpi=150)
    ax.bar(etiquetas, ahorros, color=colores)
    ax.scatter(etiquetas, minimos, color="black", zorder=3, s=18, label="Peor ola")
    ax.axhline(100 * META_AHORRO, color="gray", linestyle="--", label="Meta 20 %")

    for x, a in zip(etiquetas, ahorros):
        ax.text(x, a + 1, f"{a:.1f} %", ha="center", fontsize=9)

    ax.set_xlabel("Pedidos por ola")
    ax.set_ylabel("Distancia ahorrada (%)")
    ax.set_title("Ruta optimizada frente a orden de llegada")
    ax.legend(
        handles=[
            Patch(color="#2a7f62", label="Ahorro medio: cumple la meta"),
            Patch(color="#b5502d", label="Ahorro medio: no cumple"),
            *ax.get_legend_handles_labels()[0],
        ],
        frameon=False,
        fontsize=8,
        loc="upper left",
    )
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(destino)
    plt.close(fig)


def escribir_resultados(carpeta: Path, filas, resultados, productos, segundos) -> str:
    """
    Escribe rutas.csv, la gráfica y resumen.txt; devuelve el texto del resumen.

    Complejidad:
        Tiempo: O(f).
        Espacio: O(1).
    """
    carpeta.mkdir(exist_ok=True)

    with open(carpeta / "rutas.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)

    graficar(filas, carpeta / "ahorro_rutas.png")
    fefo_ok = resultados["violaciones"] == 0
    tipica = next(f for f in filas if f["pedidos_por_ola"] == TAMANO_TIPICO)
    ruta_ok = tipica["ahorro"] >= META_AHORRO
    lineas = [
        f"Demostración (semilla {SEMILLA}, {productos} productos, tiempo {segundos:.0f} s)",
        "",
        "1. FEFO (despacho respeta vencimiento)",
        f"   pedidos despachados verificados: {resultados['despachados']}",
        f"   rechazados (sin stock, no se verifican): {resultados['rechazados']}",
        f"   violaciones de FEFO: {resultados['violaciones']}",
        f"   RESULTADO: {'CUMPLE (100 %)' if fefo_ok else 'NO CUMPLE'}",
        "",
        "2. Ruta de recolección (meta: >= 20 % menos distancia)",
    ]

    for f in filas:
        marca = "cumple" if f["ahorro"] >= META_AHORRO else "NO cumple"
        lineas.append(
            f"   olas de {f['pedidos_por_ola']:>2} pedidos: ahorro medio {f['ahorro']:.1%}, "
            f"peor ola {f['ahorro_minimo']:.1%} -> {marca}"
        )

    lineas.append(
        f"   RESULTADO con ola típica de {TAMANO_TIPICO}: "
        f"{'CUMPLE' if ruta_ok else 'NO CUMPLE'} ({tipica['ahorro']:.1%})"
    )
    texto = "\n".join(lineas)
    (carpeta / "resumen.txt").write_text(texto + "\n", encoding="utf-8")

    return texto


def main() -> None:
    """
    Corre la demostración completa.

    Complejidad:
        Tiempo: carga + rutas + despacho de todos los pedidos.
        Espacio: O(n + L + p).
    """
    ap = argparse.ArgumentParser(description="Demostración del criterio de éxito.")
    ap.add_argument("--productos", type=int, default=10_000)
    ap.add_argument("--olas", type=int, default=20, help="olas por tamaño")
    ap.add_argument("--rapido", action="store_true", help="2.000 productos, 5 olas")
    ap.add_argument("--carpeta", default="datos")
    ap.add_argument("--salida", default="resultados")
    args = ap.parse_args()

    if args.rapido:
        args.productos, args.olas = 2_000, 5

    inicio = time.perf_counter()
    sistema = cargar_sistema(args.carpeta, args.productos)
    resultados = {"despachados": 0, "rechazados": 0, "violaciones": 0}
    filas = medir_rutas(sistema, args.olas, resultados)

    while sistema.total_pendientes() > 0:
        despachar_verificado(sistema, resultados)

    texto = escribir_resultados(
        Path(args.salida),
        filas,
        resultados,
        args.productos,
        time.perf_counter() - inicio,
    )
    print(texto)
    print(f"\nArchivos en {args.salida}/")


if __name__ == "__main__":
    main()
