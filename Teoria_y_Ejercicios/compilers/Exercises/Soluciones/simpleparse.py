
from sly import Parser
from sly import Lexer
from simplelex import SimpleLexer
from simpleleast import *
    
class SimpleParser(Parser):
    tokens = SimpleLexer.tokens

    @_('ID ASSIGN expr')
    def assignment(self, p):
        return Assignment(p.ID, p.expr)

    @_('expr PLUS term')
    def expr(self, p):
        return BinOp('+', p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        return BinOp('*', p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr

    @_('NUMBER')
    def factor(self, p):
        return Number(p.NUMBER)

    @_('ID')
    def factor(self, p):
        return Identifier(p.ID)

if __name__ == '__main__':
    text = 'a = 2 + 3 * (4 + 5)'
    lexer = SimpleLexer()
    parser = SimpleParser()
    result = parser.parse(lexer.tokenize(text))
    print('location:', result.location)
    print('value:', result.value)
    print(result)
