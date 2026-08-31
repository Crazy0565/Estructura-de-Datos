# IS061 - ESTRUCTURA DE DATOS
# SESIÓN 5 - EL ARREGLO DINÁMICO
# Archivo de entrega: taller_s05.py

import sys

# Se usa para permitir el QuickSort con pivote último sobre una lista ordenada.

sys.setrecursionlimit(5000)

# VÍA A - RETO 1
# CAPACIDAD Y TAMAÑO

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

# VÍA A - RETO 2
# REDIMENSIONAR Y AGREGAR

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

# VÍA A - RETO 3
# LAS TRES POLÍTICAS DE CRECIMIENTO

def simular_politica(n, politica):

    capacidad = 1
    tamano = 0
    copias = 0
    redim = 0

    for i in range(n):

        if tamano == capacidad:

            copias += tamano
            capacidad = politica(capacidad)
            redim += 1

        tamano += 1

    return copias, redim, capacidad

def politica_uno(capacidad):
    return capacidad + 1

def politica_diez(capacidad):
    return capacidad + 10

def politica_doble(capacidad):
    return capacidad * 2

# VÍA A - RETO 4
# COSTO AMORTIZADO

def agregar_con_costos(self, valor):

    costo = 1

    if self.tamano == self.capacidad:

        # Las copias más la escritura del elemento nuevo.
        costo += self.tamano
        _redimensionar(self, self.capacidad * 2)

    self.datos[self.tamano] = valor
    self.tamano += 1

    self.costos.append(costo)

# VÍA A - RETO 5
# COMPROBAR QUÉ HACE PYTHON

def capacidades_python():

    import sys

    base = sys.getsizeof([])
    lista = []
    previa = None
    secuencia = []

    for i in range(200):

        capacidad = (sys.getsizeof(lista) - base) // 8

        if capacidad != previa:

            secuencia.append((i, capacidad))
            previa = capacidad

        lista.append(i)

    return secuencia

# EJECUCIÓN DE LA VÍA A

print("\n" + "=" * 65)
print("VÍA A - EL ARREGLO DINÁMICO")
print("=" * 65)

# RETO 1 - REPRESENTACIÓN

print("\nRETO 1 - CAPACIDAD Y TAMAÑO")

a = ArregloDinamico()

a.agregar(10)
a.agregar(20)
a.agregar(30)

print(a)

assert repr(a) == (
    "ArregloDinamico(tamano=3, capacidad=4, datos=[10, 20, 30])"
)

# RETO 2 - AGREGAR Y REDIMENSIONAR

print("\nRETO 2 - AGREGAR Y REDIMENSIONAR")

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

# RETO 3 - LAS TRES POLÍTICAS

print("\nRETO 3 - LAS TRES POLÍTICAS")

politicas = [
    ("capacidad + 1", politica_uno),
    ("capacidad + 10", politica_diez),
    ("capacidad × 2", politica_doble)
]

print(
    f"\n{'Política':<20}"
    f"{'Copias':>18}"
    f"{'Redim.':>12}"
    f"{'Copias/inserción':>20}"
)

print("-" * 70)

resultados_politicas = {}

for nombre, funcion in politicas:

    copias, redim, capacidad = simular_politica(100000, funcion)

    copias_por_insercion = copias / 100000

    resultados_politicas[nombre] = (
        copias,
        redim,
        capacidad,
        copias_por_insercion
    )

    print(
        f"{nombre:<20}"
        f"{copias:>18,}"
        f"{redim:>12,}"
        f"{copias_por_insercion:>20,.5f}"
    )

assert resultados_politicas["capacidad + 1"][0] == 4999950000
assert resultados_politicas["capacidad + 10"][0] == 499960000
assert resultados_politicas["capacidad × 2"][0] == 131071

# Crecer de diez en diez hace menos redimensionamientos,
# pero sigue copiando cantidades que crecen con n.
# Por eso sigue siendo O(n²) en total.

# RETO 4 - COSTO AMORTIZADO

print("\nRETO 4 - COSTO AMORTIZADO")

c = ArregloDinamico()
c.costos = []

ArregloDinamico.agregar_con_costos = agregar_con_costos

for i in range(100000):
    c.agregar_con_costos(i)

maximo = max(c.costos)
promedio = sum(c.costos) / len(c.costos)

print("Costo máximo:", maximo)
print("Costo promedio:", promedio)

assert maximo == 65537
assert round(promedio, 5) == 2.31071

# El máximo puede ser muy grande porque una inserción
# puede obligar a copiar todo el arreglo.
# El promedio sigue siendo constante porque esas copias
# costosas ocurren solamente algunas veces.

# RETO 5 - CAPACIDADES DE PYTHON

print("\nRETO 5 - CAPACIDAD REAL DE PYTHON")

secuencia = capacidades_python()

for posicion, capacidad in secuencia:
    print(posicion, capacidad)

print("\nPython crece de forma proporcional, no duplicando exactamente.")

