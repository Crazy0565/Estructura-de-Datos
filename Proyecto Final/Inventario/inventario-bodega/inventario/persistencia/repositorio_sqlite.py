"""
Capa de persistencia en SQLite (módulo `sqlite3` de la biblioteca estándar).

Regla de diseño: SQL solo guarda y recupera. Todo el trabajo del sistema
(buscar, ordenar, despachar) sigue haciéndose con las estructuras propias
en memoria. Al abrir se reconstruye el SistemaInventario leyendo la base;
al guardar se escribe una foto completa del estado dentro de una sola
transacción (si algo falla, la base queda como estaba).
"""

import sqlite3

from inventario.dominio.devolucion import Devolucion
from inventario.dominio.lote import Lote
from inventario.dominio.pedido import Pedido
from inventario.dominio.producto import Producto
from inventario.estructuras.arreglo import ArregloDinamico
from inventario.nucleo.sistema import SistemaInventario

ESQUEMA = """
CREATE TABLE IF NOT EXISTS meta (
    clave TEXT PRIMARY KEY,
    valor INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS productos (
    posicion INTEGER PRIMARY KEY,
    id INTEGER NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    tiempo_produccion INTEGER NOT NULL,
    fecha_produccion TEXT NOT NULL,
    precio REAL NOT NULL,
    pasillo INTEGER NOT NULL,
    estante INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS lotes (
    id_producto INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_produccion TEXT NOT NULL,
    fecha_vencimiento TEXT NOT NULL,
    PRIMARY KEY (id_producto, codigo)
);
CREATE TABLE IF NOT EXISTS pedidos (
    posicion INTEGER PRIMARY KEY,
    numero INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS urgencias (
    numero INTEGER PRIMARY KEY,
    urgencia INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS historial (
    posicion INTEGER PRIMARY KEY,
    numero INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    estado TEXT NOT NULL,
    motivo TEXT NOT NULL,
    tomas TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS devoluciones (
    posicion INTEGER PRIMARY KEY,
    numero INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    codigo_lote TEXT NOT NULL,
    cantidad INTEGER NOT NULL
);
"""

TABLAS = (
    "meta",
    "productos",
    "lotes",
    "pedidos",
    "urgencias",
    "historial",
    "devoluciones",
)


def _tomas_a_texto(tomas: ArregloDinamico | None) -> str:
    """
    Serializa el detalle de un despacho como 'lote:unidades;lote:unidades'.

    Complejidad:
        Tiempo: O(k) para k tomas.
        Espacio: O(k).
    """
    if tomas is None:
        return ""

    partes = []

    for i in range(len(tomas)):
        codigo, unidades = tomas[i]
        partes.append(f"{codigo}:{unidades}")

    return ";".join(partes)


def _texto_a_tomas(texto: str) -> ArregloDinamico | None:
    """
    Reconstruye el detalle de un despacho desde su texto. '' equivale a
    "sin detalle" (pedido rechazado). El código de lote se separa por el
    último ':' para tolerar códigos que lo contengan.

    Complejidad:
        Tiempo: O(k) para k tomas.
        Espacio: O(k).
    """
    if texto == "":
        return None

    tomas = ArregloDinamico()

    for parte in texto.split(";"):
        codigo, unidades = parte.rsplit(":", 1)
        tomas.agregar((codigo, int(unidades)))

    return tomas


