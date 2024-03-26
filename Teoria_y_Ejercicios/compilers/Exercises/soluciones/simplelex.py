# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = {NUMBER, ID, ASSIGN, PLUS, LPAREN, TIMES, RPAREN,
               LT, LE, GT, GE, EQ, NE, IF, ELSE, WHILE }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PLUS = r'\+'
    LPAREN = r'\('
    TIMES = r'\*'
    RPAREN = r'\)'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    ASSIGN = '='
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1
    
    
    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')
    

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