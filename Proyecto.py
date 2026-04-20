KEYWORDS = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "int": "INT_TYPE",
    "float": "FLOAT_TYPE",
    "bool": "BOOL_TYPE",
    "string": "STRING_TYPE",
    "Read": "READ",
    "Write": "WRITE",
    "return": "RETURN"
}


OPERATORS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULT",
    "/": "DIV",
    ">": "GT",
    "<": "LT",
    "=": "ASSIGN",
    "==": "EQ",
    "!=": "NEQ",
    ">=": "GTE",
    "<=": "LTE",
    "#": "HASHTAG"
}

SYMBOLS = {
    "(": "LPAREN",
    ")": "RPAREN",
    ":": "COLON",
    ",": "COMMA"
}

class Token:
    def __init__(self, type_, value, line, col_start, col_end):
        self.type = type_
        self.value = value
        self.line = line
        self.col_start = col_start
        self.col_end = col_end

    def __str__(self):
        if self.value is not None:
            return f"{self.type}({self.value}) [{self.line}:{self.col_start}-{self.col_end}]"
        return f"{self.type} [{self.line}:{self.col_start}-{self.col_end}]"

class Lexer:
    def __init__(self, text):
        self.lines = text.splitlines()
        self.line_num = 0
        self.tokens = []
        self.errors = []
        self.indent_stack = [0]  


    def tokenize(self):
        for raw_line in self.lines:
            self.line_num += 1
            self.process_line(raw_line)

        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token("DEDENT", None, self.line_num, 1, 1))

        self.tokens.append(Token("EOF", None, self.line_num, 1, 1))
        return self.tokens

    def process_line(self, raw_line):
        i = 0
        col = 1

        spaces = 0
        while i < len(raw_line) and raw_line[i] == " ":
            spaces += 1
            i += 1

        self.handle_indentation(spaces)

        if i >= len(raw_line) or raw_line[i] == "#":
            return

        while i < len(raw_line):
            ch = raw_line[i]

            if ch.isspace():
                i += 1
                col += 1
                continue

            start_col = col

            if ch.isalpha() or ch == "_":
                lex = ""
                while i < len(raw_line) and (raw_line[i].isalnum() or raw_line[i] == "_"):
                    lex += raw_line[i]
                    i += 1
                    col += 1

                if len(lex) > 31:
                    self.errors.append(
                        f"line {self.line_num}, col {start_col}: ERROR identificador muy largo"
                    )
                    lex = lex[:31]

                token_type = KEYWORDS.get(lex, "ID")
                self.tokens.append(Token(token_type, lex, self.line_num, start_col, col - 1))
                continue

            if ch.isdigit():
                num = ""
                is_float = False

                while i < len(raw_line) and (raw_line[i].isdigit() or raw_line[i] == "."):
                    if raw_line[i] == ".":
                        if is_float:
                            break
                        is_float = True
                    num += raw_line[i]
                    i += 1
                    col += 1

                token_type = "FLOAT" if is_float else "INT"
                self.tokens.append(Token(token_type, num, self.line_num, start_col, col - 1))
                continue

            if ch == '"':
                i += 1
                col += 1
                value = ""

                while i < len(raw_line) and raw_line[i] != '"':
                    value += raw_line[i]
                    i += 1
                    col += 1

                if i >= len(raw_line):
                    self.errors.append(
                        f"line {self.line_num}, col {start_col}: ERROR cadena sin cerrar"
                    )
                    return

                i += 1
                col += 1
                self.tokens.append(Token("STRING", value, self.line_num, start_col, col - 1))
                continue

            two = raw_line[i:i+2]
            if two in OPERATORS:
                self.tokens.append(Token(OPERATORS[two], two, self.line_num, col, col + 1))
                i += 2
                col += 2
                continue

            if ch in OPERATORS:
                self.tokens.append(Token(OPERATORS[ch], ch, self.line_num, col, col))
                i += 1
                col += 1
                continue

            if ch in SYMBOLS:
                self.tokens.append(Token(SYMBOLS[ch], ch, self.line_num, col, col))
                i += 1
                col += 1
                continue
            self.errors.append(
                f"line (self.line_num), col {col}: error, el caracter es inesperado '{ch}'"
            )
    
    def handle_indentation(self, spaces):
        current = self.indent_stack[-1]

        if spaces > current:
            self.indent_stack.append(spaces)
            self.tokens.append(Token("INDENT", None, self.line_num, 1, spaces))
        elif spaces < current:
            while self.indent_stack and spaces < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token("DEDENT", None, self.line_num, 1, spaces))
        if self.indent_stack[-1] != spaces:
            self.errors.append(
                f"line {self.line_num}, col 1: error de indentacion invalida"
            )

def summarize_tokens(tokens, errors):
    summary = {
        "KEYWORDS": 0,
        "ID": 0,
        "INT": 0,
        "FLOAT": 0,
        "STRING": 0,
        "OPERATORS": 0,
        "SYMBOLS": 0,
        "INDENT": 0,
        "DEDENT": 0,
        "NEWLINE": 0,
        "EOF": 0,
    }

    keyword_types = set(KEYWORDS.values())
   ## operators_types = set(OPERATORS.values())
   ## symbol_types = set(SYMBOLS.values())

    for t in tokens:
        if t.type in keyword_types:
            summary["KEYWORDS"] +=1
        elif t.type == "ID":
            summary["ID"] +=1
        elif t.type == "INT":
            summary["INT"] +=1
        elif t.type == "FLOAT":
            summary["FLOAT"] +=1
        elif t.type == "STRING":
            summary["STRING"] +=1
        elif t.type == "OPERATORS":
            summary["OPERATORS"] +=1
        elif t.type == "SYMBOLS":   
            summary["SYMBOLS"] +=1
        elif t.type == "INDENT":
            summary["INDENT"] +=1
        elif t.type == "DEDENT":
            summary["DEDENT"] +=1
        elif t.type == "NEWLINE":
            summary["NEWLINE"] +=1
        elif t.type == "EOF":
            summary["EOF"] +=1

    totalTokens = len(tokens)

    return summary, totalTokens, len(errors)

import os

def main():
    print("MiniLang - Analizador Léxico")
    print("Buscando archivos .mlng...\n")

    files = [f for f in os.listdir() if f.endswith(".mlng")]

    if not files:
        print("No se encontraron archivos .mlng en la carpeta.")
        return

    for filename in files:
        print(f"Procesando {filename}...")

        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error al leer {filename}: {e}")
            continue

        lexer = Lexer(text)
        tokens = lexer.tokenize()

        summary, total, err_count = summarize_tokens(tokens, lexer.errors)

        # construir resumen en una sola línea
        summary_parts = [f"Total={total}"]
        summary_parts += [f"{k}={v}" for k, v in summary.items()]
        summary_parts.append(f"ERRORES={err_count}")
        summary_line = "Resumen: " + " | ".join(summary_parts)

        out_file = filename.replace(".mlng", ".out")

        try:
            with open(out_file, "w", encoding="utf-8") as f:
                for t in tokens:
                    f.write(str(t) + "\n")
                f.write(summary_line + "\n")
        except Exception as e:
            print(f"Error al escribir {out_file}: {e}")
            continue

        if lexer.errors:
            print("  → errores encontrados:")
            for e in lexer.errors:
                print("    ", e)
        else:
            print("  → analisis completado")

        print("  → " + summary_line)

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()