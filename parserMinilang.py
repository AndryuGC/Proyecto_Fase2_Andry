import os
import ply.yacc as yacc
from Proyecto import Lexer

# =========================================
# TOKENS: Iguales que Proyecto.py
# =========================================

tokens = (
    'IF', 'ELIF', 'ELSE', 'WHILE',
    'INT_TYPE', 'FLOAT_TYPE', 'BOOL_TYPE', 'STRING_TYPE',
    'READ', 'WRITE', 'RETURN', 'FUNC',
    'BOOL', 'ID', 'INT', 'FLOAT', 'STRING',
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',
    'GT', 'LT', 'ASSIGN', 'EQ', 'NEQ', 'GTE', 'LTE',
    'LPAREN', 'RPAREN', 'COLON', 'COMMA', 'SEMICOLON',
    'AND', 'OR', 'NOT',
    'INDENT', 'DEDENT', 'NEWLINE'
)

# =========================================
# PRECEDENCIA
# De menor a mayor:
# or, and, not, comparaciones, +/-, */%/
# =========================================

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'UMINUS'),
)

# =========================================
# ADAPTADOR DE TOKENS DEL LEXER ORIGINAL
# =========================================

class PlyTokenAdapter:
    """
    Convierte los Token de Proyecto.py al formato que espera PLY.
    Ignora EOF porque PLY usa None para fin de entrada.
    """
    def __init__(self, tokens_list):
        self.tokens = [t for t in tokens_list if t.type != 'EOF']
        self.index = 0

    def token(self):
        if self.index >= len(self.tokens):
            return None

        src = self.tokens[self.index]
        self.index += 1

        tok = yacc.YaccSymbol()
        tok.type = src.type
        tok.value = src.value if src.value is not None else src.type
        tok.lineno = src.line
        tok.lexpos = src.col_start
        tok.col_start = src.col_start
        tok.col_end = src.col_end
        return tok


# =========================================
# REGISTRO DE ERRORES SINTÁCTICOS
# =========================================

syntax_errors = []


def add_syntax_error(message, p):
    if p is None:
        syntax_errors.append("Línea ?, columna ?: símbolo 'EOF': Error: sintaxis incompleta al final del archivo")
        return

    value = p.value if p.value is not None else p.type
    col = getattr(p, 'col_start', getattr(p, 'lexpos', '?'))
    syntax_errors.append(
        f"Línea {p.lineno}, columna {col}, símbolo '{value}': Error: {message}"
    )


# =========================================
# GRAMÁTICA
# =========================================

def p_program(p):
    'program : opt_newlines stmt_list opt_newlines'
    pass


def p_opt_newlines(p):
    '''opt_newlines : opt_newlines NEWLINE
                    | empty'''
    pass


def p_stmt_list_multi(p):
    'stmt_list : stmt_list statement'
    pass


def p_stmt_list_single(p):
    'stmt_list : statement'
    pass


def p_statement_simple(p):
    '''statement : declaration stmt_end
                 | assignment stmt_end
                 | write_stmt stmt_end
                 | read_stmt stmt_end
                 | return_stmt stmt_end
                 | func_call stmt_end'''
    pass


def p_statement_compound(p):
    '''statement : if_stmt
                 | while_stmt
                 | func_def'''
    pass


def p_statement_blank(p):
    'statement : NEWLINE'
    pass


def p_stmt_end(p):
    '''stmt_end : SEMICOLON NEWLINE
                | NEWLINE'''
    pass


# =========================
# DECLARACIONES
# =========================

def p_declaration(p):
    'declaration : type decl_list'
    pass


def p_decl_list_single(p):
    'decl_list : decl_item'
    pass


def p_decl_list_multi(p):
    'decl_list : decl_item COMMA decl_list'
    pass


def p_decl_item_id(p):
    'decl_item : ID'
    pass


def p_decl_item_assign(p):
    'decl_item : ID ASSIGN expression'
    pass


