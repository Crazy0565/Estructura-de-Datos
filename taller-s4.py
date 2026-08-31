# IS061 - ESTRUCTURA DE DATOS
# SESIÓN 4 - ORDENAR Y BUSCAR
# Archivo de entrega: taller_s4.py

import random
import math
import sys

# Se usa para QuickSort con pivotesobre la lista ordenada
sys.setrecursionlimit(5000)


# PREPARACIÓN DE LAS TRES LISTAS

random.seed(11)
N = 1000

aleatoria = [random.randint(1, 9999) for _ in range(N)]
ordenada = sorted(aleatoria)
al_reves = ordenada[::-1]

print("=" * 65)
print("PREPARACIÓN DE DATOS")
print("=" * 65)
print(aleatoria[:5])

assert aleatoria[:5] == [7412, 9172, 7630, 7403, 8321]


# VÍA A - RETO 1 Y RETO 2
# BURBUJA CON CONTADORES Y BANDERA

def burbuja(a):
    a = list(a)

    n = len(a)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):

        hubo_cambio = False

        for j in range(n - 1 - i):

            comparaciones += 1

            if a[j] > a[j + 1]:

                a[j], a[j + 1] = a[j + 1], a[j]

                intercambios += 1
                hubo_cambio = True

        # RETO 2:
        # Si no hubo intercambios, la lista ya está ordenada.
        if not hubo_cambio:
            break

    return a, comparaciones, intercambios

# VÍA A - RETO 3
# SELECCIÓN

def seleccion(a):
    a = list(a)

    n = len(a)
    comparaciones = 0
    intercambios = 0

    for i in range(n - 1):

        menor = i

        for j in range(i + 1, n):

            comparaciones += 1

            if a[j] < a[menor]:
                menor = j

        # El intercambio debe estar FUERA del ciclo interno.
        if menor != i:

            a[i], a[menor] = a[menor], a[i]

            intercambios += 1

    return a, comparaciones, intercambios

# VÍA A - RETO 4
# INSERCIÓN

def insercion(a):
    a = list(a)

    comparaciones = 0
    movimientos = 0

    for i in range(1, len(a)):

        actual = a[i]
        j = i - 1

        while j >= 0:

            comparaciones += 1

            if a[j] > actual:

                a[j + 1] = a[j]

                movimientos += 1

                j -= 1

            else:
                break

        a[j + 1] = actual
        movimientos += 1

    return a, comparaciones, movimientos

# VÍA A - EJECUCIÓN Y ASSERTS

print("\n" + "=" * 65)
print("VÍA A - RETOS 1 AL 6")
print("=" * 65)

escenarios = [
    ("Aleatoria", aleatoria),
    ("Ordenada", ordenada),
    ("Al revés", al_reves)
]

algoritmos_a = [
    ("Burbuja", burbuja),
    ("Selección", seleccion),
    ("Inserción", insercion)
]

resultados_a = {}

print(
    f"\n{'Algoritmo':<15}"
    f"{'Escenario':<15}"
    f"{'Comparaciones':>18}"
    f"{'Movimientos':>18}"
)

print("-" * 66)

for nombre, funcion in algoritmos_a:

    resultados_a[nombre] = {}

    for nombre_escenario, lista in escenarios:

        salida, comparaciones, movimientos = funcion(lista)

        assert salida == ordenada

        resultados_a[nombre][nombre_escenario] = (
            comparaciones,
            movimientos
        )

        print(
            f"{nombre:<15}"
            f"{nombre_escenario:<15}"
            f"{comparaciones:>18,}"
            f"{movimientos:>18,}"
        )


# Comprobaciones específicas

assert resultados_a["Burbuja"]["Ordenada"][0] == 999

assert resultados_a["Selección"]["Aleatoria"][0] == 499500
assert resultados_a["Selección"]["Ordenada"][0] == 499500
assert resultados_a["Selección"]["Al revés"][0] == 499500

assert resultados_a["Inserción"]["Aleatoria"][0] == 241994

# VÍA A - RETO 5
# TABLA DE NUEVE CASILLAS EN CONSOLA

print("\n" + "=" * 65)
print("RETO 5 - TABLA DE NUEVE CASILLAS")
print("=" * 65)

print(
    f"\n{'Algoritmo':<15}"
    f"{'Aleatoria':>15}"
    f"{'Ordenada':>15}"
    f"{'Al revés':>15}"
)

print("-" * 60)

for nombre in resultados_a:

    ale = resultados_a[nombre]["Aleatoria"][0]
    ord_ = resultados_a[nombre]["Ordenada"][0]
    rev = resultados_a[nombre]["Al revés"][0]

    print(
        f"{nombre:<15}"
        f"{ale:>15,}"
        f"{ord_:>15,}"
        f"{rev:>15,}"
    )

