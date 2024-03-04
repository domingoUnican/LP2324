# simplelex.py

from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { LPAREN, RPAREN, NUMBER, ID, IF, ELSE, WHILE, LE, GE, EQ, NE, GT, LT, ASSIGN, PLUS, TIMES }

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    @_(r'\(')
    def LPAREN(self,t):
        return t
    
    @_(r'\)')
    def RPAREN(self,t):
        return t
     
    NUMBER = r'\d+'

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        if t.value == 'if':
            t.type = "IF"

        if t.value == 'else':
            t.type = "ELSE"

        if t.value == 'while':
            t.type = "WHILE"
        
        return t

    LE = r'\<\='
    GE = r'\>\='
    EQ = r'\=\='
    NE = r'\!\='
    ASSIGN  = r'\='
    PLUS = r'\+'
    TIMES = r'\*'
    GT = r'\>'
    LT = r'\<' 

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
if __name__ == '__main__':
    #text = 'a = 3 + (4 * 5)'
    
    #text = '''
     #      a < b
      #     a <= b
       #    a > b
        #   a >= b
         #  a == b
          # a != b
    #'''

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