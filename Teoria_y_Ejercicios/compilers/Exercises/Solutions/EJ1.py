import re
from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, IF, ELSE, WHILE, IGUAL, INSTRUCTIONS, VAR, PLUS, LPAREN, RPAREN, TIMES, MINUS, LE, LT, GE, GT, EQ, NE, NOT, AND, OR, SEMICOLON, COMMA, LBRACKET, RBRACKET, LBRACE, RBRACE, DOT}

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    VAR = r'int_|float_|char_|bool_'
    PLUS = r'\+'
    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES = r'\*'
    MINUS = r'-'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    NOT = r'!'
    AND = r'&&'
    OR = r'\|\|'
    SEMICOLON = r';'
    COMMA = r','
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'{'
    RBRACE = r'}'
    DOT = r'\.'


    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')
    
    # Error handling rule
    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    text = '''
           if a < b
           else a <= b
           while a > b
           a >= b
           a == b
           a != b
    '''
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)