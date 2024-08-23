import csv
import itertools
import sys

PROBS = {

    # Probabilidades incondicionales de tener el gen
    'gene': {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    'trait': {

        # Probabilidad del rasgo dadas dos copias del gen
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probabilidad de un rasgo dada una copia del gen
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probabilidad del rasgo en ausencia de gen
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Probabilidad de mutación
    'mutation': 0.01
}


def main():
    """
    Este es el punto de entrada del programa. Verifica que el número de argumentos proporcionado en la 
    línea de comandos sea correcto (debería ser solo un archivo CSV). Luego, carga los datos del archivo 
    CSV, genera todas las combinaciones posibles de personas que pueden tener uno o dos genes y el rasgo 
    correspondiente, calcula las probabilidades conjuntas para esas combinaciones y actualiza las probabilidades 
    de cada persona. Finalmente, normaliza los resultados y los imprime.
    """

    # Verifica si el programa recibe un archivo CSV como argumento
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    # Llama a load_data para cargar los datos de los individuos y sus padres
    people = load_data(sys.argv[1])

    # Crea una estructura probabilities para almacenar las probabilidades de que cada persona tenga 0, 1 o 2 
    # copias del gen, así como la probabilidad de que tenga o no el rasgo
    probabilities = {
        person: {
            'gene': {
                2: 0,
                1: 0,
                0: 0
            },
            'trait': {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Recorre todos los conjuntos de personas que puedan tener el rasgo
    names = set(people)
    for have_trait in powerset(names):

        # Comprobar si el conjunto actual de personas infringe la información conocida
        fails_evidence = any(
            (people[person]['trait'] is not None and people[person]['trait'] != (person in have_trait)) for person in names
        )
        if fails_evidence:
            continue

        # Recorrer todos los conjuntos de personas que podrían tener el gen
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Actualizar las probabilidades con la nueva probabilidad conjunta
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Garantizar que las probabilidades suman 1
    normalize(probabilities)

    # Imprimir resultados
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Cargar datos de genes y rasgos de un archivo a un diccionario.
    Se supone que el archivo es un CSV que contiene los campos nombre, madre, padre, rasgo.
    Madre, padre deben estar ambos en blanco, o ambos ser nombres válidos en el CSV.
    Rasgo debe ser 0 o 1 si el rasgo es conocido, en blanco en caso contrario.
    """
    # Abre el archivo CSV
    # Itera sobre cada fila del archivo
    # Almacena el nombre de la persona, el nombre de sus padres (si son conocidos) y si se conoce si tienen el rasgo
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            data[name] = {
                'name': name,
                'mother': row['mother'] or None,
                'father': row['father'] or None,
                'trait': (True if row['trait'] == '1' else False if row['trait'] == '0' else None)
            }

    return data


def powerset(s):
    """Genera y retorna el conjunto potencia (todas las posibles combinaciones) de un conjunto dado s."""
    # Convierte el conjunto s en una lista
    s = list(s)

    # Utiliza itertools.chain y itertools.combinations para generar todas las combinaciones posibles 
    # de elementos en s, desde 0 hasta el número total de elementos
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Calcula y devuelve una probabilidad conjunta.

    La probabilidad devuelta debe ser la probabilidad de que:
        * todas las personas del conjunto `un_gen` tengan una copia del gen
        * todos los del conjunto `dos_genes` tengan dos copias del gen
        * todos los que no están en «un_gen» o «dos_genes» no tienen el gen
        * todos los del conjunto `have_trait` tienen el rasgo
        * todos los que no están en el conjunto `tienen_rasgo` no tienen el rasgo.
    """
    # Inicializa la probabilidad conjunta en 1.0
    probability = 1.0

    # Para cada persona, determina cuántos genes tiene en función de si están 
    # en los conjuntos one_gene o two_genes
    for person in people:

        # Determinar el número de genes que tiene la persona
        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2
        else:
            genes = 0

        # Determinar si la persona presenta el rasgo
        has_trait = person in have_trait

        # Obtener probabilidad génica
        mother = people[person]['mother']
        father = people[person]['father']

        # Si no hay padres, utilice la probabilidad incondicional
        if mother is None and father is None:
            gene_prob = PROBS['gene'][genes]

        # Si se conocen los padres, calcule la probabilidad a partir de los padres
        else:
            mother_genes = 0 if mother not in one_gene and mother not in two_genes else 1 if mother in one_gene else 2
            father_genes = 0 if father not in one_gene and father not in two_genes else 1 if father in one_gene else 2

            # Calcular la probabilidad del gen
            if genes == 0:
                gene_prob = (1 - inherit_prob(mother_genes)) * (1 - inherit_prob(father_genes))
            elif genes == 1:
                gene_prob = inherit_prob(mother_genes) * (1 - inherit_prob(father_genes)) + (1 - inherit_prob(mother_genes)) * inherit_prob(father_genes)
            else:
                gene_prob = inherit_prob(mother_genes) * inherit_prob(father_genes)

        # Obtener probabilidad de rasgo
        trait_prob = PROBS['trait'][genes][has_trait]

        # Multiplicar por la probabilidad conjunta
        probability *= gene_prob * trait_prob

    return probability


def inherit_prob(genes):
    """Devuelve la probabilidad de que un padre con un determinado número de genes transmita un gen a su hijo."""

    # Si el padre no tiene genes (0 genes), la probabilidad de heredar un gen es la probabilidad de mutación
    if genes == 0:
        return PROBS['mutation']
    
    # Si el padre tiene 1 gen, la probabilidad es 0.5 (heredar o no)
    elif genes == 1:
        return 0.5

    # Si el padre tiene 2 genes, la probabilidad de heredar un gen es 1 menos la probabilidad de mutación
    else:
        return 1 - PROBS['mutation']


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Añadir a `probabilidades` una nueva probabilidad conjunta `p`.
    Cada persona debe tener sus distribuciones «gen» y «rasgo» actualizadas.
    Qué valor de cada distribución se actualiza depende de si la persona está 
    en `have_gene` y `have_trait`, respectivamente.
    """
    # Para cada persona, determina si tiene 0, 1 o 2 genes según los conjuntos one_gene y two_genes, 
    # y actualiza la probabilidad correspondiente en probabilities
    for person in probabilities:

        # Determina si la persona tiene el rasgo según si está en have_trait 
        # y actualiza la probabilidad correspondiente
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p

        # Determinar si la persona tiene el rasgo
        probabilities[person]['trait'][person in have_trait] += p


def normalize(probabilities):
    """
    Actualizar las `probabilidades` de forma que cada distribución de probabilidad
    esté normalizada (es decir, que sume 1, con las proporciones relativas iguales).
    """

    # Para cada persona, suma todas las probabilidades de tener 0, 1 o 2 genes y divide cada 
    # valor por la suma total para normalizar las probabilidades
    for person in probabilities:
        
        # Normalizar las probabilidades de los genes
        gene_total = sum(probabilities[person]['gene'].values())
        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] /= gene_total

        # Normalizar las probabilidades de los rasgos
        trait_total = sum(probabilities[person]['trait'].values())
        for trait in probabilities[person]['trait']:
            probabilities[person]['trait'][trait] /= trait_total


if __name__ == '__main__':
    main()