# Python no duplica exactamente su capacidad.
# Aun así, sigue teniendo costo O(1) amortizado porque
# el crecimiento es proporcional al tamaño actual.

# VÍA B - RETO 1
# ELIMINAR DEL FINAL

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

ArregloDinamico.eliminar = eliminar

print("\n" + "=" * 65)
print("VÍA B - ENCOGER, LOCALIDAD Y MEMORIA")
print("=" * 65)

# RETO 1 - ELIMINAR

print("\nRETO 1 - ELIMINAR")

d = ArregloDinamico()

for i in range(1000):
    d.agregar(i)

for i in range(1000):
    d.eliminar()

print("Tamaño final:", d.tamano)
print("Capacidad final:", d.capacidad)

assert d.tamano == 0
assert d.capacidad == 1

# VÍA B - RETO 2
# EFECTO ACORDEÓN

print("\nRETO 2 - EFECTO ACORDEÓN")

e = ArregloDinamico(1000)

for i in range(1000):
    e.agregar(i)

for i in range(20000):

    if i % 2 == 0:
        e.agregar(0)
    else:
        e.eliminar()

print("Copias:", e.copias)
print("Copias por operación:", e.copias / 20000)

# Con la regla de la mitad, añadir dispara el crecimiento
# y quitar dispara el encogimiento una y otra vez.
# Esto produce un costo lineal por operación en este caso.

# VÍA B - RETO 3
# REGLA DEL CUARTO

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

ArregloDinamico.eliminar_cuarto = eliminar_cuarto

print("\nRETO 3 - REGLA DEL CUARTO")

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

# Después de duplicar, el arreglo queda al 50 % de capacidad.
# Con la regla del cuarto hay que quitar aproximadamente
# la mitad de los elementos antes de volver a encoger.

# VÍA B - RETO 4
# LOCALIDAD DE REFERENCIA

def recorrer(datos, paso):

    import time

    t0 = time.perf_counter()
    total = 0

    for i in range(0, len(datos), paso):
        total += datos[i]

    dt = time.perf_counter() - t0

    return dt / (len(datos) / paso) * 1e9, total

print("\nRETO 4 - LOCALIDAD")

N = 4_000_000
datos = list(range(N))

for paso in (1, 16, 1024):

    tiempo, total = recorrer(datos, paso)

    print(
        f"Paso {paso:<4} | "
        f"{tiempo:.2f} ns por elemento"
    )

# Las tres versiones hacen la misma operación de suma.
# Sin embargo, recorrer seguido aprovecha mejor la localidad
# porque la memoria se trae en bloques y se aprovechan
# los datos vecinos.

# VÍA B - RETO 5
# QUÉ GUARDA DE VERDAD UNA LISTA

print("\nRETO 5 - MEMORIA")

import array

n = 1_000_000

lista = list(range(n))
arr = array.array("q", range(n))

# La lista guarda direcciones: hay que sumar el peso
# de cada entero por separado.
peso_lista = (
    sys.getsizeof(lista)
    + sum(sys.getsizeof(i) for i in lista)
)

memoria_lista = peso_lista / 1024 / 1024
memoria_array = sys.getsizeof(arr) / 1024 / 1024

print("lista ", round(memoria_lista, 1), "MB")
print("array ", round(memoria_array, 1), "MB")

tiempo_lista = None
tiempo_array = None

import time

t0 = time.perf_counter()
sum(lista)
tiempo_lista = time.perf_counter() - t0

t0 = time.perf_counter()
sum(arr)
tiempo_array = time.perf_counter() - t0

print("sum(lista):", tiempo_lista)
print("sum(array):", tiempo_array)

# La lista pesa más porque guarda direcciones de objetos.
# Cada entero de Python es un objeto independiente con
# su propia información adicional. array guarda los valores
# juntos y con un tamaño fijo.

# CONCLUSIÓN

print("\n" + "=" * 65)
print("CONCLUSIÓN")
print("=" * 65)

print("""
El arreglo dinámico mantiene separado el tamaño de la capacidad.
Al duplicar la capacidad, la mayoría de las inserciones cuestan
una sola operación, mientras que unas pocas deben copiar todo
el arreglo. Por eso agregar tiene costo O(1) amortizado.

Crecer de uno en uno o de diez en diez sigue produciendo un costo
total O(n²), porque el crecimiento es por una cantidad fija.

Para eliminar, la regla de la mitad puede producir el efecto
acordeón. La regla del cuarto deja suficiente distancia entre
el crecimiento y el encogimiento para mantener el costo amortizado.

La localidad de referencia explica por qué recorrer memoria de
forma seguida puede ser más rápido aunque se hagan las mismas
operaciones.

Finalmente, una lista de Python guarda referencias a objetos,
mientras que array y numpy pueden almacenar los valores de forma
más compacta.
""")

print("=" * 65)
print("TALLER FINALIZADO CORRECTAMENTE")
print("=" * 65)
