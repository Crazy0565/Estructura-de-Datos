# Sistema de inventario y despacho de bodega — Entrega 3

Proyecto de Estructuras de Datos (IS061, 2026-2). Integrantes: Jerónimo Mazo Restrepo, Juan Felipe Méndez Martínez, Juan Andrés Sánchez Rojas. Docente: Camilo Rendón Vinasco.

El sistema administra 10.000 productos con lotes y vencimientos, despacha pedidos con FEFO (primero vence, primero sale) y calcula la ruta de recolección dentro de la bodega. Todas las estructuras del núcleo son propias (sin `list`, `dict`, `heapq` ni `sorted` en el núcleo); SQLite solo guarda el estado y la ventana (tkinter) es una capa delgada.

## Requisitos

- Python 3.11 o superior.
- `pip install -r requirements.txt` (pytest y matplotlib).
- Para la ventana: tkinter (en Linux: `sudo apt install python3-tk`). Sin tkinter todo lo demás funciona y las pruebas de la ventana se omiten.

## Del clon a ejecutar en menos de 5 minutos

```bash
git clone <URL-del-repositorio>
cd <carpeta-del-proyecto>
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python iniciar.py --sin-ventana    # sistema completo: genera 10.000 productos, los carga y resume (~2 s)
python iniciar.py                  # lo mismo y abre la ventana
python -m pytest -q                # todas las pruebas (~3 s)
python demostracion.py --rapido    # criterio de éxito en versión pequeña (~10 s)
```

No hay pasos manuales ocultos: `iniciar.py` genera los CSV con semilla fija, crea la base `inventario.db` y la reutiliza en las siguientes ejecuciones (`--reiniciar` la regenera).

## Demostración del criterio de éxito

`python demostracion.py` (≈3 min con 10.000 productos) escribe en `resultados/`:

- `resumen.txt`: FEFO verificado en cada despacho y ahorro de ruta por tamaño de ola.
- `rutas.csv` y `ahorro_rutas.png`: los datos y la gráfica.

Criterio 1 (el despacho respeta el vencimiento en el 100 % de los casos): se cumple, 0 violaciones en 29.596 despachos verificados con un verificador independiente. Criterio 2 (ruta con ≥ 20 % menos distancia): se cumple con olas de 5 o más pedidos y **no** con olas de 3 pedidos (9,9 %); el detalle y la explicación están en el informe.

## Mediciones (opcionales)

```bash
python medicion_escala.py   # carga/despacho/búsqueda a 10.000 referencias
python medicion_arbol.py    # BST frente a AVL
python medicion_grafo.py    # lista frente a matriz de adyacencia, cola de prioridad
python medicion_ruta.py     # ahorro de la ruta
```

Los tiempos dependen de la máquina; las tablas del informe son de un entorno de referencia y conviene repetirlas en el equipo propio.

## Mapa de módulos

| Parte | Archivos |
|---|---|
| Estructuras lineales | `arreglo.py`, `nodo.py`, `lista_lotes.py`, `lote.py`, `cola_enlazada.py`, `cola_circular.py`, `pila.py`, `matriz.py` |
| Árbol propio | `arbol_productos.py` (BST iterativo y AVL recursivo) |
| Cola de prioridad | `cola_prioridad.py` (montículo mínimo) |
| Grafo y algoritmos | `grafo_bodega.py` (lista y matriz de adyacencia), `algoritmos_grafo.py` (BFS, DFS, componentes, Dijkstra), `plano_bodega.py` |
| Ruta de recolección | `ruta_recoleccion.py` |
| Núcleo del sistema | `sistema.py` (SistemaInventario), `pedido.py`, `producto.py`, `devolucion.py`, `busqueda.py`, `ordenamiento.py` |
| Bordes | `persistencia.py` (SQLite), `gui.py` (tkinter), `main.py` (consola), `iniciar.py` (arranque) |
| Datos y demostración | `generador_datos.py`, `demostracion.py`, `medicion_*.py` |
| Pruebas | `tests/` (507 pruebas) |
| Documentos | `anexos/Anexo IA.md`, `reparto/Reparto.md` |
