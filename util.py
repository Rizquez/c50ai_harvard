class Node():
    """
    La clase `Node` se utiliza para representar un estado en un grafo y contiene informacion sobre como se llego 
    a ese estado. Cada nodo tiene un estado, un nodo padre (que representa el nodo anterior en el camino) y una 
    accion (la accion que llevo al nodo actual desde el nodo padre).
    """

    def __init__(self, state, parent, action):
        """
        Inicializa un nuevo nodo.

        Parametros:
        - state: El estado que este nodo representa.
        - parent: El nodo padre desde el cual se llego a este nodo (es decir, el nodo anterior en el camino).
        - action: La accion que se tomo para llegar a este nodo desde el nodo padre.

        Atributos:
        - state (objeto): Representa el estado en el grafo o problema.
        - parent (Node): Nodo anterior en el camino.
        - action (objeto): Accion que condujo desde el nodo padre hasta este nodo.
        """
        self.state = state # Estado actual representado por este nodo
        self.parent = parent # Nodo padre
        self.action = action # Accion tomada desde el nodo padre


class StackFrontier():
    """
    La clase StackFrontier implementa una frontera de busqueda basada en una pila (LIFO - Last In, First Out). 
    Se utiliza en algoritmos de busqueda en profundidad (DFS - Depth First Search). Los nodos se añaden a la 
    pila y el ultimo nodo añadido es el primero en ser removido.
    """

    def __init__(self):
        """
        Inicializa una frontera de tipo pila (LIFO - Last In, First Out).

        Atributos:
        - frontier (lista): Lista que almacena los nodos en la frontera.
        """
        self.frontier = []  # Frontera inicializada como una lista vacia

    def add(self, node):
        """
        Añade un nodo a la frontera.

        Parametros:
        - node (Node): Nodo que sera añadido a la frontera.
        """
        # Añadir nodo a la lista de frontera
        self.frontier.append(node)  

    def contains_state(self, state):
        """
        Verifica si la frontera contiene un nodo con un estado especifico.

        Parametros:
        - state (objeto): El estado que se desea verificar.

        Retorna:
        - bool: True si algun nodo en la frontera tiene el estado especificado, False en caso contrario.
        """
        # Verifica si algun nodo en la frontera tiene el estado dado
        return any(node.state == state for node in self.frontier)  

    def empty(self):
        """
        Verifica si la frontera esta vacia.

        Retorna:
        - bool: True si la frontera esta vacia, False si contiene nodos.
        """
        # Retorna True si la frontera esta vacia, False en caso contrario
        return len(self.frontier) == 0  

    def remove(self):
        """
        Elimina el ultimo nodo añadido a la frontera (comportamiento LIFO) y lo devuelve.

        Retorna:
        - node (Node): El ultimo nodo añadido a la frontera.

        Excepciones:
        - Exception: Si la frontera esta vacia, lanza una excepcion.
        """
        # Lanza una excepcion si la frontera esta vacia
        if self.empty():
            raise Exception("empty frontier")  
        
        # Toma el ultimo nodo de la lista (ultimo añadido)
        # Elimina el ultimo nodo de la lista
        # Devuelve el nodo eliminado
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1] 
            return node  


class QueueFrontier(StackFrontier):
    """
    La clase QueueFrontier hereda de StackFrontier, pero sobrescribe el metodo remove para 
    implementar una frontera basada en una cola (FIFO - First In, First Out). Se utiliza en 
    algoritmos de busqueda en amplitud (BFS - Breadth First Search). En lugar de remover el 
    ultimo nodo añadido (como en la pila), remueve el primer nodo añadido a la frontera.
    """

    def remove(self):
        """
        Elimina el primer nodo añadido a la frontera (comportamiento FIFO) y lo devuelve.

        Retorna:
        - node (Node): El primer nodo añadido a la frontera.

        Excepciones:
        - Exception: Si la frontera esta vacia, lanza una excepcion.
        """
        # Lanza una excepcion si la frontera esta vacia
        if self.empty():
            raise Exception("empty frontier")  
        
        # Toma el primer nodo de la lista (el primero que fue añadido)
        # Elimina el primer nodo de la lista
        # Devuelve el nodo eliminado
        else:
            node = self.frontier[0]  
            self.frontier = self.frontier[1:]  
            return node  

