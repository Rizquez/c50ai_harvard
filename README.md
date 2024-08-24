# PageRank
Este proyecto implementa el algoritmo de PageRank, que calcula la importancia de las páginas web en un corpus de documentos HTML. La importancia se determina a partir de los enlaces entre las páginas utilizando dos enfoques: muestreo aleatorio y un método iterativo basado en las ecuaciones del algoritmo original de PageRank.

El algoritmo de PageRank funciona asignando a cada página un valor que refleja su "importancia" basado en los enlaces que recibe. Este valor se distribuye de manera proporcional a las páginas enlazadas por cada página, lo que simula el comportamiento de un usuario que navega aleatoriamente por la web.

El algoritmo puede tardar más tiempo en converger dependiendo del tamaño del corpus y la complejidad de los enlaces entre páginas. El valor de convergencia para el método iterativo se establece cuando la diferencia en los valores de PageRank entre iteraciones sucesivas es menor a 0.001.

## Estructura del Proyecto

El archivo principal del proyecto es `pagerank.py`, el cual realiza las siguientes tareas:

- Crawl (exploración del corpus): Lee los archivos HTML de un directorio específico y construye un diccionario con las páginas y sus enlaces salientes.
- Transition Model: Define un modelo de transición basado en un factor de amortiguación (damping factor) para simular el comportamiento del usuario navegando en la web.
- PageRank con muestreo: Usa un enfoque de simulación basado en muestras aleatorias para calcular los valores de PageRank de cada página.
- PageRank con iteración: Calcula los valores de PageRank de manera determinística utilizando la ecuación de PageRank iterativamente hasta que los valores convergen.
