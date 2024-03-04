# coding: utf-8

from sly import Lexer
import os
import re
import sys

class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
              ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
              INHERITS, ISVOID, LET, LOOP, NEW, OF,
              POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN, SEMICOLON,
              EQ, PLUS, MINUS, MULT, DIV, LPAREN, RPAREN, LT, GT, DOT, COMMA, COLON, AT,}
    
    #ignore = '\t '
    literals = {';', ':', '@', '.', ',', '<', '(', ')', '+', '-', '*', '/', '=', '{', '}', '>', '==', '!=', '~'}
    # Ejemplo
    ELSE = r'\b[eE][lL][sS][eE]\b'

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    #tokens
    #then
    @_(r'\b[tT][hH][eE][nN]\b')
    def THEN(self, t):
        t.type = 'THEN'
        return t
    
    #BOOLEANOS
    @_(r"\b[t][rR][uU][eE]\b")
    def BOOL_CONST1(self, t):
        t.type = 'BOOL_CONST'
        t.value = True
        return t
    
    @_(r"\b[f][aA][lL][sS][eE]\b")
    def BOOL_CONST2(self, t):
        t.type = 'BOOL_CONST'
        t.value = False
        return t
    
    #enteros
    @_(r"[0-9]+")
    def INT_CONST(self, t):
        t.value = t.value
        return t
    
    #notacion especial
    @_(r"[<][=]")
    def LE(self, t):
        t.type = 'LE'
        return t
    
    @_(r"[=][>]")
    def DARROW(self, t):
        t.type = 'DARROW'
        return t
    
    @_(r"[<][-]")
    def ASSIGN(self, t):
        t.type = 'ASSIGN'
        return t
    # comentarios de una línea
    @_(r'--.*')
    def ignore_comment(self, t):
        pass

    # comentarios de varias líneas
    @_(r'\(\*(.|\n)*?\*\)')
    def ignore_multiline_comment(self, t):
        self.lineno += t.value.count('\n')

        #palabras reservadas
    #=======================================
    #else
    @_(r'\b[eE][lL][sS][eE]\b')
    def ELSE(self, t):
        return t
    
    #if
    @_(r'\b[iI][fF]\b')
    def IF(self, t):
        t.type = 'IF'
        return t
    
    #fi
    @_(r'\b[fF][iI]\b')
    def FI(self, t):
        t.type = 'FI'
        return t

    
    #not
    @_(r'\b[nN][oO][tT]\b')
    def NOT(self, t):
        return t
    
    #in
    @_(r'\b[iI][nN]\b')
    def IN(self, t):
        return t
    
    #case
    @_(r'\b[cC][aA][sS][eE]\b')
    def CASE(self, t):
        return t
    
    #esac
    @_(r'\b[eE][sS][aA][cC]\b')
    def ESAC(self, t):
        return t
    
    #class
    @_(r'\b[cC][lL][aA][sS][sS]\b')
    def CLASS(self, t):
        t.type = 'CLASS'
        return t
    
    #inherits
    @_(r'\b[iI][nN][hH][eE][rR][iI][tT][sS]\b')
    def INHERITS(self, t):
        return t
    
    #isvoid
    @_(r'\b[iI][sS][vV][oO][iI][dD]\b')
    def ISVOID(self, t):
        return t
    
    #let
    @_(r'\b[lL][eE][tT]\b')
    def LET(self, t):
        return t
    
    #loop
    @_(r'\b[lL][oO][oO][pP]\b')
    def LOOP(self, t):
        return t
    
    #new
    @_(r'\b[nN][eE][wW]\b')
    def NEW(self, t):
        return t
    
    #of
    @_(r'\b[oO][fF]\b')
    def OF(self, t):
        return t
    
    #pool
    @_(r'\b[pP][oO][oO][lL]\b')
    def POOL(self, t):
        return t
    
    #while
    @_(r'\b[wW][hH][iI][lL][eE]\b')
    def WHILE(self, t):
        return t

    # strings
    @_(r'"([^"\\\n]|(\\.))*?"')
    def STR_CONST(self, t):

        t.value = t.value.replace("\n", "\\n")
        t.value = t.value.replace("\t", "\\t")
        t.value = t.value.replace("\b", "\\b")
        t.value = t.value.replace("\r", "\\r")
        if len(t.value) > 1024:
            raise ValueError("String length exceeds limit of 1024 characters")
        return t

        #identificadores de tipos
    @_(r"\b[A-Z][a-zA-Z0-9_]*\b")
    def TYPEID(self, t):
        return t

        # identificadores de objetos
    @_(r"[a-z][a-zA-Z0-9_]*\b")
    def OBJECTID(self, t):
        return t

    
    #=======================================
    #espacios
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
