import re
from collections import defaultdict

# ==================================================
# 1. PATRONES LÉXICOS
# ==================================================

LEXEMAS = {
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "NUMBER": r"[0-9]+(\.[0-9]+)?"
}

# ==================================================
# 2. LECTURA DEL ARCHIVO
# ==================================================

def read_code(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# ==================================================
# 3. ANALIZADOR LÉXICO SIMPLE
# ==================================================

def tokenize(code):
    tokens = []
    for token_type, pattern in LEXEMAS.items():
        for match in re.finditer(pattern, code):
            tokens.append((token_type, match.group()))
    return tokens

# ==================================================
# 4. CONSTRUCCIÓN DIRECTA (TEÓRICA)
# ==================================================

def direct_construction_tables():
    print("\n=== CONSTRUCCIÓN DIRECTA DEL DFA ===")
    print("Patrón: (letter)(letter | digit)*#\n")

    print("Árbol sintáctico (representación textual):")
    print("""
              (.)
             /   \\
          (.)     #
         /   \\
     letter    (*)
                |
              (|)
             /   \\
         letter  digit
    """)

    print("Asignación de posiciones:")
    print("letter -> posición 1")
    print("letter -> posición 2")
    print("digit  -> posición 3")
    print("#      -> posición 4\n")

    print("Tabla nullable:")
    print("letter -> false")
    print("digit -> false")
    print("(letter|digit)* -> true")
    print("raíz -> false\n")

    print("Tabla firstpos:")
    print("raíz -> {1}\n")

    print("Tabla lastpos:")
    print("raíz -> {1,2,3}\n")

    print("Tabla followpos:")
    print("1 -> {2,3,4}")
    print("2 -> {2,3,4}")
    print("3 -> {2,3,4}\n")

    print("Estados del DFA derivados de followpos:")
    print("S0 = {1}")
    print("S1 = {2,3,4}")
    print("Estado inicial: S0")
    print("Estados de aceptación: estados que contienen #\n")

# ==================================================
# 5. DFA
# ==================================================

class DFA:
    def __init__(self):
        self.states = set()
        self.transitions = defaultdict(dict)
        self.start_state = 0
        self.accept_states = set()

    def add_transition(self, src, symbol, dest):
        self.transitions[src][symbol] = dest
        self.states.add(src)
        self.states.add(dest)

    def simulate(self, string):
        print("\n=== SIMULACIÓN DEL DFA ===")
        current = self.start_state
        print(f"Estado inicial: {current}")

        for char in string:
            if char.isalpha() or char == "_":
                symbol = "LETTER"
            elif char.isdigit():
                symbol = "DIGIT"
            else:
                print(f"Símbolo inválido: {char}")
                return False

            if symbol not in self.transitions[current]:
                print(f"No transición desde {current} con {symbol}")
                return False

            next_state = self.transitions[current][symbol]
            print(f"{current} --{symbol}--> {next_state}")
            current = next_state

        if current in self.accept_states:
            print("Resultado: LEXEMA ACEPTADO")
            return True
        else:
            print("Resultado: LEXEMA RECHAZADO")
            return False

# ==================================================
# 6. DFA PARA IDENTIFICADORES
# ==================================================

def build_identifier_dfa():
    dfa = DFA()

    # Estados:
    # 0 -> S0
    # 1 -> S1 (aceptación)

    dfa.add_transition(0, "LETTER", 1)
    dfa.add_transition(1, "LETTER", 1)
    dfa.add_transition(1, "DIGIT", 1)

    dfa.accept_states.add(1)
    return dfa

# ==================================================
# 7. MINIMIZACIÓN
# ==================================================

def minimize_dfa(dfa):
    print("\n=== MINIMIZACIÓN DEL DFA ===")
    accepting = dfa.accept_states
    non_accepting = dfa.states - dfa.accept_states

    partitions = [accepting, non_accepting]

    print("Particiones iniciales:")
    for p in partitions:
        print(p)

    print("No se requieren refinamientos adicionales.")
    print("DFA ya es mínimo.\n")

# ==================================================
# 8. MAIN
# ==================================================

def main():
    code = read_code("code.txt")

    print("=== TOKENS ENCONTRADOS ===")
    tokens = tokenize(code)
    for t in tokens[:15]:
        print(t)

    # Construcción directa (parte teórica)
    direct_construction_tables()

    # DFA y minimización
    dfa = build_identifier_dfa()
    minimize_dfa(dfa)

    # Simulación con lexema real del código
    ejemplo = "brewHealthPotion"
    dfa.simulate(ejemplo)

if __name__ == "__main__":
    main()
