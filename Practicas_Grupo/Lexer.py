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
    literals = {"=","+","-","*","/","(",")","<",">",".",";",":","@",'"','{','}'}
    # Ejemplo
    ELSE = r'\b[eE][lL][sS][eE]\b'

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]


    @_(r'\b[iI][fF]\b')
    def IF(self,t):
        return t

    @_(r'\b[fF][iI]\b')
    def FI(self,t):
        return t
        
    @_(r'\b[tT][hH][eE][nN]')
    def THEN(self,t):
        return t
    
    @_(r'\b[nN][oO][tT]\b')
    def NOT(self,t):
        return t

    @_(r'\b[iI][nN]\b')
    def IN(self,t):
        return t

    @_(r'\b[cC][aA][sS][eE]\b')
    def CASE(self, t):
        return t
    
    @_(r'[Ee][Ss][Aa][Cc]')
    def ESAC(self,t):
        return t
    
    @_(r'\b[Cc][Ll][aA][Ss]{2}\b')
    def CLASS(self,t):
        return t
    
    @_(r'\b[Nn][Ee][Ww]\b')
    def NEW(self,t):
        return t
    
    @_(r'\b[Ll][Oo]{2}[Pp]\b')
    def LOOP(self,t):
        return t
    
    @_(r'\b[Ll][Ee][Tt]\b')
    def LET(self,t):
        return t

    @_(r'\b[Ii][Ss][Vv][Oo][Ii][Dd]\b')
    def ISVOID(self,t):
        return t
    
    @_(r'\b[Ii][Nn][Hh][Ee][Rr][Ii][Tt][Ss]\b')
    def INHERITS(self,t):
        return t

    @_(r'\b[Oo][Ff]\b')
    def OF(self,t):
        return t

    @_(r'\b[Pp][Oo][Oo][Ll]\b')
    def POOL(self,t):
        return t
    
    @_(r'\b[Tt][Hh][Ee][Nn]\b')
    def THEN(self,t):
        return t
    
    @_(r'\b[Ww][Hh][Ii][Ll][Ee]\b')
    def WHILE(self,t):
        return t
        
    #@_(r'\bT[Rr][Uu][Ee]\b')
    #def TRUE(self,t):
    #    return t
        
    #@_(r'\bF[Aa][Ll][Ss][Ee]\b')
    #def FALSE(self,t):
    #    return t

    @_(r'\b((t[rR][uU][eE])|(f[aA][lL][sS][eE]))\b')
    def BOOL_CONST(self,t):
        t.value = t.value[0] == 't'
        return t
    
    @_(r'[A-Z][A-Za-z0-9_]*')
    def TYPEID(self,t):
        return t

    @_(r'[a-z][A-Za-z0-9_]*')
    def OBJECTID(self,t):
        return t

    @_(r'[0-9]+')
    def INT_CONST(self,t):
        return t

    @_(r'\b<=\b')
    def LE(self,t):
        return t

    @_(r'\b=>\b')
    def DARROW(self,t):
        return t
    
    @_(r'\b<-\b')
    def ASSIGN(self,t):
        return t
    
    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'-{2}.*\n?$|\(\*(.|\n)*\*\)')
    def comments(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'(["])(.{1,1024})\1')
    def STR_CONST(self, t):
        t.value = t.value[1:-1]
        #completar TODO
        

    
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