class RepositorioSQLite:
    """
    Guarda y recupera un SistemaInventario en un archivo SQLite.

    Complejidad:
        Guardar y cargar: O(n + L + p + h + d) en el tamaño del estado
        (productos, lotes, pedidos, historial, devoluciones).
        Espacio: O(1) extra en guardar; el sistema reconstruido en cargar.
    """

    def __init__(self, ruta: str) -> None:
        """
        Abre (o crea) la base y garantiza que el esquema exista. Usar ':memory:'
        para una base temporal.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self.ruta = ruta
        self._con = sqlite3.connect(ruta)
        self._con.executescript(ESQUEMA)

    def cerrar(self) -> None:
        """
        Cierra la conexión.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        self._con.close()

    def guardar(self, sistema: SistemaInventario) -> None:
        """
        Reemplaza el contenido de la base por el estado actual del sistema,
        en una sola transacción: si algo falla, no se aplica nada.

        Complejidad:
            Tiempo: O(n + L + p + h + d).
            Espacio: O(1).
        """
        with self._con:
            for tabla in TABLAS:
                self._con.execute(f"DELETE FROM {tabla}")

            meta = (
                ("ultimo_pedido", sistema._ultimo_pedido),
                ("ultima_devolucion", sistema._ultima_devolucion),
            )
            self._con.executemany("INSERT INTO meta VALUES (?, ?)", meta)

            for i in range(len(sistema.catalogo)):
                p = sistema.catalogo[i]
                self._con.execute(
                    "INSERT INTO productos VALUES (?,?,?,?,?,?,?,?,?)",
                    (
                        i,
                        p.id,
                        p.nombre,
                        p.categoria,
                        p.tiempo_produccion,
                        p.fecha_produccion,
                        p.precio,
                        p.pasillo,
                        p.estante,
                    ),
                )

                for lote in p.lotes:
                    self._con.execute(
                        "INSERT INTO lotes VALUES (?,?,?,?,?)",
                        (
                            p.id,
                            lote.codigo,
                            lote.cantidad,
                            lote.fecha_produccion,
                            lote.fecha_vencimiento,
                        ),
                    )

            # Primero los urgentes (en el orden en que saldrán) y luego los
            # normales; la urgencia de cada uno va en su propia tabla.
            pendientes = sistema.siguientes_pedidos(sistema.total_pendientes())

            for i in range(len(pendientes)):
                pedido = pendientes[i]
                self._con.execute(
                    "INSERT INTO pedidos VALUES (?,?,?,?)",
                    (i, pedido.numero, pedido.id_producto, pedido.cantidad),
                )

                if pedido.urgencia > 0:
                    self._con.execute(
                        "INSERT INTO urgencias VALUES (?,?)",
                        (pedido.numero, pedido.urgencia),
                    )

            for i, pedido in enumerate(sistema.historial):
                self._con.execute(
                    "INSERT INTO historial VALUES (?,?,?,?,?,?,?)",
                    (
                        i,
                        pedido.numero,
                        pedido.id_producto,
                        pedido.cantidad,
                        pedido.estado,
                        pedido.motivo,
                        _tomas_a_texto(pedido.tomas),
                    ),
                )

            # La pila se recorre de la cima al fondo: posición 0 = cima.
            for i, dev in enumerate(sistema.devoluciones):
                self._con.execute(
                    "INSERT INTO devoluciones VALUES (?,?,?,?,?)",
                    (i, dev.numero, dev.id_producto, dev.codigo_lote, dev.cantidad),
                )

    def cargar(self) -> SistemaInventario:
        """
        Reconstruye un SistemaInventario con lo guardado. Con una base vacía
        devuelve un sistema vacío. El orden de las filas se lee de la columna
        `posicion` guardada; no se usa SQL para ordenar datos del dominio.

        Complejidad:
            Tiempo: O(n + L + p + h + d) más los costos de reinsertar.
            Espacio: O(n + L + p + h + d).
        """
        sistema = SistemaInventario()
        c = self._con

        meta = dict(c.execute("SELECT clave, valor FROM meta"))
        sistema._ultimo_pedido = meta.get("ultimo_pedido", 0)
        sistema._ultima_devolucion = meta.get("ultima_devolucion", 0)

        filas = c.execute(
            "SELECT id, nombre, categoria, tiempo_produccion, fecha_produccion,"
            " precio, pasillo, estante FROM productos ORDER BY posicion"
        )

        for (
            id_,
            nombre,
            cat,
            tiempo,
            fprod,
            precio,
            pasillo,
            estante,
        ) in filas.fetchall():
            producto = Producto(
                id_, nombre, cat, 0, tiempo, fprod, "", precio, pasillo, estante
            )

            lotes = c.execute(
                "SELECT codigo, cantidad, fecha_produccion, fecha_vencimiento"
                " FROM lotes WHERE id_producto = ?",
                (id_,),
            )

            for codigo, cantidad, lp, lv in lotes.fetchall():
                producto.lotes.insertar(Lote(codigo, cantidad, lp, lv))

            sistema.agregar(producto)

        for numero, id_producto, cantidad, urgencia in c.execute(
            "SELECT p.numero, p.id_producto, p.cantidad, COALESCE(u.urgencia, 0)"
            " FROM pedidos p LEFT JOIN urgencias u ON u.numero = p.numero"
            " ORDER BY p.posicion"
        ).fetchall():
            pedido = Pedido(numero, id_producto, cantidad, urgencia)

            if urgencia > 0:
                sistema.urgentes.encolar(-urgencia, pedido)
            else:
                sistema.pedidos.encolar(pedido)

        for numero, id_producto, cantidad, estado, motivo, tomas in c.execute(
            "SELECT numero, id_producto, cantidad, estado, motivo, tomas"
            " FROM historial ORDER BY posicion"
        ).fetchall():
            pedido = Pedido(numero, id_producto, cantidad)
            pedido.estado = estado
            pedido.motivo = motivo
            pedido.tomas = _texto_a_tomas(tomas)
            sistema.historial.encolar(pedido)

        # Se apila del fondo hacia la cima para recuperar el mismo orden.
        for numero, id_producto, codigo, cantidad in c.execute(
            "SELECT numero, id_producto, codigo_lote, cantidad"
            " FROM devoluciones ORDER BY posicion DESC"
        ).fetchall():
            sistema.devoluciones.apilar(
                Devolucion(numero, id_producto, codigo, cantidad)
            )

        return sistema
