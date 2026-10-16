# Justificación de estructuras (Entrega 2)

Borrador de la sección "por qué cada estructura y no otra" del informe.
Las mediciones salen de `python medicion_lotes.py` y `python medicion_colas.py` (la Fase 4
las formaliza con gráficas).
Los tiempos varían entre ejecuciones; lo que importa es el orden de magnitud y la tendencia.

## 1. Lista ligada sencilla de lotes (`ListaLotes`)

**Operación que la justifica.** Despachar siempre primero el lote que vence antes.
Con la lista ordenada por vencimiento, ese lote es la cabeza y despachar es quitar
desde ahí: O(1) si el primer lote alcanza, O(k) si hay que consumir k lotes.

**Alternativa: `ArregloDinamico`.** Quitar el primer elemento obliga a desplazar todos
los demás: O(n). Medido (una operación):

| n | `ListaLotes.despachar(1)` | `ArregloDinamico.eliminar(0)` | `list.pop(0)` |
|---|---|---|---|
| 1.000 | 1,46 µs | 91,09 µs | 0,24 µs |
| 10.000 | 1,96 µs | 1.169,93 µs | 1,62 µs |
| 100.000 | 1,11 µs | 6.747,60 µs | 15,03 µs |

Lectura honesta de la tabla:
- La lista se mantiene plana (O(1)) mientras el arreglo propio crece de forma lineal.
- Contra `list.pop(0)` la lista gana solo con tamaños grandes: `list` está escrito en C y
  mueve la memoria de golpe, así que con pocos elementos es más rápido. Un producto real
  tiene pocos lotes, de modo que la ventaja práctica es de clase de complejidad, no de
  milisegundos. La elección se defiende por la operación (sacar de la cabeza sin
  desplazar nada) y por no depender de una estructura de la biblioteca estándar.

**Contra `deque`.** `deque.popleft()` es constante y unas 10 veces más rápido que
`ListaLotes.despachar(1)` (≈0,1 µs frente a ≈1 µs; `python benchmark_graficas.py`, gráfica
`graficas/frente.png`). La lista propia no gana en velocidad: gana en que, además de quitar
de la cabeza, mantiene el orden por vencimiento y permite fusionar dos listas sin copiar.

**Por qué sencilla y no doble.** Ninguna operación del dominio recorre los lotes hacia
atrás ni borra un nodo conociéndolo de antemano. Eliminar por código ya exige buscar
desde la cabeza, así que el puntero `anterior` de una lista doble costaría memoria sin
ahorrar tiempo.

**Costos que se aceptan.**
- Insertar un lote es O(n): hay que buscar su posición y comprobar que el código no se
  repita. Se acepta porque un producto tiene pocos lotes y se insertan rara vez frente
  a los despachos.
- No hay acceso por índice. Ninguna operación lo necesita.
- El stock total se mantiene como acumulado, así que consultarlo es O(1).

**Operaciones incluidas (y no más):** `insertar`, `buscar`, `primero`, `despachar`,
`eliminar_lote`, `stock_total`, `fusionar` y recorrido.

## 2. Recursividad: fusión de dos listas ordenadas

**Por qué es la solución natural.** Una lista ligada es una estructura recursiva: un nodo
más el resto de la lista. Fusionar dos listas ordenadas se dice igual: se decide cuál de
las dos cabezas va primero y se fusiona recursivamente lo que queda
(`_fusionar_nodos` en `lista_lotes.py`). Los nodos se reutilizan, no se copian.

**Dónde se usa en el sistema.** `SistemaInventario.cargar_lotes_csv` arma un embarque
por producto y lo fusiona con los lotes que el producto ya tiene.

**Análisis de profundidad de pila.**
- Cada llamada consume un nodo, así que la profundidad llega a n + m.
- Python limita la recursión a 1.000 llamadas. Medido: la versión recursiva fusionó
  hasta 990 lotes en total y falló (`RecursionError`) por encima de eso.
- Espacio: O(n + m) por la pila, frente a O(1) de la versión iterativa.
- Si desborda, no deja las listas a medias: la asignación de enlaces ocurre al volver de
  cada llamada, así que un `RecursionError` no modifica ninguna lista (hay una prueba).

**Alternativa iterativa.** `fusionar_iterativo` usa un bucle y un nodo ficticio: mismo
O(n + m) en tiempo, O(1) en espacio y sin límite de pila. Medido: 50.000 lotes en
12,3 ms.

| Total de lotes | Recursiva | Iterativa |
|---|---|---|
| 100 | 0,045 ms | 0,015 ms |
| 400 | 0,120 ms | 0,081 ms |
| 900 | 0,257 ms | 0,166 ms |
| 1.400 | `RecursionError` | 0,225 ms |
| 5.000 | `RecursionError` | 0,582 ms |
| 50.000 | `RecursionError` | 12,281 ms |

**Decisión.** `fusionar` usa la recursiva mientras el total sea ≤ `LIMITE_RECURSION` (500,
la mitad del límite de Python para dejar margen a las llamadas del programa) y la
iterativa por encima. Con los datos reales (pocos lotes por producto) siempre se usa la
recursiva; la iterativa protege el sistema si un producto llegara a tener miles de lotes.

