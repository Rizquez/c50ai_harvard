import sys
from crossword import *

class CrosswordCreator():
    """
    La clase CrosswordCreator maneja la creacion y resolucion de un crucigrama utilizando tecnicas 
    de CSP (Constraint Satisfaction Problem). El objetivo principal es asignar palabras a las variables 
    (ubicaciones en el crucigrama) de manera que respeten las restricciones de longitud y de superposicion 
    de letras.
    """

    def __init__(self, crossword):
        """
        Crea una nueva instancia del generador de crucigramas CSP.
        Inicializa los dominios con todas las palabras disponibles para cada variable.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Este metodo transforma una asignacion de palabras a un crucigrama en una representacion 
        de cuadricula 2D, colocando las letras de las palabras en las posiciones correspondientes 
        segun la direccion (horizontal o vertical) de cada variable.
        """
        # Se inicializa una matriz letters de tamaño self.crossword.width por self.crossword.height, 
        # donde cada posicion es None
        # Esta matriz representa la cuadricula del crucigrama
        letters = [
            [None for _ in range(self.crossword.width)] for _ in range(self.crossword.height)
        ]

        # Para cada variable y palabra en la asignacion (assignment), se determina su direccion (DOWN o ACROSS)
        for variable, word in assignment.items():
            direction = variable.direction

            # Luego, letra por letra, la palabra se coloca en la matriz letters en las coordenadas correctas, 
            # ya sea de forma horizontal (ACROSS) o vertical (DOWN)
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Este metodo imprime la cuadricula del crucigrama en la terminal, mostrando las palabras asignadas 
        en las posiciones correctas. Las celdas vacias son representadas por un espacio, y las celdas que 
        no son parte del crucigrama (como los bloques negros) son representadas por un caracter especial.
        """
        # Llama a letter_grid para generar una representacion de la cuadricula con las palabras asignadas
        letters = self.letter_grid(assignment)

        # Recorre cada posicion de la cuadricula
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                # Si la celda en la estructura del crucigrama es parte del espacio del crucigrama (True), 
                # imprime la letra correspondiente o un espacio vacio
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")

                # Si la celda no es parte del crucigrama (False), imprime un bloque solido
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Guarda la representacion grafica del crucigrama como una imagen. Usa la libreria PIL para crear una 
        imagen en blanco y negro del crucigrama, dibujando las palabras y los bloques negros. El resultado 
        se guarda en un archivo.
        """
        # Crear una imagen vacia
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Crear un lienzo en blanco
        img = Image.new(
            'RGBA',
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            'black'
        )

        # Fuente y dibujo
        font = ImageFont.truetype('assets/fonts/OpenSans-Regular.ttf', 80)
        draw = ImageDraw.Draw(img)

        # Para cada celda en la estructura del crucigrama, si la celda es parte del espacio jugable (True), 
        # se dibuja un rectangulo blanco
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)
                ]

                # Si esa celda tiene una letra asignada, se dibuja la letra centrada en la celda
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2), rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], 
                            fill="black", 
                            font=font
                        )

        # La imagen resultante se guarda en un archivo
        img.save(filename)

    def solve(self):
        """
        Este metodo realiza el proceso principal de resolucion del crucigrama. Primero aplica la 
        consistencia de nodos, luego aplica consistencia de arcos (AC-3), y finalmente utiliza 
        backtracking para encontrar una solucion consistente con las restricciones.
        """
        # Aplica la consistencia de nodos para asegurarse de que todas las variables tengan dominios 
        # que respeten sus restricciones unarias (tamaño de palabra)
        self.enforce_node_consistency()

        # Ejecuta el algoritmo AC-3 para forzar la consistencia de arcos (relaciones entre variables)
        self.ac3()

        # Finalmente, aplica backtracking para encontrar una solucion completa
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Actualiza `self.domains` para que cada variable sea consistente con el nodo.
        (Elimine cualquier valor que sea inconsistente con las restricciones unarias de una variable; 
        en este caso, la longitud de la palabra). De una variable; en este caso, la longitud de la palabra).
        """
        # Recorre cada variable y verifica si las palabras en su dominio tienen la longitud correcta
        for var in self.domains:
            words_to_remove = set()
            for word in self.domains[var]:

                # Si una palabra no tiene la longitud correcta, se añade a un conjunto temporal words_to_remove
                if len(word) != var.length:
                    words_to_remove.add(word)

            # Al final, elimina esas palabras incorrectas del dominio de la variable
            self.domains[var] -= words_to_remove

    def revise(self, x, y):
        """
        Haz que la variable `x` sea coherente con la variable `y`.
        Para ello, elimine los valores de `self.domains[x]` para los que no hay
        valor correspondiente posible para `y` en `self.domains[y]`.

        Devuelve True si se ha hecho una revision del dominio de `x`; devuelve
        False si no se ha hecho ninguna revision.
        """
        # Verifica si x y y tienen un solapamiento (una letra comun en una posicion especifica)
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False

        # Para cada palabra en el dominio de x, comprueba si tiene una letra en la posicion 
        # correcta que coincida con alguna palabra en el dominio de y
        i, j = overlap
        words_to_remove = set()
        for wx in self.domains[x].copy():
            match_found = any(wx[i] == wy[j] for wy in self.domains[y])

            # Si no se encuentra ninguna coincidencia, se elimina esa palabra del dominio de x
            # Si se realizo alguna modificacion al dominio de x, devuelve True, de lo contrario, False
            if not match_found:
                words_to_remove.add(wx)
                revised = True

        self.domains[x] -= words_to_remove

        return revised

    def ac3(self, arcs=None):
        """
        Actualiza `self.domains` de forma que cada variable sea consistente con los arcos.
        Si `arcs` es Ninguno, comienza con la lista inicial de todos los arcos del problema.
        Si no, usa `arcs` como lista inicial de arcos a hacer consistentes.

        Devuelve True si se cumple la consistencia de arcos y no hay dominios vacios;
        devuelve False si uno o mas dominios terminan vacios.
        """
        # Si no se proporcionan arcos, se generan todos los arcos posibles basados en las variables vecinas
        if arcs is None:
            arcs = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]

        # Se extraen los arcos uno por uno y se aplica el metodo revise
        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):

                # Si despues de revisar se eliminan todas las palabras del dominio de una variable, 
                # el metodo devuelve False, lo que indica un fallo
                if not self.domains[x]:
                    return False
                
                # Si el dominio se revisa con exito, se añaden nuevos arcos para seguir revisando consistencias
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Devuelve True si `assignment` esta completo (es decir, asigna un valor a cada
        variable del crucigrama); en caso contrario devuelve False.
        """
        # Simplemente verifica si el numero de variables en la asignacion es igual al 
        # numero total de variables en el crucigrama, indicando que todas las variables 
        # tienen una palabra asignada
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Devuelve True si la `asignacion` es consistente (es decir, las palabras encajan 
        en el crucigrama sin caracteres conflictivos); devuelve False en caso contrario.
        crucigrama sin caracteres conflictivos); devuelve False en caso contrario.
        """
        # Comprueba si la longitud de las palabras asignadas coincide con la longitud 
        # requerida por la variable
        if len(set(assignment.values())) < len(assignment):
            return False 
        
        # Verifica que todas las variables vecinas asignadas respeten las restricciones 
        # de superposicion de letras. Si una letra en la posicion de solapamiento no coincide, 
        # devuelve False
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if word[i] != assignment[neighbor][j]:
                        return False
                    
        return True

    def order_domain_values(self, var, assignment):
        """
        Devuelve una lista de valores en el dominio de `var`, ordenados por
        el numero de valores que descartan para las variables vecinas.
        El primer valor de la lista, por ejemplo, debe ser el que
        que descarta el menor numero de valores entre los vecinos de `var`.
        """
        # Si la asignacion esta completa, la retorna
        if self.assignment_complete(assignment):
            return assignment
        
        # Selecciona una variable no asignada usando select_unassigned_variable
        var = self.select_unassigned_variable(assignment)

        # Intenta asignar los valores del dominio ordenados por el criterio de 
        # menor conflicto
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            # Si la asignacion es consistente, realiza un backtracking recursivo 
            # con la nueva asignacion
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)

                # Si se encuentra una solucion, la retorna, de lo contrario, 
                # retrocede y prueba otra asignacion
                if result is not None:
                    return result

        return None

    def select_unassigned_variable(self, assignment):
        """
        Devuelve una variable no asignada que no forme ya parte de `asignacion`.
        Elige la variable con el minimo numero de valores restantes en su dominio. 
        Si hay empate, elige la variable con mayor grado. Si hay un empate, cualquiera 
        de las variables empatadas son aceptables valores de retorno.
        """
        # Selecciona la variable no asignada que tenga el menor numero de valores 
        # posibles en su dominio, ya que esto aumenta las probabilidades de exito 
        # en la busqueda
        return min((v for v in self.crossword.variables if v not in assignment), key=lambda var: len(self.domains[var]))

    def backtrack(self, assignment):
        """
        Usando la Busqueda de Retroceso, tome como entrada una asignacion parcial 
        para el crucigrama y devuelve una asignacion completa si es posible hacerlo.

        La `asignacion` es un mapeo de variables (claves) a palabras (valores).

        Si no es posible, devuelve Ninguno.
        """
        return list(self.domains[assignment])


def main():
    """
    El metodo main se encarga de:
        - Validar los argumentos pasados por la linea de comandos.
        - Inicializar el crucigrama y el creador del crucigrama.
        - Intentar resolver el crucigrama utilizando el metodo solve().
        - Imprimir la solucion en la terminal si se encuentra una, o 
        guardar la solucion en un archivo de imagen si se especifica un 
        archivo de salida. Si no se encuentra ninguna solucion, informa al usuario.
    """
    # Comprobar el uso
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Analizar los argumentos de la linea de comandos
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generar crucigrama
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Imprimir resultado
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
