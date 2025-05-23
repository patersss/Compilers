import ply.lex as lex
from ast_nodes import *
import ply.yacc as yacc
import sys

tokens = [
    'NUMBER', 'IDENT',
    'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
    'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON',
    'GT', 'LT', 'GE', 'LE',
    'EQUALS', 'NOTEQUALS',
    'GT_INPUT', 'LT_OUTPUT',
    'OR', 'AND', 'NOT'
]

reserved = {
    'cin': 'CIN',
    'cout': 'COUT',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'do': 'DO',
    'int': 'TINT',
    'bool': 'BOOL',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens += reserved.values()

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_SEMICOLON = r';'
t_GT = r'>'
t_LT = r'<'
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_GE = r'>='
t_LE = r'<='
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'!'
t_GT_INPUT = r'>>'
t_LT_OUTPUT = r'<<'

t_ignore = ' \r\t'


def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ccode_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


class ParserError(Exception):
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(self.message)


def t_error(t):
    print(f"Лексическая ошибка: недопустимый символ '{t.value[0]}' в строке {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


def p_expr_list(t):
    '''expr_list :
                 | expr_list statement'''
    if len(t) > 1:
        if t[2]:
            t[1].add_child(t[2])
        t[0] = t[1]
    else:
        t[0] = ExprListNode()


def p_statement(t):
    '''statement : expr_statement
                 | block
                 | selection_statement
                 | iteration_statement'''
    t[0] = t[1]


def p_expr_statement(t):
    '''expr_statement : semicolons
                      | expression semicolons'''
    t[0] = t[1]


def p_block(t):
    'block : LBRACE expr_list RBRACE'
    t[0] = t[2]


def p_selection_statement(t):
    'selection_statement : if'
    t[0] = t[1]


def p_iteration_statement(t):
    '''iteration_statement : for
                           | while
                           | dowhile'''
    t[0] = t[1]


def p_expression(t):
    '''expression : logical_expression
                  | assignment
                  | function
                  | identification'''
    t[0] = t[1]


def p_logical_expression(t):
    'logical_expression : logical_or_expression'
    t[0] = t[1]


def p_logical_or_expression(t):
    '''logical_or_expression : logical_and_expression
                             | logical_or_expression OR logical_and_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]


def p_logical_and_expression(t):
    '''logical_and_expression : equality_expression
                              | logical_and_expression AND equality_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]


def p_equality_expression(t):
    '''equality_expression : relational_expression
                           | equality_expression EQUALS relational_expression
                           | equality_expression NOTEQUALS relational_expression '''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]


def p_relational_expression(t):
    '''relational_expression : additive_expression
                             | relational_expression GT additive_expression
                             | relational_expression LT additive_expression
                             | relational_expression GE additive_expression
                             | relational_expression LE additive_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]


def p_additive_expression(t):
    '''additive_expression : multiplicative_expression
                           | additive_expression ADD multiplicative_expression
                           | additive_expression SUB multiplicative_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]


def p_multiplicative_expression(t):
    '''multiplicative_expression : unary_expression
                                 | multiplicative_expression MUL unary_expression
                                 | multiplicative_expression DIV unary_expression
                                 | multiplicative_expression MOD unary_expression'''
    if len(t) > 2:
        t[0] = BinOpNode(BinOp(t[2]), t[1], t[3])
    else:
        t[0] = t[1]

def p_unary_expression(t):
    '''unary_expression : group
                        | NOT group
                        | SUB group'''
    if len(t) > 2:
        t[0] = UnOpNode(UnOp(t[1]), t[2])
    else:
        t[0] = t[1]


def p_group(t):
    '''group : ident
             | LPAREN logical_expression RPAREN
             | number
             | bool_value'''
    if len(t) > 2:
        t[0] = t[2]
    else:
        t[0] = t[1]


def p_if(t):
    '''if : IF LPAREN expression RPAREN statement
          | IF LPAREN expression RPAREN statement ELSE statement'''

    if len(t) > 6:
        t[0] = IfNode(t[3], t[5], t[7])
    else:
        t[0] = IfNode(t[3], t[5])


def p_statement_assign(t):
    'assignment : ident ASSIGN logical_expression'
    t[0] = AssignNode(t[1], t[3])


def p_function(t):
    '''function : cin
                | cout'''
    t[0] = t[1]


def p_identification(t):
    '''identification : type ident
                      | type ident ASSIGN logical_expression'''
    if len(t) > 3:
        t[0] = IdentificationNode(t[1], t[2], t[4])
    else:
        t[0] = IdentificationNode(t[1], t[2])


def p_type(t):
    '''type : TINT
            | BOOL
            | CHAR'''
    t[0] = t[1]


def p_for(t):
    '''for : FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN statement'''
    t[0] = ForNode(t[3], t[5], t[7], t[9])


def p_dowhile(t):
    '''dowhile : DO statement WHILE LPAREN expression RPAREN '''
    t[0] = DoWhileNode(t[2], t[5])


def p_while(t):
    '''while : WHILE LPAREN expression RPAREN statement'''
    t[0] = WhileNode(t[3], t[5])


def p_output(t):
    'cout : COUT LT_OUTPUT logical_expression'
    t[0] = OutputNode(t[3])


def p_input(t):
    'cin : CIN GT_INPUT ident'
    t[0] = InputNode(t[3])


def p_ident(t):
    '''ident : IDENT'''
    t[0] = IdentNode(t[1])

def p_bool_value(t):
    '''bool_value : TRUE
                  | FALSE'''
    t[0] = BoolValueNode(t[1])


def p_expression_number(t):
    'number : NUMBER'
    t[0] = NumNode(t[1])


def p_semicolons(p):
    '''semicolons : SEMICOLON
                  | semicolons SEMICOLON'''


def p_error(t):
    if t is None:
        print("Синтаксическая ошибка: неожиданный конец файла")
    else:
        print(f"Синтаксическая ошибка в строке {t.lineno}: неожиданный токен '{t.value}'")
    raise ParserError("Ошибка синтаксического анализа")


parser = yacc.yacc()

def build_tree(s):
    try:
        result = parser.parse(s)
        if result is None:
            raise ParserError("Не удалось построить AST")
        return result.tree
    except ParserError as e:
        print(f"Ошибка: {e.message}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as file:
            code = file.read()
            tree = build_tree(code)
            if tree:
                from ast_visualizer import print_ast
                print_ast(tree)
    else:
        print("Использование: python cTreeParser.py <имя_файла>")
