from arreglo import ArregloDinamico
from matriz import MatrizBodega
from producto import Producto


def mostrar_menu():
    """Muestra las opciones disponibles."""
    print("\n===== SISTEMA DE INVENTARIO =====")
    print("1. Agregar producto")
    print("2. Buscar producto por ID")
    print("3. Eliminar producto")
    print("4. Consultar ubicación")
    print("5. Mostrar información")
    print("6. Salir")


def agregar_producto(inventario, bodega):
    """Solicita los datos y agrega un producto."""
    id_producto = int(input("ID: "))
    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    cantidad = int(input("Cantidad: "))
    tiempo = int(input("Tiempo de producción (días): "))
    fecha_produccion = input("Fecha de producción (YYYY-MM-DD): ")
    fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
    precio = float(input("Precio: "))
    pasillo = int(input("Pasillo (0-99): "))
    estante = int(input("Estante (0-99): "))

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
        estante
    )

    inventario.agregar(producto)
    bodega.asignar(pasillo, estante, producto)

    print("Producto agregado correctamente.")


def buscar_producto(inventario):
    """Busca un producto mediante recorrido lineal."""
    id_producto = int(input("ID del producto: "))

    for i in range(len(inventario)):
        producto = inventario[i]

        if producto.id == id_producto:
            print("\nProducto encontrado:")
            print(producto)
            return

    print("Producto no encontrado.")


def eliminar_producto(inventario, bodega):
    """Elimina un producto del arreglo y de la bodega."""
    id_producto = int(input("ID del producto: "))

    for i in range(len(inventario)):
        producto = inventario[i]

        if producto.id == id_producto:
            bodega.eliminar(producto.pasillo, producto.estante)

            for j in range(i, len(inventario) - 1):
                inventario.datos[j] = inventario.datos[j + 1]

            inventario.datos[inventario.tamaño - 1] = None
            inventario.tamaño -= 1

            print("Producto eliminado correctamente.")
            return

    print("Producto no encontrado.")


def consultar_ubicacion(bodega):
    """Consulta un producto por su ubicación."""
    pasillo = int(input("Pasillo: "))
    estante = int(input("Estante: "))

    producto = bodega.obtener(pasillo, estante)

    if producto:
        print("\nProducto ubicado:")
        print(producto)
    else:
        print("No hay ningún producto en esa ubicación.")


def mostrar_informacion(inventario, bodega):
    """Muestra información general de las estructuras."""
    print("\n===== INFORMACIÓN =====")
    print(f"Productos almacenados: {len(inventario)}")
    print(f"Capacidad del arreglo: {inventario.capacidad}")
    print(f"Matriz de bodega: {bodega.filas}x{bodega.columnas}")
    print(f"Ubicaciones disponibles: {bodega.filas * bodega.columnas}")


def main():
    """Ejecuta el sistema de inventario."""
    inventario = ArregloDinamico()
    bodega = MatrizBodega()

    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto(inventario, bodega)

        elif opcion == "2":
            buscar_producto(inventario)

        elif opcion == "3":
            eliminar_producto(inventario, bodega)

        elif opcion == "4":
            consultar_ubicacion(bodega)

        elif opcion == "5":
            mostrar_informacion(inventario, bodega)

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()