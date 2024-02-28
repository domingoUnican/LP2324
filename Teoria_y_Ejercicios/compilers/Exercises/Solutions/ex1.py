# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { ID, NUMBER, LT, LE, GT, GE, EQ, NE }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'
    LT = r'<'
    LE = r'<='
    GT = r'>'
    GE = r'>='
    EQ = r'=='
    NE = r'!='

    def error(self, t):
        print(f'Bad character {t.value[0]}')
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
        if tok.type != 'WS':
            print(tok)
