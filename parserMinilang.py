# parser_minilang.py
# Gramática base de MiniLang
#
# programa        -> lista_sentencias EOF
#
# lista_sentencias -> sentencia lista_sentencias
#                  | ε
#
# sentencia       -> declaracion NEWLINE
#                 | asignacion NEWLINE
#                 | write_stmt NEWLINE
#                 | read_stmt NEWLINE
#                 | return_stmt NEWLINE
#                 | llamada_funcion NEWLINE
#                 | if_stmt
#                 | while_stmt
#                 | func_def
#                 | NEWLINE
#
# declaracion     -> tipo ID
#                 | tipo ID ASSIGN expresion
#
# tipo            -> INT_TYPE
#                 | FLOAT_TYPE
#                 | BOOL_TYPE
#                 | STRING_TYPE
#
# asignacion      -> ID ASSIGN expresion
#
# write_stmt      -> WRITE LPAREN argumentos_opt RPAREN
#
# read_stmt       -> READ LPAREN RPAREN
#                 | READ LPAREN STRING RPAREN
#
# return_stmt     -> RETURN expresion
#
# if_stmt         -> IF expresion COLON NEWLINE INDENT lista_sentencias DEDENT else_if_list else_opt
#
# else_if_list    -> ELIF expresion COLON NEWLINE INDENT lista_sentencias DEDENT else_if_list
#                 | ε
#
# else_opt        -> ELSE COLON NEWLINE INDENT lista_sentencias DEDENT
#                 | ε
#
# while_stmt      -> WHILE expresion COLON NEWLINE INDENT lista_sentencias DEDENT
#
# func_def        -> FUNC ID LPAREN parametros_opt RPAREN COLON NEWLINE INDENT lista_sentencias DEDENT
#
# parametros_opt  -> parametros
#                 | ε
#
# parametros      -> ID
#                 | ID COMMA parametros
#
# argumentos_opt  -> argumentos
#                 | ε
#
# argumentos      -> expresion
#                 | expresion COMMA argumentos
#
# llamada_funcion -> ID LPAREN argumentos_opt RPAREN
#
# expresion       -> or_expr
#
# or_expr         -> and_expr
#                 | or_expr OR and_expr
#
# and_expr        -> not_expr
#                 | and_expr AND not_expr
#
# not_expr        -> NOT not_expr
#                 | comparacion
#
# comparacion     -> arit_expr
#                 | arit_expr GT arit_expr
#                 | arit_expr LT arit_expr
#                 | arit_expr GTE arit_expr
#                 | arit_expr LTE arit_expr
#                 | arit_expr EQ arit_expr
#                 | arit_expr NEQ arit_expr
#
# arit_expr       -> termino
#                 | arit_expr PLUS termino
#                 | arit_expr MINUS termino
#
# termino         -> factor
#                 | termino MULT factor
#                 | termino DIV factor
#                 | termino MOD factor
#
# factor          -> INT
#                 | FLOAT
#                 | STRING
#                 | BOOL
#                 | ID
#                 | llamada_funcion
#                 | LPAREN expresion RPAREN
#                 | MINUS factor