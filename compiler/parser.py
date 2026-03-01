import sys
from lexer import Lexer


# =========================
# PARSER SIMPLE
# =========================

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # token actual
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # avanzar
    def advance(self):
        self.pos += 1

    # verificar token esperado
    def expect(self, token_type):

        token = self.current()

        if token is None:
            raise SyntaxError("Fin inesperado del archivo")

        if token[0] != token_type:
            raise SyntaxError(
                f"Se esperaba {token_type} y se encontró {token[0]}"
            )

        self.advance()

    # =========================
    # GRAMÁTICA SIMPLE
    # ID = VALOR ;
    # =========================
    def parse(self):

        while self.current() is not None:

            self.expect("IDENTIFIER")
            self.expect("ASSIGN")

            token = self.current()

            if token[0] not in ("NUMBER", "IDENTIFIER"):
                raise SyntaxError("Se esperaba NUMBER o ID")

            self.advance()

            self.expect("SEMICOLON")

        return True


# =========================
# EJECUCIÓN DESDE TERMINAL
# =========================

def main():

    if len(sys.argv) < 2:
        print("Uso: python parser.py archivo.txt")
        return

    file_path = sys.argv[1]

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        parser.parse()

        print("Análisis sintáctico correcto")

    except Exception as e:
        print(f" Error sintáctico: {e}")


if __name__ == "__main__":
    main()