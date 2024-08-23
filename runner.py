import pygame
import sys
import time
from minesweeper import Minesweeper, MinesweeperAI

# Definicion de las dimensiones del tablero (8x8) y el numero de minas (8)
HEIGHT = 8
WIDTH = 8
MINES = 8

# Colores RGB que se usaran para dibujar los elementos del juego (fondo, celdas, texto)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Inicializacion de todos los modulos de Pygame
# Y configuracion de una ventana de 600x400 píxeles donde se mostrara el juego
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Se cargan distintas fuentes tipograficas para mostrar textos en el juego (tamaños pequeño, mediano y grande)
OPEN_SANS = 'assets/fonts/OpenSans-Regular.ttf'
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Se calcula el tamaño del tablero en funcion del tamaño de la pantalla, dejando márgenes (padding) 
# Se calcula tambien el tamaño de cada celda del tablero
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Carga y ajusta el tamaño de las imagenes que representan una bandera (para marcar minas) y una mina
flag = pygame.image.load('assets/images/flag.png')
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load('assets/images/mine.png')
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Se inicializa el juego y la IA. 
# Minesweeper representa la logica del juego, 
# mientras que MinesweeperAI toma decisiones basadas en la informacion del tablero
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

# Lleva un registro de las celdas reveladas, las celdas marcadas y si se ha alcanzado una mina.
revealed = set() # Guarda las celdas que han sido reveladas por el jugador
flags = set() # Guarda las celdas que han sido marcadas como minas
lost = False # Un booleano que indica si el jugador ha perdido el juego al revelar una mina

# Mostrar instrucciones inicialmente
# Un booleano que indica si las instrucciones del juego deben mostrarse en pantalla
instructions = True

# El juego corre en un bucle infinito que mantiene la ventana abierta y actualiza constantemente la pantalla
while True:

    # Comprobar si el juego ha salido
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Captura eventos de Pygame, como cerrar la ventana. Si se detecta un evento de salida, el juego se cierra
    if instructions:

        # Titulo
        title = largeFont.render('Play Minesweeper', True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Reglas
        rules = [
            'Click a cell to reveal it.',
            'Right-click a cell to mark it as a mine.',
            'Mark all mines successfully to win!'
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Boton de juego
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Comprobar si se ha pulsado el boton de reproduccion
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Dibujo del tablero
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Dibujar rectangulo para celda
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Añade una mina, una bandera o un número si es necesario
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(str(game.nearby_mines((i, j))), True, BLACK)
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    # Comprobar si el botón derecho del ratón permite activar el marcado
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # Si se pulsa el botón de IA, realiza un movimiento de IA
        if aiButton.collidepoint(mouse) and not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    flags = ai.mines.copy()
                    print("No moves left to make.")
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")
            time.sleep(0.2)

        # Restablecer el estado del juego
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
            revealed = set()
            flags = set()
            lost = False
            continue

        # Movimiento hecho por el usuario
        elif not lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in flags
                            and (i, j) not in revealed):
                        move = (i, j)

    # Realizar movimientos y actualizar los conocimientos de IA
    if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)

    pygame.display.flip()
