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
    IF = __kw('if')
    FI = __kw('fi')
    THEN = __kw('then')
    ELSE = __kw('else')
    CASE = __kw('case')
    ESAC = __kw('esac')
    LOOP = __kw('loop')
    WHILE = __kw('while')
    POOL = __kw('pool')
    NOT = __kw('not')
    IN = __kw('in')
    ISVOID = __kw('isvoid')
    CLASS = __kw('class')
    INHERITS = __kw('inherits')
    LET = __kw('let')
    NEW = __kw('new')
    OF = __kw('of')

    # language=PythonRegExp
    @_(r'--(?=(?P<lc_atom>.*))(?P=lc_atom)')
    def LINE_COMMENT(self, t):
        pass

    # language=PythonRegExp
    @_(r'\(\*')
    def BLOCK_COMMENT_START(self, t):
        self.push_state(CoolLexer.BlockComment)

    class BlockComment(Lexer):
        tokens = {}

        # @_(r'(?:[^(*\n-]|-(?!-)|\((?!\*)|\*(?!\)))+')
        # language=PythonRegExp
        @_(r'(?:[^(*\n]|\((?!\*)|\*(?!\)))+')
        def COMMENT_PART(self, t):
            pass

        # # language=PythonRegExp
        # @_(r'[\s\S]$')
        # def error_EOF_IN_COMMENT(self, t):
        #     print("!!!! EOF in comment found")
        #     sys.stdout.flush()
        #     if t == '\n':
        #         self.lineno += 1
        #         t.lineno += 1
        #     t.type = "ERROR"
        #     t.value = "EOF in comment"
        #     return t

        # @_(r'--.*')
        # def LINE_COMMENT(self, t):
        #     pass

        @_(r'\(\*')
        def BLOCK_COMMENT_START(self, t):
            self.push_state(CoolLexer.BlockComment)

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
                result = f'#{token.lineno} {token.type} "{token.value}"'
            else:
                result = f'#{token.lineno} {token.type}'
            list_strings.append(result)
        return list_strings
