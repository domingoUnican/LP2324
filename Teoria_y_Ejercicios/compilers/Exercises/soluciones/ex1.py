# ex1.py
from sly import Lexer

import re

ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'

patterns = [ID, NUMBER, SPACE]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

class Ejercicio1(Lexer):
    tokens = {IGUAL,RESERVADO}

    ignore = ' \t'
    #usamos estos cuando no hacemos nada con el tokery 
    # y los nombres declarados asi van en la lista tokens
    IGUAL = r'='
    
    RESERVADO = r'IF|INT'
    
    #@_ (r'IF|INT')
    #def RESERVADA(self, t):
     #   return t
    @_('\n')
    def ignore_newline(self, t):
        self.lineno += 1
    
    def error(self, t):
        print('Bad character %r' % t.value[0])
        self.index += 1


# Sample usage
text = 'abc INT \n = IF'
resultado = Ejercicio1()
for tok in resultado.tokenize(text):
    print(tok)