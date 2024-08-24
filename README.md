# Shopping Classifier
Este proyecto implementa un modelo de clasificación utilizando un algoritmo de K-Vecinos más Cercanos (k-NN) para predecir si un visitante de un sitio web generará ingresos basados en sus comportamientos de navegación.

El proyecto lee datos de comportamiento de usuarios en un sitio web desde un archivo CSV, los procesa y utiliza un modelo de clasificación k-NN (con k=1) para predecir si esos usuarios realizarán una compra. La predicción se basa en diversas características del comportamiento del usuario, como el tiempo pasado en diferentes tipos de páginas, tasas de abandono, el sistema operativo que usan, y si es un visitante recurrente.

## Estructura del Código
El código se divide en las siguientes funciones principales:

- main(): Controla el flujo del programa, gestionando la lectura de datos, la división de los conjuntos de entrenamiento y prueba, el entrenamiento del modelo, y la evaluación de los resultados.
- load_data(filename): Carga los datos desde un archivo CSV y los convierte en listas de características (evidence) y etiquetas (labels). Procesa variables categóricas como meses y tipos de visitantes.
- train_model(evidence, labels): Entrena un modelo k-NN con k=1 usando las características (evidence) y etiquetas (labels) proporcionadas.
- evaluate(labels, predictions): Calcula la sensibilidad (True Positive Rate) y la especificidad (True Negative Rate) del modelo, comparando las etiquetas reales con las predicciones.
