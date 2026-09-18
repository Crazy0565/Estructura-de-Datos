# Resultados de las pruebas de complejidad

> Las mediciones corresponden a una ejecución del proyecto en Python 3.13.15. Los tiempos pueden variar según el equipo y las condiciones de ejecución.

## 1. Pruebas de complejidad

| Productos | Generación (s) | Inserción (s) | Acceso (s) | Búsqueda lineal (s) | Búsqueda binaria (s) | Capacidad |
|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 0.000584 | 0.000499 | 0.000001300 | 0.000040 | 0.000003700 | 1.280 |
| 5.000 | 0.002730 | 0.002390 | 0.000001400 | 0.000194 | 0.000005000 | 5.120 |
| 10.000 | 0.004746 | 0.004626 | 0.000000900 | 0.000379 | 0.000003800 | 10.240 |
| 50.000 | 0.022802 | 0.030623 | 0.000001800 | 0.002049 | 0.000006200 | 81.920 |
| 100.000 | 0.045162 | 0.082452 | 0.000001100 | 0.003953 | 0.000007700 | 163.840 |

## 2. Algoritmos de ordenamiento

| Productos | Bubble Sort (s) | QuickSort (s) |
|---:|---:|---:|
| 1.000 | 0.057956 | 0.000179 |
| 5.000 | 1.570549 | 0.000787 |
| 10.000 | 5.883838 | 0.001480 |
| 50.000 | Omitido | 0.007553 |
| 100.000 | Omitido | 0.021337 |

Bubble Sort se omitió para 50.000 y 100.000 elementos debido a su crecimiento cuadrático, evitando una ejecución innecesariamente costosa.

## 3. Escalabilidad de la matriz

| Matriz | Ubicaciones | Tiempo de creación (s) |
|---:|---:|---:|
| 10×10 | 100 | 0.00001400 |
| 20×20 | 400 | 0.00001990 |
| 30×30 | 900 | 0.00002110 |
| 40×40 | 1.600 | 0.00003450 |
| 50×50 | 2.500 | 0.00004860 |
| 60×60 | 3.600 | 0.00006990 |
| 70×70 | 4.900 | 0.00014950 |
| 80×80 | 6.400 | 0.00015800 |
| 90×90 | 8.100 | 0.00015660 |
| 100×100 | 10.000 | 0.00018180 |

La matriz comienza con un tamaño configurable y puede ampliarse cuando se asigna una posición que se encuentra fuera de sus límites actuales.

## 4. Comparación de QuickSort con sorted()

Se utilizaron 1.000 entradas con IDs en orden aleatorio.

| Algoritmo | Tiempo (s) |
|---|---:|
| QuickSort | 0.00208150 |
| sorted() | 0.00016580 |

Resultado de la verificación:

**Orden correcto: SI**

Los resultados producidos por QuickSort y sorted() fueron iguales para las 1.000 entradas.

Además, esta comparación se encuentra implementada como prueba automatizada en 	ests/test_comparacion_sorted.py.

## 5. Benchmark: ArregloDinamico vs list

### Inserción

| Elementos | ArregloDinamico (s) | list (s) |
|---:|---:|---:|
| 1.000 | 0.00011900 | 0.00002230 |
| 5.000 | 0.00056620 | 0.00018130 |
| 10.000 | 0.00132500 | 0.00040970 |
| 50.000 | 0.00908350 | 0.00247770 |
| 100.000 | 0.01689870 | 0.00609890 |

### Acceso

| Elementos | ArregloDinamico (s) | list (s) |
|---:|---:|---:|
| 1.000 | 0.000000900 | 0.000000100 |
| 5.000 | 0.000001300 | 0.000000300 |
| 10.000 | 0.000001000 | 0.000000200 |
| 50.000 | 0.000001200 | 0.000000100 |
| 100.000 | 0.000001200 | 0.000000300 |

El benchmark permite comparar la implementación propia con la estructura list de Python. Las diferencias de tiempo son esperables debido a las optimizaciones internas de la implementación estándar.

## 6. Complejidades

| Operación | Complejidad temporal | Complejidad espacial |
|---|---|---|
| Acceso al arreglo | O(1) | O(1) |
| Inserción en arreglo | O(1) amortizado | O(1) |
| Redimensionamiento del arreglo | O(n) | O(n) |
| Búsqueda lineal | O(n) | O(1) |
| Búsqueda binaria | O(log n) | O(1) |
| Bubble Sort, mejor caso | O(n) | O(1) |
| Bubble Sort, caso promedio | O(n²) | O(1) |
| Bubble Sort, peor caso | O(n²) | O(1) |
| QuickSort, caso promedio | O(n log n) | O(n) |
| QuickSort, peor caso | O(n²) | O(n) |
| Creación de matriz n×n | O(n²) | O(n²) |
| Ampliación de matriz | O(n²) | O(n²) |

## 7. Pruebas automatizadas

La suite contiene actualmente **24 pruebas automatizadas**.

Resultado:

24 passed

Entre ellas se encuentra la comparación de QuickSort frente a sorted() utilizando 1.000 entradas aleatorias.

## 8. Carga de datos desde archivo

El sistema permite cargar productos desde productos.csv mediante la opción correspondiente de main.py.

La prueba realizada cargó correctamente:

Cargados: 5

Inventario: 5

También se verificó que el primer producto cargado quedara correctamente ubicado en la matriz de bodega.

## 9. Conclusiones

Los experimentos permiten observar el comportamiento de las estructuras y algoritmos al aumentar la cantidad de datos.

La búsqueda lineal incrementa su tiempo conforme aumenta el número de elementos, mientras que la búsqueda binaria mantiene tiempos reducidos cuando los datos están ordenados.

Bubble Sort presenta un crecimiento considerable al aumentar la cantidad de elementos, mientras que QuickSort permite realizar pruebas con cantidades mayores.

El arreglo dinámico aumenta automáticamente su capacidad y permitió trabajar con 100.000 productos. La matriz de bodega también puede ampliarse para atender nuevas posiciones.

Las comparaciones con list y sorted() permiten contrastar las implementaciones propias con estructuras y funciones de la biblioteca estándar de Python.
