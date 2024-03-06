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

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia = [p.Clase])

    @_("CLASS TYPEID INHERITSTYPEID '{' '}'")
    def Clase(self, p):
        return Clase(p.TYPEID0, p.TYPEID1, [])

    @_("CLASS TYPEID INHERITSTYPEID '{' cuerpo_clase '}'")
    def Clase(self, p):
        return Clase(p.TYPEID0, p.TYPEID1, p.cuerpo_clase)

    @_("INHERITS TYPEID")
    def INHERITSTYPEID(self, p):
        return p.TYPEID

    @_("")
    def cuerpo_clase(self, p):
        return []

    @_("cuerpo_clase caracteristica ';'")
    def cuerpo_clase(self, p):
        return p.cuerpo_clase + [p.caracteristica]

    @_("Atributo ';' ")
    def caracteristica(self, p):
        return p.Atributo

    @_("Metodo ';' ")
    def caracteristica(self, p):
        return p.Metodo

    @_("OBJECTID ':' TYPEID")
    def Atributo(self, p):
        return Atributo(p.OBJECTID, p.TYPEID)

    @_("OBJECTID ':' TYPEID ASSIGN expr")
    def Atributo(self, p):
        return Atributo(p.OBJECTID, p.TYPEID, p.expr)

    @_("OBJECTID '(' ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return Metodo(p.OBJECTID, p.TYPEID, [], p.expr)

    @_("OBJECTID '(' formal ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return Metodo(p.OBJECTID, p.TYPEID, p.formal, p.expr)

    @_("")
    def formal(self, p):
        return []

    @_("OBJECTID ':' TYPEID")
    def formal(self, p):
        return [Formal(p.OBJECTID, p.TYPEID)]

    @_("OBJECTID ASSIGN expr")
    def expr(self, p):
        return Assign(p.OBJECTID, p.expr)

    @_("expr '+' expr ',' expr '-' expr ',' expr '*' expr ',' expr '/' expr ',' expr '<' expr ',' expr LE expr ',' expr '=' expr")
    def expr(self, p):
        return BinOp(p[1], p.expr0, p.expr1)

    @_("NOT expr")
    def expr(self, p):
        return Not(p.expr)

    @_("ISVOID expr")
    def expr(self, p):
        return EsNulo(p.expr)

    @_("'~' expr")
    def expr(self, p):
        return Neg(p.expr)

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("'@' TYPEID '.' OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodo(p.TYPEID,p.OBJECTID, [])

    @_("'@' TYPEID '.' OBJECTID '(' expr ')'")
    def expr(self, p):
        return LlamadaMetodo(p.TYPEID, p.OBJECTID, p.expr)

    @_("OBJECTID '(' expr ')'")
    def expr(self, p):
        return LlamadaMetodoEstatico(p.OBJECTID, p.expr)

    @_("OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodoEstatico(p.OBJECTID, [])

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        return If(p.expr0, p.expr1, p.expr2)

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        return While(p.expr0, p.expr1)

    @_("LET OBJECTID ':' TYPEID lista_inicia IN expr")
    def expr(self, p):
        ultima_inicia = p.lista_inicia[-1]
        # Vamos a suponer que ultima_inicia = [nombre, tipo, inicializacion]
        temp = Let(nombre = ultima_inicia[0],
                    tipo = ultima_inicia[1], 
                    inicializacion=ultima_inicia[2], 
                    cuerpo = p.expr)
        
        for i in range(len(p.lista_inicia), 0, -1):
            ultima_inicia = p.lista_inicia[i]
            temp = Let(nombre=ultima_inicia[0])
        return temp
    
    @_("OBJECTID ':' TYPEID")
    def lista_inicia(self, p):
        return [p.lista_inicia] + [p.asignacion]

    # @_("LET declaraciones IN expr")
    # def expr(self, p):
    #     return Let(p.declaraciones, p.expr)

    # @_("OBJECTID ':' TYPEID asignacion")
    # def declaraciones(self, p):
    #     return [(p.OBJECTID, p.TYPEID, p.asignacion)]

    # @_("OBJECTID ':' TYPEID")
    # def declaraciones(self, p):
    #     return [(p.OBJECTID, p.TYPEID, None)]


    @_("CASE expr OF '{' '}' ESAC")
    def expr(self, p):
        return Case(p.expr, [])

    @_("CASE expr OF '{' cuerpo_case '}' ESAC")
    def expr(self, p):
        return Case(p.expr, p.cuerpo_case)

    @_("")
    def cuerpo_case(self, p):
        return []

    @_("cuerpo_case OBJECTID ':' TYPEID DARROW expr ';' ")
    def cuerpo_case(self, p):
        return p.cuerpo_case + [(p.OBJECTID, p.TYPEID, p.expr)]

    @_("NEW TYPEID")
    def expr(self, p):
        return New(p.TYPEID)

    @_("'{' expr '}'")
    def expr(self, p):
        return p.expr

    @_("OBJECTID")
    def expr(self, p):
        return p.OBJECTID

    @_("INT_CONST")
    def expr(self, p):
        return p.INT_CONST

    @_("STR_CONST")
    def expr(self, p):
        return p.STR_CONST

    @_("BOOL_CONST")
    def expr(self, p):
        return p.BOOL_CONST



