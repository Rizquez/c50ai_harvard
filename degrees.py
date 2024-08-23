import csv
import sys
from util import Node, StackFrontier, QueueFrontier

# Mapea nombres a un conjunto de person_ids correspondientes
names = {}

# Mapea person_ids a un diccionario de: nombre, nacimiento, peliculas (un conjunto de movie_ids)
people = {}

# Mapea movie_ids a un diccionario de: titulo, año, estrellas (un conjunto de person_ids)
movies = {}


def load_data(directory):
    """
    Carga los datos desde tres archivos CSV (people.csv, movies.csv, stars.csv) 
    y los almacena en las variables globales names, people, y movies.

    - people.csv: Contiene la informacion de las personas (nombre, nacimiento, y las peliculas en las que han actuado).
    - movies.csv: Contiene la informacion de las peliculas (titulo, año y las estrellas de cada pelicula).
    - stars.csv: Relaciona personas con peliculas.
    """
    # Cargar personas
    with open(f'{directory}/people.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row['id']] = {
                'name': row['name'],
                'birth': row['birth'],
                'movies': set()
            }
            if row['name'].lower() not in names:
                names[row['name'].lower()] = {row['id']}
            else:
                names[row['name'].lower()].add(row['id'])

    # Cargar peliculas
    with open(f'{directory}/movies.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row['id']] = {
                'title': row['title'],
                'year': row['year'],
                'stars': set()
            }

    # Cargar estrellas
    with open(f'{directory}/stars.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row['person_id']]['movies'].add(row['movie_id'])
                movies[row['movie_id']]['stars'].add(row['person_id'])
            except KeyError:
                pass


def main():
    """
    Es el punto de entrada del programa. Carga los datos desde los archivos CSV y luego solicita 
    al usuario que ingrese dos nombres de actores para encontrar el camino mas corto entre ellos 
    (numero de grados de separacion). Imprime los resultados mostrando las conexiones de peliculas 
    entre los actores.

    - Llama a load_data() para cargar los datos.
    - Utiliza person_id_for_name() para obtener los IDs de los actores.
    - Llama a shortest_path() para encontrar el camino mas corto entre dos actores.
    - Imprime los resultados mostrando los actores y las peliculas que los conectan.
    """
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Cargar datos desde archivos en memoria
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]['name']
            person2 = people[path[i + 1][1]]['name']
            movie = movies[path[i + 1][0]]['title']
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Implementa un algoritmo de busqueda en amplitud (BFS) para encontrar el camino 
    mas corto entre dos actores, utilizando una cola (QueueFrontier) para gestionar 
    los nodos que se estan explorando. Si se encuentra el destino, se reconstruye el 
    camino desde el nodo objetivo hasta el nodo inicial y se retorna la lista de 
    conexiones (peliculas y actores). Si no se encuentra el camino, retorna None.
    """
    # Inicializacion de la frontera
    frontier = QueueFrontier()
    start_node = Node(state=source, parent=None, action=None)
    frontier.add(start_node)
    
    # Set de actores visitados
    explored = set()

    # Busqueda en amplitud
    while not frontier.empty():
        # Extraemos el primer nodo de la frontera
        node = frontier.remove()
        
        # Si el nodo actual es el objetivo, reconstruimos el camino
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))  # (movie_id, person_id)
                node = node.parent
            path.reverse()
            return path
        
        # Marcar el nodo como explorado
        explored.add(node.state)
        
        # Expandimos los vecinos del nodo actual
        for movie_id, person_id in neighbors_for_person(node.state):
            if person_id not in explored and not frontier.contains_state(person_id):
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)
    
    # Si no hay camino
    return None


def person_id_for_name(name):
    """
    Dada una cadena de nombre, retorna el person_id correspondiente desde el diccionario names. 
    Si hay multiples personas con el mismo nombre, solicita al usuario que elija el person_id 
    deseado. Si no se encuentra ningun ID para el nombre ingresado, retorna None.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person['name']
            birth = person['birth']
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Dado un person_id, retorna un conjunto de pares (movie_id, person_id) que representan 
    a las personas que actuaron junto a esa persona en las peliculas en las que participo.
    """
    movie_ids = people[person_id]['movies']
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]['stars']:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == '__main__':
    main()
