# ex1.py

import re

ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'
IGUAL =  r'(?P<IGUAL>\=)'
RESERVADO = r'(?P<RESERVADO>\b((INT)|(IF))\b)'
ERROR = r'(?P<ERROR>.)'

patterns = [RESERVADO, ID, NUMBER, SPACE, IGUAL, ERROR]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        m = pat.match(text,index)
        #if m:
        if m.lastgroup != "SPACE":
            yield (m.lastgroup, m.group())
        index = m.end()
        #else:
            #print('Bad char %r' % text[index])
            #index = index + 1

# Sample usage
text = 'abc 123 cde 456 = INTINT $ hola $ h /'

for tok in tokenize(text):
    print(tok)
