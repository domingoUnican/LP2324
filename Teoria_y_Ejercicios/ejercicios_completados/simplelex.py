# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = {ASSIGN,PLUS,LPAREN,TIMES,RPAREN, NUMBER, ID }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    ASSIGN = r'='
    PLUS = r'\+'
    LPAREN = r'\('
    TIMES = r'\*'
    RPAREN = r'\)'
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    text = 'a = 3 + (4 * 5)'
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)