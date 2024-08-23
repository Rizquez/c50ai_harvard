import nltk
import sys

# Definicion de las reglas de produccion para los terminales en la gramatica
# Estas son las palabras especificas que pueden aparecer en la oracion
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Definicion de las reglas de produccion para los no terminales en la gramatica
# Estos son los simbolos que pueden ser expandidos en otros simbolos, y definen la estructura sintactica de la oracion
NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det ADJ N | NP P NP
VP -> V | V NP | V NP PP | V PP
PP -> P NP
ADJ -> Adj | Adj ADJ
"""

# Creacion de la gramatica combinando los terminales y no terminales
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)

# Inicializacion del parser (analizador sintactico) con la gramatica definida
parser = nltk.ChartParser(grammar)


def main():
    """
    Funcion principal que maneja la logica principal del programa.
    Si se proporciona un archivo como argumento de la linea de comandos,
    lee la oracion desde el archivo, de lo contrario solicita una oracion
    como entrada del usuario. La oracion se procesa, se analiza y se 
    imprimen las frases nominales.
    """

    # Si se proporciona un archivo como argumento, lee la oracion del archivo
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Convierte la oracion en una lista de palabras despues de preprocesarla
    else:
        s = input("Sentence: ")

    # Convierte la oracion en una lista de palabras despues de preprocesarla
    s = preprocess(s)

    # Intenta analizar la oracion
    try:
        # Convierte la salida del parser en una lista de arboles de analisis sintactico
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    
    # Si no se puede analizar la oracion, informa al usuario
    if not trees:
        print("Could not parse sentence.")
        return

    # Imprime cada arbol sintactico y las frases nominales que encuentra
    for tree in trees:

        # Imprime el arbol de manera estructurada
        tree.pretty_print()
        print("Noun Phrase Chunks")

        # Extrae y muestra las frases nominales
        for np in np_chunk(tree):
            print(" ".join(np.flatten())) # Convierte la frase nominal en una cadena y la imprime


def preprocess(sentence):
    """
    Convertir `sentencia` en una lista de sus palabras.
    Preprocesar la frase convirtiendo todos los caracteres a minusculas
    y eliminando cualquier palabra que no contenga al menos un caracter
    alfabetico.
    """
    # Tokeniza la oracion y la convierte en minusculas
    words = nltk.word_tokenize(sentence.lower())

    # Filtra las palabras que contienen al menos un caracter alfabetico
    return [word for word in words if any(c.isalpha() for c in word)]


def np_chunk(tree):
    """
    Devuelve una lista de todos los trozos de frases nominales del arbol de frases.
    Un fragmento de frase nominal se define como cualquier subarbol de la oracion
    cuya etiqueta es «NP» que no contiene otras frases, frases sustantivas como subarbol.
    """
    # Funcion auxiliar que determina si un subarbol es una frase nominal
    def is_np_chunk(subtree):

        # Verifica si la etiqueta del subarbol es NP
        if subtree.label() == "NP":

            # Asegura que no haya otras frases nominales dentro de este subarbol
            return not any(child.label() == "NP" for child in subtree)
        return False

    # Devuelve una lista de subarboles que cumplen con la condicion de ser frases nominales
    return [subtree for subtree in tree.subtrees(is_np_chunk)]


if __name__ == "__main__":
    main()
