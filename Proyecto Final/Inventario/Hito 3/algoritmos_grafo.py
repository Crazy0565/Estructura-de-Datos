"""
Algoritmos propios sobre grafos (cualquiera de las dos representaciones):

    bfs                 recorrido por anchura (cola propia)
    dfs                 recorrido por profundidad, iterativo (pila propia)
    componentes_conexas qué nodos están conectados entre sí
    dijkstra            distancias mínimas desde un origen (cola de prioridad)
    camino_minimo       la ruta más corta entre dos nodos

Todo es iterativo, así que un grafo de decenas de miles de nodos no
desborda la pila de recursión de Python.
"""

from collections.abc import Iterator

from arreglo import ArregloDinamico
from cola_enlazada import ColaEnlazada
from cola_prioridad import ColaPrioridad
from pila import PilaEnlazada

INFINITO = float("inf")


def _arreglo_de(n: int, valor) -> ArregloDinamico:
    """
    Crea un arreglo de n posiciones, todas con el mismo valor.

    Complejidad:
        Tiempo: O(n).
        Espacio: O(n).
    """
    arreglo = ArregloDinamico(n)

    for _ in range(n):
        arreglo.agregar(valor)

    return arreglo


def bfs(grafo, origen: int) -> Iterator[int]:
    """
    Recorre por anchura los nodos alcanzables desde `origen`: primero el
    origen, luego sus vecinos, luego los vecinos de estos, etc.

    Complejidad:
        Tiempo: O(V + E) con lista de adyacencia (O(V²) con matriz).
        Espacio: O(V).
    """
    grafo._validar_nodo(origen)
    visitado = _arreglo_de(grafo.numero_nodos, False)
    cola = ColaEnlazada()
    visitado[origen] = True
    cola.encolar(origen)

    while not cola.esta_vacia():
        nodo = cola.desencolar()
        yield nodo

        for vecino, _ in grafo.vecinos(nodo):
            if not visitado[vecino]:
                visitado[vecino] = True
                cola.encolar(vecino)


def dfs(grafo, origen: int) -> Iterator[int]:
    """
    Recorre por profundidad los nodos alcanzables desde `origen`, yendo lo
    más lejos posible por un camino antes de retroceder. Iterativo.

    Complejidad:
        Tiempo: O(V + E) con lista de adyacencia (O(V²) con matriz).
        Espacio: O(V).
    """
    grafo._validar_nodo(origen)
    visitado = _arreglo_de(grafo.numero_nodos, False)
    pila = PilaEnlazada()
    pila.apilar(origen)

    while not pila.esta_vacia():
        nodo = pila.desapilar()

        if visitado[nodo]:
            continue

        visitado[nodo] = True
        yield nodo

        for vecino, _ in grafo.vecinos(nodo):
            if not visitado[vecino]:
                pila.apilar(vecino)


def componentes_conexas(grafo) -> tuple[int, ArregloDinamico]:
    """
    Agrupa los nodos en componentes conexas. Devuelve (cantidad, etiquetas):
    etiquetas[i] es el número de componente (desde 0) del nodo i.

    Complejidad:
        Tiempo: O(V + E) con lista de adyacencia.
        Espacio: O(V).
    """
    n = grafo.numero_nodos
    etiquetas = _arreglo_de(n, -1)
    cantidad = 0

    for inicio in range(n):
        if etiquetas[inicio] != -1:
            continue

        for nodo in bfs(grafo, inicio):
            etiquetas[nodo] = cantidad

        cantidad += 1

    return cantidad, etiquetas


def dijkstra(
    grafo, origen: int, destino: int | None = None
) -> tuple[ArregloDinamico, ArregloDinamico]:
    """
    Distancias mínimas desde `origen` a todos los nodos (INFINITO si no hay
    camino). Devuelve (distancias, previos): previos[v] es el nodo anterior a
    v en su camino mínimo (-1 si no tiene). Si se indica `destino`, se detiene
    al fijar su distancia.

    Requiere pesos positivos (el grafo ya los exige).

    Complejidad:
        Tiempo: O((V + E) log V) con lista de adyacencia.
        Espacio: O(V + E) por la cola de prioridad.
    """
    grafo._validar_nodo(origen)
    n = grafo.numero_nodos
    distancia = _arreglo_de(n, INFINITO)
    previo = _arreglo_de(n, -1)
    cerrado = _arreglo_de(n, False)
    cola = ColaPrioridad()
    distancia[origen] = 0
    cola.encolar(0, origen)

    while not cola.esta_vacia():
        d, nodo = cola.desencolar_con_prioridad()

        if cerrado[nodo]:
            continue

        cerrado[nodo] = True

        if nodo == destino:
            break

        for vecino, peso in grafo.vecinos(nodo):
            nueva = d + peso

            if nueva < distancia[vecino]:
                distancia[vecino] = nueva
                previo[vecino] = nodo
                cola.encolar(nueva, vecino)

    return distancia, previo


def camino_minimo(
    grafo, origen: int, destino: int
) -> tuple[float, ArregloDinamico] | None:
    """
    Ruta más corta de `origen` a `destino`. Devuelve (distancia, camino) con
    el camino como arreglo de nodos desde el origen hasta el destino, o None
    si no hay camino.

    Complejidad:
        Tiempo: O((V + E) log V).
        Espacio: O(V + E).
    """
    grafo._validar_nodo(destino)
    distancia, previo = dijkstra(grafo, origen, destino)

    if distancia[destino] == INFINITO:
        return None

    camino = ArregloDinamico()
    nodo = destino

    while nodo != -1:
        camino.agregar(nodo)
        nodo = previo[nodo]

    izquierda, derecha = 0, len(camino) - 1

    while izquierda < derecha:
        temporal = camino[izquierda]
        camino[izquierda] = camino[derecha]
        camino[derecha] = temporal
        izquierda += 1
        derecha -= 1

    return distancia[destino], camino
