# simplelex.py

from sly import Lexer


class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, ASSIGN, PLUS, LPAREN, RPAREN, MULTIPLY, LT, LE, GT, GE, EQ, NE, IF, ELSE, WHILE }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE

    EQ = r'=='
    ASSIGN = r'='
    PLUS = r'\+'
    LPAREN = r'\('
    RPAREN = r'\)'
    MULTIPLY = r'\*'

    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')

# Example
if __name__ == '__main__':

    # Output 1
    print("OUTPUT 1")
    text = 'a = 3 + (4 * 5)'
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)

    print("=====================================")

    # Output 2
    print("OUTPUT 2")
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
    
    print("=====================================")

    # Output 3
    print("OUTPUT 3")
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