def p_type(p):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | BOOL_TYPE
            | STRING_TYPE'''
    pass


# =========================
# ASIGNACIÓN
# =========================

def p_assignment(p):
    'assignment : ID ASSIGN expression'
    pass


# =========================
# WRITE / READ / RETURN
# =========================

def p_write_stmt(p):
    'write_stmt : WRITE LPAREN args_opt RPAREN'
    pass


def p_read_stmt(p):
    'read_stmt : READ LPAREN read_args_opt RPAREN'
    pass


def p_return_stmt(p):
    'return_stmt : RETURN expression'
    pass


def p_args_opt(p):
    '''args_opt : args
                | empty'''
    pass


def p_args_single(p):
    'args : expression'
    pass


def p_args_multi(p):
    'args : expression COMMA args'
    pass


def p_read_args_opt(p):
    '''read_args_opt : read_args
                     | empty'''
    pass


def p_read_args_single_string(p):
    'read_args : STRING'
    pass


def p_read_args_single_id(p):
    'read_args : ID'
    pass


def p_read_args_prompt_and_id(p):
    'read_args : STRING COMMA ID'
    pass


# =========================
# FUNCIONES
# =========================

def p_func_def(p):
    'func_def : FUNC return_type_opt ID LPAREN params_opt RPAREN COLON NEWLINE INDENT block DEDENT'
    pass


def p_return_type_opt(p):
    '''return_type_opt : type
                       | empty'''
    pass


def p_params_opt(p):
    '''params_opt : params
                  | empty'''
    pass


def p_params_single(p):
    'params : param'
    pass


def p_params_multi(p):
    'params : param COMMA params'
    pass


def p_param_id(p):
    'param : ID'
    pass


def p_param_typed(p):
    'param : type ID'
    pass


def p_func_call(p):
    'func_call : ID LPAREN args_opt RPAREN'
    pass


# =========================
# IF / ELIF / ELSE
# =========================

def p_if_stmt(p):
    'if_stmt : IF expression COLON NEWLINE INDENT block DEDENT elif_list else_opt'
    pass


def p_elif_list_multi(p):
    'elif_list : elif_list elif_item'
    pass


def p_elif_list_empty(p):
    'elif_list : empty'
    pass


def p_elif_item(p):
    'elif_item : ELIF expression COLON NEWLINE INDENT block DEDENT'
    pass


def p_else_opt_block(p):
    'else_opt : ELSE COLON NEWLINE INDENT block DEDENT'
    pass


def p_else_opt_empty(p):
    'else_opt : empty'
    pass


# =========================
# WHILE
# =========================

def p_while_stmt(p):
    'while_stmt : WHILE expression COLON NEWLINE INDENT block DEDENT'
    pass


# =========================
# BLOQUES
# =========================

def p_block_multi(p):
    'block : block statement'
    pass


def p_block_single(p):
    'block : statement'
    pass


# =========================
# EXPRESIONES
# =========================

def p_expression_or(p):
    'expression : expression OR expression'
    pass


def p_expression_and(p):
    'expression : expression AND expression'
    pass


def p_expression_not(p):
    'expression : NOT expression'
    pass


def p_expression_compare(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression GTE expression
                  | expression LTE expression
                  | expression EQ expression
                  | expression NEQ expression'''
    pass


def p_expression_arith(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression MOD expression'''
    pass


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    pass


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    pass


def p_expression_func_call(p):
    'expression : func_call'
    pass


def p_expression_id(p):
    'expression : ID'
    pass


def p_expression_literals(p):
    '''expression : INT
                  | FLOAT
                  | STRING
                  | BOOL'''
    pass


# =========================
# VACÍO
# =========================

def p_empty(p):
    'empty :'
    pass


# =========================
# ERRORES
# =========================

def p_error(p):
    if p:
        add_syntax_error("error sintáctico", p)
    else:
        add_syntax_error("fin inesperado del archivo", p)


# =========================================
# EJECUCIÓN
# =========================================

_parser = None


def get_parser():
    global _parser
    if _parser is None:
        _parser = yacc.yacc(start='program', write_tables=False, debug=False)
    return _parser


def run_parser(text):
    global syntax_errors
    syntax_errors = []

    # Lexer original
    lexer = Lexer(text)
    tokens_list = lexer.tokenize()

    # Parser ascendente de PLY usando los tokens reales
    adapter = PlyTokenAdapter(tokens_list)
    parser = get_parser()
    parser.parse(lexer=adapter)

    return lexer.errors, syntax_errors


def main():
    print("Proyecto - Fase 2 - Analizador Sintáctico Ascendente MiniLang")
    print("-------------------------------------------------------------\n")

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
            print(f"  Error al leer {filename}: {e}")
            continue

        lex_errors, syn_errors = run_parser(text)
        all_errors = lex_errors + syn_errors

        out_file = filename.replace(".mlng", ".parserMinilang.out")

        try:
            with open(out_file, "w", encoding="utf-8") as f:
                if not all_errors:
                    f.write("OK\n")
                else:
                    for err in all_errors:
                        f.write(err + "\n")
        except Exception as e:
            print(f"  Error al escribir {out_file}: {e}")
            continue

        if not all_errors:
            print("  OK")
        else:
            print("  → errores encontrados:")
            for err in all_errors:
                print("    ", err)

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()