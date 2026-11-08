import csv
from collections.abc import Callable
from typing import Any

from arbol_productos import ArbolAVL
from arreglo import ArregloDinamico
from busqueda import busqueda_binaria, busqueda_lineal
from cola_circular import ColaCircular
from cola_enlazada import ColaEnlazada
from cola_prioridad import ColaPrioridad
from devolucion import Devolucion
from lista_lotes import ListaLotes
from lote import Lote
from matriz import MatrizBodega
from ordenamiento import quick_sort
from pedido import DESPACHADO, RECHAZADO, Pedido
from pila import PilaEnlazada
from plano_bodega import PlanoBodega
from producto import Producto
from ruta_recoleccion import ResultadoRuta, comparar_rutas

CRITERIOS_ORDEN = ("id", "nombre", "vencimiento", "tiempo_produccion")
CAPACIDAD_HISTORIAL = 5


def clave_de_orden(criterio: str) -> Callable[[Producto], Any]:
    """
    Devuelve la función que extrae el campo por el que se ordena.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    if criterio == "id":
        return lambda producto: producto.id

    if criterio == "nombre":
        return lambda producto: producto.nombre

    if criterio == "vencimiento":
        return lambda producto: producto.fecha_vencimiento

    if criterio == "tiempo_produccion":
        return lambda producto: producto.tiempo_produccion

    raise ValueError(f"Criterio de orden desconocido: {criterio}")


class SistemaInventario:
    """
    Núcleo del sistema: coordina el catálogo (arreglo dinámico) y las
    ubicaciones físicas (matriz de bodega), sin depender de la consola.

    Mantiene un indicador de si el catálogo está ordenado por ID, para
    elegir entre búsqueda binaria y búsqueda lineal.

    También gestiona el despacho:
        - pedidos pendientes en una cola enlazada (FIFO sin tope, para que
          ningún pedido se pierda);
        - historial de los últimos despachos en una cola circular de
          capacidad fija (al llenarse sale el más antiguo);
        - devoluciones en una pila (se revierte primero la última).

    Complejidad:
        Espacio: O(n + m² + p), con n productos, una matriz de m x m y p
        pedidos pendientes.
    """

    def __init__(self) -> None:
        """
        Crea un sistema vacío.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.catalogo = ArregloDinamico()
        self.bodega = MatrizBodega()
        self.pedidos = ColaEnlazada()
        self.urgentes = ColaPrioridad()
        self.indice = ArbolAVL()
        self._plano: PlanoBodega | None = None
        self.historial = ColaCircular(CAPACIDAD_HISTORIAL)
        self.devoluciones = PilaEnlazada()
        self._ordenado_por_id = True
        self._ultimo_pedido = 0
        self._ultima_devolucion = 0

    @property
    def ordenado_por_id(self) -> bool:
        """
        Indica si el catálogo está ordenado por ID.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self._ordenado_por_id

    def agregar(self, producto: Producto) -> None:
        """
        Agrega un producto al catálogo y lo ubica en la bodega.

        La ubicación se reserva primero: si está ocupada se lanza
        ValueError y el catálogo no cambia.

        Complejidad:
            Tiempo: O(1) amortizado.
            Tiempo: O(m²) si la matriz de bodega se amplía.
            Espacio: O(1) amortizado.
        """
        self.bodega.asignar(producto.pasillo, producto.estante, producto)

        total = len(self.catalogo)

        if self._ordenado_por_id and total > 0:
            ultimo = self.catalogo[total - 1]
            self._ordenado_por_id = ultimo.id <= producto.id

        self.catalogo.agregar(producto)
        self.indice.insertar(producto.id, producto)

    def buscar_indexado(self, id_producto: int) -> Producto | None:
        """
        Busca un producto por su ID en el índice AVL, esté o no ordenado el
        catálogo.

        Complejidad:
            Tiempo: O(log n) siempre.
            Espacio: O(1).
        """
        return self.indice.buscar(id_producto)

    def buscar_por_id(self, id_producto: int) -> Producto | None:
        """
        Busca un producto por su ID.

        Usa búsqueda binaria si el catálogo está ordenado por ID y búsqueda
        lineal en caso contrario.

        Complejidad:
            Tiempo: O(log n) si está ordenado por ID, O(n) si no.
            Espacio: O(1).
        """

        def clave(producto: Producto) -> int:
            return producto.id

        if self._ordenado_por_id:
            return busqueda_binaria(self.catalogo, id_producto, clave)

        return busqueda_lineal(self.catalogo, id_producto, clave)

    def eliminar_por_id(self, id_producto: int) -> Producto | None:
        """
        Elimina un producto del catálogo y libera su ubicación.

        Devuelve el producto eliminado, o None si no existe. El orden del
        resto del catálogo se conserva.

        Complejidad:
            Tiempo: O(n) por la localización y el desplazamiento.
            Espacio: O(1).
        """
        producto = self.buscar_por_id(id_producto)

        if producto is None:
            return None

        self.bodega.eliminar(producto.pasillo, producto.estante)
        self.catalogo.eliminar(self._posicion(producto))
        self.indice.eliminar(producto.id)

        return producto

    def consultar_ubicacion(self, pasillo: int, estante: int) -> Producto | None:
        """
        Devuelve el producto ubicado en un pasillo y estante, o None si
        la ubicación está libre. Lanza IndexError si queda fuera de la bodega.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.bodega.obtener(pasillo, estante)

    def ubicaciones_libres(self) -> int:
        """
        Cuenta las ubicaciones sin producto. Cada producto ocupa exactamente
        una ubicación, porque la matriz rechaza las ubicaciones repetidas.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.bodega.tamaño * self.bodega.tamaño - len(self.catalogo)

    def ordenar(self, criterio: str) -> None:
        """
        Reordena el catálogo con QuickSort según el criterio indicado.

        Complejidad:
            Tiempo: O(n log n) en promedio, O(n²) en el peor caso.
            Espacio: O(n) por las listas auxiliares de QuickSort.
        """
        ordenados = quick_sort(self.catalogo, clave_de_orden(criterio))

        nuevo = ArregloDinamico()

        for i in range(len(ordenados)):
            nuevo.agregar(ordenados[i])

        self.catalogo = nuevo
        self._ordenado_por_id = criterio == "id"

    def cargar_csv(self, ruta: str) -> int:
        """
        Carga productos desde un CSV y devuelve cuántos se cargaron.

        Si una fila apunta a una ubicación ocupada se lanza ValueError; las
        filas anteriores ya quedan cargadas.

        Complejidad:
            Tiempo: O(n) filas, más O(m²) por cada ampliación de la matriz.
            Espacio: O(n).
        """
        cargados = 0

        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                producto = Producto(
                    int(fila["id"]),
                    fila["nombre"],
                    fila["categoria"],
                    int(fila["cantidad"]),
                    int(fila["tiempo_produccion"]),
                    fila["fecha_produccion"],
                    fila["fecha_vencimiento"],
                    float(fila["precio"]),
                    int(fila["pasillo"]),
                    int(fila["estante"]),
                )

                self.agregar(producto)
                cargados += 1

        return cargados

    def registrar_lote(
        self,
        id_producto: int,
        codigo: str,
        cantidad: int,
        fecha_produccion: str,
        fecha_vencimiento: str,
    ) -> Lote | None:
        """
        Registra un lote nuevo en un producto, en el lugar que le toca por
        vencimiento. Devuelve el lote, o None si el producto no existe.

        Lanza ValueError si los datos del lote son inválidos o el código ya
        existe en ese producto.

        Complejidad:
            Tiempo: O(log n) o O(n) por la búsqueda del producto, más O(l)
            por la inserción ordenada entre sus l lotes.
            Espacio: O(1).
        """
        producto = self.buscar_por_id(id_producto)

        if producto is None:
            return None

        lote = Lote(codigo, cantidad, fecha_produccion, fecha_vencimiento)
        producto.lotes.insertar(lote)

        return lote

    def despachar_producto(
        self, id_producto: int, cantidad: int
    ) -> ArregloDinamico | None:
        """
        Despacha unidades de un producto tomando primero el lote que vence
        antes. Devuelve el detalle (código de lote, unidades), o None si el
        producto no existe. Lanza ValueError si el stock no alcanza.

        Complejidad:
            Tiempo: O(log n) o O(n) por la búsqueda, más O(k) por los k
            lotes que se tocan.
            Espacio: O(k).
        """
        producto = self.buscar_por_id(id_producto)

        if producto is None:
            return None

        return producto.lotes.despachar(cantidad)

    def cargar_lotes_csv(self, ruta: str) -> int:
        """
        Carga lotes desde un CSV como un embarque: agrupa los lotes de cada
        producto en una lista ordenada y la fusiona con la que ya tiene.

        Es todo o nada: si una fila es inválida se lanza ValueError antes de
        fusionar nada. Devuelve cuántos lotes se cargaron.

        Complejidad:
            Tiempo: O(f * (log p + l)) para f filas, l lotes por producto y p
            productos distintos del archivo, más O(l) por cada fusión.
            Espacio: O(f).
        """
        pendientes = ArbolAVL()
        cargados = 0

        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                id_producto = int(fila["id_producto"])
                producto = self.buscar_por_id(id_producto)

                if producto is None:
                    raise ValueError(f"El producto {id_producto} no existe.")

                codigo = fila["codigo_lote"].strip()

                if producto.lotes.buscar(codigo) is not None:
                    raise ValueError(
                        f"El lote {codigo} ya existe en el producto {id_producto}."
                    )

                embarque = self._embarque_de(pendientes, producto)
                embarque.insertar(
                    Lote(
                        codigo,
                        int(fila["cantidad"]),
                        fila["fecha_produccion"],
                        fila["fecha_vencimiento"],
                    )
                )
                cargados += 1

        for _, (producto, embarque) in pendientes:
            producto.lotes.fusionar(embarque)

        return cargados

    def registrar_pedido(
        self, id_producto: int, cantidad: int, urgencia: int = 0
    ) -> Pedido | None:
        """
        Registra un pedido pendiente. Los normales van al final de la cola
        FIFO; los urgentes (urgencia 1 a 9) van a la cola de prioridad y se
        despachan antes, primero los más urgentes y, a igual urgencia, por
        orden de llegada. Devuelve el pedido, o None si el producto no
        existe. Lanza ValueError si la cantidad no es positiva o la urgencia
        es inválida.

        Complejidad:
            Tiempo: O(log n) o O(n) por la búsqueda del producto, más O(1)
            por encolar (O(log u) si es urgente, con u urgentes).
            Espacio: O(1).
        """
        if self.buscar_por_id(id_producto) is None:
            return None

        pedido = Pedido(self._ultimo_pedido + 1, id_producto, cantidad, urgencia)
        self._ultimo_pedido += 1

        if urgencia > 0:
            self.urgentes.encolar(-urgencia, pedido)
        else:
            self.pedidos.encolar(pedido)

        return pedido

    def total_pendientes(self) -> int:
        """
        Cantidad de pedidos pendientes, urgentes y normales.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return len(self.pedidos) + len(self.urgentes)

    def siguientes_pedidos(self, maximo: int) -> ArregloDinamico:
        """
        Los próximos `maximo` pedidos en el orden en que se despacharían
        (urgentes primero), sin sacarlos de las colas.

        Complejidad:
            Tiempo: O(u + maximo log u + maximo).
            Espacio: O(u + maximo).
        """
        resultado = self.urgentes.en_orden(maximo)

        for pedido in self.pedidos:
            if len(resultado) >= maximo:
                break

            resultado.agregar(pedido)

        return resultado

    def despachar_siguiente(self) -> Pedido | None:
        """
        Procesa el siguiente pedido: el urgente más prioritario si hay, y si no el
        más antiguo de la cola normal. Devuelve el pedido ya
        resuelto, o None si no hay pendientes.

        Si hay stock, se despacha tomando primero los lotes que vencen antes
        y el pedido queda despachado. Si el producto ya no existe o el stock
        no alcanza, el pedido queda rechazado con su motivo y sale de la
        cola, para que no bloquee a los que siguen. En ambos casos pasa al
        historial.

        Complejidad:
            Tiempo: O(log n) o O(n) por la búsqueda del producto, más O(k)
            por los k lotes tocados.
            Espacio: O(k).
        """
        if self.pedidos.esta_vacia() and self.urgentes.esta_vacia():
            return None

        if not self.urgentes.esta_vacia():
            pedido = self.urgentes.desencolar()
        else:
            pedido = self.pedidos.desencolar()

        producto = self.buscar_por_id(pedido.id_producto)

        if producto is None:
            pedido.estado = RECHAZADO
            pedido.motivo = "El producto ya no existe."
        else:
            try:
                pedido.tomas = producto.lotes.despachar(pedido.cantidad)
                pedido.estado = DESPACHADO
            except ValueError as error:
                pedido.estado = RECHAZADO
                pedido.motivo = str(error)

        self._archivar(pedido)

        return pedido

    def cargar_pedidos_csv(self, ruta: str) -> int:
        """
        Carga pedidos desde un CSV (columnas id_producto y cantidad, y
        opcionalmente urgente con 1 o 0) y los registra en el orden del archivo. Devuelve cuántos se cargaron.

        Es todo o nada: si una fila es inválida o su producto no existe, se
        lanza ValueError antes de encolar ninguno.

        Complejidad:
            Tiempo: O(f * n) para f filas, por la búsqueda de cada producto.
            Espacio: O(f).
        """
        validados = ArregloDinamico()

        with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
            for fila in csv.DictReader(archivo):
                id_producto = int(fila["id_producto"])
                cantidad = int(fila["cantidad"])

                if self.buscar_por_id(id_producto) is None:
                    raise ValueError(f"El producto {id_producto} no existe.")

                if cantidad <= 0:
                    raise ValueError("La cantidad del pedido debe ser mayor que cero.")

                urgente = fila.get("urgente", "0").strip().lower() in (
                    "1",
                    "true",
                    "si",
                )
                validados.agregar((id_producto, cantidad, 1 if urgente else 0))

        for i in range(len(validados)):
            id_producto, cantidad, urgencia = validados[i]
            self.registrar_pedido(id_producto, cantidad, urgencia)

        return len(validados)

    def registrar_devolucion(
        self,
        id_producto: int,
        cantidad: int,
        fecha_produccion: str,
        fecha_vencimiento: str,
    ) -> Devolucion | None:
        """
        Registra unidades devueltas: entran como un lote nuevo del producto
        y la devolución se apila para poder revertirla. Devuelve el registro,
        o None si el producto no existe. Lanza ValueError si los datos del
        lote son inválidos.

        Complejidad:
            Tiempo: O(log n) o O(n) por la búsqueda, más O(l) por la
            inserción ordenada entre sus l lotes.
            Espacio: O(1).
        """
        producto = self.buscar_por_id(id_producto)

        if producto is None:
            return None

        numero = self._ultima_devolucion + 1
        codigo = f"DEV-{numero}"

        producto.lotes.insertar(
            Lote(codigo, cantidad, fecha_produccion, fecha_vencimiento)
        )

        self._ultima_devolucion = numero
        devolucion = Devolucion(numero, id_producto, codigo, cantidad)
        self.devoluciones.apilar(devolucion)

        return devolucion

    def deshacer_ultima_devolucion(self) -> Devolucion | None:
        """
        Revierte la devolución más reciente retirando su lote. Devuelve el
        registro, o None si no hay devoluciones.

        La devolución sale de la pila aunque no se pueda revertir. Si su lote
        ya se despachó por completo o el producto ya no existe, se lanza
        ValueError. Si el lote se despachó en parte, se retira lo que quedaba.

        Complejidad:
            Tiempo: O(log n) o O(n) por la búsqueda, más O(l) por retirar el
            lote.
            Espacio: O(1).
        """
        if self.devoluciones.esta_vacia():
            return None

        devolucion = self.devoluciones.desapilar()
        producto = self.buscar_por_id(devolucion.id_producto)

        if (
            producto is None
            or producto.lotes.eliminar_lote(devolucion.codigo_lote) is None
        ):
            raise ValueError(
                "La devolución ya no se puede revertir: su lote se despachó "
                "por completo o el producto ya no existe."
            )

        return devolucion

    def _archivar(self, pedido: Pedido) -> None:
        """
        Guarda un pedido resuelto en el historial. Si el historial está
        lleno, sale primero el más antiguo.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        if self.historial.esta_llena():
            self.historial.desencolar()

        self.historial.encolar(pedido)

    def _embarque_de(self, pendientes: ArbolAVL, producto: Producto) -> ListaLotes:
        """
        Devuelve la lista de lotes pendientes de un producto, creándola si
        todavía no existe.

        Los embarques se guardan en un árbol AVL por ID de producto, así que
        encontrar el de un producto cuesta O(log p) y no O(p).

        Complejidad:
            Tiempo: O(log p), con p productos distintos en el archivo.
            Espacio: O(1).
        """
        encontrado = pendientes.buscar(producto.id)

        if encontrado is not None:
            return encontrado[1]

        embarque = ListaLotes()
        pendientes.insertar(producto.id, (producto, embarque))

        return embarque

    def _posicion(self, producto: Producto) -> int:
        """
        Devuelve el índice de un producto dentro del catálogo.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(1).
        """
        for i in range(len(self.catalogo)):
            if self.catalogo[i] is producto:
                return i

        raise ValueError("El producto no está en el catálogo.")

    def plano(self) -> PlanoBodega:
        """
        Grafo de la planta del mismo tamaño que la matriz de bodega. Se
        reconstruye solo si la bodega creció.

        Complejidad:
            Tiempo: O(m²) al construirlo; O(1) si ya estaba hecho.
            Espacio: O(m²).
        """
        if self._plano is None or self._plano.lado != self.bodega.tamaño:
            self._plano = PlanoBodega(self.bodega.tamaño)

        return self._plano

    def ruta_de_recoleccion(self, cantidad: int) -> ResultadoRuta | None:
        """
        Calcula la ruta de recolección de los próximos `cantidad` pedidos sin
        despacharlos: orden de llegada frente a ruta optimizada. Devuelve
        None si ninguno tiene producto existente.

        Complejidad:
            Tiempo: O(k (V + E) log V + k²) con k pedidos, V = m² ubicaciones.
            Espacio: O(V + k²).
        """
        siguientes = self.siguientes_pedidos(cantidad)
        plano = self.plano()
        nodos = ArregloDinamico()

        for i in range(len(siguientes)):
            producto = self.buscar_indexado(siguientes[i].id_producto)

            if producto is not None:
                nodos.agregar(plano.nodo_de(producto.pasillo, producto.estante))

        if len(nodos) == 0:
            return None

        return comparar_rutas(plano, nodos)

    def despachar_ola(
        self, cantidad: int
    ) -> tuple[ArregloDinamico, ResultadoRuta | None]:
        """
        Despacha hasta `cantidad` pedidos como una ola: calcula antes la ruta
        de recolección y luego procesa cada pedido con el despacho normal
        (FEFO). Devuelve (pedidos resueltos, ruta).

        Complejidad:
            Tiempo: la de ruta_de_recoleccion más k despachos.
            Espacio: O(V + k²).
        """
        ruta = self.ruta_de_recoleccion(cantidad)
        resueltos = ArregloDinamico()

        for _ in range(cantidad):
            pedido = self.despachar_siguiente()

            if pedido is None:
                break

            resueltos.agregar(pedido)

        return resueltos, ruta
