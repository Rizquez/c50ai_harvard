
class Sentence():
    """
    Sentence es una clase base abstracta que define la interfaz para las sentencias logicas. 
    Las subclases deben sobrescribir los metodos evaluate, formula, y symbols. Tambien proporciona 
    metodos de validacion y parentetizacion de expresiones.
    """

    def evaluate(self, model):
        """Evalua la sentencia logica."""
        raise Exception("nothing to evaluate")

    def formula(self):
        """Retorna la formula en formato de cadena que representa la sentencia logica."""
        return ""

    def symbols(self):
        """Retorna un conjunto de todos los simbolos en la sentencia logica."""
        return set()

    @classmethod
    def validate(cls, sentence):
        """Verifica que la sentencia sea una instancia valida de la clase `Sentence`."""

        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):
        """Asegura que una expresion este correctamente parentetizada."""

        def balanced(s):
            """Verifica si una cadena tiene parentesis balanceados."""

            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        
        if not len(s) or s.isalpha() or (s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):
    """
    Representa un simbolo proposicional como una variable logica. El metodo evaluate 
    verifica el valor de verdad del simbolo en un modelo dado, el cual es un diccionario 
    que asigna valores de verdad (True o False) a los simbolos.
    """

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        """Evalua el valor de verdad de este simbolo en el modelo dado."""
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


class Not(Sentence):
    """
    Representa una sentencia logica de negacion (¬). 
    El metodo evaluate retorna el valor de verdad negado de la sentencia contenida (operand).
    """

    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        """Evalua la negacion de la sentencia."""
        return not self.operand.evaluate(model)

    def formula(self):
        """Retorna la formula de la sentencia negada."""
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        """Retorna los simbolos utilizados en la sentencia negada."""
        return self.operand.symbols()


class And(Sentence):
    """
    Representa una conjuncion logica (∧). 
    La sentencia se evalua como True solo si todas las sentencias dentro de la conjuncion son True.
    """

    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self):
        return hash(("and", tuple(hash(conjunct) for conjunct in self.conjuncts)))

    def __repr__(self):
        conjunctions = ", ".join([str(conjunct) for conjunct in self.conjuncts])
        return f"And({conjunctions})"

    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        """Evalua la conjuncion de las sentencias."""
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        """Retorna la formula de la conjuncion."""
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula()) for conjunct in self.conjuncts])

    def symbols(self):
        """Retorna los simbolos utilizados en la conjuncion."""
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    """
    Representa una disyuncion logica (∨). 
    La sentencia se evalua como True si al menos una de las sentencias dentro de la disyuncion es True.
    """
    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(
            ("or", tuple(hash(disjunct) for disjunct in self.disjuncts))
        )

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        """Evalua la disyuncion de las sentencias."""
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        """Retorna la formula de la disyuncion."""
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join([Sentence.parenthesize(disjunct.formula()) for disjunct in self.disjuncts])

    def symbols(self):
        """Retorna los simbolos utilizados en la disyuncion."""
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    """
    Representa una implicacion logica (=>). 
    La sentencia se evalua como True si el antecedente es False o si el consecuente es True.
    """
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent)

    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        """Evalua la implicacion."""
        return ((not self.antecedent.evaluate(model)) or self.consequent.evaluate(model))

    def formula(self):
        """Retorna la formula de la implicacion."""
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        """Retorna los simbolos utilizados en la implicacion."""
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    """
    Representa una bicondicional logica (<=>). 
    Se evalua como True si ambas sentencias tienen el mismo valor de verdad.
    """
    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Biconditional) and self.left == other.left and self.right == other.right)

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        """Evalua la bicondicional."""
        return ((self.left.evaluate(model) and self.right.evaluate(model)) or (not self.left.evaluate(model) and not self.right.evaluate(model)))

    def formula(self):
        """Retorna la formula de la bicondicional."""
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        """Retorna los simbolos utilizados en la bicondicional."""
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """
    Esta funcion utiliza una tecnica de enumeracion de modelos para verificar si una base de 
    conocimiento (knowledge) implica una consulta (query). Genera todos los modelos posibles 
    asignando valores de verdad a los simbolos y verifica si la consulta es verdadera en todos 
    los modelos donde la base de conocimiento es verdadera.
    """

    def check_all(knowledge, query, symbols, model):
        """Verifica si la base de conocimiento implica la consulta, dado un modelo especifico."""

        # Si el modelo tiene una asignacion para cada simbolo
        if not symbols:

            # Si la base de conocimientos es verdadera en el modelo, la consulta tambien debe serlo
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True
        
        # En caso contrario
        else:
            
            # Elija uno de los simbolos restantes no utilizados
            remaining = symbols.copy()
            p = remaining.pop()

            # Crear un modelo en el que el simbolo sea verdadero
            model_true = model.copy()
            model_true[p] = True

            # Crear un modelo en el que el simbolo sea falso
            model_false = model.copy()
            model_false[p] = False

            # Garantizar que la vinculacion se cumple en ambos modelos
            return (check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false))

    # Obtener todos los simbolos tanto en el conocimiento como en la consulta
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Comprobar que el conocimiento implica consulta
    return check_all(knowledge, query, symbols, dict())
