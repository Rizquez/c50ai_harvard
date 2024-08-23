import random

class Minesweeper():
    """
    Esta clase representa el juego de Minesweeper (Buscaminas). 

    Contiene una representacion del tablero, la colocacion de las 
    minas y metodos para interactuar con este tablero.
    """

    def __init__(self, height=8, width=8, mines=8):
        """Inicializa un tablero de juego con minas colocadas aleatoriamente."""

        # Variables height, width y mines con los valores proporcionados como argumentos
        self.height = height
        self.width = width
        self.mines = set()

        # Creacion de un tablero vacio (self.board) que es una matriz 2D llena de valores False, 
        # lo que indica que ninguna celda contiene una mina inicialmente
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Añadir minas aleatorias en el tablero. Usa random.randrange para generar posiciones 
        # aleatorias y verifica que las posiciones seleccionadas no tengan ya una mina
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # Al principio, el jugador no ha encontrado minas asi que almacenamos las posiciones de 
        # las minas en el conjunto self.mines y las posiciones encontradas por el jugador en 
        # self.mines_found
        self.mines_found = set()

    def print(self):
        """
        Imprime una representacion basada en texto del tablero, mostrando donde estan las minas. 
        Se representa con una "X" para las minas y un espacio vacio para las celdas libres.
        """

        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        """
        Verifica si una celda especifica contiene una mina.

        Este metodo recibe una tupla (i, j) que representa la 
        posicion en el tablero y devuelve True si hay una mina 
        en esa posicion.
        """
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Devuelve el numero de minas adyacentes a una celda dada.

        Recorre las celdas adyacentes dentro de un rango de una fila y columna 
        (es decir, las 8 celdas circundantes) y cuenta cuantas de esas celdas 
        contienen minas.

        Ignora la celda en si misma y solo cuenta las celdas dentro de los limites 
        del tablero.
        """
        # Contador de las minas cercanas
        count = 0

        # Recorrer todas las celdas de una fila y una columna
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignorar la propia celda
                if (i, j) == cell:
                    continue

                # Actualizar recuento si la celda esta dentro de los limites y es mia
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Comprueba si el jugador ha ganado el juego.

        El jugador gana si ha identificado correctamente todas las minas, 
        es decir, si el conjunto self.mines_found es igual al conjunto self.mines.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Enunciado logico sobre un juego de Buscaminas.

    Un enunciado consiste en un conjunto de casillas del tablero
    y un recuento del numero de esas casillas que son minas.
    """

    def __init__(self, cells, count):
        """
        Constructor que inicializa una oracion con un conjunto de celdas (cells) 
        y un recuento de cuantas de esas celdas contienen minas (count).
        """
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        """
        Compara dos oraciones para ver si son iguales. Devuelve True si las celdas 
        y el recuento de minas son los mismos.
        """
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """
        Devuelve una representacion en cadena de texto de la oracion, mostrando las 
        celdas y el recuento de minas.
        """
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Devuelve el conjunto de todas las celdas que se sabe que contienen minas.

        Si el numero de celdas en la oracion es igual al recuento de minas, entonces 
        todas las celdas deben ser minas.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Devuelve el conjunto de todas las celdas que se sabe que son seguras.

        Si el recuento de minas es 0, entonces todas las celdas de la oracion 
        son seguras.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Actualiza la oracion al marcar una celda especifica como una mina.

        Elimina la celda del conjunto de celdas y disminuye el recuento de minas.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Actualiza la oracion al marcar una celda especifica como segura.

        Elimina la celda del conjunto de celdas.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Esta clase representa un jugador de Minesweeper con capacidades logicas. 

    La IA usa su conocimiento del tablero para hacer movimientos inteligentes 
    y deducir que celdas son seguras o contienen minas.
    """

    def __init__(self, height=8, width=8):
        """
        Constructor que inicializa la IA.

        Inicializa el tamaño del tablero y define conjuntos vacios para almacenar 
        los movimientos realizados, las celdas que son minas y las celdas seguras.
        
        Tambien inicializa una lista vacia (self.knowledge) para almacenar las 
        oraciones que representan el conocimiento del juego.
        """

        # Fijar altura y anchura iniciales
        self.height = height
        self.width = width

        # Seguimiento de las celdas en las que se ha hecho clic
        self.moves_made = set()

        # Mantenga un registro de las celulas que se sabe que son seguras o minas
        self.mines = set()
        self.safes = set()

        # Lista de frases sobre el juego que se sabe que son ciertas
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marca una celda especifica como una mina y actualiza el 
        conocimiento en consecuencia.

        Agrega la celda al conjunto de minas y actualiza todas 
        las oraciones en el conocimiento para marcar esa celda 
        como mina.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marca una celda especifica como segura y actualiza el 
        conocimiento en consecuencia.

        Agrega la celda al conjunto de celdas seguras y actualiza 
        todas las oraciones en el conocimiento para marcar esa celda 
        como segura.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Llamada cuando el tablero del Buscaminas nos dice, para una determinada
        celda segura, cuantas celdas vecinas tienen minas en ellas.

        Esta funcion deberia:
            1) marcar la casilla como movimiento realizado
            2) marcar la casilla como segura
            3) añadir una nueva frase a la base de conocimientos de la IA basada 
            en el valor de «celda» y «recuento»
            4) marcar cualquier casilla adicional como segura o como mina si puede 
            concluirse a partir de la base de conocimientos de la IA
            5) añadir nuevas frases a la base de conocimientos de la IA si pueden 
            deducirse de los conocimientos existentes
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbors = [(cell[0] + i, cell[1] + j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)]
        neighbors = [n for n in neighbors if 0 <= n[0] < self.height and 0 <= n[1] < self.width and n not in self.moves_made]
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)
        for sentence in self.knowledge:
            known_mines = sentence.known_mines()
            known_safes = sentence.known_safes()
            for mine in known_mines:
                self.mark_mine(mine)
            for safe in known_safes:
                self.mark_safe(safe)

    def make_safe_move(self):
        """
        Devuelve una casilla segura a elegir en el tablero del Buscaminas.
        El movimiento debe ser conocido para ser seguro, y no ya un movimiento
        ya realizado.

        Esta funcion puede utilizar el conocimiento en self.mines, self.safes
        y self.moves_made, pero no debe modificar ninguno de esos valores.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Devuelve un movimiento a realizar en el tablero del Buscaminas.
        
        Debe elegir aleatoriamente entre las casillas que:
            1) no hayan sido ya elegidas
            2) no se sepa que son minas
        """
        choices = [(i, j) for i in range(self.height) for j in range(self.width) if (i, j) not in self.moves_made and (i, j) not in self.mines]
        if choices:
            return random.choice(choices)
        return None
