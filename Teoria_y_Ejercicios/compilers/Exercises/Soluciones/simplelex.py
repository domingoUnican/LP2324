# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { ID,IF,ELSE,WHILE, NUMBER,GE, LE,LT, GT, EQ, NE,ASSIGN,PLUS,LPAREN,RPAREN, TIMES, MINUS, DIVIDE,}

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    NUMBER = r'\d+'
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    ASSIGN = r'='
    PLUS = r'\+'
    MINUS = r'-'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES = r'\*'
    
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
