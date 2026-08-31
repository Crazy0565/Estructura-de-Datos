class Agenda:
    """
    Representa una agenda de contactos.

    Los contactos se almacenan ordenados alfabéticamente
    por nombre.
    """

    def __init__(self):
        """
        Crea una agenda vacía.

        Complejidad: O(1)
        """
        self._contactos = []

    def __len__(self) -> int:
        """
        Devuelve la cantidad de contactos.

        Complejidad: O(1)
        """
        return len(self._contactos)

    def _buscar_posicion(self, nombre: str) -> int:
        """
        Busca mediante búsqueda binaria la posición de un nombre.

        Devuelve la posición donde está el nombre o donde debería
        insertarse si no existe.

        Complejidad: O(log n)
        """
        izquierda = 0
        derecha = len(self._contactos)

        while izquierda < derecha:
            medio = (izquierda + derecha) // 2

            if self._contactos[medio][0] < nombre:
                izquierda = medio + 1
            else:
                derecha = medio

        return izquierda

    def contiene(self, nombre: str) -> bool:
        """
        Indica si existe un contacto con el nombre dado.

        Complejidad: O(log n)
        """
        posicion = self._buscar_posicion(nombre)

        return (
            posicion < len(self._contactos)
            and self._contactos[posicion][0] == nombre
        )

    def telefono_de(self, nombre: str) -> str:
        """
        Devuelve el teléfono asociado a un nombre.

        Lanza KeyError si el nombre no existe.

        Complejidad: O(log n)
        """
        posicion = self._buscar_posicion(nombre)

        if (
            posicion >= len(self._contactos)
            or self._contactos[posicion][0] != nombre
        ):
            raise KeyError(nombre)

        return self._contactos[posicion][1]

    def nombres(self) -> list[str]:
        """
        Devuelve los nombres ordenados alfabéticamente.

        Complejidad: O(n)
        """
        return [contacto[0] for contacto in self._contactos]

    def agregar(self, nombre: str, telefono: str) -> None:
        """
        Agrega un contacto o actualiza su teléfono si ya existe.

        Lanza ValueError si el nombre está vacío.

        Complejidad: O(n)
        """
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")

        posicion = self._buscar_posicion(nombre)

        if (
            posicion < len(self._contactos)
            and self._contactos[posicion][0] == nombre
        ):
            self._contactos[posicion] = (nombre, telefono)
        else:
            self._contactos.insert(posicion, (nombre, telefono))

    def eliminar(self, nombre: str) -> None:
        """
        Elimina un contacto.

        Lanza KeyError si el nombre no existe.

        Complejidad: O(n)
        """
        posicion = self._buscar_posicion(nombre)

        if (
            posicion >= len(self._contactos)
            or self._contactos[posicion][0] != nombre
        ):
            raise KeyError(nombre)

        self._contactos.pop(posicion)
