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

    

    @_("Programa Clase")
    def Programa(self, p):
        return Programa(secuencia=p[0].secuencia + [p[1]])

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia=[p[0]])

    @_("CLASS TYPEID optInherit '{' lista_atr_met '}' ';'")
    def Clase(self, p):
        return Clase(nombre=p[1], padre = p[2], caracteristica = p[4])
    
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
        return Metodo(nombre=p[0], tipo=p[3], cuerpo=p[6])

    @_("OBJECTID '(' listaFormales ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        return Metodo(nombre=p[0], tipo=p[4], cuerpo=p[7], formales=p[2])

    @_("Formal")
    def listaFormales(self, p):
        return [p[0]]

    @_("Formal ',' listaFormales")
    def listaFormales(self, p):
        return [p[0]] + p[2]

    @_("OBJECTID : TYPEID")
    def Formal(self, p):
        # #return Formal(p.OBJECTID, p.TYPEID)
        return Formal(nombre=p[0], tipo=p[2])

    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        return Asignacion(nombre=p[0], cuerpo=p[2])

    # @_("TYPEID")
    # def typeID(self, p):
    #     # #return TypeID(p.TYPEID)
    #     pass


    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return Suma(izquierda=p[0], derecha=p[2])#asi ??
        

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
        return p[1]
        

    @_("NOT Expresion")
    def Expresion(self, p):
        return Not(izquierda=p[1])

    @_("ISVOID Expresion")
    def Expresion(self, p):
        return EsNulo(str=p[1])

    @_("'~' Expresion")
    def Expresion(self, p):
        return Neg(izquierda=p[1])

    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(objeto=p[0], tipo=p[2], nombre=p[4], argumentos=[])

    @_("Expresion '@' TYPEID '.' OBJECTID '(' listaExpresiones ')'")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(objeto=p[0], tipo=p[2], nombre=p[4], argumentos=p[6])

    @_("Expresion")
    def listaExpresiones(self, p):
        return [p[0]]

    @_("Expresion ',' listaExpresiones")
    def listaExpresiones(self, p):
        return [p[0]] + p[2]

    @_("optExpresion OBJECTID '(' listaExpresiones ')'")
    def Expresion(self, p):
        return LlamadaMetodo(objeto=p[0], nombre=p[1], argumentos=p[3])

    @_("optExpresion OBJECTID '(' ')'")
    def Expresion(self, p):
        return LlamadaMetodo(objeto=p[0], nombre=p[1], argumentos=[])

    @_("")
    def optExpresion(self, p):
        return NoExpr()

    @_("Expresion '.'")
    def optExpresion(self, p):
        return p[0]

    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        return Condicional(condicion = p[1], verdadero = p[3], falso=p[5])

    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        return Bucle(condicion=p[1], cuerpo=p[3])
    
    ####################################### TODO LET FOTO 6 DE MARZO

    @_("LET OBJECTID ':' TYPEID optArrow starFormal IN Expresion")
    def Expresion(self, p):

    @_("")
    def optArrow(self, p):
        return NoExpr()
    
    @_("ASSIGN Expresion")
    def optArrow(self, p):
        return Asignacion(nombre=None, cuerpo=p[2])

    @_("")
    def starFormal(self, p):
        return NoExpr()
    
    @_("',' OBJECTID ':' TYPEID optArrow starFormal")
    def starFormal(self, p):
        # return Formal(nombre=p[1], tipo=p[3], inicializacion=p[4]) + p[5]
        pass

    ################################################### FIN LET

    @_("CASE Expresion OF plusExpresion ';' ESAC")
    def Expresion(self, p):
        pass

    @_("OBJECTID ':' TYPEID DARROW Expresion")
    def plusExpresion(self, p):
        pass

    @_("OBJECTID ':' TYPEID DARROW Expresion plusExpresion")
    def plusExpresion(self, p):
        pass

    @_("NEW TYPEID")
    def Expresion(self, p):
        pass
    
    @_("'{'expresiones'}'")
    def Expresion(self, p):
        return Bloque(secuencia=p[1])

    @_("Expresion ';'")
    def expresiones(self, p):
        return [p[0]]

    @_("Expresion ';' expresiones")
    def expresiones(self, p):
        return [p[0]] + p[2]
    
    @_("OBJECTID")
    def Expresion(self, p):
        return Objeto(nombre=p[0])

    @_("INT_CONST")
    def Expresion(self, p):
        #return IntConst(p.INT_CONST)
        return Entero(valor=p[0]) #TODO ??????

    @_("STR_CONST")
    def Expresion(self, p):
        # #return StrConst(p.STR_CONST)
        return String(valor=p[0]) #TODO ?????? 
        

    @_("BOOL_CONST")
    def Expresion(self, p):
        return Booleano(valor=p[0])#TODO ??????

    