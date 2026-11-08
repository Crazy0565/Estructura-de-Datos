"""Gráficas del informe de la Entrega 1 (inserción, búsquedas, ordenamientos, acceso).

Los tiempos son los medidos en la Entrega 1 (ver docs/entrega1/resultados.md).
Uso: python -m mediciones.graficas_entrega1   (escribe PNG en docs/entrega1/graficas/)
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CARPETA = Path(__file__).resolve().parents[1] / "docs" / "entrega1" / "graficas"

CANTIDADES = [1000, 5000, 10000, 50000, 100000]
INSERCION = [0.000681, 0.002720, 0.005408, 0.029080, 0.081061]
ACCESO = [0.000001200, 0.000001600, 0.000000900, 0.000001100, 0.000002200]
LINEAL = [0.000038, 0.000188, 0.000395, 0.002000, 0.003892]
BINARIA = [0.000003600, 0.000004100, 0.000004200, 0.000006100, 0.000007800]
QUICK_SORT = [0.000164, 0.000799, 0.001657, 0.007957, 0.018977]
BUBBLE_SORT = [0.050138, 1.446117, 5.426820]  # 50.000 y 100.000 se omitieron


def graficar(
    series: dict[str, tuple[list[int], list[float]]], titulo: str, archivo: str
) -> None:
    """
    Dibuja las series (nombre -> (x, y)) y guarda la gráfica como PNG.

    Complejidad:
        Tiempo: O(k·m) para k series de m puntos.
        Espacio: O(k·m).
    """
    plt.figure()

    for nombre, (xs, ys) in series.items():
        plt.plot(xs, ys, marker="o", label=nombre)

    plt.xlabel("Cantidad de productos")
    plt.ylabel("Tiempo (segundos)")
    plt.title(titulo)

    if len(series) > 1:
        plt.legend()

    plt.grid(True)
    plt.savefig(CARPETA / archivo)
    plt.close()


def main() -> None:
    """
    Genera las cuatro gráficas de la Entrega 1.

    Complejidad:
        Tiempo: O(1) (cantidad fija de puntos).
        Espacio: O(1).
    """
    CARPETA.mkdir(parents=True, exist_ok=True)
    graficar(
        {"Inserción": (CANTIDADES, INSERCION)},
        "Tiempo de inserción",
        "grafica_insercion.png",
    )
    graficar(
        {
            "Búsqueda lineal": (CANTIDADES, LINEAL),
            "Búsqueda binaria": (CANTIDADES, BINARIA),
        },
        "Comparación de búsquedas",
        "grafica_busquedas.png",
    )
    graficar(
        {
            "Bubble Sort": (CANTIDADES[:3], BUBBLE_SORT),
            "QuickSort": (CANTIDADES, QUICK_SORT),
        },
        "Comparación de algoritmos de ordenamiento",
        "grafica_ordenamientos.png",
    )
    graficar(
        {"Acceso": (CANTIDADES, ACCESO)},
        "Tiempo de acceso al arreglo",
        "grafica_acceso.png",
    )
    print(f"Gráficas en {CARPETA}")


if __name__ == "__main__":
    main()
