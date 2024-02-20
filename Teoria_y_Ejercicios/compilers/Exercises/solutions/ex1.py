import re

RESERVED = r'(?P<RESERVED>[iI][fF]|[iI][nN][tT])'
ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'
EQUALS = r'(?P<EQUALS>=)'
INVALID = r'(?P<INVALID>[^a-zA-Z0-9_\s=])'

patterns = [RESERVED, ID, NUMBER, SPACE, EQUALS, INVALID]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        m = pat.match(text,index)
        if m.group() != ' ':
            if m.lastgroup == 'RESERVED':
                yield ('RESERVED', m.group())
            else:
                yield (m.lastgroup, m.group())
            index = m.end()
        elif m.group() == ' ':
            index = m.end()
        else:
            raise SyntaxError('Bad char %r' % text[index])
        

# Sample usage
text = 'abc IF INT = 123 cde 456'
for tok in tokenize(text):
    print(tok)
