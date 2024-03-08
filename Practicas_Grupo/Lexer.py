# coding: utf-8

from sly import Lexer
import os
import re
import sys





class CoolLexer(Lexer):
    tokens = {OBJECTID, INT_CONST, BOOL_CONST,ASSIGN, TYPEID,
            ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
            INHERITS, ISVOID, LET, LOOP, NEW, OF,
            POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ERROR,COMMENT_1LINEA,COMMENT_BLOQUE}
    #ignore = '\t '
    literals = {'==','=', '+', '-', '*', '/', '(', ')', '<', '>', '.',' ' ,';', ':', '@', ',','{', '}', '[', ']', '~'}
    # Ejemplo
    LE          = r'[<][=]'
    DARROW      = r'[=][>]'
    ASSIGN      = r'[<][-]'
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
    TYPEID      = r'[A-Z]([a-zA-Z0-9_])*'
    INT_CONST   = r'\d+'
    

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                        for i in ['0', '1']
                        for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    @_(r'\b[tT][rR][uU][eE](?![a-zA-Z0-9])|[fF][aA][lL][sS][eE](?![a-zA-Z0-9])\b')
    def BOOL_CONST(self, t):
        t.type = 'BOOL_CONST'
        if t.value[0] == 't':
            t.value = True
        elif t.value[0] == 'f':
            t.value = False
        return t

    @_(r'[a-z]([a-zA-Z0-9_])*')
    def OBJECTID(self, t):
        return t
    
    @_(r'[_]|[!]|[#]|[$]|[%]|[&]|[>]|[?]|[`]|[[]|[]]|[\\]|[|]|[\^]|[\\x*[a-zA-Z0-9]+]|[]|[]|[]|[]|\x00')
    def ERROR(self, t):
        t.type = 'ERROR'
        if t.value == '\\':
            t.value = '\\\\'
        elif t.value == '\x00':
            t.value = "\\000"
        elif t.value == '_':
            t.value = '_'
        elif t.value == '':
            t.value = '\\001'
        elif t.value == '':
            t.value = '\\002'
        elif t.value == '':
            t.value = '\\003'
        elif t.value == '':
            t.value = '\\004'
        t.value = '"' + t.value + '"'
        return t
    
    @_(r'--.*')
    def COMENT_1LINEA(self, t):
        pass

    @_(r'\(\*')
    def COMMENT_BLOQUE(self, t):
        self.begin(Comment)

    @_(r'\*\)')
    def COMMENT_UNMATCHED(self, t):
        t.value = '"' + "Unmatched *)" + '"'
        t.type = 'ERROR'
        return t

    @_(r"\s")
    def spaces(self, t):
        pass

    @_(r'"')
    def STR_CONST(self, t):
        self.begin(StringLexer)

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

class StringLexer(Lexer):
    tokens = {STR_CONST, ERROR}
    _acumulado = ""
    error_nullchar_escaped = False
    error_nullchar = False

    
    @_(r'"')
    def STR_CONST(self, t):
        if self.error_nullchar_escaped:
            t.value = '"' + "String contains escaped null character." + '"'
            t.type = 'ERROR'
            self.error_nullchar_escaped = False
        elif self.error_nullchar:
            t.value = '"' + "String contains null character." + '"'
            t.type = 'ERROR'
            self.error_nullchar = False  
        else:
            t.value = self._acumulado
            self._acumulado = ""
            t.value = '"' + t.value + '"'
        self.begin(CoolLexer)
        return t


    @_(r'\\[\r\n]')
    def SALTOESCAPADO(self, t):
        self._acumulado += "\\n"
        self.lineno += 1
    
    
    @_(r'\\\x00')
    def NULLCHAR_ESCAPED(self, t):
        print("NULLCHAR")
        self.error_nullchar_escaped = True

    @_(r'\x00')
    def NULLCHAR(self, t):
        print("NULLCHAR2")
        self.error_nullchar = True
    

    @_(r'\\\\')
    def DOBLE_BARRA(self, t):
        self._acumulado += t.value[0:]

    @_(r'\t')
    def TABULADORESCAPADO(self, t):
        self._acumulado += '\\t'
    
    @_(r'\\\t')
    def TABULADOR(self, t):
        self._acumulado += '\\t'
    
    @_(r'\\\x08')
    def BACKSPACE(self, t):
        self._acumulado += '\\b'
    
    @_(r'\\\f')
    def FORMFEED(self, t):
        self._acumulado += '\\f'
    
    
    @_(r'\x1B')
    def ESCAPE(self, t):
        print("ESCAPE")
        self._acumulado += "\033"
    
    @_(r'\\[^a-zA-Z0-9\n]')
    def CARACTERESPECIAL(self, t):
        self._acumulado += t.value
    
    @_(r'\\.') # El punto no representa el salto de linea
    def COMILLASESCAPADO(self, t):
        if t.value[1] == 'b':
            t.value = '\\b'
        elif t.value[1] == 'n':
            t.value = '\\n'
        elif t.value[1] == 'f':
            t.value = '\\f'
        elif t.value[1] == 't':
            t.value = '\\t'
        else:
            t.value = t.value[1:]
        
        self._acumulado +=  t.value

    @_(r'[^\\]\n')
    def salto_linea_error(self, t):
        if not self.error_nullchar:
            self._acumulado = ''
            self.begin(CoolLexer)
            t.value = '"' + "Unterminated string constant" + '"'
            t.type = 'ERROR'
            return t
    
    @_(r'[\\\n]$')
    def salto_linea_escapado_y_EOF(self, t):
        t.value = '"' + "EOF in string constant" + '"'
        t.type = 'ERROR'
        return t

    @_(r'(?:\\")$')
    def QUOTE_EOF(self, t):
        t.value = '"' + "EOF in string constant" + '"'
        t.type = 'ERROR'
        return t
    
    @_(r'[^"]$')
    def EOF(self, t):
        print("EOF")
        t.value = '"' + "EOF in string constant" + '"'
        t.type = 'ERROR'
        return t

    @_(r'.')
    def CUALQUIER_COSA(self, t):
        self._acumulado += t.value
    
    def error(self, t):
        self.index += 1

class Comment(Lexer):
    tokens = {CMT_CONST}
    cmt_id = 0

    @_(r'\*\)')
    def CMT_CONST(self, t):
        if self.cmt_id == 0:
            self.begin(CoolLexer)
        else:
            self.cmt_id -= 1

    @_(r'\(\*')
    def inside_CMT_CONST(self, t):
        self.cmt_id += 1

    @_(r'\n')
    def salto_linea(self, t):
        self.lineno += 1

    @_(r'.$')
    def EOF_CMT(self, t):
        print("EOF comment")
        t.value = "EOF in comment"
        t.type = 'ERROR'
        return t

    @_(r'.')
    def caracter(self, t):
        pass


    

