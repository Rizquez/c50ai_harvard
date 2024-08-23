import csv
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    """
    Este es el metodo principal del programa. Su objetivo es verificar 
    los argumentos de la linea de comandos, cargar los datos, dividirlos 
    en conjuntos de entrenamiento y prueba, entrenar el modelo k-NN, hacer 
    predicciones y calcular metricas de rendimiento como sensibilidad y especificidad.
    """

    # Comprobar los argumentos de la linea de comandos
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Cargar los datos de la hoja de calculo y dividirlos en conjuntos de entrenamiento y de prueba
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Entrenar el modelo y hacer predicciones
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Imprimir resultados
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Cargar datos de compras de un archivo CSV `filename` y convertirlos en una lista de
    listas de pruebas y una lista de etiquetas. Devuelve una tupla (pruebas, etiquetas).

    Evidence debe ser una lista de listas, donde cada lista contiene los siguientes valores, 
    en orden:
    - Administrativo, un entero
    - Duracion_administrativa, un numero de coma flotante
    - Informacional, un entero
    - Informational_Duration, un numero de coma flotante
    - Relacionado con el producto, un entero
    - ProductRelated_Duration, numero de coma flotante
    - BounceRates, numero de coma flotante
    - ExitRates, numero en coma flotante
    - PageValues, un numero de coma flotante
    - SpecialDay, un numero de coma flotante
    - Mes, un indice de 0 (enero) a 11 (diciembre)
    - OperatingSystems, un entero
    - Navegador, un entero
    - Region, un entero
    - TrafficType, un entero
    - VisitorType, un entero 0 (no regresa) o 1 (regresa)
    - Weekend, un entero 0 (si es falso) o 1 (si es verdadero)

    labels debe ser la lista correspondiente de etiquetas, donde cada etiqueta
    es 1 si Ingresos es verdadero, y 0 en caso contrario.
    """
    # Listas vacias evidence y labels para almacenar los datos procesados
    evidence = []
    labels = []

    # Diccionario month_mapping para convertir los nombres de los meses en 
    # indices numericos (0 para enero, 11 para diciembre)
    month_mapping = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }

    # Abrir el archivo CSV usando el modulo csv, saltar la primera fila 
    # (encabezados) y comienzar a procesar las filas restantes
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) 

        # Cada fila se convierte en una lista de caracteristicas (evidence), 
        # donde los valores numericos se convierten adecuadamente (enteros o flotantes) 
        # y los datos categoricos (meses, tipos de visitantes, fines de semana) se mapean 
        # a enteros. Se almacena la etiqueta binaria en la lista labels
        for row in reader:
            evidence.append([
                int(row[0]),
                float(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                month_mapping[row[10]],
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                1 if row[15] == 'Returning_Visitor' else 0,
                1 if row[16] == 'TRUE' else 0
            ])
            labels.append(1 if row[17] == 'TRUE' else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Dada una lista de listas de evidencias y una lista de etiquetas, 
    devuelve un modelo k-proximo mas cercano (k=1) entrenado en los datos.
    """
    # Se crea una instancia del clasificador k-NN con k=1, lo que significa 
    # que la prediccion se basara en el vecino mas cercano
    model = KNeighborsClassifier(n_neighbors=1)

    # El modelo se entrena usando el metodo fit() con los datos de entrenamiento
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Dada una lista de etiquetas reales y una lista de etiquetas 
    predichas, devuelve una tupla (sensibilidad, especificidad).

    Se supone que cada etiqueta es un 1 (positivo) o un 0 (negativo).

    La `sensibilidad` debe ser un valor de coma flotante de 0 a 1 que 
    representa la «tasa de verdaderos positivos»: la proporcion de
    etiquetas positivas reales que se identificaron correctamente.

    La «especificidad» debe ser un valor flotante de 0 a 1 que representa 
    la «tasa de verdaderos negativos»: la proporcion de etiquetas etiquetas 
    negativas reales identificadas correctamente.
    """
    # Se cuenta cuantas veces tanto la etiqueta real como la prediccion fueron 1 (positivo)
    true_positives = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 1)

    # Se cuenta cuantas veces tanto la etiqueta real como la prediccion fueron 0 (negativo)
    true_negatives = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 0)

    # Se cuentan los casos donde el modelo fallo (es decir, la etiqueta real era 1 y la prediccion fue 0 o viceversa)
    false_negatives = sum(1 for actual, predicted in zip(labels, predictions) if actual == 1 and predicted == 0)
    false_positives = sum(1 for actual, predicted in zip(labels, predictions) if actual == 0 and predicted == 1)
    
    # Se calculan las tasas dividiendo los verdaderos positivos y negativos entre el total de positivos o negativos reales
    sensitivity = true_positives / (true_positives + false_negatives)
    specificity = true_negatives / (true_negatives + false_positives)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
