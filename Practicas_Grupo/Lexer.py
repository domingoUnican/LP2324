# coding: utf-8
import importlib
from types import ModuleType
from typing import Mapping, Sequence
import builtins

# built_in__import__ = builtins.__import__
#
#
# def __patched__import(
#         name: str, globals: Mapping[str, object] | None = None,
#         locals: Mapping[str, object] | None = None,
#         fromlist: Sequence[str] = (),
#         level: int = 0) -> ModuleType:
#     if name == 're':
#         name = 'regex'
#         print("Patched ")
#     return built_in__import__(name, globals, locals, fromlist, level)
#
#
# builtins.__import__ = __patched__import

import re
from sly.lex import Token
#from Practicas_Grupo.sly.lex import Token

from sly import Lexer
import os
import sys


# Dummy decorator to appease PyCharm not understanding the Lexer metaclass
def _(_):
    return lambda _: None

@_(r'\\\n$')
def ERROR_ADD_LINE(self, t):
    self.lineno += 1
    self._caracteres = '"'
    t.type = "ERROR"
    t.value = '"EOF in string constant"'
    self._caracteres = '"'
    self._contador = 0
    self.begin(CoolLexer)
    return t
    
@_(r'\\\n')
def ADD_LINE(self, t):
    self._contador += 1
    self.lineno += 1
    self._caracteres += r'\n'



@_(r'([^"]|(\\\n))$')
def FIN_FICHERO(self, t):
    t.type = "ERROR"
    t.value = '"EOF in string constant"'
    self._caracteres = '"'
    self.begin(CoolLexer)
    return t

@_(r'.*\x00[^"]*"?')
def CARACTER_FIN(self, t):
    self._caracteres = '"'
    t.type = "ERROR"
    if '\\\x00' in t.value: 
        t.value = '"String contains escaped null character."'
    else:
        t.value = '"String contains null character."'
    self.begin(CoolLexer)
    return t

@_(r'\n')
def SALTO_LINEA(self, t):
    self._caracteres = '"'
    self.lineno += 1
    t.type = "ERROR"
    t.value = '"Unterminated string constant"'
    self._contador = 0
    self.begin(CoolLexer)
    return t
@_(r'.')
def CAR(self, t):
    self._contador += 1
    if t.value in CoolLexer.CARACTERES_CONTROL:
            self._caracteres += (
                '\\'+str(oct(int(t.value.encode("ascii").hex(), 16)).replace('o', '0'))[-3:])
    else:
        self._caracteres += t.value

def error(self, t):
    print(f'ERROR en linea {t.lineno} por {t.value}\n')

class Comments(Lexer):
    tokens = {}
    profundidad = 1


    @_(r'\n?\(\*\*\)')
    def COMMENTOPEN(self, t):
        pass
        
    @_(r'[^\\]\*\)$')
    def ERROR(self, t):
        self.profundidad -= 1
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)
        else:
            t.type = "ERROR"
            t.value = '"EOF in comment"'
            self.begin(CoolLexer)
            return t

    @_(r'(.|\n)$')
    def ERROR2(self, t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        self.begin(CoolLexer)
        return t
    
    @_(r'([^\\]\*\))')
    def INSIDE(self, t):
        self.lineno += t.value.count("\n")
        self.profundidad -= 1
        if not self.profundidad:
            self.profundidad = 1
            self.begin(CoolLexer)

    @_(r'[^\\]\(\*')
    def OUTSIDE(self, t):
        self.lineno += t.value.count("\n")
        self.profundidad += 1
    @_(r'\n')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'.')
    def EAT(self, t):
        pass

    def salida(self, texto):
        return ['#1 ERROR "EOF in string constant"']
    

