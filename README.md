# Proyecto de Visualización de Atenciones con BERT

Este proyecto utiliza un modelo de lenguaje basado en BERT (Bidirectional Encoder Representations from Transformers) para realizar predicciones sobre tokens enmascarados y generar visualizaciones gráficas de las puntuaciones de autoatención del modelo. Esto permite explorar cómo el modelo presta atención a diferentes partes del texto de entrada durante la predicción.

## Estructura del código
- Tokenización: El texto de entrada es tokenizado usando el AutoTokenizer de Hugging Face.
- Modelo BERT para predicciones: Se utiliza el modelo TFBertForMaskedLM de TensorFlow para predecir los posibles reemplazos del token [MASK].
- Visualización de las Atenciones: Se generan diagramas que representan las puntuaciones de autoatención en diferentes capas y cabezas del modelo. Estos diagramas muestran qué partes del texto reciben más o menos atención.