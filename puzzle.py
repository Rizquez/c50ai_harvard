from logic import *

# Creacion de caballero y canalla (A)
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

# Creacion de caballero y canalla (B)
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

# Creacion de caballero y canalla (C)
CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),  # A debe ser o un caballero o un canalla, no puede ser ambos
    Not(And(AKnight, AKnave)),  # A no puede ser ambos (caballero y canalla)
    Biconditional(AKnight, And(AKnight, AKnave))  # A dice: "Soy ambos, caballero y canalla"
)
# A dice que es tanto un caballero como un canalla, lo cual es una contradiccion logica, 
# ya que un personaje no puede ser ambas cosas al mismo tiempo
# Se usa una bicondicional para representar que si A es un caballero (y por lo tanto dice la verdad), 
# entonces la afirmacion "soy ambos" tambien debe ser cierta (lo cual es imposible). Por lo tanto, 
# esto implica que A es un canalla, ya que su afirmacion no puede ser verdadera.


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # A es un caballero o un canalla
    Or(BKnight, BKnave),  # B es un caballero o un canalla
    Not(And(AKnight, AKnave)),  # A no puede ser ambos
    Not(And(BKnight, BKnave)),  # B no puede ser ambos
    Biconditional(AKnight, And(AKnave, BKnave))  # A dice: "Somos ambos canallas"
)
# A afirma que tanto el como B son canallas.
# Se establece la regla de que un personaje solo puede ser caballero o canalla, pero no ambos.
# La bicondicional asegura que si A es un caballero, entonces la afirmacion "somos ambos canallas" 
# debe ser verdadera, y si A es un canalla, entonces esta afirmacion es falsa.


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A es un caballero o un canalla
    Or(BKnight, BKnave),  # B es un caballero o un canalla
    Not(And(AKnight, AKnave)),  # A no puede ser ambos
    Not(And(BKnight, BKnave)),  # B no puede ser ambos
    Biconditional(AKnight, AKnight),  # A dice: "Somos del mismo tipo"
    Biconditional(BKnight, BKnave),  # B dice: "Somos de tipos diferentes"
    Biconditional(AKnight, BKnight),  # A y B son del mismo tipo
    Biconditional(AKnave, BKnave)  # Si A es canalla, entonces B tambien lo es
)
# A dice que tanto el como B son del mismo tipo (ambos caballeros o ambos canallas).
# B dice que son de tipos opuestos (uno es caballero y el otro es canalla).
# Se representa la contradiccion de las afirmaciones usando bicondicionales: si A es un caballero, 
# su afirmacion debe ser verdadera, lo que implica que B tambien es un caballero, pero la afirmacion 
# de B sugiere lo contrario, lo cual genera una paradoja que debe resolverse mediante deduccion.


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A es un caballero o un canalla
    Or(BKnight, BKnave),  # B es un caballero o un canalla
    Or(CKnight, CKnave),  # C es un caballero o un canalla
    Not(And(AKnight, AKnave)),  # A no puede ser ambos
    Not(And(BKnight, BKnave)),  # B no puede ser ambos
    Not(And(CKnight, CKnave)),  # C no puede ser ambos
    Or(AKnight, AKnave),  # A hace una afirmacion no clara
    Implication(AKnight, Or(AKnight, AKnave)),  # Si A es caballero, entonces su afirmacion es verdadera
    Implication(AKnave, Not(Or(AKnight, AKnave))),  # Si A es canalla, entonces su afirmacion es falsa
    Biconditional(BKnight, Biconditional(AKnave, AKnave)),  # B afirma lo que dijo A
    Biconditional(BKnave, Not(Biconditional(AKnave, AKnave))),  # Si B es canalla, miente sobre la afirmacion de A
    Biconditional(BKnight, CKnave),  # B dice que C es un canalla
    Biconditional(BKnave, Not(CKnave)),  # Si B es canalla, C no es un canalla
    Biconditional(CKnight, AKnight),  # C dice que A es un caballero
    Biconditional(CKnave, Not(AKnight))  # Si C es canalla, A no es un caballero
)
# A hace una afirmacion ambigua (o es un caballero o un canalla, pero no se sabe cual).
# B dice que A dijo "Soy un canalla", y tambien afirma que C es un canalla.
# C dice que A es un caballero.
# Las reglas logicas se utilizan para definir las implicaciones y contradicciones de cada afirmacion. 
# Se relacionan las afirmaciones de cada personaje con la verdad o falsedad de las otras, y el objetivo 
# es deducir quien es caballero y quien es canalla.


def main():
    """
    La funcion crea una lista con todos los simbolos que representan las posibles identidades de A, B y C.

    Tambien organiza los puzzles en una lista:
        - knowledge0
        - knowledge1
        - knowledge2
        - knowledge3

    Luego, itera sobre cada puzzle, verificando cuales de los simbolos (caballero o canalla) son ciertos en 
    cada caso utilizando la funcion model_check(), que verifica los posibles modelos que satisfacen el conjunto 
    de proposiciones logicas.
    """
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
