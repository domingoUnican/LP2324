# ex1.py

import re

RESERVED = r'(?P<RESERVED>int|if)'
EQUAL = r'(?P<EQUAL>=)'
ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'

patterns = [RESERVED, EQUAL, ID, NUMBER, SPACE]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        m = pat.match(text,index)

        if m is None:
            print('Bad character %r' % text[index])
            index = index + 1
        elif m.group() != ' ' :
            yield (m.lastgroup, m.group())
            index = m.end()
        elif m.group() == ' ':
            index = m.end()
        else:
            raise SyntaxError('Bad char %r' % text[index]) #esto es innecesario, pero bueh

# Sample usage
text = 'abc if = 123 $ cde 456'

for tok in tokenize(text):
    #if tok != ('SPACE', ' '):
    print(tok)