# VÍA A - RETO 6
# COMPARACIONES VS MOVIMIENTOS

print("\n" + "=" * 65)
print("RETO 6 - COMPARACIONES Y MOVIMIENTOS")
print("=" * 65)

for nombre in resultados_a:

    comparaciones, movimientos = (
        resultados_a[nombre]["Aleatoria"]
    )

    print(
        f"{nombre}: "
        f"{comparaciones:,} comparaciones | "
        f"{movimientos:,} movimientos"
    )

# VÍA B - RETO 1
# FUSIONAR DOS LISTAS ORDENADAS

def fusionar(iz, de):

    resultado = []

    i = 0
    j = 0

    comparaciones = 0

    while i < len(iz) and j < len(de):

        comparaciones += 1

        if iz[i] <= de[j]:

            resultado.append(iz[i])
            i += 1

        else:

            resultado.append(de[j])
            j += 1

    # Agregar lo que quede.
    resultado.extend(iz[i:])
    resultado.extend(de[j:])

    return resultado, comparaciones


# Prueba oficial del reto 1

prueba_fusion, comp_fusion = fusionar(
    [1, 4, 7],
    [2, 3, 9]
)

assert prueba_fusion == [1, 2, 3, 4, 7, 9]
assert comp_fusion == 5

# VÍA B - RETO 2
# MERGE SORT / MEZCLA

def mezcla(a):

    if len(a) <= 1:
        return list(a), 0

    mitad = len(a) // 2

    izquierda, c1 = mezcla(a[:mitad])
    derecha, c2 = mezcla(a[mitad:])

    juntas, c3 = fusionar(izquierda, derecha)

    return juntas, c1 + c2 + c3

# VÍA B - RETO 3
# QUICK SORT / RÁPIDA

def rapida(a, modo="medio"):

    if len(a) <= 1:
        return list(a), 0

    if modo == "medio":

        k = len(a) // 2

    elif modo == "ultimo":

        k = len(a) - 1

    else:

        raise ValueError(
            "modo debe ser 'medio' o 'ultimo'"
        )

    pivote = a[k]

    resto = a[:k] + a[k + 1:]

    menores = []
    mayores = []

    comparaciones = 0

    for v in resto:

        comparaciones += 1

        if v < pivote:
            menores.append(v)
        else:
            mayores.append(v)

    iz, c1 = rapida(menores, modo)
    de, c2 = rapida(mayores, modo)

    return (
        iz + [pivote] + de,
        comparaciones + c1 + c2
    )

# VÍA B - RETO 4
# BÚSQUEDA BINARIA

def binaria(a, x):

    lo = 0
    hi = len(a) - 1

    pasos = 0

    while lo <= hi:

        pasos += 1

        mitad = (lo + hi) // 2

        if a[mitad] == x:
            return mitad, pasos

        elif a[mitad] < x:
            lo = mitad + 1

        else:
            hi = mitad - 1

    return -1, pasos

# VÍA B - RETO 5
# PUNTO DE EQUILIBRIO

def equilibrio(n):

    costo_ordenar = n * math.log2(n)

    k = 1

    while True:

        sin_ordenar = k * n / 2

        con_orden = (
            costo_ordenar
            + k * math.log2(n)
        )

        if con_orden < sin_ordenar:
            return k

        k += 1

# EJECUCIÓN DE LA VÍA B

print("\n" + "=" * 65)
print("VÍA B - RETOS 1 AL 5")
print("=" * 65)

# RETO 1 - FUSIONAR

print("\nRETO 1 - FUSIONAR")
print("Resultado:", prueba_fusion)
print("Comparaciones:", comp_fusion)

# RETO 2 - MEZCLA

print("\nRETO 2 - MEZCLA")

salida_mezcla, comp_mezcla = mezcla(aleatoria)

assert salida_mezcla == ordenada
assert comp_mezcla == 8720

print("Comparaciones:", comp_mezcla)


# RETO 3 - QUICK SORT
# LOS CUATRO CASOS PEDIDOS

print("\nRETO 3 - RÁPIDA / QUICKSORT")


# Pivote medio - lista aleatoria

salida_medio_aleatoria, comp_medio_aleatoria = rapida(
    aleatoria,
    "medio"
)

assert salida_medio_aleatoria == ordenada

# Pivote último - lista aleatoria

salida_ultimo_aleatoria, comp_ultimo_aleatoria = rapida(
    aleatoria,
    "ultimo"
)

assert salida_ultimo_aleatoria == ordenada

# Pivote medio - lista ordenada

salida_medio_ordenada, comp_medio_ordenada = rapida(
    ordenada,
    "medio"
)

assert salida_medio_ordenada == ordenada

# Pivote último - lista ordenada

