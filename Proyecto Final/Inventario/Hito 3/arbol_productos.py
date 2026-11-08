"""
Árboles binarios de búsqueda propios para indexar productos por código.

    ArbolBinarioBusqueda: árbol sin balanceo. Insertar, buscar y eliminar
        cuestan O(h): O(log n) si las claves llegan mezcladas y O(n) si llegan
        en orden (el árbol degenera en una lista).
    ArbolAVL: el mismo árbol con rotaciones que mantienen la altura en
        O(log n) siempre, sin importar el orden de llegada.

Todas las operaciones del árbol sin balanceo son iterativas a propósito: con
10.000 claves ordenadas la altura llega a 10.000 y una versión recursiva
desbordaría la pila de Python (límite 1.000). Los recorridos usan las
estructuras propias del proyecto: `PilaEnlazada` (en orden y preorden) y
`ColaEnlazada` (por niveles). El AVL sí usa recursión, con profundidad
O(log n) garantizada.

Complejidad de espacio de ambos: O(n), un nodo por clave.
"""

from collections.abc import Iterator
from typing import Any

from cola_enlazada import ColaEnlazada
from pila import PilaEnlazada


class NodoArbol:
    """
    Nodo de un árbol binario: una clave, su valor y dos hijos.

    `altura` solo la mantiene el AVL (una hoja vale 1).

    Complejidad:
        Tiempo de creación: O(1).
        Espacio: O(1).
    """

    def __init__(self, clave: int, valor: Any) -> None:
        """
        Crea un nodo hoja.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.clave = clave
        self.valor = valor
        self.izquierdo: NodoArbol | None = None
        self.derecho: NodoArbol | None = None
        self.altura = 1


class ArbolBinarioBusqueda:
    """
    Árbol binario de búsqueda: las claves menores van a la izquierda y las
    mayores a la derecha. No admite claves repetidas.

    Complejidad:
        Espacio: O(n).
    """

    def __init__(self) -> None:
        """
        Crea un árbol vacío.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._raiz: NodoArbol | None = None
        self.tamaño = 0

    def __len__(self) -> int:
        """
        Devuelve la cantidad de claves.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño

    def __iter__(self) -> Iterator[tuple[int, Any]]:
        """
        Recorre el árbol en orden (claves de menor a mayor).

        Complejidad:
            Tiempo: O(n) el recorrido completo.
            Espacio: O(h) por la pila.
        """
        return self.inorden()

    def esta_vacio(self) -> bool:
        """
        Indica si no hay claves.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño == 0

    def contiene(self, clave: int) -> bool:
        """
        Indica si la clave está en el árbol.

        Complejidad:
            Tiempo: O(h).
            Espacio: O(1).
        """
        return self._nodo(clave) is not None

    def buscar(self, clave: int) -> Any | None:
        """
        Devuelve el valor de la clave, o None si no existe.

        Complejidad:
            Tiempo: O(h): O(log n) en promedio, O(n) en el peor caso.
            Espacio: O(1).
        """
        nodo = self._nodo(clave)

        return None if nodo is None else nodo.valor

    def insertar(self, clave: int, valor: Any) -> None:
        """
        Inserta una clave nueva. Lanza ValueError si ya existe.

        Complejidad:
            Tiempo: O(h).
            Espacio: O(1).
        """
        nuevo = NodoArbol(clave, valor)

        if self._raiz is None:
            self._raiz = nuevo
            self.tamaño = 1
            return

        actual = self._raiz

        while True:
            if clave == actual.clave:
                raise ValueError(f"La clave {clave} ya existe.")

            if clave < actual.clave:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    break

                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    break

                actual = actual.derecho

        self.tamaño += 1

    def eliminar(self, clave: int) -> Any | None:
        """
        Elimina una clave y devuelve su valor, o None si no existe.

        Resuelve los tres casos: hoja, un hijo y dos hijos (en este último
        el nodo toma la clave de su sucesor en orden, el menor del subárbol
        derecho, y se elimina el sucesor, que tiene a lo sumo un hijo).

        Complejidad:
            Tiempo: O(h).
            Espacio: O(1).
        """
        padre: NodoArbol | None = None
        actual = self._raiz

        while actual is not None and actual.clave != clave:
            padre = actual
            actual = actual.izquierdo if clave < actual.clave else actual.derecho

        if actual is None:
            return None

        valor = actual.valor

        if actual.izquierdo is not None and actual.derecho is not None:
            padre_sucesor = actual
            sucesor = actual.derecho

            while sucesor.izquierdo is not None:
                padre_sucesor = sucesor
                sucesor = sucesor.izquierdo

            actual.clave = sucesor.clave
            actual.valor = sucesor.valor
            padre, actual = padre_sucesor, sucesor

        hijo = actual.izquierdo if actual.izquierdo is not None else actual.derecho

        if padre is None:
            self._raiz = hijo
        elif padre.izquierdo is actual:
            padre.izquierdo = hijo
        else:
            padre.derecho = hijo

        self.tamaño -= 1

        return valor

    def minimo(self) -> tuple[int, Any]:
        """
        Devuelve la menor clave y su valor. Lanza IndexError si está vacío.

        Complejidad:
            Tiempo: O(h).
            Espacio: O(1).
        """
        if self._raiz is None:
            raise IndexError("El árbol está vacío.")

        actual = self._raiz

        while actual.izquierdo is not None:
            actual = actual.izquierdo

        return actual.clave, actual.valor

    def maximo(self) -> tuple[int, Any]:
        """
        Devuelve la mayor clave y su valor. Lanza IndexError si está vacío.

        Complejidad:
            Tiempo: O(h).
            Espacio: O(1).
        """
        if self._raiz is None:
            raise IndexError("El árbol está vacío.")

        actual = self._raiz

        while actual.derecho is not None:
            actual = actual.derecho

        return actual.clave, actual.valor

    def altura(self) -> int:
        """
        Devuelve la altura del árbol (0 si está vacío, 1 si solo hay raíz).

        Complejidad:
            Tiempo: O(n): se cuentan los niveles con un recorrido por niveles.
            Espacio: O(a), con a el ancho máximo del árbol.
        """
        if self._raiz is None:
            return 0

        cola = ColaEnlazada()
        cola.encolar(self._raiz)
        niveles = 0

        while not cola.esta_vacia():
            for _ in range(len(cola)):
                nodo = cola.desencolar()

                if nodo.izquierdo is not None:
                    cola.encolar(nodo.izquierdo)

                if nodo.derecho is not None:
                    cola.encolar(nodo.derecho)

            niveles += 1

        return niveles

    def inorden(self) -> Iterator[tuple[int, Any]]:
        """
        Recorrido en orden: izquierda, nodo, derecha. Entrega las claves
        ordenadas de menor a mayor. Iterativo, con una pila propia.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(h) por la pila.
        """
        pila = PilaEnlazada()
        actual = self._raiz

        while actual is not None or not pila.esta_vacia():
            while actual is not None:
                pila.apilar(actual)
                actual = actual.izquierdo

            nodo = pila.desapilar()
            yield nodo.clave, nodo.valor
            actual = nodo.derecho

    def preorden(self) -> Iterator[tuple[int, Any]]:
        """
        Recorrido en preorden: nodo, izquierda, derecha. Sirve para copiar
        la forma del árbol. Iterativo, con una pila propia.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(h) por la pila.
        """
        if self._raiz is None:
            return

        pila = PilaEnlazada()
        pila.apilar(self._raiz)

        while not pila.esta_vacia():
            nodo = pila.desapilar()
            yield nodo.clave, nodo.valor

            if nodo.derecho is not None:
                pila.apilar(nodo.derecho)

            if nodo.izquierdo is not None:
                pila.apilar(nodo.izquierdo)

    def por_niveles(self) -> Iterator[tuple[int, Any]]:
        """
        Recorrido por niveles (anchura): la raíz, luego sus hijos, luego los
        nietos, etc. Iterativo, con una cola propia.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(a), con a el ancho máximo del árbol.
        """
        if self._raiz is None:
            return

        cola = ColaEnlazada()
        cola.encolar(self._raiz)

        while not cola.esta_vacia():
            nodo = cola.desencolar()
            yield nodo.clave, nodo.valor

            if nodo.izquierdo is not None:
                cola.encolar(nodo.izquierdo)

            if nodo.derecho is not None:
                cola.encolar(nodo.derecho)

    def rango(self, desde: int, hasta: int) -> Iterator[tuple[int, Any]]:
        """
        Entrega, en orden, las claves entre `desde` y `hasta` (inclusive).

        Poda los subárboles que no pueden contener claves del rango, así que
        no recorre todo el árbol.

        Complejidad:
            Tiempo: O(h + k), con k las claves entregadas.
            Espacio: O(h) por la pila.
        """
        pila = PilaEnlazada()
        actual = self._raiz

        while actual is not None or not pila.esta_vacia():
            while actual is not None:
                if actual.clave >= desde:
                    pila.apilar(actual)
                    actual = actual.izquierdo
                else:
                    actual = actual.derecho

            if pila.esta_vacia():
                return

            nodo = pila.desapilar()

            if nodo.clave > hasta:
                return

            yield nodo.clave, nodo.valor
            actual = nodo.derecho

    def _nodo(self, clave: int) -> NodoArbol | None:
        """
        Devuelve el nodo de la clave, o None.

        Complejidad:
            Tiempo: O(h).
            Espacio: O(1).
        """
        actual = self._raiz

        while actual is not None and actual.clave != clave:
            actual = actual.izquierdo if clave < actual.clave else actual.derecho

        return actual


