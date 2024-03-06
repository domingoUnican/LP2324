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
        return Programa(secuencia = [p.Clase])

    @_("Programa Clase")
    def Programa(self, p):
        return Programa(secuencia = p.Programa.secuencia + [p.Clase])

    @_("CLASS TYPEID opcional { lista_atr_metodos }")
    def Clase(self, p):
        return Clase(nombre= p.TYPEID, padre="Object", caracteristicas=p.lista_atr_metodos)
    
    @_("")
    def lista_atr_metodos(self, p):
        return []

    @_("Atributo lista_atr_metodos")
    def lista_atr_metodos(self, p):
        return p[0] + [p[1]]

    @_("Metodo lista_atr_metodos")
    def lista_atr_metodos(self, p):
        return p[1]

    @_("")
    def opcional(self, p):
        return "Object"

    @_("INHERITS TYPEID")
    def opcional(self, p):
        return p[1]

    @_("OBJECTID ';' TYPEID opcional_expr")
    def Atributo(self, p):
        return Atributo(nombre = p.OBJECT, tipo= p.TYPEID, cuerpo=p.opcional_expr)

    @_("Expresion")
    def opcional_expr(self, p):
        return p.Expresion

    @_("")
    def opcional_expr(self, p):
        return NoExpr()

    @_("OBJECTID '(' ')' ':' TYPEID '{' Expresion  }")
    def Metodo(self, p):
        return Metodo(p.OBJECTID, [], p.TYPEID, p.Expresion)

    @_("OBJECTID '(' Formal ',' Formal ')' ':' TYPEID '{' Expresion  } ';'")
    def Metodo(self, p):
        formales = [p.Formal0, p.Formal1]
        return Metodo(p.OBJECTID, formales, p.TYPEID, p.Expresion)

    @_("OBJECTID : TYPEID")
    def Formal(self, p):
        return Formal(p.OBJECTID, p.TYPEID)

    #OBJECTID ASSIGN ⟨Expresion⟩
    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        return p[2]

    #IGNORE    
    @_("IGNORE")
    def Expresion(self, p):
        pass
    
    #[
    """@_("[")
    def Barra(self, p):
        return p[0]"""

    # ⟨Expresion⟩ + ⟨Expresion⟩
    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return p[0] + p[2]

    @_("NUMBER")
    def Expresion(self, p):
        return p.NUMBER

    # ⟨Expresion⟩ - ⟨Expresion⟩
    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        return p[0] - p[2]
    
    # ⟨Expresion⟩ * ⟨Expresion⟩
    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        return p[0] * p[2]
    
    # ⟨Expresion⟩ / ⟨Expresion⟩
    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        return p[0] / p[2]

    # ⟨Expresion⟩ < ⟨Expresion⟩
    @_("Expresion LE Expresion")
    def Expresion(self, p):
        return p[0] < p[2]
    
    # ⟨Expresion⟩ <= ⟨Expresion⟩
    @_("Expresion LT Expresion")
    def Expresion(self, p):
        return p[0] <= p[2]

    # ⟨Expresion⟩ = ⟨Expresion⟩
    @_("Expresion EQUALS Expresion")
    def Expresion(self, p):
        return p[0] == p[2]

    #( ⟨Expresion⟩ )
    @_("'(' Expresion ')'")
    def Expresion(self, p):
        return p[1]

    #NOT ⟨Expresion⟩
    @_("NOT Expresion")
    def Expresion(self, p):
       return not p[1]
    
    # ISVOID ⟨Expresion⟩
    @_("ISVOID Expresion")
    def Expresion(self, p):
        return p[1] == None
    
    # ~ ⟨Expresion⟩
    @_("'~' Expresion")
    def Expresion(self, p):
        return not p.Expresion
    
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
        return p[0] + [p[2]]
    
    @_("")
    def lstExpr(self, p):
        return []

    #[ ⟨Expresion⟩ .] OBJECTID ( (⟨Expresion⟩ ,)* ⟨Expresion⟩ )
    @_("exprOpcional OBJECTID '(' lstExpr Expresion ')'")
    def Expresion(self, p):
        pass

    # [ ⟨Expresion⟩ .] OBJECTID ( )
    @_("exprOpcional OBJECTID '(' ')'")
    def Expresion(self, p):
        #return Expresion(p.OBJECTID, None, [])
        return p.Expresion
    
    #IF ⟨Expresion⟩ THEN ⟨Expresion⟩ ELSE ⟨Expresion⟩ FI
    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        if p[1] == True:
            return p[3]
        else:
            return p[5]
    #  WHILE ⟨Expresion⟩ LOOP ⟨Expresion⟩ POOL
    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        while p[1]==True:
            return [3]

    #LET OBJECTID : TYPEID [<- ⟨Expresion⟩] (, OBJECTID : TYPEID [<- ⟨Expresion⟩])* IN ⟨Expresion⟩
    @_("LET OBJECTID ':' TYPEID exprOpcional lstArrow IN Expresion")
    def Expresion(self, p):
        ultima_inicia = p.lista_inicia[-1]
        temp  = Let(nombre = ultima_inicia[0],
                tipo=ultima_inicia[1],
                inicializacion=ultima_inicia[2],
                cuerpo = p.Expresion
                )
        for i in range(len(p.lista_inicia, 0, -1)):
            ultima_inicia = p.lista_inicia[i]
            temp  = Let(nombre = ultima_inicia[0],
                tipo=ultima_inicia[1],
                inicializacion=ultima_inicia[2],
                cuerpo = p.Expresion
                )
        return temp
            

    @_("',' OBJECTID ':' TYPEID exprOpcional lstArrow")
    def lstArrow(self, p):
        return p.Expression + [p.lstArrow]

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
    @_("CASE Expresion OF CaseList ';' ESAC")
    def Expresion(self, p):
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
    @_("{ Expresion ; listNueva } ")
    def Expresion(self, p):
        pass

    @_("Expresion ; listNueva")
    def listNueva(self, p):
        pass

    @_("")
    def listNueva(self, p):
        return []

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