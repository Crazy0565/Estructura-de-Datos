import random
import string
import time

from agenda import Agenda


random.seed(11)


def generar_nombre() -> str:
    """Genera un nombre aleatorio de 10 letras."""
    return "".join(random.choices(string.ascii_letters, k=10))


def crear_agenda(cantidad: int) -> tuple[Agenda, list[str]]:
    """
    Crea una agenda con la cantidad indicada de contactos.

    Devuelve la agenda y la lista de nombres utilizados.
    """
    agenda = Agenda()
    nombres = set()

    while len(nombres) < cantidad:
        nombres.add(generar_nombre())

    nombres = list(nombres)

    for nombre in nombres:
        agenda.agregar(nombre, "3000000000")

    return agenda, nombres


def medir_contiene(
    agenda: Agenda,
    nombre: str,
    repeticiones: int = 1000
) -> float:
    """Mide el tiempo de contiene()."""

    mejor = float("inf")

    for _ in range(repeticiones):
        inicio = time.perf_counter()

        agenda.contiene(nombre)

        fin = time.perf_counter()

        tiempo = fin - inicio

        if tiempo < mejor:
            mejor = tiempo

    return mejor


def medir_busqueda_ingenua(
    nombres: list[str],
    nombre: str,
    repeticiones: int = 1000
) -> float:
    """
    Mide una búsqueda secuencial ingenua.

    No utiliza el operador 'in'.
    """

    mejor = float("inf")

    for _ in range(repeticiones):
        inicio = time.perf_counter()

        encontrado = False

        for elemento in nombres:
            if elemento == nombre:
                encontrado = True
                break

        fin = time.perf_counter()

        tiempo = fin - inicio

        if tiempo < mejor:
            mejor = tiempo

    return mejor


def medir_agregar_eliminar(
    agenda: Agenda,
    nombre: str,
    repeticiones: int = 100
) -> float:
    """
    Mide conjuntamente agregar() y eliminar().
    """

    mejor = float("inf")

    for _ in range(repeticiones):
        inicio = time.perf_counter()

        agenda.agregar(nombre, "3000000000")
        agenda.eliminar(nombre)

        fin = time.perf_counter()

        tiempo = fin - inicio

        if tiempo < mejor:
            mejor = tiempo

    return mejor


def main():
    tamaños = [1000, 10000, 100000]

    print(
        "Tamaño | contiene | búsqueda ingenua | agregar + eliminar"
    )
    print("-" * 65)

    for cantidad in tamaños:

        # Crear la agenda.
        agenda, _ = crear_agenda(cantidad)

        # Obtener nombres una sola vez, fuera de las mediciones.
        nombres = agenda.nombres()

        # Este nombre no está en la agenda.
        nombre_buscar = "!" + "A" * 9

        # Medir contiene().
        tiempo_contiene = medir_contiene(
            agenda,
            nombre_buscar
        )

        # Medir búsqueda ingenua.
        tiempo_ingenua = medir_busqueda_ingenua(
            nombres,
            nombre_buscar
        )

        # Medir agregar() + eliminar().
        tiempo_agregar_eliminar = medir_agregar_eliminar(
            agenda,
            nombre_buscar
        )

        print(
            f"{cantidad:6d} | "
            f"{tiempo_contiene:.9f} | "
            f"{tiempo_ingenua:.9f} | "
            f"{tiempo_agregar_eliminar:.9f}"
        )


if __name__ == "__main__":
    main()
