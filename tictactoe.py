import math

# Opciones de juego y celda
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Retorna el estado inicial del tablero como una matriz de 3x3, 
    donde todas las celdas estan vacias (definidas como EMPTY). 
    Este es el tablero con el que comienza el juego.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Cuenta cuantas X y O hay en el tablero y determina quien debe 
    jugar a continuacion. Si el numero de X es menor o igual que 
    el numero de O, es el turno de X. De lo contrario, es el turno 
    de O.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    return X if x_count <= o_count else O
        

def actions(board):
    """
    Retorna un conjunto de todas las posiciones posibles en el tablero 
    donde aun no se ha jugado (es decir, las celdas que estan vacias). 
    Cada accion es representada como una tupla (i, j).
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Genera un nuevo tablero como resultado de realizar un movimiento dado por la accion (i, j). 
    Si la accion es invalida (es decir, la celda ya esta ocupada), lanza una excepcion ValueError. 
    El nuevo tablero es una copia del original, pero con el nuevo movimiento aplicado.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid action")
    
    new_board = [[board[i][j] for j in range(3)] for i in range(3)]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Verifica si hay un ganador en el tablero. Primero revisa si hay una fila, 
    columna o diagonal que contenga el mismo valor (X o O) y si no estan vacias. 
    Si hay un ganador, retorna el simbolo correspondiente (X o O). Si no hay un 
    ganador, retorna None.
    """
    for i in range(3):

        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
 
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Determina si el juego ha terminado. El juego termina si hay un ganador o 
    si todas las celdas del tablero estan llenas (empate). Retorna True si el 
    juego ha terminado y False en caso contrario.
    """
    if winner(board) is not None:
        return True
    
    if all(cell is not EMPTY for row in board for cell in row):
        return True
    
    return False


def utility(board):
    """
    Retorna un valor numerico representando el resultado del juego: 1 si X ha 
    ganado, -1 si O ha ganado, y 0 si no hay ganador (empate o juego en curso).
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Implementa el algoritmo minimax para encontrar la mejor accion posible para 
    el jugador actual (X o O). Si el juego ha terminado, retorna None. De lo 
    contrario, llama a las funciones max_value o min_value dependiendo de quien 
    es el jugador actual, y retorna la accion optima.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move

def max_value(board):
    """
    Evalua todas las posibles acciones para el jugador X utilizando recursion. 
    Intenta maximizar el valor utilitario del tablero. Si el juego ha terminado, 
    retorna el valor de utilidad. Si no, simula cada accion posible y llama a 
    min_value para predecir la mejor jugada del oponente.
    """
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_action = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_action = action
    return v, best_action


def min_value(board):
    """
    Evalua todas las posibles acciones para el jugador O. Intenta minimizar el 
    valor utilitario del tablero. Funciona de manera similar a max_value, pero 
    en este caso, el jugador intenta minimizar el valor, simulando el mejor 
    movimiento del oponente.
    """
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_action = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_action = action
    return v, best_action
