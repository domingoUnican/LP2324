# coding: utf-8

from sly import Lexer
import os
import re
import sys



class Comment(Lexer):
    tokens = {}

    @_(r'\*\)')
    def COMENT(self, t):
        self.begin(CoolLexer)
    
    @_(r'.|\n')
    def ERROR(self, t):
        pass




class STRING(Lexer):
    tokens = {STR_CONST}

    _num_string = ""    

    @_(r'[\\ ]+\n')
    def ESCAPESALTO(self, t):
        self._num_string += "\\n"
        print("Escape salto")
        return

    @_(r'\\\\')
    def ESCAPAbarra(self, t):
        self._num_string += "\\\\"
        pass

    

    @_(r'\\[btnf\\\\n"]')
    def ESCAPAR1(self, t):
        self._num_string += t.value
        pass

    @_(r'\\.')
    def ESCAPAR2(self, t):
        self._num_string += t.value.replace("\\", "")
        pass

    @_(r'\\\"')
    def COMILLAS(self, t):
        self._num_string += "\\\""
        pass

    @_(r'\"')
    def STR_CONST(self, t):
        print(t.value)
        t.value = self._num_string.replace("\t", "\\t")
        t.value = self._num_string.replace("\n", "\\n")
        self._num_string = ""
        t.value = "\"" + t.value + "\""
        self.begin(CoolLexer)
        return t


    @_(r'[^\\\n]')
    def BIEN(self, t):
        self._num_string += t.value
        pass
    
    

    @_(r'\n')
    def ERROR(self, t):
        t.value = "Unterminated string constant"
        print("Error")
        self.begin(CoolLexer)
        return t

    

class CoolLexer(Lexer):


    ignore = '\t '
    literals = {';',':','{','}','(',')','+','-','*','\\', '@', '~', '<','=','.',',','/'}

    # Ejemplo
    ELSE = r'\b[eE][lL][sS][eE]\b'

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                          for i in ['0', '1']
                          for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    


    @_(r'<=')
    def LE(self,t):
        return t

    @_(r'\"')
    def STR_CONST(self,t):
        self.begin(STRING)

        
    @_(r'\b[Ii][Ss][Vv][Oo][Ii][Dd]\b')
    def ISVOID(self,t):
        return t
    
    @_(r'\b[Ii][Nn][Hh][Ee][Rr][Ii][Tt][Ss]\b')
    def INHERITS(self,t):
        return t
    
    @_(r'\b[Oo][Ff]\b')
    def OF(self,t):
        return t
        
    @_(r'\b[Nn][Ee][Ww]\b')
    def NEW(self,t):
        return t
    
    @_(r'\b[Cc][Aa][Ss][Ee]\b')
    def CASE(self,t):
        return t
        
    @_(r'\b[Ee][Ss][Aa][Cc]\b')
    def ESAC(self,t):
        return t

    @_(r'\b[wW][hH][iI][lL][eE]\b')
    def WHILE(self,t):
        return t
    
    @_(r'\b[Ll][Oo][Oo][Pp]\b')
    def LOOP(self,t):
        return t
    
    @_(r'\b[Pp][Oo][Oo][Ll]\b')
    def POOL(self,t):
        return t
        
    @_(r'\b[Ll][Ee][Tt]\b')
    def LET(self,t):
        return t
    
    @_(r'\b[Ii][Nn]\b')
    def IN(self,t):
        return t
    
    @_(r'\b[Nn][Oo][Tt]\b')
    def NOT(self,t):
        return t
    
    @_(r'\b[Ee][Ll][Ss][Ee]\b')
    def ELSE(self,t):
        return t
    
    @_(r'\b[Ff][iI]\b')
    def FI(self,t):
        return t
    
    @_(r'\b[iI][fF]\b')
    def IF(self, t):
        return t

    @_(r'\b[Cc][Ll][Aa][Ss][Ss]\b')
    def CLASS(self, t):
        return t
    
    @_(r'[0-9]+')
    def INT_CONST(self,t):
        return t
    

    @_(r"\bf[Aa][Ll][Ss][Ee]\b|\bt[Rr][Uu][Ee]\b")
    def BOOL_CONST(self,t):
        t.value = t.value.upper() == "TRUE"

        return t
    
    @_(r'\b[Tt][Hh][Ee][Nn]\b')
    def THEN(self,t):
        return t
    
    @_(r"[a-z][a-zA-Z0-9_]*")
    def OBJECTID(self,t):
        return t
    
    @_(r"[A-Z][a-zA-Z0-9_]*")
    def TYPEID(self,t):
        return t
    

    @_(r'=>')
    def DARROW(self,t):
        return t
    
    @_(r'<-')

    def ASSIGN(self,t):
        return t
        
    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'(\-\-.*)')
    def commentsDash(self,t):
        pass 

    @_(r'(\(\*)')
    def commentsSlash(self,t):
        self.begin(Comment)

    



    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\_')
    def ERROR(self, t):
        t.value = "\"_\""
        return t
    
    def error(self, t):
        self.index += 1

    tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
            ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
            INHERITS, ISVOID, LET, LOOP, NEW, OF,
            POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN}
    
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

if __name__ == '__main__':
    a = CoolLexer()
    for i in a.tokenize('"hola\x09"'):
        print(i)
