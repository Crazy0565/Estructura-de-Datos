class ArregloDinamico:

    def __init__(self, capacidad=1):

        self.capacidad = capacidad
        self.tamano = 0
        self.datos = [None] * capacidad

        self.copias = 0
        self.redim = 0

def _redimensionar(self, nueva_capacidad):

    nuevos = [None] * nueva_capacidad

    for i in range(self.tamano):

        nuevos[i] = self.datos[i]
        self.copias += 1

    self.datos = nuevos
    self.capacidad = nueva_capacidad
    self.redim += 1

def agregar(self, valor):

    if self.tamano == self.capacidad:

        _redimensionar(self, self.capacidad * 2)

    self.datos[self.tamano] = valor
    self.tamano += 1

def eliminar(self):

    if self.tamano == 0:
        raise IndexError("está vacío")

    self.tamano -= 1

    valor = self.datos[self.tamano]
    self.datos[self.tamano] = None

    # La regla inicial: encoger al bajar de la mitad.
    if self.capacidad > 1 and self.tamano <= self.capacidad / 2:
        _redimensionar(self, self.capacidad // 2)

    return valor

ArregloDinamico._redimensionar = _redimensionar
ArregloDinamico.agregar = agregar
ArregloDinamico.eliminar = eliminar

# EJECUCIÓN DEL RETO 6

print("\n" + "=" * 65)
print("RETO 6 - ELIMINAR")
print("=" * 65)

d = ArregloDinamico()

for i in range(1000):
    d.agregar(i)

for i in range(1000):
    d.eliminar()

print("Tamaño final:", d.tamano)
print("Capacidad final:", d.capacidad)

assert d.tamano == 0
assert d.capacidad == 1

print("\nReto terminado correctamente.")
