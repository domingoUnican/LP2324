from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, ASSIGN, PLUS, LPAREN, RPAREN, TIMES,
              LT, LE, EQ, GT, NE, GE, IF, WHILE, ELSE}

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    #Hay que poner el == antes para que lo detecte antes 
    EQ = r'=='
    ASSIGN = r'='
    PLUS =  r'\+'
    LPAREN  =  r'\('
    RPAREN  =  r'\)'
    TIMES = r'\*'
    LT = r'<'
    LE =  r'<='
    GT = r'>'
    GE = r'>='
    NE = r'!'

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')

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