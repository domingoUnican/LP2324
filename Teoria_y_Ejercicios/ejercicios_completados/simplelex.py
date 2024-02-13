# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = {LE, LT, LE, GT, GE, EQ, NE, ASSIGN,PLUS,LPAREN,TIMES,RPAREN, NUMBER, ID }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    EQ = r'=='
    ASSIGN = r'='
    PLUS = r'\+'
    LPAREN = r'\('
    TIMES = r'\*'
    RPAREN = r'\)'
    NUMBER = r'\d+'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
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