def _altura(nodo: NodoArbol | None) -> int:
    """
    Altura guardada en un nodo (0 si no hay nodo).

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return 0 if nodo is None else nodo.altura


def _actualizar(nodo: NodoArbol) -> None:
    """
    Recalcula la altura de un nodo a partir de las de sus hijos.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    nodo.altura = 1 + max(_altura(nodo.izquierdo), _altura(nodo.derecho))


def _equilibrio(nodo: NodoArbol) -> int:
    """
    Factor de equilibrio: altura izquierda menos altura derecha.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    return _altura(nodo.izquierdo) - _altura(nodo.derecho)


def _rotar_derecha(y: NodoArbol) -> NodoArbol:
    """
    Rotación simple a la derecha: el hijo izquierdo pasa a ser la raíz del
    subárbol. Devuelve la nueva raíz.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    x = y.izquierdo
    y.izquierdo = x.derecho
    x.derecho = y
    _actualizar(y)
    _actualizar(x)

    return x


def _rotar_izquierda(x: NodoArbol) -> NodoArbol:
    """
    Rotación simple a la izquierda: el hijo derecho pasa a ser la raíz del
    subárbol. Devuelve la nueva raíz.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    y = x.derecho
    x.derecho = y.izquierdo
    y.izquierdo = x
    _actualizar(x)
    _actualizar(y)

    return y


def _reequilibrar(nodo: NodoArbol) -> NodoArbol:
    """
    Actualiza la altura del nodo y, si el factor de equilibrio sale de
    [-1, 1], aplica la rotación (simple o doble) que lo corrige. Devuelve la
    raíz del subárbol ya equilibrado.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    _actualizar(nodo)
    balance = _equilibrio(nodo)

    if balance > 1:
        if _equilibrio(nodo.izquierdo) < 0:
            nodo.izquierdo = _rotar_izquierda(nodo.izquierdo)

        return _rotar_derecha(nodo)

    if balance < -1:
        if _equilibrio(nodo.derecho) > 0:
            nodo.derecho = _rotar_derecha(nodo.derecho)

        return _rotar_izquierda(nodo)

    return nodo


