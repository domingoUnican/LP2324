from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { ID, NUMBER, ASSIGN, PLUS, LPAREN, RPAREN, TIMES, LT, LE, GT, GE, EQ, NE, IF, ELSE, WHILE }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    EQ = r'=='
    ASSIGN = r'='
    PLUS = r'\+'
    LPAREN = r'\('
    RPAREN = r'\)'
    TIMES = r'\*'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    # Special handling for keywords
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

    def newline(self, t):
        self.lineno += 1

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')

# Example
if _name_ == '_main_':
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
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)
