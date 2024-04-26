# ex1.py

import re


ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'

RESERVED = r'(?P<RESERVED>\b(if|int)\b|(\B=\B))'  
ERROR = r'(?P<ERROR>.)'

patterns = [RESERVED, ID, NUMBER, SPACE, ERROR]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        m = pat.match(text,index)
        if m:
            yield (m.lastgroup, m.group())
            index = m.end()
        else:
            raise SyntaxError('Bad char %r' % text[index])

# Sample usage
text = 'if = int intabc $ 123 cde 456'

for tok in tokenize(text):
    if tok[0] != 'SPACE':
        print(tok)
