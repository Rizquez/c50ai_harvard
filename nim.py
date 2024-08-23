import time
import random


class Nim():
    """
    Esta clase implementa la lógica del juego Nim.

    Nim es un juego en el que los jugadores se turnan para quitar elementos 
    de pilas. En cada turno, un jugador debe elegir una pila y quitar al menos 
    un elemento de esa pila. El jugador que se queda sin movimientos pierde.
    """

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Inicializar tablero de juego.

        Cada tablero tiene:
        - `piles`: una lista de cuántos elementos quedan en cada pila
        - `player` 0 o 1 para indicar el turno de cada jugador
        - `winner`: Ninguno, 0 o 1 para indicar quién es el ganador
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) toma una lista `piles` como entrada
        y devuelve todas las acciones disponibles `(i, j)` en ese estado.

        La acción `(i, j)` representa la acción de eliminar `j` elementos
        de la pila `i` (donde las pilas tienen índice 0).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.otro_jugador(jugador) devuelve el jugador que no es
        jugador. Asume que `player` es 0 o 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Cambia el jugador actual por el otro jugador.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Realiza el movimiento `acción` para el jugador actual.
        La acción debe ser una tupla `(i, j)`.
        """
        pile, count = action

        # Comprobación de errores
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Actualizar pila
        self.piles[pile] -= count
        self.switch_player()

        # Comprobar si hay un ganador
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():
    """
    Esta clase implementa la IA que utiliza el algoritmo Q-Learning para aprender 
    a jugar Nim. Tiene atributos y métodos para actualizar valores Q, seleccionar 
    acciones, y mejorar con la experiencia.
    """

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Inicializa la IA con un diccionario de aprendizaje Q vacío,
        una tasa alfa (de aprendizaje) y una tasa épsilon.

        El diccionario de aprendizaje Q asigna pares `(estado, acción)` 
        a un valor Q (un número).

        - El `estado` es una tupla de pilas restantes, por ejemplo (1, 1, 4, 4)
        - acción` es una tupla `(i, j)` para una acción
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Actualizar el modelo de aprendizaje Q, dado un estado anterior, 
        una acción realizada en ese estado, un nuevo estado resultante, 
        y la recompensa recibida por realizar esa acción.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Devuelve el valor Q para el estado `state` y la acción `action`.
        Si aún no existe ningún valor Q en `self.q`, devuelve 0.
        """
        # Convertimos el estado a una tupla para poder usarlo como clave en el diccionario
        key = (tuple(state), action)

        # Devolvemos el valor Q si existe, de lo contrario devolvemos 0
        return self.q.get(key, 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Actualiza el valor Q para el estado `state` y la acción `action`.
        dado el valor Q anterior `old_q`, una recompensa actual `reward`,
        y un estiamte de recompensas futuras `future_rewards`.

        Utiliza la fórmula

        Q(s, a) <- valor estimado antiguo + alfa * (nuevo valor estimado - valor estimado antiguo)

        donde `valor estimado antiguo` es el valor Q anterior, `alfa` es la 
        tasa de aprendizaje, y `nuevo valor estimado` es la suma de la recompensa 
        actual y las recompensas futuras estimadas.
        """
        # Calculamos la nueva estimacion del valor Q
        new_q = old_q + self.alpha * (reward + future_rewards - old_q)

        # Actualizamos el diccionario de valores Q
        self.q[(tuple(state), action)] = new_q

    def best_future_reward(self, state):
        """
        Dado un estado `state`, considera todos los posibles pares 
        `(state, action)` disponibles en ese estado y devuelve el 
        máximo de todos sus valores Q.

        Usa 0 como valor Q si un par `(estado, acción)` no tiene 
        valor Q en `self.q`.
        
        Q en `self.q`. Si no hay acciones disponibles en estado`, 
        devuelve 0.
        """
        # Obtenemos todas las acciones posibles para el estado actual
        possible_actions = Nim.available_actions(state)
        if not possible_actions:
            return 0
        
        # Buscamos la mejor recompensa futura
        return max([self.get_q_value(state, action) for action in possible_actions], default=0)

    def choose_action(self, state, epsilon=True):
        """
        Dado un estado `state`, devuelve una acción `(i, j)` a tomar.

        Si `epsilon` es `False`, entonces devuelve la mejor acción
        disponible en el estado (la que tenga el valor Q más alto,
        usando 0 para pares que no tienen valores Q).

        Si `epsilon` es `True`, entonces con probabilidad
        elige una acción disponible al azar,
        en caso contrario, elige la mejor acción disponible.

        Si varias acciones tienen el mismo valor Q, cualquiera de esas 
        opciones es un valor de retorno aceptable.
        """
        possible_actions = Nim.available_actions(state)
        if not possible_actions:
            return None

        if epsilon and random.random() < self.epsilon:

            # Elegimos una accion al azar
            return random.choice(list(possible_actions))
        else:
            # Elegimos la mejor accion basada en el valor Q
            q_values = {action: self.get_q_value(state, action) for action in possible_actions}
            max_q = max(q_values.values())
            
            # Elegimos una de las mejores acciones al azar si hay empates
            best_actions = [action for action, q in q_values.items() if q == max_q]
            return random.choice(best_actions)


def train(n):
    """
    Entrena la IA jugando `n` juegos contra sí misma.
    """

    player = NimAI()

    # Jugar n juegos
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Seguimiento del último movimiento realizado por cualquiera de los jugadores
        last = {
            0: {'state': None, 'action': None},
            1: {'state': None, 'action': None}
        }

        # Bucle de juego
        while True:

            # Seguimiento del estado actual y de la acción
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Seguimiento del último estado y acción
            last[game.player]['state'] = state
            last[game.player]['action'] = action

            # Moverse
            game.move(action)
            new_state = game.piles.copy()

            # Cuando termine el juego, actualiza los valores de Q con las recompensas
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]['state'],
                    last[game.player]['action'],
                    new_state,
                    1
                )
                break

            # Si el juego continúa, aún no hay recompensas
            elif last[game.player]['state'] is not None:
                player.update(
                    last[game.player]['state'],
                    last[game.player]['action'],
                    new_state,
                    0
                )

    print("Done training")

    # Devuelve la IA entrenada
    return player


def play(ai, human_player=None):
    """
    Juega una partida humana contra la IA.
    `human_player` se puede establecer en 0 o 1 
    para especificar si jugador humano se mueve 
    primero o segundo.
    """

    # Si no hay orden de los jugadores, elige el orden de los humanos al azar
    if human_player is None:
        human_player = random.randint(0, 1)

    # Crear un nuevo juego
    game = Nim()

    # Bucle de juego
    while True:

        # Imprimir el contenido de las pilas
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Calcular las acciones disponibles
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Deja que los humanos se muevan
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Haz que la IA haga un movimiento
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Moverse
        game.move((pile, count))

        # Comprobar ganador
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = 'Human' if game.winner == human_player else 'AI'
            print(f"Winner is {winner}")
            return
