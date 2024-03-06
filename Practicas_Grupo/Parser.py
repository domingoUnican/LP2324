# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *


class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia=[p.Clase])
    
    @_("Programa Clase")
    def Programa(self, p):
        return Programa(secuencia=p.Programa.secuencia + [p.Clase])
    
    @_("CLASS TYPEID opcionalPadre '{' lista_atr_metodos '}'")
    def Clase(self, p):
        return Clase(nombre=p.TYPEID,padre=p.opcionalPadre,caracteristicas=p.lista_atr_metodos)
    
    @_("")
    def opcionalPadre(self, p):
        return "Object"
    
    @_("INHERITS TYPEID")
    def opcionalPadre(self, p):
        return p.TYPEID
    
    @_("")
    def lista_atr_metodos(self, p):
        return []
    
    @_("Atributo lista_atr_metodos")
    def lista_atr_metodos(self, p):
        return [p.Atributo] + p.lista_atr_metodos
    
    @_("Metodo lista_atr_metodos")
    def lista_atr_metodos(self, p):
        return [p.Metodo] + p.lista_atr_metodos
    
    @_("OBJECTID ':' TYPEID opcional_expr")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID,tipo=p.TYPEID,cuerpo=p.opcional_expr)
    
    @_("")
    def opcional_expr(self, p):
        return NoExpr()

    @_("ASSIGN Expresion")
    def opcional_expr(self, p):
        return p.Expresion

    @_("OBJECTID '(' ')' ':' TYPEID '{' Expresion '}'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID,tipo=p.TYPEID,cuerpo=p.Expresion)

    @_("OBJECTID '(' lista_formal Formal ')' ':' TYPEID '{' Expresion '}'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID,tipo=p.TYPEID,cuerpo=p.Expresion,formales=p.lista_formal + [p.Formal])

    @_("")
    def lista_formal(self, p):
        return []

    @_("Formal ',' lista_formal")
    def lista_formal(self, p):
        return [p.Formal] + p.lista_formal

    @_("OBJECTID ':' TYPEID")
    def Formal(self, p):
        return Objeto(nombre=p.OBJECTID)

    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        pass

    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return Suma(izquierda=p[0], derecha=p[2])

    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        return Resta(izquierda=p[0], derecha=p[2])

    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        return Multiplicacion(izquierda=p[0], derecha=p[2])

    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        return Division(izquierda=p[0], derecha=p[2])

    @_("Expresion '<' Expresion")
    def Expresion(self, p):
        return Menor(izquierda=p[0], derecha=p[2])

    @_("Expresion '<=' Expresion")
    def Expresion(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])

    @_("Expresion '=' Expresion")
    def Expresion(self, p):
        return Igual(izquierda=p[0], derecha=p[2])

    @_("'(' Expresion ')'")
    def Expresion(self, p):
        return p.Expresion

    @_("NOT Expresion")
    def Expresion(self, p):
        return Not(expr=p.Expresion)

    @_("ISVOID Expresion")
    def Expresion(self, p):
        return EsNulo(expr=p.Expresion)

    @_("'~' Expresion")
    def Expresion(self, p):
        return Not(expr=p.Expresion)

    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def Expresion(self, p):
        pass

    @_("Expresion '@' TYPEID '.' OBJECTID '(' lista_expr Expresion ')'")
    def Expresion(self, p):
        pass

    @_("")
    def lista_expr(self, p):
        return []

    @_("Expresion ',' lista_expr")
    def lista_expr(self, p):
        return [p.Expresion] + p.lista_expr

    @_("opcional_expr2 OBJECTID '(' lista_expr Expresion ')'")
    def Expresion(self, p):
        pass

    @_("opcional_expr2 OBJECTID '(' ')'")
    def Expresion(self, p):
        pass

    @_("")
    def opcional_expr2(self, p):
        return NoExpr()

    @_("Expresion '.'")
    def opcional_expr2(self, p):
        pass

    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        return Condicional(condicion=p[]1,verdadero=p.[3],falso=p[5])

    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        return Bucle(condicion=p[1],cuerpo=p[3])

    @_("LET OBJECTID ':' TYPEID opcional_expresion_let lista_expr_let IN Expresion")
    def Expresion(self, p):
        #return Let(nombre=p.OBJECTID,tipo=p.TYPEID,inicializacion=,cuerpo=)
        pass

    @_("")
    def opcional_expresion_let(self, p):
        return NoExpr()

    @_("'<-' Expresion")
    def opcional_expresion_let(self, p):
        return 

    @_("")
    def lista_expr_let(self, p):
        pass

    @_("',' OBJECTID ':' TYPEID opcional_expresion_let")
    def lista_expr_let(self, p):
        pass

    @_("CASE Expresion OF '(' lista_expr_case ';' ESAC")
    def Expresion(self, p):
        pass

    @_("OBJECTID ':' TYPEID DARROW '<' Expresion '>'")
    def lista_expr_case(self, p):
        pass

    @_("OBJECTID ':' TYPEID DARROW '<' Expresion '>' lista_expr_case")
    def lista_expr_case(self, p):
        pass

    @_("NEW TYPEID")
    def Expresion(self, p):
        pass

    @_("'{' lista_expr_pc '}'")
    def Expresion(self, p):
        pass

    @_("Expresion ';'")
    def lista_expr_pc(self, p):
        pass

    @_("Expresion ';' lista_expr_pc")
    def lista_expr_pc(self, p):
        pass

    @_("OBJECTID")
    def Expresion(self, p):
        pass

    @_("INT_CONST")
    def Expresion(self, p):
        pass

    @_("STR_CONST")
    def Expresion(self, p):
        pass

    @_("BOOL_CONST")
    def Expresion(self, p):
        pass







