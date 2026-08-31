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

def eliminar_cuarto(self):

    if self.tamano == 0:
        raise IndexError("está vacío")

    self.tamano -= 1

    valor = self.datos[self.tamano]
    self.datos[self.tamano] = None

    # La regla del cuarto deja distancia entre crecer y encoger.
    if self.capacidad > 1 and self.tamano <= self.capacidad / 4:
        _redimensionar(self, self.capacidad // 2)

    return valor

ArregloDinamico._redimensionar = _redimensionar
ArregloDinamico.agregar = agregar
ArregloDinamico.eliminar_cuarto = eliminar_cuarto

# EJECUCIÓN DEL RETO 8

print("\n" + "=" * 65)
print("RETO 8 - REGLA DEL CUARTO")
print("=" * 65)

f = ArregloDinamico(1000)

for i in range(1000):
    f.agregar(i)

for i in range(20000):

    if i % 2 == 0:
        f.agregar(0)
    else:
        f.eliminar_cuarto()

print("Copias:", f.copias)
print("Copias por operación:", f.copias / 20000)