**Otros algoritmos recursivos.** `quick_sort` (Entrega 1) también es recursivo: profundidad
O(log n) en promedio y O(n) en el peor caso.

## 3. Colas y pila del despacho

El sistema usa tres estructuras distintas, cada una para una necesidad concreta. Los
tiempos salen de `python medicion_colas.py`.

### 3.1 Pedidos pendientes: `ColaEnlazada` (FIFO dinámica)

**Necesidad.** Los pedidos se atienden en orden de llegada. Encolar y desencolar deben
ser O(1) porque la cola se consulta en cada despacho.

**Por qué enlazada y no circular.** Un pedido no debe perderse porque la cola "se llenó".
La cola enlazada no tiene tope y crece con la demanda. Con un arreglo circular habría que
elegir una capacidad y rechazar pedidos al alcanzarla.

**Por qué no una cola de prioridad.** Todos los pedidos pesan igual; la urgencia que sí
existe (qué lote sale primero) ya la resuelve la lista de lotes ordenada por vencimiento.
Una cola de prioridad agregaría complejidad sin ninguna operación que la use.

**Por qué no un arreglo.** Desencolar del frente de un arreglo desplaza todo (O(n)).
Medido con `list.pop(0)`: 0,78 s para 100.000 pedidos frente a 0,09 s de la cola enlazada.

### 3.2 Historial de despachos: `ColaCircular` (FIFO estática)

**Necesidad.** Mostrar los últimos 5 pedidos resueltos (`CAPACIDAD_HISTORIAL`). Es un
búfer con memoria acotada: cuando se llena, sale el más antiguo.

**Por qué circular.** El tope fijo es justo lo que se quiere. Los índices avanzan en
círculo, así que no se desplazan elementos ni se reserva memoria nueva en cada pedido.
Cuando el historial se llena el sistema desencola el más antiguo antes de encolar el nuevo.

### 3.3 Devoluciones: `PilaEnlazada` (LIFO dinámica)

**Necesidad.** Revertir una devolución mal registrada. Lo natural es deshacer primero la
última: se registra, y si hubo un error, se retira.

**Por qué pila.** Apilar y desapilar son O(1) y el orden LIFO coincide con el de
"deshacer". Cada devolución entra como un lote nuevo (`DEV-n`) y la pila guarda lo
necesario para retirarlo.

### 3.4 Medición contra la biblioteca estándar

n operaciones de encolar seguidas de n de desencolar, en segundos:

| n | `ColaEnlazada` | `ColaCircular` | `deque` | `list.pop(0)` |
|---|---|---|---|---|
| 1.000 | 0,0005 | 0,0005 | 0,0001 | 0,0001 |
| 10.000 | 0,0058 | 0,0047 | 0,0008 | 0,0074 |
| 100.000 | 0,0938 | 0,0936 | 0,0109 | 0,7794 |

n apilar seguido de n desapilar:

| n | `PilaEnlazada` | `list` (append/pop) |
|---|---|---|
| 1.000 | 0,0004 | 0,0001 |
| 10.000 | 0,0039 | 0,0009 |
| 100.000 | 0,0544 | 0,0089 |

Lectura honesta:
- Las estructuras propias escalan de forma lineal, como declara su complejidad, pero son
  entre 5 y 9 veces más lentas que `deque` y `list`, escritos en C.
- `list.pop(0)` es el único que se degrada de forma cuadrática: es la razón de no usar un
  arreglo como cola.
- `ColaCircular` y `ColaEnlazada` tardan lo mismo; la circular no es más rápida, solo usa
  memoria fija y por eso encaja en el historial.

## 4. Cómo se integra con el resto del sistema

- `Producto` guarda su `ListaLotes`. La cantidad total y el próximo vencimiento se
  derivan de ella (propiedades), por lo que no pueden quedar desincronizados.
- Un producto sin existencias devuelve el vencimiento `9999-12-31`, así que al ordenar por
  vencimiento queda al final.
- Las fechas deben ser `YYYY-MM-DD`: con ese formato fijo, comparar como texto equivale a
  comparar cronológicamente. `Lote` valida el formato y que el vencimiento no sea anterior
  a la producción.

## 5. Límites conocidos

- `fusionar` no comprueba códigos duplicados entre las dos listas. `cargar_lotes_csv` los
  verifica antes de fusionar; quien llame a `fusionar` directamente debe garantizarlo.
- La carga de lotes y la de pedidos son todo o nada: si una fila es inválida no se aplica
  ninguna.
- Un pedido sin stock suficiente (o de un producto eliminado) se rechaza y sale de la cola,
  para no bloquear a los siguientes. Queda en el historial con su motivo, pero no se
  reintenta solo.
- Al deshacer una devolución cuyo lote ya se despachó por completo, la devolución sale de
  la pila de todas formas y se avisa que no se pudo revertir. Si el lote se despachó solo
  en parte, se retira lo que quedaba.
- El historial guarda solo los últimos 5 despachos; los anteriores se descartan.
- La fecha de vencimiento de `Leche Alpina` en `productos.csv` (2026-10-05) ya pasó. No
  afecta al código, pero conviene tenerlo presente en la demostración.
