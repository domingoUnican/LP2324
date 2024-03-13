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
    
    @_("Clase ';'")
    def Programa(self, p):
        return Programa(secuencia = [p.Clase])
    
    @_("Programa Clase ';'")
    def Programa(self, p):
        return Programa(secuencia = p.Programa.secuencia + [p.Clase])

    @_("Programa error")
    def Programa(self, p):
        self.errores.append(f", line {p.error.lineno}: syntax error at or near {p.error.value}")
        return Programa(secuencia = [p.Programa])

    @_("CLASS TYPEID '{' '}'")
    def Clase(self, p):
        return Clase(nombre=p[0], padre="Object",nombre_fichero=self.nombre_fichero, caracteristicas=[])

    @_("CLASS TYPEID '{' cuerpo_clase '}'")
    def Clase(self, p):
        return Clase(nombre=p[0], padre="Object",nombre_fichero=self.nombre_fichero, caracteristicas=p.cuerpo_clase)

    @_("CLASS TYPEID INHERITS TYPEID '{' '}'")
    def Clase(self, p):
        return Clase(nombre=p[0], padre=p[2],nombre_fichero=self.nombre_fichero, caracteristicas=[])

    @_("CLASS TYPEID INHERITS TYPEID '{' cuerpo_clase '}'")
    def Clase(self, p):
        return Clase(nombre=p[0], padre=p[2],nombre_fichero=self.nombre_fichero, caracteristicas=p.cuerpo_clase)

    @_("")
    def cuerpo_clase(self, p):
        return []

    @_("cuerpo_clase caracteristica ';'")
    def cuerpo_clase(self, p):
        return p.cuerpo_clase + [p.caracteristica]

    @_("Atributo")
    def caracteristica(self, p):
        return p.Atributo

    @_("Metodo")
    def caracteristica(self, p):
        return p.Metodo

    @_("OBJECTID ':' TYPEID")
    def Atributo(self, p):
        return Atributo(nombre=p[0], tipo=p[2], cuerpo=NoExpr())

    @_("OBJECTID ':' TYPEID ASSIGN expr")
    def Atributo(self, p):
        return Atributo(nombre=p[0], tipo=p[2],cuerpo=p.expr)

    @_("OBJECTID '(' ')' ':' TYPEID '{' '}'")
    def Metodo(self, p):
        return Metodo(formales=[],nombre=p[0], tipo=p[4], cuerpo=NoExpr())

    @_("OBJECTID '(' ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return Metodo(formales=[],nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expr)

    @_("OBJECTID '(' formal ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID, tipo=p.TYPEID, formales=p.formal, cuerpo=p.expr)

    @_("")
    def formal(self, p):
        return []

    @_("OBJECTID ':' TYPEID")
    def formal(self, p):
        return [Formal(nombre_variable=p.OBJECTID,tipo= p.TYPEID)]

    @_("OBJECTID ASSIGN expr")
    def expr(self, p):
        return Asignacion(nombre=p.OBJECTID, cuerpo=p.expr)

    @_("expr '+' expr")
    def expr(self, p):
        return Suma(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '-' expr")
    def expr(self, p):
        return Resta(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '*' expr")
    def expr(self, p):
        return Multiplicacion(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '/' expr")
    def expr(self, p):
        return Division(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '<' expr")
    def expr(self, p):
        return Menor(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr LE expr")
    def expr(self, p):
        return LeIgual(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '=' expr")
    def expr(self, p):
        return Igual(izquierda=p.expr0, derecha=p.expr1)

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

    @_("expr '@' TYPEID '.' OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodo(cuerpo=p.expr,nombre_metodo=p.OBJECTID,argumentos=[])

    @_(" expr '@' TYPEID '.' OBJECTID '(' expr ')'")
    def expr(self, p):
        return LlamadaMetodo(cuerpo=p.expr0, nombre_metodo=p.OBJECTID, argumentos=[p.expr1])

    @_("OBJECTID '(' expr ')'")
    def expr(self, p):
        return LlamadaMetodoEstatico(nombre_metodo=p.OBJECTID, argumentos=p.expr)

    @_("OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodoEstatico(nombre_metodo=p.OBJECTID, argumentos=[])

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        return Condicional(condicion=p.expr0,verdadero=p.expr1, falso=p.expr2)

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        return Bucle(condicion=p.expr0, cuerpo=p.expr1)

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
        return Swicht(expr=p.expr, casos=[])

    @_("CASE expr OF '{' cuerpo_case '}' ESAC")
    def expr(self, p):
        return Swicht(expr=p.expr, casos=[p.cuerpo_case])

    @_("")
    def cuerpo_case(self, p):
        return []

    @_("cuerpo_case OBJECTID ':' TYPEID DARROW expr ';' ")
    def cuerpo_case(self, p):
        return RamaCase(nombre_variable=p.OBJECTID,tipo=p.TYPEID,cuerpo=p.expr)

    @_("NEW TYPEID")
    def expr(self, p):
        return Nueva(p.TYPEID)

    @_("'{' expr '}'")
    def expr(self, p):
        return p.expr

    @_("OBJECTID")
    def expr(self, p):
        return Objeto(nombre=p.OBJECTID)

    @_("INT_CONST")
    def expr(self, p):
        return Entero(valor=p.INT_CONST)

    @_("STR_CONST")
    def expr(self, p):
        return String(valor=p.STR_CONST)

    @_("BOOL_CONST")
    def expr(self, p):
        return Booleano(valor=p.BOOL_CONST)
    
    @_("'{' bloque '}'")
    def expr(self, p):
        print(p.bloque)
        return Bloque(expresiones=p.bloque)
    
    @_("expr ';'")
    def bloque(self,p):
        return [p.expr]
    
    @_("bloque expr ';'")
    def bloque(self, p):
        return p.bloque + [p.expr]
    
    @_("bloque error ';'")
    def bloque(self, p):
        return p.bloque

    def error(self, p):
        if p is None:
            self.errores.append(f"EOF: syntax error")
        else:
            self.errores.append(f"\"{self.nombre_fichero}\", line {p.lineno}: syntax error at or near {p.value}")
        

    