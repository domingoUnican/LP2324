# coding: utf-8

from Lexer import CoolLexer
from sly import Parser
import sys
import os
from Clases import *

'''
<Programa> ::=<Clase>+

<Clase> ::= class TYPEID [inherits TYPEID] { (<Atributo> | <Metodo>)* }

<Atributo> ::= OBJECTID : TYPEID [ASSIGN <Expresion>]

<Metodo> ::= OBJECTID ( ) : TYPEID { <Expresion>}
            | OBJECTID (( <Formal>,  )* <Formal> ) : TYPEID { <Expresion>} 

<Formal> ::= OBJECTID : TYPEID

<Expresion> ::= OBJECTID ASSIGN <Expresion>
                | <Expresion> + <Expresion>
                | <Expresion> - <Expresion>
                | <Expresion> * <Expresion>
                | <Expresion> / <Expresion>
                | <Expresion> < <Expresion>
                | <Expresion> <= <Expresion>
                | <Expresion> = <Expresion>
                | ( <Expresion> )
                | NOT <Expresion>
                | ISVOID <Expresion>
                | ~ <Expresion>
                | <Expresion> @ TYPEID . OBJECTID ( )
                | <Expresion> @ TYPEID . OBJECTID ( (<Expresion> ,)* <Expresion> )
                | [ <Expresion> .] OBJECTID ( (<Expresion> ,)* <Expresion> )
                | [ <Expresion> .] OBJECTID ( )
                | IF <Expresion> THEN <Expresion> ELSE <Expresion> FI
                | WHILE <Expresion> LOOP <Expresion> POOL
                | LET OBJECTID : TYPEID [<- <Expresion>] (, OBJECTID : TYPEID [<- <Expresion>])* IN <Expresion>
                | CASE <Expresion> OF (OBJECTID : TYPEID DARROW <Expresion>)+ ; ESAC
                | NEW TYPEID
                | { (<Expresion> ;) + }
                | OBJECTID
                | INT_CONST
                | STR_CONST
                | BOOL_CONST                
            
                
        tokens = {OBJECTID, INT_CONST, BOOL_CONST, TYPEID,
                    ELSE, IF, FI, THEN, NOT, IN, CASE, ESAC, CLASS,
                    INHERITS, ISVOID, LET, LOOP, NEW, OF,
                    POOL, THEN, WHILE, NUMBER, STR_CONST, LE, DARROW, ASSIGN}
        
'''


