import pygame
import sys
import time
import tictactoe as ttt

# Inicializa el modulo pygame y define el tamaño de la ventana 
# del juego con un ancho de 600 pixeles y un alto de 400 pixeles
pygame.init()
size = width, height = 600, 400

# Define dos colores en formato RGB. black representa el color 
# negro, y white representa el color blanco.
black = (0, 0, 0)
white = (255, 255, 255)

# Crea una ventana con las dimensiones definidas anteriormente
screen = pygame.display.set_mode(size)

# Define tres tamaños de fuentes utilizando la fuente 
# OpenSans-Regular.ttf. Se utilizan para el titulo del 
# juego, botones y movimientos en el tablero
mediumFont = pygame.font.Font('OpenSans-Regular.ttf', 28)
largeFont = pygame.font.Font('OpenSans-Regular.ttf', 40)
moveFont = pygame.font.Font('OpenSans-Regular.ttf', 60)

# Almacena si el jugador humano elige jugar como X o O. 
# Inicialmente, es None
user = None

# Representa el estado del tablero de juego, inicializado 
# con la funcion ttt.initial_state() del modulo tictactoe.
board = ttt.initial_state()

# Bandera que indica cuando es el turno de la IA (inteligencia artificial) 
# para hacer un movimiento. Inicialmente es False
ai_turn = False

# El bucle principal se ejecuta indefinidamente mientras el programa este 
# abierto. Dentro del bucle se verifica si el usuario ha intentado cerrar 
# la ventana (evento pygame.QUIT), en cuyo caso el programa sale utilizando 
# sys.exit()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Llena la ventana con color negro antes de dibujar otros elementos sobre ella
    screen.fill(black)

    # Este condicional evaluacion la opcion para que el usuario juegue
    if user is None:

        # Dibuja el titulo
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Dibuja los botones
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Verifica si al boton se le puede dar clic
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    # Dibuja el tablero y los movimientos
    else:
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Muestra el titulo
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Turno para que juegue la IA
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Turno para que juegue el usuario
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        # Si finaliza el juego dibuja boton "Play Again" y reinicia el juego si se hace clic en el
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    # Actualiza el contenido de la pantalla con los cambios 
    # realizados en esta iteracion del bucle
    # Es necesario para que cualquier elemento dibujado se 
    # muestre en la ventana
    pygame.display.flip()