salida_ultimo_ordenada, comp_ultimo_ordenada = rapida(
    ordenada,
    "ultimo"
)

assert salida_ultimo_ordenada == ordenada

print(
    f"Pivote medio  | Aleatoria: "
    f"{comp_medio_aleatoria:,}"
)
print(
    f"Pivote último | Aleatoria: "
    f"{comp_ultimo_aleatoria:,}"
)
print(
    f"Pivote medio  | Ordenada: "
    f"{comp_medio_ordenada:,}"
)
print(
    f"Pivote último | Ordenada: "
    f"{comp_ultimo_ordenada:,}"
)

# RETO 4 - BÚSQUEDA BINARIA

print("\nRETO 4 - BÚSQUEDA BINARIA")

# Buscar todos los elementos y obtener el peor caso

peor_1000 = 0

for valor in ordenada:

    _, pasos = binaria(ordenada, valor)

    if pasos > peor_1000:
        peor_1000 = pasos


print(
    "Peor caso con 1.000 elementos:",
    peor_1000
)

assert peor_1000 == 10


# Para un millón de elementos no es necesario buscar un millón de veces:
# basta comprobar el peor número de pasos posible sobre una lista ordenada de ese tamaño.

millon = list(range(1, 1000001))

peor_millon = 0

valores_prueba = [
    1,
    2,
    3,
    500000,
    999998,
    999999,
    1000000
]

for valor in valores_prueba:

    _, pasos = binaria(millon, valor)

    if pasos > peor_millon:
        peor_millon = pasos


print(
    "Peor caso comprobado con 1.000.000 elementos:",
    peor_millon
)

print(
    "Máximo teórico para 1.000.000 elementos:",
    math.ceil(math.log2(1000000))
)

assert math.ceil(math.log2(1000000)) == 20

# RETO 5 - PUNTO DE EQUILIBRIO

print("\nRETO 5 - ¿CUÁNDO COMPENSA ORDENAR?")

equilibrio_1000 = equilibrio(1000)
equilibrio_millon = equilibrio(1000000)

print(
    "equilibrio(1000):",
    equilibrio_1000
)

print(
    "equilibrio(1000000):",
    equilibrio_millon
)

assert equilibrio_millon == 40

# TABLA FINAL DE LOS CINCO ALGORITMOS

print("\n" + "=" * 65)
print("TABLA FINAL - CINCO ALGORITMOS")
print("=" * 65)

_, comp_burbuja, _ = burbuja(aleatoria)
_, comp_seleccion, _ = seleccion(aleatoria)
_, comp_insercion, _ = insercion(aleatoria)
_, comp_mezcla_final = mezcla(aleatoria)
_, comp_rapida_final = rapida(aleatoria, "medio")

print(
    f"\n{'Algoritmo':<20}"
    f"{'Comparaciones':>20}"
)

print("-" * 42)

print(
    f"{'Burbuja':<20}"
    f"{comp_burbuja:>20,}"
)

print(
    f"{'Selección':<20}"
    f"{comp_seleccion:>20,}"
)

print(
    f"{'Inserción':<20}"
    f"{comp_insercion:>20,}"
)

print(
    f"{'Mezcla':<20}"
    f"{comp_mezcla_final:>20,}"
)

print(
    f"{'Rápida':<20}"
    f"{comp_rapida_final:>20,}"
)

# CONCLUSIÓN

print("\n" + "=" * 65)
print("CONCLUSIÓN")
print("=" * 65)

print("""
Selección no mejora cuando la lista ya está ordenada porque siempre
recorre todos los elementos restantes para encontrar el menor, por lo
que realiza prácticamente las mismas comparaciones en cualquier caso.

Sin embargo, puede convenir cuando mover elementos es costoso, porque
hace pocos intercambios aunque tenga que realizar muchas comparaciones.

Mezcla y QuickSort reducen considerablemente las comparaciones frente
a los algoritmos cuadráticos, mientras que la búsqueda binaria permite
buscar eficientemente una vez que los datos están ordenados.
""")


print("=" * 65)
print("TALLER FINALIZADO CORRECTAMENTE")
print("=" * 65)


# ============================================================
# TABLA DE NUEVE CASILLAS - VÍA A
# ============================================================
#
#                    ALEATORIA    ORDENADA    AL REVÉS
#
# Burbuja             499149         999       499500
# Selección            499500      499500       499500
# Inserción            241994         999       499500
#
#
# TABLA FINAL - CINCO ALGORITMOS SOBRE LA LISTA ALEATORIA
#
# Burbuja     -> 499149 comparaciones
# Selección   -> 499500 comparaciones
# Inserción   -> 241994 comparaciones
# Mezcla      ->   8720 comparaciones
# Rápida      -> depende de la elección del pivote