'''
clases
nodo
formal
Expresion
asignacion
llamadaMetodoEstatico
llamadaMetodo
Condicional
Bucle
Let
Bloque
RamaCase
Swicht
Nueva
OperacionBinaria
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
Programa(IterableNodo)
Caracteristica
Clase(nodo)
Metodo
Atributo
Arbol
Ambito

'''
class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []
    precedence = (
        ('nonassoc', 'LE', '<', '='), # Nonassociative operators
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'NOT', 'ISVOID', '~'),
        # ('left', '@'),
        ('left', '.'),
        # ('left', 'OBJECTID')
        ('left', '@')
    
    )
    

    @_("Programa Clase")
    def Programa(self, p):
        return Programa(secuencia=p[0].secuencia + [p[1]])

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia=[p[0]])

    @_("CLASS TYPEID optInherit '{' lista_atr_met '}' ';'")
    def Clase(self, p):
        return Clase(nombre=p[1], padre = p[2], nombre_fichero=self.nombre_fichero, caracteristicas = p[4])
    
    @_("")
    def optInherit(self, p):
        return "Object"

    @_("INHERITS TYPEID")
    def optInherit(self, p):
        return p[1]

    @_("")
    def lista_atr_met(self, p):
        return []

    @_("Atributo")
    def lista_atr_met(self, p):
        return p[0]

    @_("Metodo")
    def lista_atr_met(self, p):
        return p[0]

    @_("Atributo lista_atr_met")
    def lista_atr_met(self, p):
        return [p[0]] + p[1]

    @_("Metodo lista_atr_met")
    def lista_atr_met(self, p):
        return [p[0]] + p[1]

    @_("OBJECTID ':' TYPEID optAssign ';'")
    def Atributo(self, p):
        return Atributo(nombre=p[0], tipo=p[2], cuerpo=p[3])

    @_("")
    def optAssign(self, p):
        return NoExpr()

    @_("ASSIGN Expresion")
    def optAssign(self, p):
        return p[1]

    @_("OBJECTID '(' ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        return Metodo(nombre=p[0], tipo=p[4], cuerpo=p[6])

    @_("OBJECTID '(' listaFormales ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        return Metodo(nombre=p[0], tipo=p[5], cuerpo=p[7], formales=p[2])

    @_("Formal")
    def listaFormales(self, p):
        return [p[0]]

    @_("Formal ',' listaFormales")
    def listaFormales(self, p):
        return [p[0]] + p[2]

    @_("OBJECTID ':' TYPEID")
    def Formal(self, p):
        # #return Formal(p.OBJECTID, p.TYPEID)
        return Formal(nombre_variable=p[0], tipo=p[2])

    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        return Asignacion(nombre=p[0], cuerpo=p[2])

    # @_("TYPEID")
    # def typeID(self, p):
    #     # #return TypeID(p.TYPEID)
    #     pass

    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        return Multiplicacion(izquierda=p[0], derecha=p[2])

    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        return Division(izquierda=p[0], derecha=p[2])

    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return Suma(izquierda=p[0], derecha=p[2])
        
    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        return Resta(izquierda=p[0], derecha=p[2])
        
    @_("Expresion LE Expresion")
    def Expresion(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])
    
    @_("Expresion '<' Expresion")
    def Expresion(self, p):
        return Menor(izquierda=p[0], derecha=p[2])

    @_("Expresion '=' Expresion")
    def Expresion(self, p):
        return Igual(izquierda=p[0], derecha=p[2])

    @_("'(' Expresion ')'")
    def Expresion(self, p):
        return p[1]
        

    @_("NOT Expresion")
    def Expresion(self, p):
        return Not(expr=p[1])

    @_("ISVOID Expresion")
    def Expresion(self, p):
        return EsNulo(expr=p[1])

    @_("'~' Expresion")
    def Expresion(self, p):
        return Neg(expr=p[1])

    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=p[4], argumentos=[])

    @_("Expresion '@' TYPEID '.' OBJECTID '(' listaExpresiones ')'")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0], clase=p[2], nombre_metodo=[4], argumentos=p[6])

    @_("Expresion")
    def listaExpresiones(self, p):
        return [p[0]]

    @_("Expresion ',' listaExpresiones")
    def listaExpresiones(self, p):
        return [p[0]] + p[2]

    # @_("optExpresion OBJECTID '(' listaExpresiones ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=p[0], nombre_metodo=p[1], argumentos=p[3])

    # @_("optExpresion OBJECTID '(' ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=p[0], nombre_metodo=p[1], argumentos=[])

    # @_("")
    # def optExpresion(self, p):
    #     return NoExpr()

    # @_("Expresion '.'")
    # def optExpresion(self, p):
    #     return p[0]

    # @_("optExpresion '(' listaExpresiones ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=p[0][0], nombre_metodo=p[0][1], argumentos=p[3])
    
    # @_("OBJECTID '(' listaExpresiones ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=Objeto(nombre = "self"), nombre_metodo=p[0], argumentos=p[2])

    # @_("Expresion '.' OBJECTID '(' ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=p[0], nombre_metodo=p[2], argumentos=p[4])

    # @_("OBJECTID '(' ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=Objeto(nombre = "self"), nombre_metodo=p[0], argumentos=[])

    # @_("Expresion '.' OBJECTID '(' ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=p[0], nombre_metodo=p[2], argumentos=[])

    
    @_("optExpresion '(' listaExpresiones ')'")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=p[0][0], nombre_metodo=p[0][1], argumentos=p[2])

    @_("optExpresion '(' ')'")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=p[0][0], nombre_metodo=p[0][1], argumentos=[])



    # @_("optExpresion '(' ')'")
    # def Expresion(self, p):
    #     return LlamadaMetodo(cuerpo=p[0][0], nombre_metodo=p[0][1], argumentos=[])

    @_("OBJECTID")
    def optExpresion(self, p):
        return [Objeto(nombre='self'), p[0]]
    
    @_("Expresion '.' OBJECTID")
    def optExpresion(self, p):
        return [p[0], p[2]]

    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        return Condicional(condicion = p[1], verdadero = p[3], falso=p[5])

    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])
    
    ####################################### TODO LET FOTO 6 DE MARZO

    @_("LET OBJECTID ':' TYPEID optArrow starFormal IN Expresion")
    def Expresion(self, p):
        #return Let(nombre=p[1], tipo=p[3], inicializacion=p[4], cuerpo=p[7])

        listaFormales = [[p[1], p[3], p[4]]] + p[5]
        body = p[7]

        while listaFormales:
            valores = listaFormales.pop()
            body = Let(nombre=valores[0], tipo=valores[1], inicializacion=valores[2], cuerpo=body)

        return body

    @_("")
    def optArrow(self, p):
        return NoExpr()
    
    @_("ASSIGN Expresion")
    def optArrow(self, p):
        # return Asignacion(nombre=None, cuerpo=p[2])
        # return Expresion(p[1])
        return p[1]

    @_("")
    def starFormal(self, p):
        return []
    
    @_("',' OBJECTID ':' TYPEID optArrow starFormal")
    def starFormal(self, p):
        # return Formal(nombre=p[1], tipo=p[3], inicializacion=p[4]) + p[5]
        return [[p[1], p[3], p[4]]] + p[5]

    ################################################### FIN LET

    @_("CASE Expresion OF plusExpresion ESAC")
    def Expresion(self, p):
        return Swicht(expr=p[1], casos=p[3])

    @_("OBJECTID ':' TYPEID DARROW Expresion ';'")
    def plusExpresion(self, p):
        return [RamaCase(nombre_variable=p[0], tipo=p[2], cuerpo=p[4])]

    @_("OBJECTID ':' TYPEID DARROW Expresion ';' plusExpresion")
    def plusExpresion(self, p):
        return [RamaCase(nombre_variable=p[0], tipo=p[2], cuerpo=p[4])] + p[6]

    @_("NEW TYPEID")
    def Expresion(self, p):
        return Nueva(tipo=p[1])
    
    @_("'{' bloque '}'")
    def Expresion(self, p):
        return Bloque(expresiones=p[1])

    @_("Expresion ';'")
    def bloque(self, p):
        return [p[0]]

    def error(self, p):
        self.errores.append(f"Error de sintaxis en la linea {p.lineno} y token {p} y columna {p.index} en el fichero {self.nombre_fichero}")	

    @_("error ';' Expresion ';'")
    def bloque(self, p):
        return [p[2]]

    @_("error ';'")
    def bloque(self, p):
        return []

    @_("Expresion ';' bloque")
    def bloque(self, p):
        return [p[0]] + p[2]
    
    @_("OBJECTID")
    def Expresion(self, p):
        return Objeto(nombre=p[0])

    @_("INT_CONST")
    def Expresion(self, p):
        #return IntConst(p.INT_CONST)
        return Entero(valor=p[0]) 

    @_("STR_CONST")
    def Expresion(self, p):
        # #return StrConst(p.STR_CONST)
        return String(valor=p[0]) 
        

    @_("BOOL_CONST")
    def Expresion(self, p):
        return Booleano(valor=p[0])

    