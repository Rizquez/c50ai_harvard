import os
import cv2
import sys
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Número de veces que el modelo verá todos los datos de entrenamiento durante el proceso de entrenamiento
EPOCHS = 10

# Dimensiones a las que se redimensionan todas las imágenes (30x30 píxeles)
IMG_WIDTH = 30
IMG_HEIGHT = 30

# Número total de categorías o clases (en este caso, 43 tipos de señales de tráfico)
NUM_CATEGORIES = 43

# Proporción de los datos que se usarán para las pruebas (40% en este caso)
TEST_SIZE = 0.4

# Este script está diseñado para entrenar un modelo de red neuronal convolucional (CNN) 
# para reconocer señales de tráfico a partir de imágenes. Utiliza imágenes almacenadas 
# en diferentes carpetas (cada una representando una categoría de señales de tráfico) y 
# entrena un modelo que puede clasificar imágenes en una de las categorías.

def main():
    """
    Función principal del script que ejecuta el flujo completo de entrenamiento y evaluación
    de un modelo de red neuronal convolucional para la clasificación de señales de tráfico.
    """
    # Comprobar los argumentos de la línea de comandos
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Obtener matrices de imágenes y etiquetas para todos los archivos de imagen
    images, labels = load_data(sys.argv[1])

    # Dividir los datos en conjuntos de entrenamiento y prueba
    # Convierte las etiquetas a formato categórico utilizando to_categorical 
    # de Keras y divide las imágenes y las etiquetas en conjuntos de entrenamiento 
    # y prueba usando train_test_split de scikit-learn. El tamaño del conjunto de 
    # prueba es determinado por TEST_SIZE (40%)
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Obtener un modelo de red neuronal compilado
    model = get_model()

    # Ajustar el modelo con los datos de entrenamiento
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluar el rendimiento de la red neuronal
    model.evaluate(x_test,  y_test, verbose=2)

    # Guardar el modelo en un archivo
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Cargar datos de imagen del directorio `data_dir`.

    Supongamos que `data_dir` tiene un directorio con el nombre de cada categoría, 
    numeradas de 0 hasta NUM_CATEGORIES - 1. Dentro de cada directorio de categoría 
    habrá algún número de archivos de imagen.

    Devuelve la tupla `(imágenes, etiquetas)`. imágenes` debe ser una lista de todas 
    las de las imágenes en el directorio de datos, donde cada imagen se formatea como 
    un numpy ndarray con dimensiones IMG_WIDTH x IMG_HEIGHT x 3. `labels` debería ser 
    una lista de etiquetas enteras que representen las categorías de cada una de las
    correspondientes `imágenes`.
    """
    # Carga las imágenes y etiquetas desde el directorio data_dir. Asume que cada 
    # categoría está representada por un subdirectorio numerado del 0 al 42, y que 
    # dentro de cada subdirectorio hay archivos .ppm que son las imágenes de señales 
    # de tráfico
    images = []
    labels = []

    # Flujo lógico:
    #   Recorre cada categoría (directorio)
    #   Abre cada imagen, la redimensiona a 30x30 píxeles y la añade a la lista images
    #   La etiqueta (el número de la categoría) se añade a la lista labels
    for category in range(NUM_CATEGORIES):
        category_folder = os.path.join(data_dir, str(category))
        if os.path.isdir(category_folder):
            for file in os.listdir(category_folder):
                file_path = os.path.join(category_folder, file)
                if file_path.endswith('.ppm'):
                    img = cv2.imread(file_path)
                    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                    images.append(img)
                    labels.append(category)
    
    return images, labels


def get_model():
    """
    Devuelve un modelo de red neuronal convolucional compilado. Supongamos 
    que la de la primera capa es `(IMG_WIDTH, IMG_HEIGHT, 3)`. La capa de 
    salida debe tener unidades `NUM_CATEGORIES`, una por cada categoría.
    """
    # Descripción del modelo:
    #   - Capa Conv2D: Extrae características espaciales de las imágenes (32 filtros, tamaño de filtro 3x3)
    #   - MaxPooling2D: Reduce la dimensionalidad espacial
    #   - Otra Capa Conv2D: Más características, con más filtros (64)
    #   - MaxPooling2D: Reduce la dimensionalidad nuevamente
    #   - Flatten: Aplana los datos para poder conectarlos a una capa densa
    #   - Dense: Capa totalmente conectada con 128 neuronas y activación ReLU
    #   - Dropout: Reduce el sobreajuste apagando aleatoriamente neuronas durante el entrenamiento
    #   - Salida Dense: Tiene tantas unidades como categorías y usa softmax para predecir probabilidades de cada clase
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # Compilación del modelo: Usa el optimizador adam, la función de pérdida 
    # categorical_crossentropy y la métrica de evaluación es la precisión (accuracy)
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


if __name__ == "__main__":
    main()
