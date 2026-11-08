# Sistema de inventario y despacho de bodega

Proyecto final de Estructuras de Datos (IS061, 2026-2).
Integrantes: Jerónimo Mazo Restrepo, Juan Andrés Sánchez Rojas. 
Docente: Camilo Rendón Vinasco.

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
python iniciar.py --consola        # lo mismo y abre el menú de consola
python -m pytest -q                # todas las pruebas (~3 s)
python demostracion.py --rapido    # criterio de éxito en versión pequeña (~10 s)
```

No hay pasos manuales ocultos: `iniciar.py` genera los CSV con semilla fija en `datos/generados/`, crea la base `inventario.db` y la reutiliza en las siguientes ejecuciones (`--reiniciar` la regenera).

## Demostración del criterio de éxito

`python demostracion.py` (≈3 min con 10.000 productos) escribe en `resultados/`:

- `resumen.txt`: FEFO verificado en cada despacho y ahorro de ruta por tamaño de ola.
- `rutas.csv` y `ahorro_rutas.png`: los datos y la gráfica.

Criterio 1 (el despacho respeta el vencimiento en el 100 % de los casos): se cumple, 0 violaciones en 29.596 despachos verificados con un verificador independiente. Criterio 2 (ruta con ≥ 20 % menos distancia): se cumple con olas de 5 o más pedidos y **no** con olas de 3 pedidos (9,9 %); el detalle y la explicación están en el informe.

## Mediciones (opcionales)

```bash
python -m mediciones.escala      # carga/despacho/búsqueda a 10.000 referencias
python -m mediciones.arbol       # BST frente a AVL
python -m mediciones.grafo       # lista frente a matriz de adyacencia, cola de prioridad
python -m mediciones.ruta        # ahorro de la ruta
python -m mediciones.lotes       # lista ligada de lotes, fusión recursiva frente a iterativa
python -m mediciones.colas       # colas y pila propias frente a la biblioteca estándar
python -m mediciones.entrega1    # pruebas de complejidad de la Entrega 1 (reproduce docs/entrega1/resultados.md)
python -m mediciones.graficas_entrega1  # las 4 gráficas del informe de la Entrega 1 (docs/entrega1/graficas/)
python -m mediciones.benchmark   # gráficas propio-vs-biblioteca estándar en docs/entrega2/graficas/
```

Los tiempos dependen de la máquina; las tablas del informe son de un entorno de referencia y conviene repetirlas en el equipo propio.

## Estructura del repositorio

```
.
├── iniciar.py                  # arranque con un solo comando
├── demostracion.py             # demostración reproducible del criterio de éxito
├── requirements.txt
├── pyproject.toml              # configuración de pytest y ruff
├── inventario/                 # código del sistema
│   ├── estructuras/            # arreglo, matriz, lista de lotes, pila, colas, AVL, montículo
│   ├── algoritmos/             # búsqueda (lineal, binaria) y ordenamiento (burbuja, QuickSort)
│   ├── grafos/                 # grafo (lista y matriz), BFS/DFS/Dijkstra, plano y ruta
│   ├── dominio/                # producto, lote, pedido, devolución
│   ├── nucleo/                 # SistemaInventario (integra todo)
│   ├── persistencia/           # SQLite (solo guarda el estado)
│   ├── interfaces/             # ventana tkinter y consola con menú
│   ├── generacion/             # generador de datos sintéticos (CSV)
│   ├── arranque.py             # lógica de iniciar.py
│   └── demostracion.py         # lógica de demostracion.py
├── mediciones/                 # mediciones y gráficas de rendimiento (Entregas 1 a 3)
├── tests/                      # pruebas (507), con la misma división que el código
├── datos/ejemplo/              # CSV pequeños de ejemplo (los generados van a datos/generados/)
├── resultados/                 # salida de la demostración (resumen, rutas.csv, gráfica)
└── docs/
    ├── entrega1/               # resultados.md, gráficas, anexo de IA y reparto de la Entrega 1
    ├── entrega3/               # anexo de IA de la Entrega 3
    ├── Reparto.md              # reparto de todo el semestre
    └── ESTRUCTURA.md           # equivalencia entre nombres antiguos y actuales
```

La tabla con el nombre antiguo de cada archivo y su ubicación actual está en `docs/ESTRUCTURA.md`.

## Mapa de requisitos de la guía

| Requisito | Dónde está |
|---|---|
| Arreglo dinámico con duplicación, matriz de bodega | `inventario/estructuras/arreglo.py`, `matriz.py` |
| QuickSort, burbuja y búsqueda binaria | `inventario/algoritmos/` |
| Lista ligada (lotes por vencimiento, FEFO) y fusión recursiva | `inventario/estructuras/lista_lotes.py` |
| Pila, cola circular (estática) y cola enlazada (dinámica) | `inventario/estructuras/pila.py`, `cola_circular.py`, `cola_enlazada.py` |
| BST y AVL (recorridos, borrado con dos hijos, rotaciones) | `inventario/estructuras/arbol_productos.py` |
| Cola de prioridad (montículo) para pedidos urgentes | `inventario/estructuras/cola_prioridad.py` |
| Grafo, BFS, DFS, componentes conexas y Dijkstra | `inventario/grafos/` |
| Ruta de recolección sobre el plano | `inventario/grafos/ruta_recoleccion.py`, `plano_bodega.py` |
| CSV con 10.000 productos | `inventario/generacion/generador_datos.py` |
| SQLite, ventana y consola | `inventario/persistencia/`, `inventario/interfaces/` |
| Demostración del criterio de éxito | `demostracion.py` → `resultados/` |
| Informe de complejidad de la Entrega 1 (tablas y gráficas) | `docs/entrega1/resultados.md`, `docs/entrega1/graficas/` |
| Reparto interno y anexos de IA | `docs/Reparto.md`, `docs/entrega1/`, `docs/entrega3/Anexo_IA.md` |
