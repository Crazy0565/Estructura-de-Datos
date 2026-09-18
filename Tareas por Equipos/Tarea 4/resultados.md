# Resultados de la medicion

## Tabla de resultados

| Lado | Celdas | Tiempo (s) | Factor vs. anterior |
|---:|---:|---:|---:|
| 250 | 62,500 | 0.000201 | - |
| 500 | 250,000 | 0.000789 | 3.93 |
| 1000 | 1,000,000 | 0.003251 | 4.12 |

## Interpretacion

Al duplicar el lado de la matriz, la cantidad de celdas se cuadruplica, por lo que el tiempo de `suma()` aumenta aproximadamente cuatro veces.

Los factores obtenidos fueron 3.93 y 4.12, valores cercanos a 4, lo que es consistente con una complejidad O(f * c).

## Entorno de ejecucion

- Python: 3.13.15
- Sistema: Windows 11
- Medicion: `timeit`, 5 ejecuciones y se conserva el mejor tiempo.
- Semilla aleatoria: 11