class ArbolAVL(ArbolBinarioBusqueda):
    """
    Árbol binario de búsqueda autobalanceado (AVL): en cada nodo, las
    alturas de sus dos subárboles difieren como máximo en 1. Por eso la
    altura nunca supera 1,44 · log2(n + 2) y buscar, insertar y eliminar
    cuestan O(log n) siempre.

    Complejidad:
        Espacio: O(n). La recursión de insertar y eliminar llega a O(log n).
    """

    def insertar(self, clave: int, valor: Any) -> None:
        """
        Inserta una clave nueva y reequilibra. Lanza ValueError si existe.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(log n) por la recursión.
        """
        if self.contiene(clave):
            raise ValueError(f"La clave {clave} ya existe.")

        self._raiz = self._insertar(self._raiz, clave, valor)
        self.tamaño += 1

    def eliminar(self, clave: int) -> Any | None:
        """
        Elimina una clave, reequilibra y devuelve su valor (o None).

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(log n) por la recursión.
        """
        nodo = self._nodo(clave)

        if nodo is None:
            return None

        valor = nodo.valor
        self._raiz = self._eliminar(self._raiz, clave)
        self.tamaño -= 1

        return valor

    def altura(self) -> int:
        """
        Devuelve la altura del árbol, leída de la raíz.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return _altura(self._raiz)

    def _insertar(self, nodo: NodoArbol | None, clave: int, valor: Any) -> NodoArbol:
        """
        Inserta recursivamente y reequilibra al regresar por cada nodo.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(log n).
        """
        if nodo is None:
            return NodoArbol(clave, valor)

        if clave < nodo.clave:
            nodo.izquierdo = self._insertar(nodo.izquierdo, clave, valor)
        else:
            nodo.derecho = self._insertar(nodo.derecho, clave, valor)

        return _reequilibrar(nodo)

    def _eliminar(self, nodo: NodoArbol | None, clave: int) -> NodoArbol | None:
        """
        Elimina recursivamente (la clave existe) y reequilibra al regresar.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(log n).
        """
        if nodo is None:
            return None

        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar(nodo.derecho, clave)
        else:
            if nodo.izquierdo is None:
                return nodo.derecho

            if nodo.derecho is None:
                return nodo.izquierdo

            sucesor = nodo.derecho

            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo

            nodo.clave = sucesor.clave
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_minimo(nodo.derecho)

        return _reequilibrar(nodo)

    def _eliminar_minimo(self, nodo: NodoArbol) -> NodoArbol | None:
        """
        Quita el menor nodo de un subárbol y devuelve su nueva raíz.

        Complejidad:
            Tiempo: O(log n).
            Espacio: O(log n).
        """
        if nodo.izquierdo is None:
            return nodo.derecho

        nodo.izquierdo = self._eliminar_minimo(nodo.izquierdo)

        return _reequilibrar(nodo)
