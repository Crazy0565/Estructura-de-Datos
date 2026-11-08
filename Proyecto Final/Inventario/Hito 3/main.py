from persistencia import RepositorioSQLite
from producto import Producto
from sistema import CRITERIOS_ORDEN, SistemaInventario

RUTA_PRODUCTOS = "productos.csv"
RUTA_LOTES = "lotes.csv"
RUTA_PEDIDOS = "pedidos.csv"

RUTA_DB = "inventario.db"


def mostrar_menu() -> None:
    """
    Muestra las opciones disponibles.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    print("\n===== SISTEMA DE INVENTARIO =====")
    print("-- Catálogo --")
    print("1. Agregar producto")
    print("2. Buscar producto por ID")
    print("3. Eliminar producto")
    print("4. Consultar ubicación")
    print("5. Mostrar información")
    print("6. Cargar productos desde CSV")
    print("7. Ordenar catálogo")
    print("8. Listar catálogo")
    print("-- Lotes --")
    print("9. Registrar lote de un producto")
    print("10. Ver lotes de un producto")
    print("11. Despachar unidades (primero el lote que vence antes)")
    print("12. Cargar lotes desde CSV")
    print("-- Pedidos --")
    print("13. Registrar pedido")
    print("14. Despachar siguiente pedido")
    print("15. Ver pedidos pendientes")
    print("16. Ver últimos despachos")
    print("17. Cargar pedidos desde CSV")
    print("-- Devoluciones --")
    print("18. Registrar devolución")
    print("19. Deshacer última devolución")
    print("0. Salir")


def leer_entero(mensaje: str) -> int:
    """
    Pide un número entero y repite la pregunta hasta recibir uno válido.

    Complejidad:
        Tiempo: O(1) por intento.
        Espacio: O(1).
    """
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def leer_decimal(mensaje: str) -> float:
    """
    Pide un número decimal y repite la pregunta hasta recibir uno válido.

    Complejidad:
        Tiempo: O(1) por intento.
        Espacio: O(1).
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número.")


def agregar_producto(sistema: SistemaInventario) -> None:
    """
    Solicita los datos de un producto y lo agrega al sistema.

    Complejidad:
        Tiempo: O(1) amortizado.
        Espacio: O(1).
    """
    id_producto = leer_entero("ID: ")
    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    cantidad = leer_entero("Cantidad: ")
    tiempo = leer_entero("Tiempo de producción (días): ")
    fecha_produccion = input("Fecha de producción (YYYY-MM-DD): ")
    fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
    precio = leer_decimal("Precio: ")
    pasillo = leer_entero("Pasillo: ")
    estante = leer_entero("Estante: ")

    try:
        producto = Producto(
            id_producto,
            nombre,
            categoria,
            cantidad,
            tiempo,
            fecha_produccion,
            fecha_vencimiento,
            precio,
            pasillo,
            estante,
        )
        sistema.agregar(producto)
    except (ValueError, IndexError) as error:
        print(f"No se pudo agregar el producto: {error}")
        return

    print("Producto agregado correctamente.")


def buscar_producto(sistema: SistemaInventario) -> None:
    """
    Busca un producto por ID y lo muestra.

    Complejidad:
        Tiempo: O(log n) si el catálogo está ordenado por ID, O(n) si no.
        Espacio: O(1).
    """
    producto = sistema.buscar_por_id(leer_entero("ID del producto: "))

    if producto is None:
        print("Producto no encontrado.")
        return

    metodo = "binaria" if sistema.ordenado_por_id else "lineal"
    print(f"\nProducto encontrado (búsqueda {metodo}):")
    print(producto)


def eliminar_producto(sistema: SistemaInventario) -> None:
    """
    Elimina un producto por ID.

    Complejidad:
        Tiempo: O(n).
        Espacio: O(1).
    """
    producto = sistema.eliminar_por_id(leer_entero("ID del producto: "))

    if producto is None:
        print("Producto no encontrado.")
        return

    print("Producto eliminado correctamente.")


