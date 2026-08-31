# Nombre completo: Jeronimo Mazo Restrepo

# 1. Calculadora de notas

print("=== 1. CALCULADORA DE NOTAS ===")

notas = []
for i in range(5):
    nota = float(input(f"Ingrese la nota {i + 1}: "))
    notas.append(nota)

suma = 0
mayor = notas[0]
menor = notas[0]

for nota in notas:
    suma = suma + nota

    if nota > mayor:
        mayor = nota

    if nota < menor:
        menor = nota

promedio = suma / 5

print(f"Promedio: {promedio:.2f}")

if promedio >= 3.0:
    print("Resultado: Aprueba")
else:
    print("Resultado: No aprueba")

print(f"Nota más alta: {mayor:.2f}")
print(f"Nota más baja: {menor:.2f}")

# 2. Contador de pares

print("\n=== 2. CONTADOR DE PARES ===")

import random

cantidad = 100
pares = 0

for i in range(cantidad):
    numero = random.randint(1, 50)

    if numero % 2 == 0:
        pares = pares + 1

print(f"Cantidad de números pares entre {cantidad} números: {pares}")

# 3. Contar las operaciones

print("\n=== 3. CONTADOR DE OPERACIONES ===")

cantidad = 100
pares = 0
operaciones = 0

for i in range(cantidad):
    numero = random.randint(1, 50)
    operaciones = operaciones + 1

    if numero % 2 == 0:
        pares = pares + 1

print(f"Números generados: {cantidad}")
print(f"Pares encontrados: {pares}")
print(f"Veces que entra al ciclo: {operaciones}")

# Con 100 números: el ciclo entra 100 veces.
# Con 1.000 números: el ciclo entra 1.000 veces.
# Con 10.000 números: el ciclo entra 10.000 veces.
#
# Estos resultados corresponden al tamaño de la entrada:
# 100 -> 100 iteraciones
# 1.000 -> 1.000 iteraciones
# 10.000 -> 10.000 iteraciones
