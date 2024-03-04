from sly import Lexer

class SimpleLexer(Lexer):
    # Token names
    tokens = { NUMBER, ID, EQUALS, SUMA, RESTA, PAREN_IZQ, PAREN_DER, ASTERISCO, MENOR, MAYOR, MENORIGUAL
    ,MAYORIGUAL, IGUALIGUAL, NOIGUAL, IF, ELSE, WHILE}

    # Ignored characters
    ignore = ' \t'

    # Token regexs
    NUMBER = r'\d+'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    NOIGUAL = r'\!='
    IGUALIGUAL = r'\=='
    EQUALS = r'='
    SUMA = r'\+'
    RESTA = r'\-'
    PAREN_IZQ = r'\('
    PAREN_DER = r'\)'
    ASTERISCO = r'\*'
    MENORIGUAL = r'\<='
    MAYORIGUAL = r'\>='
    MENOR = r'\<'
    MAYOR = r'\>'
    

    @_(r'\n+')
    def ignore_newline(self,  t):
        self.lineno += t.value.count('\n')



    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1

# Example
"""
if __name__ == '__main__':
    text = 'a = 3 + (4 * 5)'
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    text = '''
           a < b
           a <= b
           a > b
           a >= b
           a == b
           a != b
    '
    lexer = SimpleLexer()
    for tok in lexer.tokenize(text):
        print(tok)
"""
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