class ArregloDinamico:

    def __init__(self, capacidad=1):

        self.capacidad = capacidad
        self.tamano = 0
        self.datos = [None] * capacidad

        self.copias = 0
        self.redim = 0

def _redimensionar(self, nueva_capacidad):

    nuevos = [None] * nueva_capacidad

    # Aquí está el costo: se copia uno por uno.
    for i in range(self.tamano):

        nuevos[i] = self.datos[i]
        self.copias += 1

    self.datos = nuevos
    self.capacidad = nueva_capacidad
    self.redim += 1

def agregar(self, valor):

    if self.tamano == self.capacidad:

        # Cuando está lleno, se duplica la capacidad.
        _redimensionar(self, self.capacidad * 2)

    self.datos[self.tamano] = valor
    self.tamano += 1

ArregloDinamico._redimensionar = _redimensionar
ArregloDinamico.agregar = agregar

# EJECUCIÓN DEL RETO 2

print("\n" + "=" * 65)
print("RETO 2 - AGREGAR Y REDIMENSIONAR")
print("=" * 65)

b = ArregloDinamico()

for i in range(100000):
    b.agregar(i)

print("Tamaño:", b.tamano)
print("Capacidad:", b.capacidad)
print("Copias:", b.copias)
print("Redimensionamientos:", b.redim)

assert b.tamano == 100000
assert b.capacidad == 131072
assert b.copias == 131071
assert b.redim == 17
