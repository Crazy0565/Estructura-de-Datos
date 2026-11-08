**ANEXO DE USO DE HERRAMIENTAS DE INTELIGENCIA ARTIFICIAL**
**Proyecto:** Sistema de inventario y despacho de bodega
**IS061 – Estructura de Datos · 2026-2**

**Estudiantes:** Jerónimo Mazo Restrepo, Juan Andres Sanchez Rojas

## Alcance: Desarrollo completo del proyecto (Hitos 1, 2, 3 y entrega final).

## 1. Herramientas utilizadas

Durante el desarrollo del proyecto se utilizaron herramientas de inteligencia artificial como apoyo técnico para la programación, revisión, pruebas y documentación del sistema.

Las herramientas utilizadas fueron:
- ChatGPT (OpenAI): utilizado principalmente durante el desarrollo inicial del proyecto (Hito 1), como apoyo para la implementación de estructuras de datos, algoritmos, pruebas y documentación.
- Claude (Anthropic): utilizado durante las etapas posteriores del proyecto, especialmente en los Hitos 2 y 3, como asistente técnico para el desarrollo, integración, revisión y verificación del código. Durante el Hito 2 se utilizó el modelo Claude Sonnet 5.5.
Para algunas actividades se utilizaron entornos de ejecución con Python, pytest y ruff, que permitieron comprobar el funcionamiento del código y detectar posibles errores.

## 2. Propósito y alcance del uso de inteligencia artificial

La inteligencia artificial se utilizó como herramienta de asistencia durante las diferentes etapas de construcción del sistema. Su propósito fue apoyar el desarrollo técnico, facilitar la comprensión de conceptos y contribuir a la identificación y corrección de errores, sin sustituir la responsabilidad académica del estudiante.

Entre las principales actividades realizadas con este apoyo se encuentran:
- Consulta de alternativas para implementar y organizar estructuras de datos y algoritmos.
- Generación y modificación de fragmentos de código para incorporar funcionalidades y adaptar las implementaciones a los requisitos de cada entrega.
- Implementación y revisión de arreglos dinámicos, matrices, listas ligadas, pilas y colas.
- Consulta y revisión de algoritmos de búsqueda lineal, búsqueda binaria, Bubble Sort y QuickSort.
- Apoyo en la organización de módulos y en la integración de las diferentes funcionalidades del sistema.
- Revisión de operaciones relacionadas con productos, lotes, pedidos, despachos, historial y devoluciones.
- Consultas sobre SQLite, persistencia de información e integración de la base de datos con el programa.
- Apoyo en la integración de archivos CSV para la carga y gestión de productos.
- Elaboración y revisión de pruebas automatizadas mediante pytest.
- Consulta sobre mediciones de rendimiento y comparación entre estructuras de datos propias y las disponibles en la biblioteca estándar de Python.
- Revisión y complementación de anotaciones de tipo (type hints), docstrings, comentarios y explicaciones de complejidad temporal y espacial.
- Apoyo en la elaboración, organización y revisión de la documentación técnica del proyecto.

## 3. Generación de código y participación en la implementación

Durante el desarrollo de las diferentes entregas, las herramientas de inteligencia artificial no se limitaron únicamente a explicar conceptos o sugerir modificaciones. También se utilizaron para generar fragmentos de implementación, pruebas automatizadas y propuestas de corrección a partir de las instrucciones y necesidades planteadas por el estudiante.

En algunos casos se generaron partes de código y en otros se modificaron implementaciones existentes para adaptarlas a los requisitos del proyecto, corregir errores, mejorar la organización y facilitar la integración entre módulos.

Las propuestas generadas fueron revisadas durante el desarrollo y se realizaron ajustes cuando fue necesario. Entre las correcciones identificadas se encuentran:
- Ajustes de nombres de atributos y métodos para mantener la compatibilidad entre clases y módulos.
- Correcciones en la carga y gestión de productos mediante archivos CSV.
- Ajustes en las referencias y operaciones de las matrices y estructuras de almacenamiento.
- Correcciones en pruebas automatizadas para garantizar su compatibilidad con la organización del proyecto.
- Ajustes en la integración de los módulos y en las operaciones de persistencia.
- Correcciones en los benchmarks y en las mediciones de rendimiento.
- Complementación de la documentación, anotaciones de tipo y explicaciones de complejidad.

## 4. Pruebas y verificación

