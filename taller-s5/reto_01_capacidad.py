class ArregloDinamico:

    def __init__(self, capacidad=1):

        self.capacidad = capacidad
        self.tamano = 0
        self.datos = [None] * capacidad

        self.copias = 0
        self.redim = 0

    def __len__(self):
        return self.tamano

    def __getitem__(self, i):

        if not 0 <= i < self.tamano:
            raise IndexError("fuera de rango")

        return self.datos[i]

    # RETO 1:
    # Mostrar el tamaño, la capacidad y solamente
    # los elementos que están siendo usados.
    def __repr__(self):

        return (
            f"ArregloDinamico(tamano={self.tamano}, "
            f"capacidad={self.capacidad}, "
            f"datos={self.datos[:self.tamano]})"
        )

# EJECUCIÓN DEL RETO 1

print("\n" + "=" * 65)
print("RETO 1 - CAPACIDAD Y TAMAÑO")
print("=" * 65)

a = ArregloDinamico()

a.datos[0] = 10
a.tamano += 1

print(a)
