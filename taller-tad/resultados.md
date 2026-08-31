# Resultados de las mediciones

## Entorno

- Python: 3.13.15
- Computador: Windows PC (modelo no identificado por Windows)

## Mediciones

| Número de contactos | contiene() | Búsqueda ingenua | agregar() + eliminar() |
|---:|---:|---:|---:|
| 1.000 | 0,000000800 s (0,8 µs) | 0,000016700 s (16,7 µs) | 0,000002800 s (2,8 µs) |
| 10.000 | 0,000001200 s (1,2 µs) | 0,000176100 s (176,1 µs) | 0,000007800 s (7,8 µs) |
| 100.000 | 0,000001400 s (1,4 µs) | 0,002847700 s (2.847,7 µs) | 0,000058400 s (58,4 µs) |

## Interpretación

1. El tiempo de `contiene()` aumenta muy poco al pasar de 1.000 a 100.000 contactos. Esto es consistente con una búsqueda binaria de complejidad O(log n).

2. La búsqueda ingenua aumenta considerablemente al crecer el número de contactos. Al pasar de 10.000 a 100.000 contactos, el tiempo aumenta aproximadamente 16,2 veces, lo cual es consistente con una complejidad O(n).

3. La operación `agregar()` + `eliminar()` también aumenta al crecer la cantidad de contactos. Al pasar de 10.000 a 100.000 contactos, el tiempo aumenta aproximadamente 7,5 veces, lo cual es consistente con una complejidad O(n).
