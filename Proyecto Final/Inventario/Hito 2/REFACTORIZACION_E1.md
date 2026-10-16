# Registro de refactorización de la Entrega 1

Cambios hechos sobre el núcleo de la Entrega 1 al crear la carpeta `Hito 2`.
Este registro alimenta la sección "Refactorización" del informe de la Entrega 2.

| # | Problema en la Entrega 1 | Cambio realizado | Archivos | Pruebas |
|---|---|---|---|---|
| 1 | `eliminar_producto` modificaba `inventario.datos` y `inventario.tamaño` desde `main.py`, rompiendo el encapsulamiento del arreglo. | Nuevo método `ArregloDinamico.eliminar(indice)`, O(n), que desplaza los elementos y devuelve el eliminado. | `arreglo.py` | 6 nuevas en `test_arreglo.py` |
| 2 | `MatrizBodega.asignar` sobrescribía en silencio una ubicación ocupada: el producto anterior desaparecía de la matriz pero seguía en el arreglo. | `asignar` lanza `ValueError` si la ubicación la ocupa otro producto. Reasignar el mismo producto sigue permitido. | `matriz.py` | 3 nuevas en `test_matriz.py` |
| 3 | `main.py` no usaba `busqueda.py` ni `ordenamiento.py`: buscaba con un `for` propio y no ordenaba nunca. | `SistemaInventario` usa búsqueda binaria cuando el catálogo está ordenado por ID y lineal en caso contrario. Nueva opción de menú para ordenar con QuickSort por id, nombre, vencimiento o tiempo de producción. | `sistema.py`, `main.py` | `test_sistema.py` |
| 4 | La lógica del sistema estaba mezclada con `input()` y `print()`, así que no se podía probar sin teclado. | Nueva clase `SistemaInventario` con la lógica; `main.py` queda como capa de entrada y salida. | `sistema.py`, `main.py` | `test_sistema.py`, `test_main.py` |
| 5 | Cargar dos veces el CSV duplicaba los productos. | La carga pasa por `agregar`, que rechaza las ubicaciones ocupadas: la segunda carga falla en vez de duplicar. | `sistema.py` | `test_cargar_dos_veces_el_mismo_csv_no_duplica_productos` |
| 6 | `agregar` registraba el producto en el arreglo antes que en la matriz: si la matriz fallaba, los dos quedaban inconsistentes. | Se reserva primero la ubicación y solo después se agrega al catálogo. | `sistema.py` | `test_agregar_en_ubicacion_ocupada_no_cambia_el_catalogo` |
| 7 | Una entrada no numérica rompía el programa (`int(input())`) y consultar una ubicación fuera de la matriz lanzaba `IndexError` sin controlar. | `leer_entero` y `leer_decimal` repiten la pregunta; los errores se capturan y se muestran como mensaje. | `main.py` | `test_main.py` |
| 8 | "Ubicaciones disponibles" mostraba el total de celdas, no las libres. | Nuevo `ubicaciones_libres()`. | `sistema.py`, `main.py` | `test_ubicaciones_libres` |
| 9 | `main.py` no tenía anotaciones de tipo ni complejidad en los docstrings. | Anotaciones de tipo y docstrings con complejidad en todas las funciones. | `main.py`, `sistema.py` | n/a |
| 10 | El `.gitignore` empezaba con un BOM, por lo que su primera regla no funcionaba y el zip traía `__pycache__`. | `.gitignore` reescrito sin BOM, con `__pycache__/`, `*.pyc`, `.pytest_cache/` y `venv/`. | `.gitignore` | n/a |
| 11 | Archivos con BOM y saltos de línea mezclados (CRLF y LF). | Normalizados a UTF-8 sin BOM y LF. | todos los `.py` | n/a |

Cambio de menú: la salida pasa a ser la opción `0`; se agregan `7. Ordenar catálogo` y `8. Listar catálogo`.

**Pendiente:** retroalimentación del docente a la Entrega 1. Cuando se tenga, agregar aquí una fila por cada punto con su respuesta.
