# Resultados de las pruebas de complejidad

## 1. Pruebas con diferentes cantidades de productos

| Productos | Generación (s) | Inserción (s) | Acceso (s) | Búsqueda lineal (s) | Búsqueda binaria (s) | Capacidad |
|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 0.000512 | 0.000681 | 0.000001200 | 0.000038 | 0.000003600 | 1.280 |
| 5.000 | 0.002320 | 0.002720 | 0.000001600 | 0.000188 | 0.000004100 | 5.120 |
| 10.000 | 0.006025 | 0.005408 | 0.000000900 | 0.000395 | 0.000004200 | 10.240 |
| 50.000 | 0.023895 | 0.029080 | 0.000001100 | 0.002000 | 0.000006100 | 81.920 |
| 100.000 | 0.047012 | 0.081061 | 0.000002200 | 0.003892 | 0.000007800 | 163.840 |

## 2. Ordenamientos

| Productos | Bubble Sort (s) | QuickSort (s) |
|---:|---:|---:|
| 1.000 | 0.050138 | 0.000164 |
| 5.000 | 1.446117 | 0.000799 |
| 10.000 | 5.426820 | 0.001657 |
| 50.000 | No ejecutado | 0.007957 |
| 100.000 | No ejecutado | 0.018977 |

Bubble Sort no se ejecutó para 50.000 y 100.000 elementos debido a su crecimiento cuadrático de tiempo.

## 3. Escalabilidad de la matriz

| Matriz | Ubicaciones | Tiempo de creación (s) |
|---:|---:|---:|
| 10×10 | 100 | 0.00001310 |
| 20×20 | 400 | 0.00002120 |
| 30×30 | 900 | 0.00002400 |
| 40×40 | 1.600 | 0.00003210 |
| 50×50 | 2.500 | 0.00004220 |
| 60×60 | 3.600 | 0.00005310 |
| 70×70 | 4.900 | 0.00009850 |
| 80×80 | 6.400 | 0.00012880 |
| 90×90 | 8.100 | 0.00014490 |
| 100×100 | 10.000 | 0.00017330 |

## 4. Complejidades esperadas

| Operación | Complejidad |
|---|---|
| Acceso al arreglo | O(1) |
| Inserción en arreglo | O(1) amortizado |
| Redimensionamiento | O(n) |
| Búsqueda lineal | O(n) |
| Búsqueda binaria | O(log n) |
| Bubble Sort | O(n²) |
| QuickSort promedio | O(n log n) |
| Creación de matriz n×n | O(n²) |

## 5. Observaciones

Los resultados muestran que el acceso al arreglo y la búsqueda binaria mantienen tiempos muy pequeños incluso cuando aumenta la cantidad de productos.

La búsqueda lineal aumenta conforme crece la cantidad de elementos, comportamiento esperado para una operación O(n).

Bubble Sort presenta un crecimiento considerable del tiempo al aumentar la cantidad de elementos, mientras que QuickSort permite trabajar con cantidades mucho mayores de productos en tiempos reducidos.

El arreglo dinámico aumenta su capacidad automáticamente para permitir almacenar cantidades mayores de productos sin modificar el código.

La matriz puede utilizar diferentes tamaños y conservar los productos existentes cuando se amplía.