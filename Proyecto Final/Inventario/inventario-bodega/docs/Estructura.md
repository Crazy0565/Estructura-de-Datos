# Equivalencia de nombres

El proyecto pasó de una carpeta plana a un paquete organizado por partes. Esta tabla permite seguir los nombres que aparecen en los informes y en el anexo de IA.

| Archivo anterior | Ubicación actual |
|---|---|
| `arreglo.py`, `nodo.py`, `matriz.py`, `lista_lotes.py`, `pila.py`, `cola_circular.py`, `cola_enlazada.py`, `cola_prioridad.py`, `arbol_productos.py` | `inventario/estructuras/` (mismo nombre) |
| `busqueda.py`, `ordenamiento.py` | `inventario/algoritmos/` |
| `grafo_bodega.py`, `algoritmos_grafo.py`, `plano_bodega.py`, `ruta_recoleccion.py` | `inventario/grafos/` |
| `producto.py`, `lote.py`, `pedido.py`, `devolucion.py` | `inventario/dominio/` |
| `sistema.py` | `inventario/nucleo/sistema.py` |
| `persistencia.py` | `inventario/persistencia/repositorio_sqlite.py` |
| `gui.py` | `inventario/interfaces/gui.py` |
| `main.py` (consola) | `inventario/interfaces/consola.py` |
| `generador_datos.py` | `inventario/generacion/generador_datos.py` |
| `iniciar.py` | `iniciar.py` (lanzador) + `inventario/arranque.py` (lógica) |
| `demostracion.py` | `demostracion.py` (lanzador) + `inventario/demostracion.py` (lógica) |
| `medicion_escala.py`, `medicion_arbol.py`, `medicion_grafo.py`, `medicion_ruta.py`, `medicion_colas.py`, `medicion_lotes.py` | `mediciones/escala.py`, `arbol.py`, `grafo.py`, `ruta.py`, `colas.py`, `lotes.py` |
| `benchmark_graficas.py` | `mediciones/benchmark.py` (escribe en `docs/entrega2/graficas/`) |
| `prueba.py` (Hito 1) | `mediciones/entrega1.py` (mismas pruebas, ordenadas y con anotaciones) |
| `graficas.py` y `grafica_*.png` (Hito 1) | `mediciones/graficas_entrega1.py` y `docs/entrega1/graficas/` |
| `resultados.md`, `anexos/ANEXO_IA.md`, `reparto/REPARTO.md` (Hito 1) | `docs/entrega1/` |
| `productos.csv`, `lotes.csv`, `pedidos.csv` | `datos/ejemplo/` |
| `anexos/Anexo IA.md` (Hito 3), `reparto/Reparto.md` | `docs/entrega3/Anexo_IA.md`, `docs/Reparto.md` |
| `tests/test_*.py` | `tests/<parte>/test_*.py` (`test_main.py` → `tests/interfaces/test_consola.py`) |

## Archivos eliminados

Ninguno con contenido propio de la guía. Los scripts sueltos `prueba.py` y `graficas.py` se conservaron como `mediciones/entrega1.py` y `mediciones/graficas_entrega1.py`.
