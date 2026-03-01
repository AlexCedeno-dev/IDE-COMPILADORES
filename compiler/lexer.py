import re
import sys
from tokens import TOKEN_TYPES


class Lexer:

    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):

        position = 0

        while position < len(self.code):

            match = None

            # ignorar espacios
            if self.code[position].isspace():
                position += 1
                continue

            for token_type, pattern in TOKEN_TYPES.items():

                regex = re.compile(pattern)
                match = regex.match(self.code, position)

                if match:
                    lexeme = match.group(0)

                    self.tokens.append((token_type, lexeme))

                    position = match.end()
                    break

            if not match:
                raise SyntaxError(
                    f"Token desconocido: {self.code[position]}"
                )

        return self.tokens


# -------- ejecución desde terminal --------
if __name__ == "__main__":

    file_path = sys.argv[1]

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    for t in tokens:
        print(t)