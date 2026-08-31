class ArregloDinamico:

    def __init__(self, capacidad=1):

        self.capacidad = capacidad
        self.tamano = 0
        self.datos = [None] * capacidad

        self.copias = 0
        self.redim = 0
        self.costos = []

def _redimensionar(self, nueva_capacidad):

    nuevos = [None] * nueva_capacidad

    # Aquí está el costo: se copia uno por uno.
    for i in range(self.tamano):

        nuevos[i] = self.datos[i]
        self.copias += 1

    self.datos = nuevos
    self.capacidad = nueva_capacidad
    self.redim += 1

def agregar_con_costos(self, valor):

    costo = 1

    if self.tamano == self.capacidad:

        # Las copias más la escritura del elemento nuevo.
        costo += self.tamano
        _redimensionar(self, self.capacidad * 2)

    self.datos[self.tamano] = valor
    self.tamano += 1

    self.costos.append(costo)

ArregloDinamico._redimensionar = _redimensionar
ArregloDinamico.agregar_con_costos = agregar_con_costos

# EJECUCIÓN DEL RETO 4

print("\n" + "=" * 65)
print("RETO 4 - COSTO AMORTIZADO")
print("=" * 65)

c = ArregloDinamico()

for i in range(100000):
    c.agregar_con_costos(i)

maximo = max(c.costos)
promedio = sum(c.costos) / len(c.costos)

print("Costo máximo:", maximo)
print("Costo promedio:", promedio)

assert maximo == 65537
assert round(promedio, 5) == 2.31071

print("\nReto terminado correctamente.")
