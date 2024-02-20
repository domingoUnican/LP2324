# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names

    #anahdir los tokens a la lista
    tokens = { NUMBER, ID, ASSIGN, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, VAR, CONST, INT, FLOAT, CHAR, BOOL, IF, ELSE, WHILE, BREAK, RETURN}

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ASSIGN
    PLUS
    MINUS
    DIVIDE
    TIMES

    LPAREN
    RPAREN

    VAR
    CONST

    INT
    FLOAT 
    CHAR
    BOOL

    IF
    ELSE
    WHILE
    BREAK
    RETURN


    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    text = 'abc 123 $ cde 456'
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)