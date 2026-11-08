"""
Interfaz gráfica (tkinter) del sistema de inventario.

Es una capa delgada: no contiene lógica de negocio. Cada botón llama a un
método de SistemaInventario y la ventana solo muestra el resultado. Si se le
pasa un repositorio, guarda el estado después de cada acción exitosa.

Uso: python gui.py
"""

import tkinter as tk
from tkinter import filedialog, ttk

from persistencia import RepositorioSQLite
from producto import Producto
from sistema import CRITERIOS_ORDEN, SistemaInventario

RUTA_DB = "inventario.db"

CAMPOS_PRODUCTO = (
    ("id", "ID"),
    ("nombre", "Nombre"),
    ("categoria", "Categoría"),
    ("cantidad", "Cantidad"),
    ("tiempo", "Tiempo prod. (días)"),
    ("fprod", "Producción AAAA-MM-DD"),
    ("fvenc", "Vencimiento AAAA-MM-DD"),
    ("precio", "Precio"),
    ("pasillo", "Pasillo"),
    ("estante", "Estante"),
)

CAMPOS_LOTE = (
    ("id", "ID producto"),
    ("codigo", "Código lote"),
    ("cantidad", "Cantidad"),
    ("fprod", "Producción AAAA-MM-DD"),
    ("fvenc", "Vencimiento AAAA-MM-DD"),
)


