
class Variable():
    """
    Representa una variable en el crucigrama, que puede ser una palabra
    que se coloca horizontalmente (across) o verticalmente (down).
    
    Atributos:
    - i (int): Coordenada de fila donde comienza la variable (palabra).
    - j (int): Coordenada de columna donde comienza la variable (palabra).
    - direction (str): Dirección de la variable, puede ser 'across' (horizontal) o 'down' (vertical).
    - length (int): Longitud de la palabra.
    - cells (list of tuples): Lista de las celdas ocupadas por la palabra en el crucigrama.
    """

    # Se definen dos constantes ACROSS y DOWN que 
    # representan las direcciones posibles de una palabra: 
    # - horizontal
    # - vertical
    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """
        Inicializa una nueva variable con un punto de inicio, dirección y longitud.

        Args:
        - i (int): Fila inicial de la palabra.
        - j (int): Columna inicial de la palabra.
        - direction (str): Dirección de la palabra (Variable.ACROSS o Variable.DOWN).
        - length (int): Longitud de la palabra.
        """
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length

        # Calcula las celdas que ocupará la palabra
        self.cells = []
        for k in range(self.length):

            # Si la palabra es vertical, incrementa la fila; si es horizontal, incrementa la columna
            self.cells.append(
                (
                    self.i + (k if self.direction == Variable.DOWN else 0), 
                    self.j + (k if self.direction == Variable.ACROSS else 0)
                )
            )

    def __hash__(self):
        """Permite usar la clase en estructuras que requieren hashing, como conjuntos."""
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        """
        Define la igualdad entre dos variables.

        Dos variables son iguales si tienen la misma posición inicial, dirección y longitud.
        """
        return (
            (self.i == other.i) and (self.j == other.j) and (self.direction == other.direction) and (self.length == other.length)
        )

    def __str__(self):
        """Retorna una representación en forma de cadena para la variable."""
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        """Retorna una representación detallada de la variable, útil para depuración."""
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():
    """
    Representa un crucigrama con una estructura y un conjunto de palabras posibles.

    Atributos:
    - height (int): Altura del crucigrama.
    - width (int): Ancho del crucigrama.
    - structure (list of list of bool): Estructura del crucigrama, donde True representa una celda vacía y False una celda bloqueada.
    - words (set of str): Conjunto de palabras que se pueden usar para llenar el crucigrama.
    - variables (set of Variable): Conjunto de variables (palabras) del crucigrama.
    - overlaps (dict of tuple -> tuple): Diccionario que mapea pares de variables a sus índices de solapamiento (si lo hay).
    """

    def __init__(self, structure_file, words_file):
        """
        Inicializa el crucigrama a partir de un archivo de estructura y un archivo de palabras.

        Parametros:
        - structure_file (str): Ruta al archivo que contiene la estructura del crucigrama.
        - words_file (str): Ruta al archivo que contiene la lista de palabras.
        """

        # Cargar la estructura del crucigrama desde un archivo
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            # Convertir la estructura en una matriz de booleanos
            self.structure = []
            for i in range(self.height):
                row = []
                for j in range(self.width):

                    # Espacios fuera de los límites se consideran bloqueados
                    if j >= len(contents[i]):
                        row.append(False)

                    # Representa un espacio vacío en el crucigrama
                    elif contents[i][j] == "_":
                        row.append(True) 

                    # Representa una celda bloqueada
                    else:
                        row.append(False) 

                self.structure.append(row)

        # Cargar la lista de palabras desde el archivo
        with open(words_file) as f:
            self.words = set(f.read().upper().splitlines())

        # Determinar las variables del crucigrama
        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):

                # # Identificar palabras verticales
                starts_word = (
                    self.structure[i][j] and (i == 0 or not self.structure[i - 1][j])
                )
                if starts_word:
                    length = 1
                    for k in range(i + 1, self.height):
                        if self.structure[k][j]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.DOWN,
                            length=length
                        ))

                # Identificar palabras horizontales
                starts_word = (
                    self.structure[i][j] and (j == 0 or not self.structure[i][j - 1])
                )
                if starts_word:
                    length = 1
                    for k in range(j + 1, self.width):
                        if self.structure[i][k]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.ACROSS,
                            length=length
                        ))

        # Calcula los solapamientos de cada palabra
        # Para cualquier par de variables v1, v2, su solapamiento es:
        #   Ninguna, si las dos variables no se solapan; o
        #   (i, j), si el carácter i de v1 se solapa con el carácter j de v2
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:
                    # Si hay intersección, determinar en qué índice de cada palabra ocurre
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )

    def neighbors(self, var):
        """
        Dada una variable, devuelve el conjunto de variables que se solapan con ella.
        
        Parametros:
        - var (Variable): La variable para la cual se buscan los vecinos (variables solapadas).

        Retorna:
        - set of Variable: Conjunto de variables que se solapan con la variable dada.
        """
        return set(
            v for v in self.variables if v != var and self.overlaps[v, var]
        )