def consultar_ubicacion(sistema: SistemaInventario) -> None:
    """
    Muestra qué producto ocupa un pasillo y estante.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    pasillo = leer_entero("Pasillo: ")
    estante = leer_entero("Estante: ")

    try:
        producto = sistema.consultar_ubicacion(pasillo, estante)
    except IndexError:
        print("Esa ubicación está fuera de la bodega.")
        return

    if producto is None:
        print("No hay ningún producto en esa ubicación.")
        return

    print("\nProducto ubicado:")
    print(producto)


def mostrar_informacion(sistema: SistemaInventario) -> None:
    """
    Muestra información general de las estructuras.

    Complejidad:
        Tiempo: O(1).
        Espacio: O(1).
    """
    tamaño = sistema.bodega.tamaño

    print("\n===== INFORMACIÓN =====")
    print(f"Productos almacenados: {len(sistema.catalogo)}")
    print(f"Capacidad del arreglo: {sistema.catalogo.capacidad}")
    print(f"Matriz de bodega: {tamaño}x{tamaño}")
    print(f"Ubicaciones libres: {sistema.ubicaciones_libres()}")
    print(f"Pedidos pendientes: {sistema.total_pendientes()}")
    print(f"Devoluciones que se pueden revertir: {len(sistema.devoluciones)}")


def cargar_datos(sistema: SistemaInventario) -> None:
    """
    Carga el catálogo desde el archivo CSV.

    Complejidad:
        Tiempo: O(n) con n filas.
        Espacio: O(n).
    """
    try:
        cantidad = sistema.cargar_csv(RUTA_PRODUCTOS)
    except FileNotFoundError:
        print(f"No se encontró el archivo {RUTA_PRODUCTOS}.")
        return
    except (ValueError, KeyError) as error:
        print(f"No se pudo cargar el archivo: {error}")
        return

    print(f"Se cargaron {cantidad} productos correctamente.")


def ordenar_catalogo(sistema: SistemaInventario) -> None:
    """
    Reordena el catálogo con QuickSort según el criterio elegido.

    Complejidad:
        Tiempo: O(n log n) en promedio.
        Espacio: O(n).
    """
    print("Criterios disponibles:")

    for numero, criterio in enumerate(CRITERIOS_ORDEN, start=1):
        print(f"{numero}. {criterio}")

    eleccion = leer_entero("Criterio: ")

    if eleccion < 1 or eleccion > len(CRITERIOS_ORDEN):
        print("Criterio inválido.")
        return

    criterio = CRITERIOS_ORDEN[eleccion - 1]
    sistema.ordenar(criterio)
    print(f"Catálogo ordenado por {criterio}.")


def listar_catalogo(sistema: SistemaInventario) -> None:
    """
    Muestra todos los productos en el orden actual del catálogo.

    Complejidad:
        Tiempo: O(n).
        Espacio: O(1).
    """
    if len(sistema.catalogo) == 0:
        print("El catálogo está vacío.")
        return

    for i in range(len(sistema.catalogo)):
        print(sistema.catalogo[i])


def registrar_lote(sistema: SistemaInventario) -> None:
    """
    Registra un lote nuevo en un producto existente.

    Complejidad:
        Tiempo: O(n + l) con n productos y l lotes del producto.
        Espacio: O(1).
    """
    id_producto = leer_entero("ID del producto: ")
    codigo = input("Código del lote: ")
    cantidad = leer_entero("Cantidad: ")
    fecha_produccion = input("Fecha de producción (YYYY-MM-DD): ")
    fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")

    try:
        lote = sistema.registrar_lote(
            id_producto, codigo, cantidad, fecha_produccion, fecha_vencimiento
        )
    except ValueError as error:
        print(f"No se pudo registrar el lote: {error}")
        return

    if lote is None:
        print("Producto no encontrado.")
        return

    print("Lote registrado correctamente.")


def ver_lotes(sistema: SistemaInventario) -> None:
    """
    Muestra los lotes de un producto, del que vence antes al que vence después.

    Complejidad:
        Tiempo: O(n + l).
        Espacio: O(1).
    """
    producto = sistema.buscar_por_id(leer_entero("ID del producto: "))

    if producto is None:
        print("Producto no encontrado.")
        return

    print(f"\nLotes de {producto.nombre}:")

    if len(producto.lotes) == 0:
        print("  Sin lotes.")
        return

    for lote in producto.lotes:
        print(f"  {lote}")

    print(f"Total disponible: {producto.cantidad} unidades")


def despachar_unidades(sistema: SistemaInventario) -> None:
    """
    Despacha unidades de un producto tomando primero el lote que vence antes.

    Complejidad:
        Tiempo: O(n + k) con k lotes tocados.
        Espacio: O(k).
    """
    id_producto = leer_entero("ID del producto: ")
    cantidad = leer_entero("Unidades a despachar: ")

    try:
        tomas = sistema.despachar_producto(id_producto, cantidad)
    except ValueError as error:
        print(f"No se pudo despachar: {error}")
        return

    if tomas is None:
        print("Producto no encontrado.")
        return

    print("Despacho realizado:")

    for i in range(len(tomas)):
        codigo, unidades = tomas[i]
        print(f"  {unidades} unidades del lote {codigo}")


def cargar_lotes(sistema: SistemaInventario) -> None:
    """
    Carga un embarque de lotes desde el archivo CSV.

    Complejidad:
        Tiempo: O(f * (l + p)) para f filas.
        Espacio: O(f).
    """
    try:
        cantidad = sistema.cargar_lotes_csv(RUTA_LOTES)
    except FileNotFoundError:
        print(f"No se encontró el archivo {RUTA_LOTES}.")
        return
    except (ValueError, KeyError) as error:
        print(f"No se pudo cargar el archivo: {error}")
        return

    print(f"Se cargaron {cantidad} lotes correctamente.")


def registrar_pedido(sistema: SistemaInventario) -> None:
    """
    Registra un pedido al final de la cola de pendientes.

    Complejidad:
        Tiempo: O(n) por la búsqueda del producto.
        Espacio: O(1).
    """
    id_producto = leer_entero("ID del producto: ")
    cantidad = leer_entero("Cantidad: ")

    try:
        pedido = sistema.registrar_pedido(id_producto, cantidad)
    except ValueError as error:
        print(f"No se pudo registrar el pedido: {error}")
        return

    if pedido is None:
        print("Producto no encontrado.")
        return

    print(
        f"Pedido #{pedido.numero} registrado. En espera: {sistema.total_pendientes()}."
    )


def despachar_siguiente_pedido(sistema: SistemaInventario) -> None:
    """
    Procesa el pedido más antiguo y muestra cómo quedó.

    Complejidad:
        Tiempo: O(n + k) con k lotes tocados.
        Espacio: O(k).
    """
    pedido = sistema.despachar_siguiente()

    if pedido is None:
        print("No hay pedidos pendientes.")
        return

    print(pedido)

    if pedido.tomas is None:
        return

    for i in range(len(pedido.tomas)):
        codigo, unidades = pedido.tomas[i]
        print(f"  {unidades} unidades del lote {codigo}")


def ver_pedidos(sistema: SistemaInventario) -> None:
    """
    Muestra los pedidos pendientes en el orden de despacho: urgentes primero,
    luego del más antiguo al más reciente.

    Complejidad:
        Tiempo: O(p) con p pedidos pendientes.
        Espacio: O(1).
    """
    if sistema.total_pendientes() == 0:
        print("No hay pedidos pendientes.")
        return

    print("\nPedidos pendientes (el primero se atiende antes):")
    pendientes = sistema.siguientes_pedidos(sistema.total_pendientes())

    for i in range(len(pendientes)):
        pedido = pendientes[i]
        marca = f" [urgencia {pedido.urgencia}]" if pedido.urgencia else ""
        print(f"  {pedido}{marca}")


def ver_historial(sistema: SistemaInventario) -> None:
    """
    Muestra los últimos pedidos resueltos, del más antiguo al más reciente.

    Complejidad:
        Tiempo: O(h) con h la capacidad del historial.
        Espacio: O(1).
    """
    if sistema.historial.esta_vacia():
        print("Todavía no hay despachos.")
        return

    print(f"\nÚltimos despachos (máximo {sistema.historial.capacidad}):")

    for pedido in sistema.historial:
        print(f"  {pedido}")


def cargar_pedidos(sistema: SistemaInventario) -> None:
    """
    Carga pedidos desde el archivo CSV y los encola en orden.

    Complejidad:
        Tiempo: O(f * n) para f filas.
        Espacio: O(f).
    """
    try:
        cantidad = sistema.cargar_pedidos_csv(RUTA_PEDIDOS)
    except FileNotFoundError:
        print(f"No se encontró el archivo {RUTA_PEDIDOS}.")
        return
    except (ValueError, KeyError) as error:
        print(f"No se pudo cargar el archivo: {error}")
        return

    print(f"Se cargaron {cantidad} pedidos correctamente.")


def registrar_devolucion(sistema: SistemaInventario) -> None:
    """
    Registra unidades devueltas como un lote nuevo del producto.

    Complejidad:
        Tiempo: O(n + l) con l lotes del producto.
        Espacio: O(1).
    """
    id_producto = leer_entero("ID del producto: ")
    cantidad = leer_entero("Cantidad devuelta: ")
    fecha_produccion = input("Fecha de producción (YYYY-MM-DD): ")
    fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")

    try:
        devolucion = sistema.registrar_devolucion(
            id_producto, cantidad, fecha_produccion, fecha_vencimiento
        )
    except ValueError as error:
        print(f"No se pudo registrar la devolución: {error}")
        return

    if devolucion is None:
        print("Producto no encontrado.")
        return

    print(
        f"Devolución #{devolucion.numero} registrada "
        f"como lote {devolucion.codigo_lote}."
    )


def deshacer_devolucion(sistema: SistemaInventario) -> None:
    """
    Revierte la devolución más reciente.

    Complejidad:
        Tiempo: O(n + l).
        Espacio: O(1).
    """
    try:
        devolucion = sistema.deshacer_ultima_devolucion()
    except ValueError as error:
        print(f"No se pudo revertir: {error}")
        return

    if devolucion is None:
        print("No hay devoluciones para deshacer.")
        return

    print(
        f"Devolución #{devolucion.numero} revertida "
        f"(lote {devolucion.codigo_lote} retirado)."
    )


def main() -> None:
    """
    Ejecuta el menú del sistema de inventario.

    Complejidad:
        Tiempo: depende de la opción elegida en cada iteración.
        Espacio: O(n) por el catálogo.
    """
    repositorio = RepositorioSQLite(RUTA_DB)
    sistema = repositorio.cargar()

    if len(sistema.catalogo) > 0:
        print(f"Se recuperaron {len(sistema.catalogo)} productos de {RUTA_DB}.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto(sistema)
        elif opcion == "2":
            buscar_producto(sistema)
        elif opcion == "3":
            eliminar_producto(sistema)
        elif opcion == "4":
            consultar_ubicacion(sistema)
        elif opcion == "5":
            mostrar_informacion(sistema)
        elif opcion == "6":
            cargar_datos(sistema)
        elif opcion == "7":
            ordenar_catalogo(sistema)
        elif opcion == "8":
            listar_catalogo(sistema)
        elif opcion == "9":
            registrar_lote(sistema)
        elif opcion == "10":
            ver_lotes(sistema)
        elif opcion == "11":
            despachar_unidades(sistema)
        elif opcion == "12":
            cargar_lotes(sistema)
        elif opcion == "13":
            registrar_pedido(sistema)
        elif opcion == "14":
            despachar_siguiente_pedido(sistema)
        elif opcion == "15":
            ver_pedidos(sistema)
        elif opcion == "16":
            ver_historial(sistema)
        elif opcion == "17":
            cargar_pedidos(sistema)
        elif opcion == "18":
            registrar_devolucion(sistema)
        elif opcion == "19":
            deshacer_devolucion(sistema)
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

        repositorio.guardar(sistema)

    repositorio.guardar(sistema)
    repositorio.cerrar()


if __name__ == "__main__":
    main()