class AplicacionInventario(tk.Tk):
    """
    Ventana principal con una pestaña por área del sistema.

    Complejidad:
        Cada acción cuesta lo que cuesta el método del sistema que invoca;
        refrescar una tabla es O(n) en los elementos mostrados.
        Espacio: O(n) por las filas visibles.
    """

    def __init__(
        self,
        sistema: SistemaInventario,
        repositorio: RepositorioSQLite | None = None,
    ) -> None:
        """
        Construye la ventana y muestra el estado actual del sistema.

        Complejidad:
            Tiempo: O(n) por el primer refresco.
            Espacio: O(n).
        """
        super().__init__()
        self.title("Inventario y despacho de bodega")
        self.geometry("980x640")
        self.sistema = sistema
        self.repositorio = repositorio
        self.estado = tk.StringVar(value="Listo.")
        self.resumen_ruta = tk.StringVar(value="Sin ruta calculada.")
        self.vars: dict[str, dict[str, tk.StringVar]] = {}

        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True, padx=8, pady=8)
        self._construir_catalogo()
        self._construir_lotes()
        self._construir_pedidos()
        self._construir_ruta()
        self._construir_devoluciones()

        self.barra = ttk.Label(self, textvariable=self.estado, anchor="w")
        self.barra.pack(fill="x", padx=8, pady=(0, 8))
        self.refrescar()

    # ---------- utilidades ----------

    def _formulario(self, padre, nombre: str, campos) -> None:
        """
        Crea una fila de etiquetas y cajas de texto asociadas a StringVar.

        Complejidad:
            Tiempo: O(c) para c campos.
            Espacio: O(c).
        """
        marco = ttk.Frame(padre)
        marco.pack(fill="x", pady=4)
        self.vars[nombre] = {}

        for i, (clave, etiqueta) in enumerate(campos):
            var = tk.StringVar()
            self.vars[nombre][clave] = var
            fila, columna = divmod(i, 5)
            ttk.Label(marco, text=etiqueta).grid(
                row=2 * fila, column=columna, padx=2, sticky="w"
            )
            ttk.Entry(marco, textvariable=var, width=18).grid(
                row=2 * fila + 1, column=columna, padx=2
            )

    def _tabla(self, padre, columnas, alto: int = 10) -> ttk.Treeview:
        """
        Crea una tabla (Treeview) con las columnas dadas.

        Complejidad:
            Tiempo: O(c) para c columnas.
            Espacio: O(c).
        """
        tabla = ttk.Treeview(padre, columns=columnas, show="headings", height=alto)

        for columna in columnas:
            tabla.heading(columna, text=columna)
            tabla.column(columna, width=110, anchor="w")

        tabla.pack(fill="both", expand=True, pady=4)
        return tabla

    def _valor(self, formulario: str, clave: str) -> str:
        """
        Devuelve el texto de un campo sin espacios sobrantes.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        return self.vars[formulario][clave].get().strip()

    def _entero(self, formulario: str, clave: str) -> int:
        """
        Lee un campo como entero. Lanza ValueError con un mensaje claro.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        try:
            return int(self._valor(formulario, clave))
        except ValueError:
            raise ValueError(f"'{clave}' debe ser un número entero.") from None

    def _ejecutar(self, accion) -> bool:
        """
        Corre una acción; si falla muestra el error en la barra de estado.
        Si funciona, guarda en la base y refresca las tablas.

        Complejidad:
            Tiempo: la de la acción, más O(n) del refresco y del guardado.
            Espacio: O(1).
        """
        try:
            mensaje = accion()
        except (ValueError, IndexError, OSError, KeyError) as error:
            self.estado.set(f"Error: {error}")
            return False

        if self.repositorio is not None:
            self.repositorio.guardar(self.sistema)

        self.refrescar()
        self.estado.set(mensaje or "Hecho.")
        return True

    # ---------- pestaña catálogo ----------

    def _construir_catalogo(self) -> None:
        """
        Arma la pestaña de catálogo: alta, búsqueda, orden y baja.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        marco = ttk.Frame(self.pestanas, padding=8)
        self.pestanas.add(marco, text="Catálogo")
        self._formulario(marco, "producto", CAMPOS_PRODUCTO)

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=4)
        ttk.Button(
            botones, text="Agregar producto", command=self.agregar_producto
        ).pack(side="left", padx=2)
        ttk.Button(
            botones,
            text="Cargar productos CSV",
            command=lambda: self.pedir_csv("productos"),
        ).pack(side="left", padx=2)
        self.var_buscar = tk.StringVar()
        ttk.Entry(botones, textvariable=self.var_buscar, width=8).pack(
            side="left", padx=(16, 2)
        )
        ttk.Button(botones, text="Buscar por ID", command=self.buscar_producto).pack(
            side="left"
        )
        self.var_orden = tk.StringVar(value=CRITERIOS_ORDEN[0])
        ttk.Combobox(
            botones,
            textvariable=self.var_orden,
            values=CRITERIOS_ORDEN,
            width=16,
            state="readonly",
        ).pack(side="left", padx=(16, 2))
        ttk.Button(botones, text="Ordenar", command=self.ordenar).pack(side="left")
        ttk.Button(
            botones, text="Eliminar seleccionado", command=self.eliminar_seleccionado
        ).pack(side="right")

        self.tabla_catalogo = self._tabla(
            marco,
            ("ID", "Nombre", "Categoría", "Cantidad", "Vence", "Precio", "Ubicación"),
            alto=14,
        )

    def agregar_producto(self) -> bool:
        """
        Crea el producto con los datos del formulario y lo agrega al sistema.

        Complejidad:
            Tiempo: la de SistemaInventario.agregar.
            Espacio: O(1).
        """

        def accion() -> str:
            producto = Producto(
                self._entero("producto", "id"),
                self._valor("producto", "nombre"),
                self._valor("producto", "categoria"),
                self._entero("producto", "cantidad"),
                self._entero("producto", "tiempo"),
                self._valor("producto", "fprod"),
                self._valor("producto", "fvenc"),
                self._decimal("producto", "precio"),
                self._entero("producto", "pasillo"),
                self._entero("producto", "estante"),
            )

            if self.sistema.buscar_por_id(producto.id) is not None:
                raise ValueError(f"Ya existe un producto con ID {producto.id}.")

            self.sistema.agregar(producto)
            return f"Producto {producto.id} agregado."

        return self._ejecutar(accion)

    def _decimal(self, formulario: str, clave: str) -> float:
        """
        Lee un campo como número decimal.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        try:
            return float(self._valor(formulario, clave))
        except ValueError:
            raise ValueError(f"'{clave}' debe ser un número.") from None

    def buscar_producto(self) -> bool:
        """
        Busca por ID y dice si usó búsqueda binaria o lineal.

        Complejidad:
            Tiempo: O(log n) o O(n) según el catálogo esté ordenado por ID.
            Espacio: O(1).
        """

        def accion() -> str:
            try:
                id_producto = int(self.var_buscar.get().strip())
            except ValueError:
                raise ValueError("El ID debe ser un número entero.") from None

            metodo = "binaria" if self.sistema.ordenado_por_id else "lineal"
            producto = self.sistema.buscar_por_id(id_producto)

            if producto is None:
                return f"No existe el producto {id_producto} (búsqueda {metodo})."

            return f"Encontrado (búsqueda {metodo}): {producto}"

        return self._ejecutar(accion)

    def ordenar(self) -> bool:
        """
        Ordena el catálogo con el criterio elegido.

        Complejidad:
            Tiempo: O(n log n) promedio (QuickSort propio).
            Espacio: O(n).
        """

        def accion() -> str:
            self.sistema.ordenar(self.var_orden.get())
            return f"Catálogo ordenado por {self.var_orden.get()}."

        return self._ejecutar(accion)

    def eliminar_seleccionado(self) -> bool:
        """
        Elimina el producto seleccionado en la tabla.

        Complejidad:
            Tiempo: O(n) por localizar y desplazar.
            Espacio: O(1).
        """

        def accion() -> str:
            seleccion = self.tabla_catalogo.selection()

            if not seleccion:
                raise ValueError("Seleccione un producto en la tabla.")

            id_producto = int(self.tabla_catalogo.item(seleccion[0], "values")[0])
            self.sistema.eliminar_por_id(id_producto)
            return f"Producto {id_producto} eliminado."

        return self._ejecutar(accion)

    # ---------- pestaña lotes ----------

    def _construir_lotes(self) -> None:
        """
        Arma la pestaña de lotes: alta de lote, consulta y despacho FEFO.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        marco = ttk.Frame(self.pestanas, padding=8)
        self.pestanas.add(marco, text="Lotes y despacho")
        self._formulario(marco, "lote", CAMPOS_LOTE)

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=4)
        ttk.Button(botones, text="Registrar lote", command=self.registrar_lote).pack(
            side="left", padx=2
        )
        ttk.Button(botones, text="Ver lotes del producto", command=self.ver_lotes).pack(
            side="left", padx=2
        )
        ttk.Button(
            botones, text="Cargar lotes CSV", command=lambda: self.pedir_csv("lotes")
        ).pack(side="left", padx=2)
        self.var_despacho = tk.StringVar()
        ttk.Entry(botones, textvariable=self.var_despacho, width=8).pack(
            side="left", padx=(16, 2)
        )
        ttk.Button(
            botones,
            text="Despachar unidades (primero vence primero sale)",
            command=self.despachar_unidades,
        ).pack(side="left")

        self.tabla_lotes = self._tabla(
            marco, ("Código", "Cantidad", "Producción", "Vencimiento")
        )

    def registrar_lote(self) -> bool:
        """
        Registra un lote en el producto indicado.

        Complejidad:
            Tiempo: la de SistemaInventario.registrar_lote.
            Espacio: O(1).
        """

        def accion() -> str:
            id_producto = self._entero("lote", "id")
            lote = self.sistema.registrar_lote(
                id_producto,
                self._valor("lote", "codigo"),
                self._entero("lote", "cantidad"),
                self._valor("lote", "fprod"),
                self._valor("lote", "fvenc"),
            )

            if lote is None:
                raise ValueError(f"No existe el producto {id_producto}.")

            return f"Lote {lote.codigo} registrado."

        return self._ejecutar(accion)

    def ver_lotes(self) -> bool:
        """
        Muestra los lotes del producto indicado, de menor a mayor vencimiento.

        Complejidad:
            Tiempo: O(log n) o O(n) por buscar, más O(l) por mostrar.
            Espacio: O(l).
        """

        def accion() -> str:
            id_producto = self._entero("lote", "id")
            producto = self.sistema.buscar_por_id(id_producto)

            if producto is None:
                raise ValueError(f"No existe el producto {id_producto}.")

            return f"Producto {id_producto}: {producto.cantidad} unidades en {len(producto.lotes)} lotes."

        return self._ejecutar(accion)

    def despachar_unidades(self) -> bool:
        """
        Despacha unidades del producto tomando primero el lote que vence antes.

        Complejidad:
            Tiempo: O(log n) o O(n) por buscar, más O(k) por los k lotes tocados.
            Espacio: O(k).
        """

        def accion() -> str:
            id_producto = self._entero("lote", "id")

            try:
                cantidad = int(self.var_despacho.get().strip())
            except ValueError:
                raise ValueError(
                    "La cantidad a despachar debe ser un entero."
                ) from None

            tomas = self.sistema.despachar_producto(id_producto, cantidad)

            if tomas is None:
                raise ValueError(f"No existe el producto {id_producto}.")

            partes = []
            for i in range(len(tomas)):
                codigo, unidades = tomas[i]
                partes.append(f"{unidades} de {codigo}")

            return "Despachado: " + ", ".join(partes) + "."

        return self._ejecutar(accion)

    # ---------- pestaña pedidos ----------

    def _construir_pedidos(self) -> None:
        """
        Arma la pestaña de pedidos: cola pendiente e historial de despachos.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        marco = ttk.Frame(self.pestanas, padding=8)
        self.pestanas.add(marco, text="Pedidos")
        self._formulario(
            marco,
            "pedido",
            (
                ("id", "ID producto"),
                ("cantidad", "Cantidad"),
                ("urgencia", "Urgencia (0 normal, 1-9)"),
            ),
        )

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=4)
        ttk.Button(
            botones, text="Registrar pedido", command=self.registrar_pedido
        ).pack(side="left", padx=2)
        ttk.Button(
            botones, text="Despachar siguiente", command=self.despachar_siguiente
        ).pack(side="left", padx=2)
        ttk.Button(
            botones,
            text="Cargar pedidos CSV",
            command=lambda: self.pedir_csv("pedidos"),
        ).pack(side="left", padx=2)

        ttk.Label(
            marco,
            text="Pendientes en orden de despacho (urgentes primero, luego por llegada)",
        ).pack(anchor="w")
        self.tabla_pedidos = self._tabla(
            marco, ("Pedido", "Producto", "Cantidad", "Urgencia"), alto=6
        )
        ttk.Label(marco, text="Últimos 5 despachos (cola circular)").pack(anchor="w")
        self.tabla_historial = self._tabla(
            marco, ("Pedido", "Producto", "Cantidad", "Estado", "Detalle"), alto=5
        )

    def registrar_pedido(self) -> bool:
        """
        Encola un pedido nuevo.

        Complejidad:
            Tiempo: la de SistemaInventario.registrar_pedido.
            Espacio: O(1).
        """

        def accion() -> str:
            id_producto = self._entero("pedido", "id")
            texto = self._valor("pedido", "urgencia")
            urgencia = self._entero("pedido", "urgencia") if texto else 0
            pedido = self.sistema.registrar_pedido(
                id_producto, self._entero("pedido", "cantidad"), urgencia
            )

            if pedido is None:
                raise ValueError(f"No existe el producto {id_producto}.")

            return f"Pedido #{pedido.numero} en cola."

        return self._ejecutar(accion)

    def despachar_siguiente(self) -> bool:
        """
        Procesa el pedido más antiguo de la cola.

        Complejidad:
            Tiempo: la de SistemaInventario.despachar_siguiente.
            Espacio: O(k).
        """

        def accion() -> str:
            pedido = self.sistema.despachar_siguiente()

            if pedido is None:
                raise ValueError("No hay pedidos pendientes.")

            return str(pedido)

        return self._ejecutar(accion)

    # ---------- pestaña ruta ----------

    def _construir_ruta(self) -> None:
        """
        Arma la pestaña de ruta de recolección: calcula el recorrido de los
        próximos pedidos y permite despacharlos como una ola.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        marco = ttk.Frame(self.pestanas, padding=8)
        self.pestanas.add(marco, text="Ruta")
        self._formulario(marco, "ruta", (("cantidad", "Pedidos en la ola"),))
        self.vars["ruta"]["cantidad"].set("5")

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=4)
        ttk.Button(
            botones, text="Calcular ruta (sin despachar)", command=self.calcular_ruta
        ).pack(side="left", padx=2)
        ttk.Button(botones, text="Despachar ola", command=self.despachar_ola).pack(
            side="left", padx=2
        )

        ttk.Label(marco, textvariable=self.resumen_ruta).pack(anchor="w", pady=4)
        ttk.Label(
            marco, text="Orden de visita optimizado (sale y vuelve al muelle)"
        ).pack(anchor="w")
        self.tabla_ruta = self._tabla(marco, ("Visita", "Pasillo", "Estante"), alto=12)

    def _mostrar_ruta(self, ruta) -> None:
        """
        Muestra en la pestaña el resumen y el orden de visita de una ruta
        (o limpia la pestaña si no hay ruta).

        Complejidad:
            Tiempo: O(k) para k paradas.
            Espacio: O(k).
        """
        if ruta is None:
            self.resumen_ruta.set("No hay pedidos con producto existente.")
            self._llenar(self.tabla_ruta, [])
            return

        plano = self.sistema.plano()
        filas = []

        for i in range(len(ruta.orden_optimo)):
            pasillo, estante = plano.ubicacion_de(ruta.paradas[ruta.orden_optimo[i]])
            filas.append((i + 1, pasillo, estante))

        self._llenar(self.tabla_ruta, filas)
        self.resumen_ruta.set(
            f"Orden de llegada: {ruta.distancia_llegada} | "
            f"Optimizada: {ruta.distancia_optima} | "
            f"Ahorro: {ruta.ahorro:.1%}"
        )

    def calcular_ruta(self) -> bool:
        """
        Calcula y muestra la ruta de los próximos pedidos sin despacharlos.

        Complejidad:
            Tiempo: la de SistemaInventario.ruta_de_recoleccion.
            Espacio: O(V + k²).
        """

        def accion() -> str:
            ruta = self.sistema.ruta_de_recoleccion(self._entero("ruta", "cantidad"))
            self._mostrar_ruta(ruta)
            return "Ruta calculada."

        return self._ejecutar(accion)

    def despachar_ola(self) -> bool:
        """
        Despacha los próximos pedidos como una ola y muestra su ruta.

        Complejidad:
            Tiempo: la de SistemaInventario.despachar_ola.
            Espacio: O(V + k²).
        """

        def accion() -> str:
            resueltos, ruta = self.sistema.despachar_ola(
                self._entero("ruta", "cantidad")
            )

            if len(resueltos) == 0:
                raise ValueError("No hay pedidos pendientes.")

            self._mostrar_ruta(ruta)
            return f"Ola despachada: {len(resueltos)} pedidos."

        return self._ejecutar(accion)

    @staticmethod
    def _iterar(arreglo):
        """
        Recorre un ArregloDinamico como secuencia para armar las filas.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(1).
        """
        for i in range(len(arreglo)):
            yield arreglo[i]

    # ---------- pestaña devoluciones ----------

    def _construir_devoluciones(self) -> None:
        """
        Arma la pestaña de devoluciones: registrar y deshacer la última.

        Complejidad:
            Tiempo: O(1).
            Espacio: O(1).
        """
        marco = ttk.Frame(self.pestanas, padding=8)
        self.pestanas.add(marco, text="Devoluciones")
        self._formulario(
            marco,
            "devolucion",
            (
                ("id", "ID producto"),
                ("cantidad", "Cantidad"),
                ("fprod", "Producción AAAA-MM-DD"),
                ("fvenc", "Vencimiento AAAA-MM-DD"),
            ),
        )

        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=4)
        ttk.Button(
            botones, text="Registrar devolución", command=self.registrar_devolucion
        ).pack(side="left", padx=2)
        ttk.Button(
            botones, text="Deshacer la última", command=self.deshacer_devolucion
        ).pack(side="left", padx=2)

        ttk.Label(marco, text="Devoluciones (pila, la última queda arriba)").pack(
            anchor="w"
        )
        self.tabla_devoluciones = self._tabla(
            marco, ("N°", "Producto", "Lote", "Cantidad")
        )

    def registrar_devolucion(self) -> bool:
        """
        Registra una devolución como un lote nuevo y la apila.

        Complejidad:
            Tiempo: la de SistemaInventario.registrar_devolucion.
            Espacio: O(1).
        """

        def accion() -> str:
            id_producto = self._entero("devolucion", "id")
            devolucion = self.sistema.registrar_devolucion(
                id_producto,
                self._entero("devolucion", "cantidad"),
                self._valor("devolucion", "fprod"),
                self._valor("devolucion", "fvenc"),
            )

            if devolucion is None:
                raise ValueError(f"No existe el producto {id_producto}.")

            return str(devolucion)

        return self._ejecutar(accion)

    def deshacer_devolucion(self) -> bool:
        """
        Revierte la devolución más reciente.

        Complejidad:
            Tiempo: la de SistemaInventario.deshacer_ultima_devolucion.
            Espacio: O(1).
        """

        def accion() -> str:
            devolucion = self.sistema.deshacer_ultima_devolucion()

            if devolucion is None:
                raise ValueError("No hay devoluciones para deshacer.")

            return f"Devolución #{devolucion.numero} revertida."

        return self._ejecutar(accion)

    # ---------- CSV y refresco ----------

    def pedir_csv(self, tipo: str) -> bool:
        """
        Abre el selector de archivos y carga el CSV elegido.

        Complejidad:
            Tiempo: la de la carga elegida.
            Espacio: O(f) para f filas.
        """
        ruta = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])

        if not ruta:
            return False

        return self.cargar_csv(tipo, ruta)

    def cargar_csv(self, tipo: str, ruta: str) -> bool:
        """
        Carga productos, lotes o pedidos desde un CSV.

        Complejidad:
            Tiempo: la de cargar_csv, cargar_lotes_csv o cargar_pedidos_csv.
            Espacio: O(f) para f filas.
        """
        cargas = {
            "productos": self.sistema.cargar_csv,
            "lotes": self.sistema.cargar_lotes_csv,
            "pedidos": self.sistema.cargar_pedidos_csv,
        }

        def accion() -> str:
            return f"Se cargaron {cargas[tipo](ruta)} {tipo}."

        return self._ejecutar(accion)

    def refrescar(self) -> None:
        """
        Vuelve a dibujar todas las tablas desde el estado del sistema.

        Complejidad:
            Tiempo: O(n + p + h + d) en filas mostradas.
            Espacio: O(1) extra.
        """
        self._llenar(self.tabla_catalogo, self._filas_catalogo())
        self._llenar(self.tabla_lotes, self._filas_lotes())
        self._llenar(
            self.tabla_pedidos,
            [
                (p.numero, p.id_producto, p.cantidad, p.urgencia)
                for p in self._iterar(
                    self.sistema.siguientes_pedidos(self.sistema.total_pendientes())
                )
            ],
        )
        self._llenar(
            self.tabla_historial,
            [
                (p.numero, p.id_producto, p.cantidad, p.estado, self._detalle(p))
                for p in self.sistema.historial
            ],
        )
        self._llenar(
            self.tabla_devoluciones,
            [
                (d.numero, d.id_producto, d.codigo_lote, d.cantidad)
                for d in self.sistema.devoluciones
            ],
        )

    def _filas_catalogo(self) -> list[tuple]:
        """
        Filas de la tabla de catálogo, en el orden del catálogo.

        Complejidad:
            Tiempo: O(n).
            Espacio: O(n).
        """
        filas = []

        for i in range(len(self.sistema.catalogo)):
            p = self.sistema.catalogo[i]
            vence = (
                "sin existencias" if p.lotes.primero() is None else p.fecha_vencimiento
            )
            filas.append(
                (
                    p.id,
                    p.nombre,
                    p.categoria,
                    p.cantidad,
                    vence,
                    p.precio,
                    f"P{p.pasillo}-E{p.estante}",
                )
            )

        return filas

    def _filas_lotes(self) -> list[tuple]:
        """
        Filas de los lotes del producto escrito en la pestaña de lotes.

        Complejidad:
            Tiempo: O(n) por buscar, más O(l) por los lotes.
            Espacio: O(l).
        """
        try:
            producto = self.sistema.buscar_por_id(int(self._valor("lote", "id")))
        except ValueError:
            return []

        if producto is None:
            return []

        return [
            (lt.codigo, lt.cantidad, lt.fecha_produccion, lt.fecha_vencimiento)
            for lt in producto.lotes
        ]

    @staticmethod
    def _detalle(pedido) -> str:
        """
        Texto con los lotes usados (despachado) o el motivo (rechazado).

        Complejidad:
            Tiempo: O(k) para k tomas.
            Espacio: O(k).
        """
        if pedido.tomas is None:
            return pedido.motivo

        partes = []
        for i in range(len(pedido.tomas)):
            codigo, unidades = pedido.tomas[i]
            partes.append(f"{unidades} de {codigo}")

        return ", ".join(partes)

    @staticmethod
    def _llenar(tabla: ttk.Treeview, filas: list[tuple]) -> None:
        """
        Reemplaza el contenido de una tabla.

        Complejidad:
            Tiempo: O(f) para f filas.
            Espacio: O(1) extra.
        """
        for item in tabla.get_children():
            tabla.delete(item)

        for fila in filas:
            tabla.insert("", "end", values=fila)


def main() -> None:
    """
    Abre la base, muestra la ventana y guarda al cerrar.

    Complejidad:
        Tiempo: O(n) al cargar, luego depende de las acciones.
        Espacio: O(n).
    """
    repositorio = RepositorioSQLite(RUTA_DB)
    app = AplicacionInventario(repositorio.cargar(), repositorio)
    app.mainloop()
    repositorio.cerrar()


if __name__ == "__main__":
    main()
