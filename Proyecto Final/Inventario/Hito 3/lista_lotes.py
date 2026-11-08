from collections.abc import Iterator

from arreglo import ArregloDinamico
from lote import Lote
from nodo import Nodo

LIMITE_RECURSION = 500


def _fusionar_nodos(a: Nodo | None, b: Nodo | None) -> Nodo | None:
    """
    Fusiona dos cadenas de nodos ordenadas por vencimiento, de forma
    recursiva y reutilizando los nodos existentes.

    Ante un vencimiento igual, el nodo de la cadena a va primero, así que
    la fusión es estable.

    Complejidad:
        Tiempo: O(n + m).
        Espacio: O(n + m) por la pila de llamadas (una por nodo consumido).
    """
    if a is None:
        return b

    if b is None:
        return a

    if b.dato.fecha_vencimiento < a.dato.fecha_vencimiento:
        b.siguiente = _fusionar_nodos(a, b.siguiente)
        return b

    a.siguiente = _fusionar_nodos(a.siguiente, b)
    return a


class ListaLotes:
    """
    Lista ligada sencilla de lotes, ordenada por fecha de vencimiento.

    El primer nodo es siempre el lote que vence antes, así que despachar
    primero lo más próximo a vencer es quitar desde la cabeza.

    Complejidad:
        Espacio: O(n), un nodo por lote.
    """

    def __init__(self) -> None:
        """
        Crea una lista vacía.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.cabeza: Nodo | None = None
        self.tamaño = 0
        self._stock = 0

    def __len__(self) -> int:
        """
        Devuelve la cantidad de lotes.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.tamaño

    def __iter__(self) -> Iterator[Lote]:
        """
        Recorre los lotes desde el que vence antes.

        Complejidad:
            Tiempo: O(n) el recorrido completo.
            Espacio: O(1).
        """
        actual = self.cabeza

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def stock_total(self) -> int:
        """
        Devuelve las unidades sumadas de todos los lotes.

        Complejidad:
            Tiempo: O(1), porque se mantiene un acumulado.
            Espacio: O(1).
        """
        return self._stock

    def primero(self) -> Lote | None:
        """
        Devuelve el lote que vence antes, o None si no hay lotes.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self.cabeza is None:
            return None

        return self.cabeza.dato

    def buscar(self, codigo: str) -> Lote | None:
        """
        Busca un lote por su código.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(1).
        """
        for lote in self:
            if lote.codigo == codigo:
                return lote

        return None

    def insertar(self, lote: Lote) -> None:
        """
        Inserta un lote en la posición que le corresponde por vencimiento.

        Ante un vencimiento igual, el lote nuevo queda después de los
        existentes. Lanza ValueError si el código ya existe.

        Complejidad:
            Tiempo: O(n) por la búsqueda de duplicado y de la posición.
            Espacio: O(1).
        """
        if self.buscar(lote.codigo) is not None:
            raise ValueError(f"Ya existe un lote con el código {lote.codigo}.")

        nuevo = Nodo(lote)

        if (
            self.cabeza is None
            or lote.fecha_vencimiento < self.cabeza.dato.fecha_vencimiento
        ):
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            actual = self.cabeza

            while (
                actual.siguiente is not None
                and actual.siguiente.dato.fecha_vencimiento <= lote.fecha_vencimiento
            ):
                actual = actual.siguiente

            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo

        self.tamaño += 1
        self._stock += lote.cantidad

    def despachar(self, cantidad: int) -> ArregloDinamico:
        """
        Retira unidades empezando por el lote que vence antes.

        Consume lotes completos desde la cabeza y reduce el último si hace
        falta. Devuelve un arreglo de tuplas (código del lote, unidades
        tomadas). Si el stock no alcanza lanza ValueError y no cambia nada.

        Complejidad:
            Tiempo: O(k), con k los lotes que se tocan (O(1) si el primero
            alcanza).
            Espacio: O(k) por el detalle devuelto.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a despachar debe ser mayor que cero.")

        if cantidad > self._stock:
            raise ValueError(
                f"Stock insuficiente: hay {self._stock} y se piden {cantidad}."
            )

        tomas = ArregloDinamico()
        pendiente = cantidad

        while pendiente > 0:
            lote = self.cabeza.dato

            if lote.cantidad <= pendiente:
                tomas.agregar((lote.codigo, lote.cantidad))
                pendiente -= lote.cantidad
                self.cabeza = self.cabeza.siguiente
                self.tamaño -= 1
            else:
                lote.cantidad -= pendiente
                tomas.agregar((lote.codigo, pendiente))
                pendiente = 0

        self._stock -= cantidad

        return tomas

    def eliminar_lote(self, codigo: str) -> Lote | None:
        """
        Elimina un lote por su código y lo devuelve, o None si no existe.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(1).
        """
        anterior: Nodo | None = None
        actual = self.cabeza

        while actual is not None:
            if actual.dato.codigo == codigo:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                self.tamaño -= 1
                self._stock -= actual.dato.cantidad

                return actual.dato

            anterior = actual
            actual = actual.siguiente

        return None

    def fusionar(self, otra: "ListaLotes") -> None:
        """
        Absorbe los lotes de otra lista conservando el orden por vencimiento.

        Usa la versión recursiva mientras la pila de llamadas es segura y la
        iterativa cuando el total de lotes supera LIMITE_RECURSION. La otra
        lista queda vacía.

        Complejidad:
            Tiempo: O(n + m).
            Espacio: O(n + m) en la versión recursiva, O(1) en la iterativa.
        """
        if self.tamaño + otra.tamaño <= LIMITE_RECURSION:
            self.fusionar_recursivo(otra)
        else:
            self.fusionar_iterativo(otra)

    def fusionar_recursivo(self, otra: "ListaLotes") -> None:
        """
        Fusiona con recursión: cada llamada decide un nodo y delega el resto.

        La profundidad de pila llega a n + m. Con listas muy grandes lanza
        RecursionError sin haber modificado ninguna de las dos listas.

        Complejidad:
            Tiempo: O(n + m).
            Espacio: O(n + m) por la pila de llamadas.
        """
        self._validar_otra(otra)
        nueva_cabeza = _fusionar_nodos(self.cabeza, otra.cabeza)
        self._absorber(otra, nueva_cabeza)

    def fusionar_iterativo(self, otra: "ListaLotes") -> None:
        """
        Fusiona con un bucle y un nodo ficticio, sin usar la pila.

        Complejidad:
            Tiempo: O(n + m).
            Espacio: O(1).
        """
        self._validar_otra(otra)

        ficticio = Nodo(None)
        ultimo = ficticio
        a = self.cabeza
        b = otra.cabeza

        while a is not None and b is not None:
            if b.dato.fecha_vencimiento < a.dato.fecha_vencimiento:
                ultimo.siguiente = b
                b = b.siguiente
            else:
                ultimo.siguiente = a
                a = a.siguiente

            ultimo = ultimo.siguiente

        ultimo.siguiente = a if a is not None else b

        self._absorber(otra, ficticio.siguiente)

    def _validar_otra(self, otra: "ListaLotes") -> None:
        """
        Impide fusionar una lista consigo misma.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if otra is self:
            raise ValueError("No se puede fusionar una lista consigo misma.")

    def _absorber(self, otra: "ListaLotes", nueva_cabeza: Nodo | None) -> None:
        """
        Actualiza esta lista tras una fusión y deja vacía la otra.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.cabeza = nueva_cabeza
        self.tamaño += otra.tamaño
        self._stock += otra._stock

        otra.cabeza = None
        otra.tamaño = 0
        otra._stock = 0
