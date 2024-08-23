import os
import re
import sys
import random

# Factor de amortiguacion, normalmente establecido en 0.85
# Representa la probabilidad de seguir un enlace en la pagina actual
DAMPING = 0.85

# Numero de muestras que se utilizan en el metodo de muestreo de PageRank
SAMPLES = 10000


def main():
    """
    Este metodo es el punto de entrada principal del programa. 
    
    Verifica que se proporcione el argumento de la linea de comandos, llama a las funciones crawl, 
    sample_pagerank e iterate_pagerank para calcular los valores de PageRank para las paginas de un 
    corpus dado y luego imprime los resultados.
    """
    # Comprobamos si hay exactamente un argumento de la linea de comandos (el directorio del corpus)
    # Si no, termina el programa con un mensaje de error
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    # Llamamos a crawl para generar un diccionario que represente las paginas HTML en el directorio y sus enlaces
    corpus = crawl(sys.argv[1])

    # Calculamos los valores de PageRank utilizando la funcion sample_pagerank basada en el muestreo aleatorio y los imprime
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # Calculamos los valores de PageRank utilizando la funcion iterate_pagerank basada en la iteracion y los imprime
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Explora un directorio que contiene archivos HTML, identifica los enlaces en cada pagina y construye un diccionario. 
    Cada clave es una pagina, y el valor asociado es un conjunto de paginas que son enlazadas por la pagina clave.

    Retorna:
    - Un diccionario donde cada clave es una pagina, y su valor es un conjunto de paginas a las que enlaza.
    """
    # Diccionario para almacenar los enlaces de cada pagina
    pages = dict()

    # Iteracion sobre todos los archivos en el directorio
    # Si un archivo no es HTML, lo omite
    for filename in os.listdir(directory):
        if not filename.endswith('.html'):
            continue

        # Abrimos cada archivo HTML y lee su contenido
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()

            # Usamos una expresion regular para encontrar todos los enlaces <a href="..."> en la pagina
            # Y almacenamos los enlaces en el diccionario, asegurandose de excluir los enlaces que apuntan a la propia pagina
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Filtramos los enlaces para incluir solo aquellos que apuntan a otras paginas dentro del corpus 
    # (que tambien estan en el diccionario)
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Devuelve una distribucion de probabilidad sobre que pagina visitar 
    a continuacion dada la pagina actual.

    Con probabilidad `damping_factor`, elige un enlace al azar
    enlazado por `pagina`. Con probabilidad `1 - factor_amortiguacion`, 
    elige un enlace aleatorio de entre todas las paginas del corpus.
    """
    # Obtenemos el total de paginas en el corpus
    total_pages = len(corpus)
    
    # Si la pagina no contiene enlaces, distribuye la probabilidad uniformemente entre todas las paginas del corpus
    probabilities = dict()
    if len(corpus[page]) == 0:
        for p in corpus:
            probabilities[p] = 1 / total_pages

    # Si la pagina contiene enlaces
    else:

        # Asigna una probabilidad de (1 - damping_factor) / numero total de paginas para seleccionar una pagina al 
        # azar en todo el corpus
        for p in corpus:
            probabilities[p] = (1 - damping_factor) / total_pages

        # Asigna una probabilidad de damping_factor / numero de enlaces de la pagina para cada pagina enlazada
        for link in corpus[page]:
            probabilities[link] += damping_factor / len(corpus[page])
    
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Devuelve los valores de PageRank de cada pagina mediante el muestreo 
    de `n` paginas segun el modelo de transicion, empezando por una pagina 
    al azar.

    Devuelve un diccionario en el que las claves son los nombres de las paginas 
    y los valores son su valor de PageRank estimado (un valor entre 0 y 1). Todos 
    los valores de PageRank deben sumar 1.
    """
    # Diccionario con todas las paginas del corpus, asignandoles inicialmente un valor de 0
    pagerank = {page: 0 for page in corpus}

    # Seleccion de pagina al azar
    page = random.choice(list(corpus.keys()))

    # Iteracion sobre n simulacion de navegacion, en esta iteracion vamos:
    #   - Incrementa el contador de la pagina actual
    #   - Usa transition_model para determinar las probabilidades de transicion a otras paginas
    #   - Elige la siguiente pagina aleatoriamente de acuerdo con las probabilidades calculadas
    for _ in range(n):
        pagerank[page] += 1
        probabilities = transition_model(corpus, page, damping_factor)
        pages = list(probabilities.keys())
        probabilities = list(probabilities.values())
        page = random.choices(pages, weights=probabilities, k=1)[0]

    # Dividimos el valor de cada pagina por n para obtener la proporción final, 
    # de modo que todos los valores sumen 1
    for page in pagerank:
        pagerank[page] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Devuelve los valores de PageRank de cada pagina actualizando 
    iterativamente PageRank hasta la convergencia.

    Devuelve un diccionario en el que las claves son los nombres 
    de las paginas y los valores son su valor de PageRank estimado 
    (un valor entre 0 y 1). Todos los valores de PageRank deben sumar 1.
    """
    # Obtenemos el total de paginas en el corpus
    total_pages = len(corpus)

    # Inicializamos el PageRank de cada pagina con un valor uniforme (1 dividido por el numero total de paginas)
    pagerank = {page: 1 / total_pages for page in corpus}
    new_pagerank = pagerank.copy()

    # Establecemos una bandera converged en False para comenzar la iteracion y en cada iteracion, por cada pagina:
    #   - Calcula el nuevo valor de PageRank como la suma del valor amortiguado por el damping factor y los PageRank 
    #     de las paginas que enlazan hacia ella, ajustado por el numero de enlaces salientes de esas paginas
    #   - Verifica si los nuevos valores de PageRank han convergido comparando las diferencias con los valores anteriores 
    #     (si la diferencia es menor a 0.001, se considera convergido)
    converged = False
    while not converged:
        converged = True
        for page in corpus:
            rank = (1 - damping_factor) / total_pages
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    rank += damping_factor * (pagerank[possible_page] / len(corpus[possible_page]))
                if len(corpus[possible_page]) == 0:
                    rank += damping_factor * (pagerank[possible_page] / total_pages)
            new_pagerank[page] = rank

        for page in pagerank:
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False

        pagerank = new_pagerank.copy()

    return pagerank


if __name__ == "__main__":
    main()