Para comprobar el funcionamiento del sistema se utilizaron herramientas de pruebas automatizadas y análisis estático de código, principalmente pytest y ruff.

También se realizaron pruebas manuales desde el programa principal, verificaciones de las operaciones de las estructuras de datos, pruebas de persistencia y mediciones de rendimiento.

Entre los mecanismos de verificación utilizados se encuentran:
- Ejecución de pruebas automatizadas con pytest.
- Pruebas manuales de las funcionalidades desde el programa principal.
- Verificación de la carga, consulta y gestión de productos.
- Pruebas de escalabilidad con diferentes cantidades de elementos.
- Comparación de QuickSort con la función sorted() de Python.
- Comparación de las implementaciones propias de arreglos dinámicos con las listas de Python.
- Verificación de operaciones relacionadas con las listas, pilas y colas.
- Comprobación de la persistencia y recuperación de información mediante SQLite.
- Revisión estática de los archivos nuevos mediante ruff.
Como resultados registrados durante las diferentes etapas de desarrollo se encuentran:
- Hito 1: 23 pruebas automatizadas aprobadas.
- Hito 3: 507 pruebas satisfactorias en el entorno de ejecución utilizado, de las cuales 490 se ejecutaron sin tkinter.
- Revisión de código: ruff no reportó observaciones en los archivos nuevos revisados durante el Hito 3.
Estos resultados corresponden a ejecuciones realizadas en distintos momentos del desarrollo y no deben interpretarse como una suma de pruebas independientes. Los tiempos de ejecución y resultados de rendimiento pueden variar dependiendo del equipo, la configuración y el entorno utilizado.

La ejecución satisfactoria de las pruebas constituye una evidencia de verificación, pero no reemplaza la revisión del código ni garantiza por sí sola la ausencia de errores.

## 5. Responsabilidad y participación del estudiante

El estudiante fue responsable de orientar el desarrollo del proyecto, definir y aprobar el alcance de las funcionalidades de cada entrega, establecer los requerimientos, evaluar las propuestas generadas por las herramientas de inteligencia artificial y decidir qué modificaciones incorporar al sistema.

Asimismo, estuvo a cargo de la integración de los cambios, la ejecución del programa y las pruebas, la revisión de los resultados, la preparación de la documentación y la comprensión de las estructuras de datos, algoritmos y decisiones técnicas utilizadas.

Las herramientas de inteligencia artificial funcionaron como asistentes de programación y consulta. No tuvieron acceso directo al equipo personal ni al repositorio local del estudiante. Las propuestas y fragmentos generados fueron utilizados como apoyo durante el proceso de desarrollo, sin transferir a dichas herramientas la responsabilidad académica del trabajo.

El estudiante reconoce la importancia de comprender y poder explicar el funcionamiento del código durante la sustentación, así como de justificar las decisiones de implementación y las estructuras de datos seleccionadas.

## 6. Entregable final
Durante la preparación de la entrega final, se utilizó Claude (Anthropic), modelo Claude Sonnet, como apoyo para reorganizar la estructura de directorios y archivos del proyecto.

Se solicitó a la herramienta revisar la organización existente y proponer una reestructuración que permitiera presentar el proyecto de una manera más ordenada, clara y adecuada para su entrega académica.

Como resultado de este proceso, los archivos que anteriormente se encontraban distribuidos en diferentes ubicaciones fueron organizados en carpetas y subcarpetas según su funcionalidad y propósito, facilitando la identificación de los módulos, las pruebas, la documentación y los demás componentes del sistema.

La reorganización tuvo como objetivo mejorar la presentación, mantenibilidad y comprensión general del proyecto, sin alterar intencionalmente el funcionamiento de las funcionalidades implementadas.

El estudiante revisó la estructura resultante y verificó la organización de los archivos como parte de la preparación de la entrega definitiva.

## 7. Consideraciones finales

Este anexo reúne y consolida la información sobre el uso de herramientas de inteligencia artificial durante el desarrollo completo del proyecto, incluyendo las actividades de implementación, modificación, revisión, pruebas, integración y documentación realizadas en las diferentes entregas.

Se declara que el uso de estas herramientas tuvo un propósito de asistencia técnica y que la responsabilidad sobre la revisión, integración, verificación y presentación del proyecto corresponde al estudiante.

También se reconoce la importancia de realizar la revisión cruzada de las pruebas por una persona distinta de quien participó en su implementación, de acuerdo con las disposiciones establecidas en la guía del proyecto.