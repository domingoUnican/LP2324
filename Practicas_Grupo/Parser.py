# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *

#################################################################
###CLASES###
"""Nodo
Formal
Expresion
Asignacion
LlamadaMetodoEstatico
LlamadaMetodo
Condicional
Bucle
Let
Bloque
RamaCase
Swicht
Nueva
OperacionBinaria
Suma
Resta
Multiplicacion
Division
Menor
LeIgual
Igual
Neg
Not
EsNulo
Objeto
NoExpr
Entero
String
Booleano
IterableNodo
Programa
Caracteristica
Clase
Metodo
Atributo
Arbol
Ambito"""
#################################################################

class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []

    precedence = (
        ('right', ASSIGN),
        ('nonassoc', LE, DARROW, NOT),
       ('left', '+', '-'),
       ('left', '*', '/'),
       ('left', ISVOID),
       ('left', '@'),
       ('left', '.'),
    )

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia = [p.Clase])

    @_("Programa Clase")
    def Programa(self, p):
        p.Programa.secuencia.append(p.Clase)
        return Programa(secuencia = p.Programa.secuencia)

    @_("CLASS TYPEID opcional '{' lista_atr_metodos '}' ';'")
    def Clase(self, p):
        return Clase(nombre= p.TYPEID, padre="Object",caracteristicas=p.lista_atr_metodos, nombre_fichero=self.nombre_fichero)

    @_("Atributo ';' lista_atr_metodos")
    def lista_atr_metodos(self, p):
        return [p[0]] + p[2]

    @_("")
    def lista_atr_metodos(self, p):
        return []

    @_("Metodo ';' lista_atr_metodos")
    def lista_atr_metodos(self, p):
        return [p[0]]+ p[2]

    @_("")
    def opcional(self, p):
        return "Object"

    @_("INHERITS TYPEID")
    def opcional(self, p):
        return p.TYPEID

    @_("OBJECTID ':' TYPEID opcional_expr")
    def Atributo(self, p):
        return Atributo(nombre = p.OBJECTID, tipo= p.TYPEID, cuerpo=p.opcional_expr)

    @_("Expresion")
    def opcional_expr(self, p):
        return p.Expresion

    @_("")
    def opcional_expr(self, p):
        return NoExpr()

    @_("OBJECTID '(' ')' ':' TYPEID '{' Expresion  '}'")
    def Metodo(self, p):
        return Metodo(nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.Expresion)

    @_("OBJECTID ':' TYPEID")
    def Formal(self, p):
        return Formal(nombre_variable= p.OBJECTID, tipo=p.TYPEID)

    @_("OBJECTID '(' Formal ',' Formal ')' ':' TYPEID '{' Expresion  '}' ';'")
    def Metodo(self, p):
        formales = [p.Formal0, p.Formal1]
        return Metodo(nombre=p.OBJECTID, formales = formales, tipo = p.TYPEID, cuerpo=p.Expresion)
    
    #OBJECTID ASSIGN ⟨Expresion⟩
    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        return Asignacion(nombre=p.OBJECTID, cuerpo=p.Expresion)

    #IGNORE    
    @_("IGNORE")
    def Expresion(self, p):
        pass


    # ⟨Expresion⟩ + ⟨Expresion⟩
    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return Suma(izquierda=p[0], derecha=p[2])

    @_("NUMBER")
    def Expresion(self, p):
        return Entero(valor=p.NUMBER)

    # ⟨Expresion⟩ - ⟨Expresion⟩
    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        return Resta(izquierda=p[0], derecha=p[2])
    
    # ⟨Expresion⟩ * ⟨Expresion⟩
    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        return Multiplicacion(izquierda=p[0], derecha=p[2])
    
    # ⟨Expresion⟩ / ⟨Expresion⟩
    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        return Division(izquierda=p[0], derecha=p[2])

    # ⟨Expresion⟩ < ⟨Expresion⟩
    @_("Expresion LE Expresion")
    def Expresion(self, p):
        return Menor(izquierda=p[0], derecha=p[2])
    
    # ⟨Expresion⟩ <= ⟨Expresion⟩
    @_("Expresion DARROW Expresion")
    def Expresion(self, p):
        return p[0] <= p[2]

    # ⟨Expresion⟩ = ⟨Expresion⟩
    @_("Expresion '=' Expresion")
    def Expresion(self, p):
        return Igual(izquierda=p[0], derecha=p[2])
        
    #( ⟨Expresion⟩ )
    @_("'(' Expresion ')'")
    def Expresion(self, p):
        return p[1]

    #NOT ⟨Expresion⟩
    @_("NOT Expresion")
    def Expresion(self, p):
        return Not(expr=p.Expresion)
        #return not p[1]
    
    # ISVOID ⟨Expresion⟩
    @_("ISVOID Expresion")
    def Expresion(self, p):
        return EsNulo(expr=p.Expresion)
    
    # ~ ⟨Expresion⟩
    @_("'~' Expresion")
    def Expresion(self, p):
        return Neg(expr=p.Expresion)
    
    #⟨Expresion⟩ @ TYPEID . OBJECTID ( )
    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def Expresion(self, p):
        return p[4]
    
    #⟨Expresion⟩ @ TYPEID . OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    @_("Expresion '@' TYPEID '.' OBJECTID '(' lstExpr Expresion ')'")
    def Expresion(self, p):
        return p[4]
    
    @_("Expresion ',' lstExpr")
    def lstExpr(self, p):
        return p[0] + p[2]
    
    @_("Expresion")
    def lstExpr(self, p):
        return p.Expresion

    #[ ⟨Expresion⟩ .] OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    @_("exprOpcional OBJECTID '(' lstExpr Expresion ')'")
    def Expresion(self, p):
        return 1

    # [ ⟨Expresion⟩ .] OBJECTID ( )
    @_("exprOpcional OBJECTID '(' ')'")
    def Expresion(self, p):
        #return Expresion(p.OBJECTID, None, [])
        return p.exprOpcional
    
    #IF ⟨Expresion⟩ THEN ⟨Expresion⟩ ELSE ⟨Expresion⟩ FI
    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        return Condicional(condicion=p[1], verdadero=p[3], falso=p[5])
    
    #  WHILE ⟨Expresion⟩ LOOP ⟨Expresion⟩ POOL
    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])

    #LET OBJECTID : TYPEID [<- ⟨Expresion⟩] (, OBJECTID : TYPEID [<- ⟨Expresion⟩])* IN ⟨Expresion⟩
    @_("LET OBJECTID ':' TYPEID exprOpcional lstArrow IN Expresion")
    def Expresion(self, p):
        lista = [p.exprOpcional] + p.lstArrow
        if lista == []:
            return p.Expresion
        else:
            ultima_inicia = lista[-1] #-1
            temp  = Let(nombre = ultima_inicia[0],
                    tipo=ultima_inicia[1],
                    inicializacion=ultima_inicia[2],
                    cuerpo = p.Expresion
                    )
            for i in range(len(lista, 0, -1)):
                ultima_inicia = lista[i]
                temp  = Let(nombre = ultima_inicia[0],
                    tipo=ultima_inicia[1],
                    inicializacion=ultima_inicia[2],
                    cuerpo = p.Expresion
                    )
            return temp
            

    @_("',' OBJECTID ':' TYPEID exprOpcional lstArrow")
    def lstArrow(self, p):
        return [p.exprOpcional] + [p.lstArrow]

    @_("ASSIGN Expresion")
    def exprOpcional(self, p):
        return p.Expresion

    @_("")
    def exprOpcional(self, p):
        return NoExpr()

    @_("Expresion '.'")
    def exprOpcional(self, p):
        return p.Expresion
    
    @_("")
    def lstArrow(self, p):
        return []

    #CASE ⟨Expresion⟩ OF (OBJECTID : TYPEID DARROW <Expresion>)+ ; ESAC
    @_("Case Expresion OF CaseList ';' ESAC")
    def Expresion(self, p):
        return p.CaseList

    @_("OBJECTID ':' TYPEID DARROW Expresion")
    def Case(self, p):
        return RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion)

    @_("Case CaseList")
    def CaseList(self, p):
        return [p.Case] + p.CaseList

    @_("Case")
    def CaseList(self, p):
        return [p.Case]

    #  NEW TYPEID
    @_("NEW TYPEID")
    def Expresion(self, p):
        return Nueva(tipo=p.TYPEID)

    #{ (⟨Expresion⟩ ;) + }
    @_("'{' listNueva '}' ")
    def Expresion(self, p):
        return Bloque(expresiones=p.listNueva)

    @_("Expresion ';' listNueva")
    def listNueva(self, p):
        return [p.Expresion] + p.listNueva

    @_("Expresion ';'")
    def listNueva(self, p):
        return [p.Expresion]

    #OBJECTID
    @_("OBJECTID")
    def Expresion(self, p):
        return Objeto(nombre=p.OBJECTID)

    # INT_CONST
    @_("INT_CONST")
    def Expresion(self, p):
        return Entero(valor = p.INT_CONST)

    #STR_CONST
    @_("STR_CONST")
    def Expresion(self, p):
        return String(valor= p.STR_CONST)

    #BOOL_CONST
    @_("BOOL_CONST")
    def Expresion(self, p):
        return Booleano(valor = p.BOOL_CONST)
    
    