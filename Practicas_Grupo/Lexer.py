# coding: utf-8

from sly import Lexer
import os
import re
import sys





class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
            ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
            INHERITS, ISVOID, LET, LOOP, NEW, OF,
            POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN, ERROR}
    #ignore = '\t '
    literals = {'==', '+', '-', '*', '/', '(', ')', '<', '>', '.',' ' ,';', ':', '@', ','}
    # Ejemplo
    INT_CONST   = r'\d+'
    TYPEID      = r'[A-Z]([a-zA-Z0-9_])*'
    OBJECTID    = r'[a-z]([a-zA-Z0-9_])*'
    LE          = r'[<][=]'
    DARROW      = r'[=][>]'
    ASSIGN      = r'\b[<][-]\b'
    STR_CONST   = r'\"([^\\\n]|(\\.))*?\"' #Preguntar
    IF          = r'\b[iI][fF]\b'
    FI          = r'\b[fF][iI]\b'
    THEN        = r'\b[tT][hH][eE][nN]\b'
    NOT         = r'\b[nN][oO][tT]\b'
    IN          = r'\b[iI][nN]\b'
    CASE        = r'\b[cC][aA][sS][eE]\b'
    ELSE        = r'\b[eE][lL][sS][eE]\b'
    ESAC        = r'\b[eE][sS][aA][cC]\b'
    CLASS       = r'\b[cC][lL][aA][sS][sS]\b'
    INHERITS    = r'\b[iI][nN][hH][eE][rR][iI][tT][sS]\b'
    ISVOID      = r'\b[iI][sS][vV][oO][iI][dD]\b'
    LET         = r'\b[lL][eE][tT]\b'
    LOOP        = r'\b[lL][oO][oO][pP]\b'
    NEW         = r'\b[nN][eE][wW]\b'
    OF          = r'\b[oO][fF]\b'
    POOL        = r'\b[pP][oO][oO][lL]\b'
    WHILE       = r'\b[wW][hH][iI][lL][eE]\b'
    

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                        for i in ['0', '1']
                        for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    


    @_(INT_CONST) # r'(\d+)' para que coja los numeros de mas de un digito
    def INT_CONST(self,t):
        t.value = int(t.value)
        t.type = 'INT_CONST'
        return t

    @_(THEN) 
    def THEN(self,t):
        t.type = 'THEN'
        return t

    @_(OBJECTID)
    def OBJECTID(self, t):
        t.type = 'OBJECTID'
        return t
    
    @_(TYPEID)
    def TYPEID(self, t):
        t.type = 'TYPEID'
        return t

    @_(IF)
    def IF(self, t):
        t.type = 'IF'
        return t

    @_(FI)
    def FI(self, t):
        t.type = 'FI'
        return t

    @_(ASSIGN)
    def ASSIGN(self, t):
        t.type = 'ASSIGN'
        return t

    @_(DARROW)
    def DARROW(self, t):
        t.type = 'DARROW'
        return t

    @_(LE)
    def LE(self, t):
        t.type = 'LE'
        return t

    @_(r'\b[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]\b')
    def BOOL_CONST(self, t):
        t.type = 'BOOL_CONST'
        if t.value == 'true':
            t.value = True
        elif t.value == 'false':
            t.value = False
        else:
            t.type = 'TYPEID'
        return t

    @_(NOT)
    def NOT(self, t):
        t.type = 'NOT'
        return t
    
    @_(IN)
    def IN(self, t):
        t.type = 'IN'
        return t
    
    @_(CASE)
    def CASE(self, t):
        t.type = 'CASE'
        return t
    
    @_(ELSE)
    def ELSE(self, t):
        t.type = 'ELSE'
        return t
    
    @_(ESAC)
    def ESAC(self, t):
        t.type = 'ESAC'
        return t
    
    @_(CLASS)
    def CLASS(self, t):
        t.type = 'CLASS'
        return t
    
    @_(INHERITS)
    def INHERITS(self, t):
        t.type = 'INHERITS'
        return t
    
    @_(ISVOID)
    def ISVOID(self, t):
        t.type = 'ISVOID'
        return t
    
    @_(LET)
    def LET(self, t):
        t.type = 'LET'
        return t
    
    @_(LOOP)
    def LOOP(self, t):
        t.type = 'LOOP'
        return t
    
    @_(NEW)
    def NEW(self, t):
        t.type = 'NEW'
        return t
    
    @_(OF)
    def OF(self, t):
        t.type = 'OF'
        return t
    
    @_(POOL)
    def POOL(self, t):
        t.type = 'POOL'
        return t
    
    @_(WHILE)
    def WHILE(self, t):
        t.type = 'WHILE'
        return t
    
    @_(r'[_]|[!]|[#]|[$]|[%]|[&]|[>]|[?]|[`]|[[]|[]]|[\\]|[|]|[\^]|[\\x*[a-zA-Z0-9]+]|[]|[]|[]|[]')
    def ERROR(self, t):
        t.type = 'ERROR'
        if t.value == '\\':
            t.value = '\\\\'
        elif t.value in self.CARACTERES_CONTROL:
            t.value = f'\\{t.value}'
        return t

    @_(r'"')
    def empiezaString():
        self.begin(STRING)
    
    @_(r'--.*')
    def comentario1Linea(self, t):
        pass

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

class STRING (Lexer):
    tokens = {STR_CONST,ERROR}
