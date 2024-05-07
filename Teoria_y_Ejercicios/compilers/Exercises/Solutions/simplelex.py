# simplelex.py

from sly import Lexer
import re

class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, IF, ELSE, WHILE, PLUS, LPAREN, RPAREN, TIMES, LE, GE, NE, ASSIGN, LT, GT, EQ}

    # Ignored characters
    ignore = ' \t'

    #literales
    #literales={'+','*','(',')'}

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    
    #LITERALES 
    
    PLUS = r'(\+)'
    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES = r'\*'

    LE = r'(<=)'
    GE = r'(>=)'
    EQ = r'={2}'
    NE = r'(!=)'
    LT = r'(<)'
    GT = r'(>)'
    ASSIGN = r'='
    

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    #text = 'a = 3 + (4 * 5)'

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