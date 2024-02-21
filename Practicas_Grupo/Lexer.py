# coding: utf-8

from sly import Lexer
import os
import re
import sys





class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN, IGNORE, CLASS}
    #ignore = '\t '
    IGNORE = r'(\(\*((?:.|\n)*?)\*\))|(\-\-.*)'
    literals = {'-', ':', '(', ')', '{', '}', ';', '+', '*', '~', ',', '<', '.', '=', '/', '@'}
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

    LE = r'\<\='

    DARROW = r'\=\>'

    ASSIGN = r'\<\-'

    BOOL_CONST = r'\b([t][rR][uU][eE])\b|\b([f][aA][lL][sS][eE])\b'


    NOT = r'\b[nN][oO][tT]\b' #terminar de revisar

    CASE = r'\b[cC][aA][sS][eE]\b'

    CLASS = r'\b[cC][lL][aA][sS][sS]\b'
    
    INHERITS = r'\b[iI][nN][hH][eE][rR][iI][tT][sS]\b'

    ISVOID = r'\b[iI][sS][vV][oO][iI][dD]\b'

    LET = r'\b[lL][eE][tT]\b'

    LOOP = r'\b[lL][oO][oO][pP]\b'

    NEW = r'\b[nN][eE][wW]\b'

    OF = r'\b[oO][fF]\b'

    TYPEID = r'\b[A-Z][a-zA-Z0-9\_]*' 

    OBJECTID = r'[a-z][a-zA-Z0-9\_]*'

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    

    @_(r'"(?:\\.|[^"])*"|"(?:\\\\(?:\\[a-ac-eg-mo-qs-su-z0-9])|\\[a-ac-eg-mo-qs-su-z0-9]|[^"])*"')
    def STR_CONST(self, t):

        pattern_to_replace = r'(?<!\\)(\\([a-ac-eg-mo-qs-su-z0-9]))'

        def replace_fn(match):
            return match.group(2)
        
        
        t.value = re.sub(pattern_to_replace, replace_fn, t.value)
        t.value = t.value.replace("\t", "\\t")
        t.value = re.sub('\\\n', r'\\n', t.value)
        return t

    @_(r'\(\*.*\*\)')
    def IGNORE(self, t):
        pass

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
        #self.lineno += t.value.count('\r')
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
                result = f'#{token.lineno} \'{token.type}\''
            elif token.type == 'STR_CONST':
                result += token.value
            elif token.type == 'INT_CONST':
                result += str(token.value)
            elif token.type == 'ERROR':
                result = f'#{token.lineno} {token.type} {token.value}'
            else:
                result = f'#{token.lineno} {token.type}'
            result += '\n'
            list_strings.append(result)
        return list_strings
