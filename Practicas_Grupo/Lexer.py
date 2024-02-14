# coding: utf-8

from sly import Lexer
import os
import re
import sys





class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN}
    #ignore = '\t '
    literals = {'-'}
    # Ejemplo
     

    ELSE = r'\b[eE][lL][sS][eE]\b'

    IF = r'\b[iI][fF]\b'

    FI = r'\b[fF][iI]\b'

    THEN = r'\b[tT][hH][eE][nN]\b'

    IN = r'\b[iI][nN]\b'

    ESAC = r'\b[eE][sS][aA][cC]\b'

    POOL = r'\b[pP][oO][oO][lL]\b'

    WHILE = r'\b[wW][hH][iI][lL][eE]\b'

    INT_CONST = r'[0-9]+'

    NUMBER = r'^-?\d+(\.\d+)?$'



    LE = r'\b\<\=\b'

    DARROW = r'\b\=\>\b'

    ASSIGN = r'\b<-\b'

    BOOL_CONST = r'\b([t][rR][uU][eE])\b|\b([f][aA][lL][sS][eE])\b|\b[iI][nN][tT]\b'

    TYPEID = r'\b([T][rR][uU][eE])\b|\b([F][aA][lL][sS][eE])\b|\b([iI][nN][tT])\b|\b([fF][oO][aA][tT])\b'

    NOT = r'\b[nN][oO][tT]\b' #terminar de revisar
    CASE = r'\b[cC][aA][sS][eE]\b'
    CLASS = r'\b[cC][lL][aA][sS][sS]\b'
    
    INHERITS = r'\b[iI][nN][hH][eE][rR][iI][tT][sS]\b'
    ISVOID = r'\b[iI][sS][vV][oO][iI][dD]\b'
    LET = r'\b[lL][eE][tT]\b'
    LOOP = r'\b[lL][oO][oO][pP]\b'
    NEW = r'\b[nN][eE][wW]\b'
    OF = r'\b[oO][fF]\b'
    OBJECTID = r'[a-z].*'
    #STR_CONST = r'[a-zA-Z]+'

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r'\b([t][rR][uU][eE])\b|\b([f][aA][lL][sS][eE])\b|\b[iI][nN][tT]\b')
    def BOOL_CONST(self, t):
        if t.value[0] == 't':
            t.value = True
            return t
        else:
            t.value = False
            return t
    
    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    
    def error(self, t):
        self.index += 1


    def salida(self, texto):
        lexer = CoolLexer()
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type in self.literals:
                result = f'#{token.lineno} \'{token.type}\' '
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append(result)
        return list_strings
