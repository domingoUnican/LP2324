# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    literals = CoolLexer.literals
    debugfile = "salida.out"
    errores = []
    precedence = (
        ('right', "ASSIGN"),
        ('left', "NOT"),
        ('left', "+", "-"),
        ('left', "*", "/"),
        ('left', "ISVOID"),
    )

    @_("CLASS OBJECTID")
    def Programa(self, p):
        pass