class CoolLexer(Lexer):

    tokens = {
        INT_CONST, STR_CONST, BOOL_CONST,  # NUMBER
        TYPEID, OBJECTID,
        LE, DARROW, ASSIGN,
        IF, FI, THEN, ELSE, CASE, ESAC, LOOP, WHILE, POOL,
        NOT, IN, ISVOID,
        CLASS, INHERITS,
        LET, NEW, OF,
        TRUE, FALSE,
    }

    literals = {
        '==', r'+', '-', '*', '/', '(', ')', '<', '.', ',', ';', ':', '@', '{', '}',
        '~', '=',  
    }

    @staticmethod
    def __kw(kw):
        return r'\b' + ''.join(f'[{l.upper()}{l.lower()}]' for l in kw) + r'\b'

    # Ejemplo

        @_(r'\*\)')
        def BLOCK_COMMENT_END(self, t):
            self.pop_state()

        @_(r'\n+')
        def ignore_newlines(self, t):
            self.lineno += t.value.count('\n')

    # language=PythonRegExp
    @_(r'<=')
    def LE(self, t):
        return t

    # language=PythonRegExp
    @_(r'=>')
    def DARROW(self, t):
        return t

    # language=PythonRegExp
    @_(r'<-')
    def ASSIGN(self, t):
        return t

    # language=PythonRegExp
    @_(r'\bt[Rr][Uu][Ee]\b|\bf[Aa][Ll][Ss][Ee]\b')
    def BOOL_CONST(self, t):
        t.value = t.value[0] == 't'
        return t

    # language=PythonRegExp
    INT_CONST = r'\d+'

    # language=PythonRegExp
    # @_(r'\b(?:0x[0-9a-fA-F]+\b|0o[0-7]+|0b[01]+|\d+)\b')
    # def INT_CONST(self, t):
    #     if t.value[:2] == '0x':
    #         t.value = int(t.value[2:], 16)
    #     elif t.value[:2] == '0o':
    #         t.value = int(t.value[2:], 8)
    #     elif t.value[:2] == '0b':
    #         t.value = int(t.value[2:], 2)
    #     else:
    #         t.value = int(t.value)
    #     return t

    # @_(r'(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?|\d+[eE][+-]?\d+')
    # def FLOAT_CONST(self, t):
    #     t.value = float(t.value)
    #     return t

    # language=PythonRegExp
    @_(r'"(?:[^"\\\n\0]|\\(?:[\s\S]|$))*(?:"|\n(?!(?:[ \t]*\n)?$)|\0(?:[^"\\\n]|\\(?:[\s\S]|$))*"?|$)')
    def STR_CONST(self, t):
        lines = t.value.count('\n')
        self.lineno += lines
        t.lineno += lines
        s = t.value  # [1:-1]
        # s = s.replace(r'\b', '\b')
        # s = s.replace(r'\t', '\t')
        # s = s.replace(r'\n', '\n')
        # s = s.replace(r'\r', '\r')
        # s = s.replace('\\\\', '\\')
        tt = re.sub(r'\\[\s\S]', '', s)
        if tt[-1] != '"':
            t.type = "ERROR"
            if '\0' in tt:
                t.value = "String contains null character."
            elif len(tt) >= 1 and tt[-1] == '\n':
                t.value = "Unterminated string constant"
            else:
                t.value = "EOF in string constant"
            return t
        has_null = False
        def replace_escape(m):
            nonlocal has_null
            if m.group('null'):
                has_null = True
                return m.group('null')
            if m.group('preserved'):
                return m.group('preserved')
            return m.group('repl')
        s = re.sub(
            # r'\\(?P<repl>[^btnr\\])|(?P<preserved>\\\\)',
            r'\\(?P<repl>[^btnf"\\\0])|(?P<preserved>\\["\\])|(?P<null>\\\0)',
            replace_escape, s)
        if has_null:
            t.type = "ERROR"
            t.value = "String contains escaped null character."
            return t
        if '\0' in s:
            t.type = "ERROR"
            t.value = "String contains null character."
            return t
        s = s.replace('\b', r'\b')
        s = s.replace('\t', r'\t')
        s = s.replace('\n', r'\n')
        # s = s.replace('\r', r'\r')
        s = s.replace('\f', r'\f')

        def replace_control_char(m):
            return f'\\0{oct(ord(m.group(0)))[2:]:>02}'
        s = re.sub(r'[\x01-\x1F\x7F]', replace_control_char, s)
        if len(re.findall(r'\\0[0-7]{2}|\\.|.', s[1:-1])) > 1024:
            t.type = "ERROR"
            t.value = "String constant too long"
            return t
        t.value = s
        return t

    CARACTERES_CONTROL = [
        bytes.fromhex(i + hex(j)[-1]).decode('ascii')
        for i in ['0', '1']
        for j in range(16)
    ] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]

    # language=PythonRegExp
    TYPEID = r'[A-Z][a-zA-Z0-9_]*'
    # language=PythonRegExp
    OBJECTID = r'[a-z][a-zA-Z0-9_]*'

    @_(r'"')
    def STR_CONST(self, t):
        self.begin(Strings)
        

    @_(r'[!#$%^&_>\?`\[\]\\\|\x00]')
    def ERROR2(self, t):
        t.type = "ERROR"
        if t.value == '\\':
            t.value = '\\\\'
        if t.value in self.CARACTERES_CONTROL:
            t.value = '\\' + \
                str(oct(int(t.value.encode("ascii").hex(), 16)
                        ).replace('o', '0')[-3:])
        t.value = '"'+t.value+'"'
        return t

    @_(r'\(\*\*\)')
    def COMMENT0(self, t):
        pass
    @_(r'\(\*$')
    def ERROR7(self, t):
        t.type = "ERROR"
        t.value = '"EOF in comment"'
        return t

    
    @_(r'\(\*')
    def COMMENT(self, t):
        Comments.profundidad = 1
        self.begin(Comments)

    
    @_(r'\*\)')
    def ERRORCIERRE(self, t):
        t.value = '"Unmatched *)"'
        t.type = 'ERROR'
        return t
        
    @_(r'--.*(\n|$)')
    def LINECOMMENT(self, t):
        self.lineno += t.value.count("\n")

    @_(r'\d+')
    def INT_CONST(self, t):
        t.value = t.value
        return t

    @_(r'\bt[rR][uU][eE]\b|\bf[aA][lL][sS][eE]\b')
    def BOOL_CONST(self, t):
        t.value = t.value[0] =='t'
        return t

    @_(r'[A-Z][a-zA-Z0-9_]*')
    def TYPEID(self, t):
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r'[a-z_][a-zA-Z0-9_]*')
    def OBJECTID(self, t):
        if t.value.lower() in self._key_words:
            t.value = t.value.upper()
            t.type = t.value
        return t

    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')


    @_(r'\*\)')
    def error_END_BLOCK_COMMENT(self, t):
        t.type = "ERROR"
        t.value = "Unmatched *)"
        return t


    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        t.type = "ERROR"

        def replace_control_char(m):
            return f'\\0{oct(ord(m.group(0)))[2:]:>02}'
        t.value = re.sub(
            r'[\x00-\x1F\x7F]', replace_control_char,
            t.value[0].replace('\\', '\\\\'))
        return t

    def tokenize(self, text, lineno=1, index=0):
        yield from super().tokenize(text, lineno, index)
        stack = self._Lexer__state_stack
        if stack and len(stack):
            # if stack[-1] == CoolLexer.BlockComment:  # ?
            if True:
                tok = Token()
                tok.type = "ERROR"
                tok.value = "EOF in comment"
                tok.lineno = self.lineno
                tok.index = self.index
                yield tok


    def salida(self, texto):
        list_strings = []
        lexer = CoolLexer()
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
                result = f'#{token.lineno} {token.type} "{token.value}"'
            else:
                result = f'#{token.lineno} {token.type}'

            list_strings.append(result)
        return list_strings

    def tests(self):
        for fich in TESTS:
            f = open(os.path.join(DIR, fich), 'r')
            g = open(os.path.join(DIR, fich + '.out'), 'r')
            resultado = g.read()
            entrada = f.read()
            texto = '\n'.join(self.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            f.close(), g.close()
            if texto.strip().split() != resultado.strip().split():
                print(f"Revisa el fichero {fich}")

