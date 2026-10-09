# Resultados — Tarea 5

## Medición

La cuenta se hizo con los avances de los punteros, siguiendo la regla de la guía. En liebre y tortuga se cuentan tres avances por vuelta: uno del puntero lento y dos del rápido.

| Nodos | Dos pasadas | Liebre y tortuga |
|---:|---:|---:|
| 1.001 | 1.501 | 1.500 |
| 10.001 | 15.001 | 15.000 |
| 100.001 | 150.001 | 150.000 |

## Lectura de los resultados

Los dos métodos hacen una cantidad parecida de avances, alrededor de una vez y media el número de nodos. La ventaja de liebre y tortuga es que encuentra el centro en una sola pasada por la cadena, sin tener que contar primero y volver a empezar. Esto sirve cuando interesa recorrer la estructura una sola vez.

En dos pasadas se entra desde la cabeza dos veces: una para contar y otra para llegar al centro. En liebre y tortuga solo se inicia el recorrido una vez, aunque el puntero rápido avanza dos enlaces por vuelta.

En la lista sencilla, antes de cambiar `actual.siguiente` hay que guardar el siguiente nodo en una variable, porque si no se pierde el resto de la cadena. En la doble, al invertir se intercambian los enlaces `siguiente` y `anterior` de cada nodo.

## Reparto del trabajo

Trabajo realizado individualmente: implementación de las dos estructuras, pruebas, mediciones y redacción de este archivo.
