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

class CoolParser(Parser):
    nombre_fichero = ''
    tokens = CoolLexer.tokens
    debugfile = "salida.out"
    errores = []

    

    @_("Programa Clase")
    def Programa(self, p):
        return Programa(secuencia=[p.Programa.secuencia + [p.Clase])

    @_("Clase")
    def Programa(self, p):
        return Programa(secuencia=[p.Clase])

    @_("CLASS TYPEID optInherit '{' lista_atr_met '}' ';'")
    def Clase():
        pass
    
    @_("")
    def optInherit(self, p):
        pass

    @_("INHERITS TYPEID")
    def optInherit(self, p):
        pass

    @_("")
    def lista_atr_met(self, p):
        pass

    @_("Atributo")
    def lista_atr_met(self, p):
        pass

    @_("Metodo")
    def lista_atr_met(self, p):
        pass

    @_("Atributo lista_atr_met")
    def lista_atr_met(self, p):
        pass

    @_("Metodo lista_atr_met")
    def lista_atr_met(self, p):
        pass

    @_("OBJECTID ':' TYPEID optAssign ';'")
    def Atributo(self, p):
        pass

    @_("")
    def optAssign(self, p):
        pass

    @_("ASSIGN Expresion")
    def optAssign(self, p):
        pass

    @_("OBJECTID '(' ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        pass

    @_("OBJECTID '(' listaFormales ')' ':' TYPEID '{' Expresion '}' ';'")
    def Metodo(self, p):
        pass

    @_("Formal")
    def listaFormales(self, p):
        pass

    @_("Formal ',' listaFormales")
    def listaFormales(self, p):
        pass

    @_("OBJECTID : TYPEID")
    def Formal(self, p):
        # #return Formal(p.OBJECTID, p.TYPEID)
        pass

    @_("OBJECTID : ASSIGN Expresion")
    def Expresion(self, p):
        pass

    # @_("TYPEID")
    # def typeID(self, p):
    #     # #return TypeID(p.TYPEID)
    #     pass

    
    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        #return BinOp('+', p.Expresion0, p.Expresion1)
        pass

    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        #return BinOp('-', p.Expresion0, p.Expresion1)
        pass

    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        #return BinOp('*', p.Expresion0, p.Expresion1)
        pass

    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        #return BinOp('/', p.Expresion0, p.Expresion1)
        pass

    @_("Expresion '<' Expresion")
    def Expresion(self, p):
        #return BinOp('<', p.Expresion0, p.Expresion1)
        pass

    @_("Expresion '<=' Expresion")
    def Expresion(self, p):
        #return BinOp('<=', p.Expresion0, p.Expresion1)
        pass

    @_("Expresion '=' Expresion")
    def Expresion(self, p):
        #return BinOp('=', p.Expresion0, p.Expresion1)
        pass

    @_("'(' Expresion ')'")
    def Expresion(self, p):
        #return p.Expresion
        pass

    @_("NOT Expresion")
    def Expresion(self, p):
        #return UnOp('not', p.Expresion)
        pass

    @_("ISVOID Expresion")
    def Expresion(self, p):
        #return UnOp('isvoid', p.Expresion)
        pass

    @_("'~' Expresion")
    def Expresion(self, p):
        #return UnOp('~', p.Expresion)
        pass

    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def Expresion(self, p):
        pass

    @_("Expresion '@' TYPEID '.' OBJECTID '(' listaExpresiones ')'")
    def Expresion(self, p):
        pass

    @_("Expresion")
    def listaExpresiones(self, p):
        pass

    @_("Expresion ',' listaExpresiones")
    def listaExpresiones(self, p):
        pass

    @_("optExpresion OBJECTID '(' listaExpresiones ')'")
    def Expresion(self, p):
        pass

    @_("optExpresion OBJECTID '(' ')'")
    def Expresion(self, p):
        pass

    @_("")
    def optExpresion(self, p):
        pass

    @_("Expresion '.'")
    def optExpresion(self, p):
        pass

    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        pass

    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        pass

    @_("LET OBJECTID ':' TYPEID optArrow starFormal IN Expresion")
    def Expresion(self, p):
        pass

    @_("")
    def optArrow(self, p):
        pass
    
    @_("'<-' Expresion")
    def optArrow(self, p):
        pass

    @_("")
    def starFormal(self, p):
        pass

    @_("',' OBJECTID ':' TYPEID optArrow starFormal")
    def starFormal(self, p):
        pass

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
        pass

    @_("Expresion ';'")
    def expresiones(self, p):
        pass

    @_("Expresion ';' expresiones")
    def expresiones(self, p):
        pass
    
    @_("OBJECTID")
    def Expresion(self, p):
        #return ObjectID(p.OBJECTID)
        pass

    @_("INT_CONST")
    def Expresion(self, p):
        #return IntConst(p.INT_CONST)
        pass

    @_("STR_CONST")
    def Expresion(self, p):
        # #return StrConst(p.STR_CONST)
        pass

    @_("BOOL_CONST")
    def Expresion(self, p):
        #return BoolConst(p.BOOL_CONST)
        pass

    