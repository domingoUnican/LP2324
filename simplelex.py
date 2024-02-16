# simplelex.py

from sly import Lexer
import re

class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, ASSIGN, PLUS, LPAREN, RPAREN, TIMES, LT, LE, GT, GE, EQ, NE}

    # Ignored characters
    ignore = ' \t'

    #literales
    #literales={'+','*','(',')'}

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    #LITERALES 
    ASSIGN = r'(=)'
    PLUS = r'(\+)'
    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES = r'\*'
    LT = r'(<)'
    LE = r'(<=)'
    GT = r'(>)'
    GE = r'(>=)'
    EQ = r'(==)'
    NE = r'(!=)'


    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    #text = 'a = 3 + (4 * 5)'
    text = '''
            a < b
            a <= b
            a > b
            a >= b
            a == b
            a != b
        '''
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)