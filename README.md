# Crossword CSP Solver
Este proyecto es un generador y solucionador de crucigramas basado en técnicas de CSP (Constraint Satisfaction Problem). Se utiliza para crear y resolver crucigramas dados una estructura y un conjunto de palabras. El objetivo es asignar palabras a las ubicaciones del crucigrama respetando restricciones de longitud y superposición de letras. El programa implementa varios algoritmos como consistencia de nodos, consistencia de arcos (AC-3), y backtracking para encontrar soluciones válidas.

## Archivos Principales

### generate.py
- Este archivo contiene la lógica principal del programa para resolver crucigramas.
- Se encarga de leer la estructura del crucigrama y la lista de palabras, resolver el crucigrama utilizando algoritmos CSP y mostrar o guardar el resultado.

### crossword.py
- Este archivo define las clases principales utilizadas para representar el crucigrama y las variables.
- Incluye la clase Variable, que representa las palabras que deben ser ubicadas en el crucigrama, y la clase Crossword, que representa la estructura del crucigrama y gestiona las variables y sus solapamientos.