# Heredity

Este proyecto tiene como objetivo calcular las probabilidades conjuntas de que los individuos en un grupo familiar específico tengan un cierto número de copias de un gen particular y si expresan un rasgo asociado con dicho gen. El programa utiliza datos genealógicos para determinar las probabilidades basadas en mutaciones, herencia genética y la expresión de rasgos.

Este programa toma un archivo CSV que contiene información genealógica y de rasgos de varios individuos. Basado en esta información y utilizando probabilidades conocidas sobre herencia genética y mutaciones, calcula las probabilidades conjuntas de que cada individuo tenga un número específico de copias del gen y si presentan o no un rasgo.

El programa genera todas las posibles combinaciones de personas que podrían tener uno o dos genes, así como aquellas que podrían presentar o no el rasgo, y luego actualiza las probabilidades basadas en estas combinaciones.

## Estructura del Proyecto
El proyecto contiene un único archivo Python:

- heredity.py: Contiene la lógica principal del programa. Incluye funciones para cargar los datos, calcular probabilidades conjuntas y normalizar los resultados.
