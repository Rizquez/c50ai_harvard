# Traffic Sign Recognition using CNN
Este proyecto implementa una red neuronal convolucional (CNN) para clasificar imágenes de señales de tráfico en diferentes categorías. El modelo está entrenado en un conjunto de datos de imágenes etiquetadas, donde cada imagen corresponde a una categoría de señal de tráfico.

Este proyecto está diseñado para reconocer señales de tráfico utilizando un modelo de red neuronal convolucional (CNN) construido con TensorFlow y Keras. Las imágenes de entrada son redimensionadas a 30x30 píxeles, y el modelo es capaz de clasificar las imágenes en una de 43 categorías diferentes de señales de tráfico.

El modelo sigue una arquitectura sencilla de CNN que consiste en capas convolucionales, capas de agrupamiento (pooling) y capas densas, con el fin de extraer características espaciales de las imágenes y realizar la clasificación.

## Entrenamiento del Modelo
El modelo es entrenado usando el conjunto de datos cargado desde el directorio proporcionado. Durante el entrenamiento, el conjunto de datos es dividido en un conjunto de entrenamiento y un conjunto de prueba, utilizando un 40% de los datos para las pruebas y un 60% para el entrenamiento.

El modelo será entrenado durante 10 épocas (EPOCHS=10), y el progreso del entrenamiento se muestra en la consola.

## Evaluación del Modelo
Después del entrenamiento, el modelo es evaluado en el conjunto de prueba. Los resultados de la evaluación se muestran en la consola, incluyendo la precisión del modelo sobre los datos de prueba.

## Guardado del Modelo
Si especificas un nombre de archivo en la línea de comandos, el modelo entrenado se guardará en ese archivo utilizando el formato .h5. Puedes cargar este modelo posteriormente para hacer predicciones sobre nuevas imágenes de señales de tráfico.
