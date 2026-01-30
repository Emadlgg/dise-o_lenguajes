# =========================
# Token
# =========================
class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"{self.tipo:<15} {self.lexema:<20} (L{self.linea}, C{self.columna})"


# =========================
# Lexer
# =========================
class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.symbols = {}

        self.keywords = {
            "public", "class", "static", "void", "int", "double",
            "private", "final", "return", "if", "else", "new", "this"
        }

    def current_char(self):
        return self.code[self.pos] if self.pos < len(self.code) else None

    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1

    def tokenize(self):
        while self.current_char() is not None:
            c = self.current_char()

            # Ignorar espacios
            if c.isspace():
                self.advance()
                continue

            # Comentarios //
            if c == '/' and self.pos + 1 < len(self.code) and self.code[self.pos + 1] == '/':
                while self.current_char() and self.current_char() != '\n':
                    self.advance()
                continue

            # Identificadores y palabras reservadas
            if c.isalpha() or c == '_':
                start_col = self.column
                lexema = ""
                while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
                    lexema += self.current_char()
                    self.advance()

                if lexema in self.keywords:
                    self.tokens.append(Token("KEYWORD", lexema, self.line, start_col))
                else:
                    self.tokens.append(Token("IDENTIFIER", lexema, self.line, start_col))
                    self.symbols.setdefault(lexema, len(self.symbols) + 1)
                continue

            # Números
            if c.isdigit():
                start_col = self.column
                lexema = ""
                dots = 0
                while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
                    if self.current_char() == '.':
                        dots += 1
                    lexema += self.current_char()
                    self.advance()

                if dots <= 1:
                    self.tokens.append(Token("NUMBER", lexema, self.line, start_col))
                else:
                    self.tokens.append(Token("LEXICAL_ERROR", lexema, self.line, start_col))
                continue

            # Strings
            if c == '"':
                start_col = self.column
                self.advance()
                lexema = ""
                while self.current_char() and self.current_char() != '"':
                    lexema += self.current_char()
                    self.advance()

                if self.current_char() == '"':
                    self.advance()
                    self.tokens.append(Token("STRING", lexema, self.line, start_col))
                else:
                    self.tokens.append(Token("LEXICAL_ERROR", lexema, self.line, start_col))
                continue

            # Símbolos
            self.tokens.append(Token("SYMBOL", c, self.line, self.column))
            self.advance()

        return self.tokens


# =========================
# Programa Principal
# =========================
if __name__ == "__main__":
    with open("codigo.txt", "r", encoding="utf-8") as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    print("TOKENS ENCONTRADOS:\n")
    for t in tokens:
        print(t)

    print("\nTABLA DE SÍMBOLOS:")
    for name, idx in lexer.symbols.items():
        print(f"{idx}: {name}")
