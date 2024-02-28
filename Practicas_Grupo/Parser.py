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
        pass

    @_("Programa Clase")
    def Programa(self, p):
        pass

    @_("CLASS TYPEID opcional '{' lista_atr_metodos'}'")
    def Clase(self, p):
        pass

    @_("")
    def opcional(self, p):
        pass

    @_("inherits TYPEID")
    def opcional(self, p):
        pass

    @_("OBJECT ';' TYPEID opcional_expr")
    def Atributo(self, p):
        pass

    @_("")
    def lista_atr_metodos(self, p):
        pass

    @_("Atributo lista_atr_metodos")
    def lista_atr_metodos(self, p):
        pass

    @_("Metodo lista_atr_metodos")
    def lista_atr_metodos(self, p):
        pass

    @_("OBJECTID '('')' ':' TYPEID '{'Expresion'}'")
    def Metodo(self, p):
        pass

    @_("OBJECTID '(' Formal ',' Formal ')' ':' TYPEID '{' Expresion '}'' ';'")
    def Metodo(self, p):
        pass

    @_('OBJECTID ":" TYPEID')
    def Formal(self, p):
        return p.OBJECTID, p.TYPEID

    #OBJECTID ASSIGN ⟨Expresion⟩
    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        pass

    # ⟨Expresion⟩ + ⟨Expresion⟩
    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        pass

    # ⟨Expresion⟩ - ⟨Expresion⟩
    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        pass
    
    # ⟨Expresion⟩ * ⟨Expresion⟩
    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        pass
    
    # ⟨Expresion⟩ / ⟨Expresion⟩
    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        pass

    # ⟨Expresion⟩ < ⟨Expresion⟩
    @_("Expresion LE Expresion")
    def Expresion(self, p):
        pass
    
    # ⟨Expresion⟩ <= ⟨Expresion⟩
    @_("Expresion LT Expresion")
    def Expresion(self, p):
        pass

    # ⟨Expresion⟩ = ⟨Expresion⟩
    @_("Expresion EQUALS Expresion")
    def Expresion(self, p):
        pass

    #( ⟨Expresion⟩ )
    @_("'(' Expresion ')'")
    def Expresion(self, p):
        pass

    #NOT ⟨Expresion⟩
    @_("NOT Expresion")
    def Expresion(self, p):
        pass
    
    # ISVOID ⟨Expresion⟩
    @_("ISVOID Expresion")
    def Expresion(self, p):
        pass
    
    # ~ ⟨Expresion⟩
    @_("'~' Expresion")
    def Expresion(self, p):
        pass
    
    #⟨Expresion⟩ @ TYPEID . OBJECTID ( )
    @_("Expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def Expresion(self, p):
        pass
    
    #⟨Expresion⟩ @ TYPEID . OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    @_("Expresion '@' TYPEID '.' OBJECTID '(' lstExpr Expresion')'")
    def Expresion(self, p):
        pass
    
    @_("Expresion ',' lstExpr")
    def lstExpr(self, p):
        pass

    @_("")
    def lstExpr(self, p):
        pass

    #[ ⟨Expresion⟩ .] OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    @_("'[' Expresion '.'']' OBJECTID '(' lstExpr Expresion')'")
    def Expresion(self, p):
        pass

    # [ ⟨Expresion⟩ .] OBJECTID ( )
    @_("'[' Expresion '.'']' OBJECTID '(' ')'")
    def Expresion(self, p):
        pass
    
    #IF ⟨Expresion⟩ THEN ⟨Expresion⟩ ELSE ⟨Expresion⟩ FI
    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        pass
    #  WHILE ⟨Expresion⟩ LOOP ⟨Expresion⟩ POOL
    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        pass

    #LET OBJECTID : TYPEID [<- ⟨Expresion⟩] (, OBJECTID : TYPEID [<- ⟨Expresion⟩])* IN ⟨Expresion⟩
    @_("LET OBJECTID ':' TYPEID '['ASSIGN Expresion']' lstArrow IN Expresion")
    def Expresion(self, p):
        pass

    @_("',' OBJECTID ':' TYPEID '['ASSIGN Expresion']'lstArrow")
    def lstArrow(self, p):
        pass
    
    @_("")
    def lstArrow(self, p):
        pass

    #CASE ⟨Expresion⟩ OF (OBJECTID : TYPEID DARROW <Expresion>)+ ; ESAC
    @_("CASE Expression OF CaseList ';' ESAC")
    def Expression(self, p):
        pass

    @_("OBJECTID ':' TYPEID DARROW Expresion")
    def Case(self, p):
        pass

    @_("Case CaseList")
    def CaseList(self, p):
        pass

    @_("Case")
    def CaseList(self, p):
        pass

    #  NEW TYPEID
    @_("NEW TYPEID")
    def Expresion(self, p):
        pass

    #{ (⟨Expresion⟩ ;) + }
    @_("'{'Expresion ; listNueva'}'")
    def Expresion(self, p):
        pass

    @_("Expresion ; listNueva")
    def listNueva(self, p):
        pass

    @_("")
    def listNueva(self, p):
        pass

    #OBJECTID
    @_("OBJECTID")
    def Expresion(self, p):
        pass

    # INT_CONST
    @_("INT_CONST")
    def Expresion(self, p):
        pass

    #STR_CONST
    @_("STR_CONST")
    def Expresion(self, p):
        pass

    #BOOL_CONST
    @_("BOOL_CONST")
    def Expresion(self, p):
        pass