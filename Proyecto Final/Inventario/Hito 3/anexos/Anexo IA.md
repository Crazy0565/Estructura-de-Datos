# Anexo de uso de herramientas de IA — Entrega 3

## Herramienta utilizada

Se utilizó Claude (Anthropic) como herramienta de asistencia durante el desarrollo de la Entrega 3. La herramienta se consultó desde una sesión con entorno de ejecución (Python 3.13, pytest y ruff).

## Propósito y alcance del uso

La IA se empleó como asistente técnico y de consulta. Su función fue apoyar el proceso de desarrollo, no tomar las decisiones académicas ni sustituir la responsabilidad del estudiante sobre el proyecto.

Entre los usos que se le dieron estuvieron:

- Consultar alternativas para implementar y organizar estructuras de datos y algoritmos.
- Solicitar explicaciones sobre fragmentos de código, errores y resultados de ejecución.
- Apoyar la identificación y corrección de errores encontrados durante las pruebas.
- Revisar posibles mejoras de rendimiento y ayudar a interpretar las mediciones.
- Apoyar la organización de la integración y la elaboración de documentación.
- Proponer y generar fragmentos de implementación y pruebas que posteriormente debían ser ejecutados y comprobados.

**Transparencia sobre la implementación:** en esta entrega, la herramienta también generó una parte importante del código y de las pruebas a partir de las indicaciones del estudiante. Por tanto, su participación no se limitó exclusivamente a corregir errores o responder preguntas. El estudiante definió el alcance, orientó el desarrollo, tomó las decisiones sobre qué incorporar, ejecutó el sistema y las verificaciones, y debe estar en capacidad de explicar y sustentar lo entregado. Esta declaración busca describir el uso de la herramienta con precisión, sin atribuirle decisiones ni responsabilidad académica.

## Actividades en las que se utilizó como apoyo

| Área | Apoyo proporcionado por la IA | Revisión o verificación realizada |
|---|---|---|
| Generación de datos | Apoyo para construir un generador de datos sintéticos de productos, lotes y pedidos. | Se verificaron el determinismo, los conteos y la carga de los datos en el sistema. |
| Árboles BST y AVL | Apoyo en la implementación de recorridos, eliminación de nodos y rotaciones. | Se ejecutaron pruebas de casos relevantes y mediciones de altura. |
| Cola de prioridad | Apoyo para implementar un montículo mínimo con comportamiento estable en empates. | Se comparó su comportamiento con `heapq` como referencia. |
| Grafos | Apoyo en la implementación de listas y matrices de adyacencia y sus operaciones. | Se verificaron las interfaces y se realizaron mediciones de memoria. |
| Algoritmos de grafos | Apoyo con BFS, DFS, componentes conexas y Dijkstra. | Se contrastaron resultados mediante pruebas y referencias independientes. |
| Plano de bodega | Apoyo para representar la bodega mediante un grafo. | Se comprobaron las distancias obtenidas. |
| Ruta de recolección | Apoyo para implementar vecino más cercano y 2-opt. | Se compararon resultados y se ajustó el criterio para evitar entregar una ruta peor que el orden de llegada. |
| Integración | Apoyo para incorporar las estructuras y funcionalidades al sistema existente. | Se ejecutaron pruebas de integración, interfaz y persistencia, además de comprobar la compatibilidad con el Hito 2. |
| Rendimiento | Apoyo para detectar y corregir un cuello de botella durante la carga de lotes. | Se midieron los tiempos antes y después del ajuste. |
| Demostración | Apoyo para preparar una demostración reproducible del criterio de éxito. | Se verificó el comportamiento FEFO y se ejecutaron pruebas para detectar posibles incumplimientos. |
| Documentación | Apoyo para organizar y redactar borradores del informe, README, reparto y guía de sustentación. | Se contrastó la documentación con el código y las mediciones disponibles. |

## Verificación

En el entorno utilizado para el desarrollo se reportaron 507 pruebas satisfactorias (490 sin `tkinter`) y una revisión de `ruff` sin observaciones en los archivos nuevos. Los tiempos y resultados de rendimiento dependen del entorno de ejecución y deben poder reproducirse en el equipo utilizado para la entrega.

La ejecución de pruebas es una evidencia de verificación, pero no reemplaza la revisión y comprensión del código por parte del estudiante. También queda pendiente la revisión cruzada de las pruebas por una persona distinta de quien participó en la implementación, de acuerdo con la regla de autoría indicada en la guía.

## Responsabilidad del estudiante

El estudiante estuvo a cargo de orientar el trabajo, definir y aprobar el alcance de las fases, decidir qué cambios incorporar, ejecutar el sistema y las pruebas, revisar los resultados y preparar la sustentación. La herramienta no tuvo acceso al equipo personal ni al repositorio local del estudiante y no asume la responsabilidad académica del trabajo.

**Participación individual adicional:** [COMPLETAR con las actividades que el estudiante realizó directamente, por ejemplo, revisión de módulos, ajustes manuales, pruebas propias o decisiones de integración. No incluir actividades que no se hayan realizado.]
