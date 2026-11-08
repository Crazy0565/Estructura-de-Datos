"""
Ruta de recolección: en qué orden pasar por las ubicaciones de un pedido.

El operario sale del muelle, recoge los productos de un pedido (cada uno en
una ubicación del plano) y vuelve al muelle. Se comparan dos órdenes:

    - Orden de llegada: se visitan las ubicaciones tal como están en el pedido.
    - Ruta optimizada: vecino más cercano + mejora 2-opt, usando las
      distancias reales por los corredores (Dijkstra sobre el plano).

Es el problema del viajante: la solución exacta es exponencial, por eso se
usa una heurística y se mide cuánto se ahorra (criterio de éxito: >= 20 %).

Estructuras propias: ArregloDinamico para todo (sin list/dict).
"""

from inventario.estructuras.arreglo import ArregloDinamico
from inventario.grafos.algoritmos_grafo import INFINITO, dijkstra
from inventario.grafos.plano_bodega import MUELLE, PlanoBodega


def matriz_de_distancias(
    plano: PlanoBodega, paradas: ArregloDinamico
) -> ArregloDinamico:
    """
    Distancia mínima entre cada par de paradas (paradas[0] debe ser el muelle).
    Se corre Dijkstra una vez desde cada parada.

    Complejidad:
        Tiempo: O(k (V + E) log V) con k paradas.
        Espacio: O(k²) para la matriz (más O(V) transitorio).
    """
    k = len(paradas)
    matriz = ArregloDinamico(k)

    for i in range(k):
        distancias, _ = dijkstra(plano.grafo, paradas[i])
        fila = ArregloDinamico(k)

        for j in range(k):
            fila.agregar(distancias[paradas[j]])

        matriz.agregar(fila)

    return matriz


def distancia_de_ruta(matriz: ArregloDinamico, orden: ArregloDinamico) -> int:
    """
    Distancia total muelle -> orden[0] -> ... -> orden[-1] -> muelle.
    `orden` contiene índices de parada (1..k-1); el 0 es el muelle.

    Complejidad:
        Tiempo: O(m) con m paradas visitadas.
        Espacio: O(1).
    """
    total = 0
    actual = 0

    for i in range(len(orden)):
        total += matriz[actual][orden[i]]
        actual = orden[i]

    return total + matriz[actual][0]


def orden_de_llegada(k: int) -> ArregloDinamico:
    """
    Orden tal cual vienen las paradas en el pedido: 1, 2, ..., k-1.

    Complejidad:
        Tiempo: O(k).
        Espacio: O(k).
    """
    orden = ArregloDinamico(k)

    for i in range(1, k):
        orden.agregar(i)

    return orden


def vecino_mas_cercano(matriz: ArregloDinamico) -> ArregloDinamico:
    """
    Desde el muelle, ir siempre a la parada no visitada más cercana.

    Complejidad:
        Tiempo: O(k²).
        Espacio: O(k).
    """
    k = len(matriz)
    visitada = ArregloDinamico(k)

    for _ in range(k):
        visitada.agregar(False)

    visitada[0] = True
    orden = ArregloDinamico(k)
    actual = 0

    for _ in range(k - 1):
        mejor = -1

        for j in range(1, k):
            if not visitada[j] and (
                mejor == -1 or matriz[actual][j] < matriz[actual][mejor]
            ):
                mejor = j

        visitada[mejor] = True
        orden.agregar(mejor)
        actual = mejor

    return orden


def mejorar_2opt(matriz: ArregloDinamico, orden: ArregloDinamico) -> ArregloDinamico:
    """
    Mejora una ruta invirtiendo tramos mientras eso acorte la distancia
    (2-opt). Modifica y devuelve `orden`.

    Complejidad:
        Tiempo: O(k²) por pasada; el número de pasadas es pequeño en la práctica.
        Espacio: O(1).
    """
    m = len(orden)
    mejoro = True

    while mejoro:
        mejoro = False

        for i in range(m - 1):
            for j in range(i + 1, m):
                antes = orden[i - 1] if i > 0 else 0
                despues = orden[j + 1] if j + 1 < m else 0
                actual = matriz[antes][orden[i]] + matriz[orden[j]][despues]
                nuevo = matriz[antes][orden[j]] + matriz[orden[i]][despues]

                if nuevo < actual:
                    _invertir(orden, i, j)
                    mejoro = True

    return orden


def _invertir(orden: ArregloDinamico, i: int, j: int) -> None:
    """
    Invierte orden[i..j] en el mismo arreglo.

    Complejidad:
        Tiempo: O(j - i).
        Espacio: O(1).
    """
    while i < j:
        orden[i], orden[j] = orden[j], orden[i]
        i += 1
        j -= 1


class ResultadoRuta:
    """
    Resultado de comparar ambas rutas de un pedido.

    Atributos: paradas (nodos del plano, sin el muelle), orden_llegada,
    orden_optimo (índices 1..k-1 sobre `paradas` con el muelle en 0),
    distancia_llegada, distancia_optima y ahorro (fracción 0..1).
    """

    def __init__(
        self,
        paradas: ArregloDinamico,
        orden_llegada: ArregloDinamico,
        orden_optimo: ArregloDinamico,
        dist_llegada: float,
        dist_optima: float,
    ) -> None:
        """
        Guarda ambos órdenes con sus distancias y calcula el ahorro.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.paradas = paradas
        self.orden_llegada = orden_llegada
        self.orden_optimo = orden_optimo
        self.distancia_llegada = dist_llegada
        self.distancia_optima = dist_optima
        self.ahorro = (
            0.0 if dist_llegada == 0 else (dist_llegada - dist_optima) / dist_llegada
        )


def comparar_rutas(plano: PlanoBodega, nodos: ArregloDinamico) -> ResultadoRuta:
    """
    Calcula la ruta en orden de llegada y la optimizada para un pedido cuyas
    ubicaciones son los `nodos` del plano (en el orden del pedido).

    Complejidad:
        Tiempo: O(k (V + E) log V + k²).
        Espacio: O(k² + V).
    """
    paradas = ArregloDinamico(len(nodos) + 1)
    paradas.agregar(MUELLE)

    for i in range(len(nodos)):
        paradas.agregar(nodos[i])

    matriz = matriz_de_distancias(plano, paradas)
    llegada = orden_de_llegada(len(paradas))
    optimo = mejorar_2opt(matriz, vecino_mas_cercano(matriz))

    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == INFINITO:
                raise ValueError("hay ubicaciones inalcanzables desde el muelle")

    dist_llegada = distancia_de_ruta(matriz, llegada)
    dist_optima = distancia_de_ruta(matriz, optimo)

    if dist_optima > dist_llegada:
        # La heurística no garantiza ganar; nunca se entrega una ruta peor.
        optimo, dist_optima = llegada, dist_llegada

    return ResultadoRuta(paradas, llegada, optimo, dist_llegada, dist_optima)
