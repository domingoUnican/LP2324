# ex1.py

import re

ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
NUMBER = r'(?P<NUMBER>\d+)'
SPACE = r'(?P<SPACE>\s+)'

patterns = [ID, NUMBER, SPACE]

# Make the master regex pattern
pat = re.compile('|'.join(patterns))

def tokenize(text):
    index = 0
    while index < len(text):
        try:
            m = pat.match(text, index)
            if m:
                if m.lastgroup != 'SPACE':
                    yield (m.lastgroup, m.group())
                index = m.end()
            else:
                raise SyntaxError('Bad char %r' % text[index])
        except SyntaxError as e:
            print(f"Bad character '{text[index]}'")
            index += 1  # Move to the next character

# Sample usage
text = 'abc 123 $ cde 456'

for tok in tokenize(text):
    print(tok)
