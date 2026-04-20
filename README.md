# Proyecto Fase 2 - Analizador Sintáctico Ascendente (MiniLang)

**Curso:** Compiladores  
**Estudiante:** Andry González Cantoral  
**Fecha:** Abril 2026  

---

# Descripción

Este proyecto implementa un **compilador parcial para MiniLang**, específicamente:

- Fase 1: Analizador Léxico (Lexer)
- Fase 2: Analizador Sintáctico (Parser)

El sistema permite:

- Leer archivos `.mlng`
- Analizar tokens (lexer)
- Validar estructura del lenguaje (parser)
- Reportar errores léxicos y sintácticos
- Continuar análisis hasta el final del archivo (EOF)

---

# Cómo ejecutar

Ubicar todos los archivos en la misma carpeta y ejecutar:
Compilarlo con el Pyhton Debugger o cualquier compilador de su preferencia.
El programa:

Busca archivos .mlng
Genera resultados en consola
Crea archivos .parser.out

---

# Estructura del proyecto

Proyecto.py            → Analizador Léxico (Fase 1)
parserMinilang.py      → Analizador Sintáctico (Fase 2)
*.mlng                 → Archivos de prueba
*.parser.out           → Resultados del parser

--- 

# Explicación de las Clases y Archivos del Código

### 🔹 Clase Token

Representa cada unidad léxica identificada en el código.

Atributos:
- `type`: tipo de token (INT, ID, PLUS, etc.)
- `value`: valor del token
- `line`: número de línea
- `col_start`, `col_end`: posición del token

Ejemplo:
INT(10) [1:5-6]

---

### 🔹 Clase Lexer

Encargada de analizar el texto línea por línea y generar tokens.

Funciones principales:

#### `tokenize()`
- Recorre todas las líneas del archivo
- Genera tokens
- Agrega tokens especiales como:
  - INDENT
  - DEDENT
  - NEWLINE
  - EOF

---

#### `process_line()`
- Analiza cada línea individualmente
- Detecta:
  - Identificadores y palabras reservadas
  - Números (enteros y flotantes)
  - Strings
  - Operadores
  - Símbolos
- Maneja comentarios (`#`)
- Detecta errores léxicos como:
  - caracteres inválidos
  - cadenas sin cerrar
  - números mal formados

---

#### `handle_indentation()`
- Controla los niveles de indentación
- Genera:
  - INDENT (cuando aumenta indentación)
  - DEDENT (cuando disminuye)
- Detecta errores de indentación inválida

---

### 🔹 Función summarize_tokens()
- Cuenta los tipos de tokens generados
- Genera un resumen estadístico del archivo analizado

---

### 🔹 Función main()
- Busca archivos `.mlng`
- Ejecuta el lexer sobre cada archivo
- Muestra:
  - errores léxicos
  - resumen de tokens
- Genera archivo `.out`

---

## 📌 parserMinilang.py (Analizador Sintáctico - Fase 2)

Este archivo implementa el **parser**, que valida la estructura del programa usando los tokens generados por el lexer.

---

### 🔹 Clase Parser

Encargada de:
- recorrer la lista de tokens
- validar la gramática del lenguaje
- detectar errores sintácticos
- continuar el análisis después de errores

---

### 🔹 Control de flujo del parser

El parser utiliza:

- `current_token`: token actual
- `advance()`: avanzar al siguiente token
- `peek()`: ver el siguiente token sin avanzar

---

### 🔹 Manejo de errores

#### `add_error()`
- Registra errores sintácticos
- Incluye:
  - línea
  - columna
  - símbolo
  - descripción del error

---

#### `synchronize()`
- Permite recuperación de errores
- Avanza hasta encontrar:
  - NEWLINE
  - DEDENT
  - EOF

Esto evita que el parser se detenga en el primer error.

---

### 🔹 Función match()

- Verifica que el token actual sea el esperado
- Si coincide:
  - avanza
- Si no:
  - registra error

---

### 🔹 Función match_statement_end()

Permite finalizar sentencias de dos formas:

- con `;`
- o con salto de línea

Ejemplo válido:
int x = 5;
int x = 5

---

## 🔹 Estructura del parser

---

### `parse()`
Punto de entrada del parser.

- Inicia el análisis
- Verifica que el programa termine correctamente en EOF

---

### `parse_program()`
- Recorre todo el archivo
- Llama a `parse_statement()` repetidamente

---

### `parse_statement()`
Reconoce los diferentes tipos de sentencias:

- declaración
- asignación
- escritura (Write)
- lectura (Read)
- return
- funciones
- if / elif / else
- while

---

## 🔹 Sentencias

---

### `parse_declaration()`

Permite:

int x;
int x = 5;
int a, b, c;
int x = 1, y = 2;

---

### `parse_assignment()`

Ejemplo:
x = 10;

---

### `parse_write()`

Ejemplo:
Write("Hola");

---

### `parse_read()`

Ejemplo:
Read();
Read(x);
Read("Ingrese dato", x);

---

### `parse_function_call()`

Ejemplo:
suma(5, 3);

---

### `parse_return()`

Ejemplo:
return x + y;

---

## 🔹 Estructuras de control

---

### `parse_if()`

Soporta:

if condición:
    ...
elif condición:
    ...
else:
    ...

---

### `parse_while()`

Ejemplo:

while condición:
    ...

---

### `parse_function_def()`

Permite:

func suma(a, b):
func int suma(int a, int b):

Incluye:
- tipo de retorno opcional
- parámetros tipados

---

## 🔹 Parámetros

---

### `parse_parameters()`

Permite:

a, b
int a, float b

---

## 🔹 Expresiones

---

### `parse_expression()`

Maneja precedencia de operadores.

Orden implementado:

1. OR
2. AND
3. NOT
4. Comparaciones (>, <, ==, !=)
5. Suma y resta (+, -)
6. Multiplicación, división y módulo (*, /, %)

---

### `parse_factor()`

Reconoce:

- números
- strings
- booleanos
- identificadores
- llamadas a función
- expresiones entre paréntesis
- negativos

---

## 🔹 Función run_parser()

Conecta lexer y parser:

1. Ejecuta el lexer
2. Genera tokens
3. Ejecuta el parser
4. Devuelve:
   - errores léxicos
   - errores sintácticos

---

## 🔹 Función main()

- Busca archivos `.mlng`
- Ejecuta el análisis completo
- Muestra resultados en consola
- Genera archivo `.parser.out`

Resultado:

- "OK" si no hay errores
- lista de errores si existen
