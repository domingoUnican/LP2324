# gone/tokenizer.py

from .errors import error
from sly import Lexer

class GoneLexer(Lexer):
    tokens = {
        ID, CONST, VAR, PRINT,
        INTEGER, FLOAT, CHAR,
        PLUS, MINUS, TIMES, DIVIDE,
        ASSIGN, LPAREN, RPAREN, SEMI,
    }

    ignore = ' \t\r'

    @_(r'/\*(.|\n)*?\*/')
    def COMMENT(self, t):
        self.lineno += t.value.count('\n')

    @_(r'//.*\n')
    def CPPCOMMENT(self, t):
        self.lineno += 1

    @_(r'/\*(.|\n)*')
    def COMMENT_UNTERM(self, t):
        error(self.lineno, "Unterminated comment")

    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    SEMI = r';'
    LPAREN = r'\('
    RPAREN = r'\)'
    ASSIGN = r'='

    FLOAT = r'(\d+\.\d+)|(\d+\.)|(\.\d+)'

    INTEGER = r'\d+'

    CHAR = r"('((\\x[0-9a-fA-F]{2})|(\\n)|(\\')|(\\\\)|(.))')"

    @_(r"'.*\n")
    def CHAR_UNTERM(self, t):
        error(self.lineno, "Unterminated character literal")
        self.lineno += 1

    ID = '[a-zA-Z_][a-zA-Z0-9_]*'

    ID['const'] = CONST
    ID['var'] = VAR
    ID['print'] = PRINT

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        error(self.lineno, "Illegal character %r" % t.value[0])
        self.index += 1

def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 -m gone.tokenizer filename\n")
        raise SystemExit(1)
    lexer = GoneLexer()
    text = open(sys.argv[1]).read()
    for tok in lexer.tokenize(text):
        print(tok)

if __name__ == '__main__':
    main()
