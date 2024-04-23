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
    
    precedence = (
        ('left', ASSIGN, NOT),
        ('nonassoc', '='),
       ('left', '+', '-'),
       ('left', LE, '<', '~'),
       ('left', '*', '/'),
        ('left', ISVOID),
        ('left', '@'),
        ('left', '.')
    )

    ###Clase y programa###
    
    @_("clase ';' ")
    def Programa(self, p):
        return Programa(secuencia = [p[0]])
    
    
    @_("Programa clase ';' ")
    def Programa(self, p):
        return Programa(secuencia = p.Programa.secuencia + [p[1]])
    
    @_("CLASS TYPEID inherits '{' caracteristicas '}'")
    def clase(self, p):
        return Clase(nombre=p.TYPEID, padre=p[2], caracteristicas=p[4], nombre_fichero=self.nombre_fichero)
    
    ####Inherits####
    @_("")
    def inherits(self, p):
        return "Object"
    
    @_("INHERITS TYPEID")
    def inherits(self, p):
        return p.TYPEID
    
    ####Caracteristicas####
    @_("")
    def caracteristicas(self, p):
        return []
    
    @_("Atributo ';' caracteristicas")
    def caracteristicas(self, p):
        return [p.Atributo] + p[2]
    
    @_("metodo ';' caracteristicas")
    def caracteristicas(self, p):
        return [p[0]] + p[2]
    
    ####Atributos####
    @_("OBJECTID ':' TYPEID opt_expr ")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID,tipo=p.TYPEID,cuerpo=p.opt_expr)
    
    @_("")
    def opt_expr(self, p):
        return NoExpr()

    @_("ASSIGN expresion")
    def opt_expr(self, p):
        return p.expresion
    
    ####Metodos####
    @_("OBJECTID '(' ')' ':' TYPEID '{' expresion '}'")
    def metodo(self, p):
        return Metodo(nombre = p.OBJECTID, tipo = p.TYPEID,cuerpo=p.expresion, formales = [])

    @_("OBJECTID '(' Formal formal_list ')' ':' TYPEID '{' expresion '}'")
    def metodo(self, p):
        return Metodo(nombre = p.OBJECTID,tipo = p.TYPEID,cuerpo=p.expresion,formales=[p.Formal] + p.formal_list)
    

    ###Formales###
    @_("")
    def formal_list(self, p):
        return []
    
    @_("OBJECTID ':' TYPEID")
    def Formal(self, p):
        return Formal(nombre_variable=p.OBJECTID, tipo=p.TYPEID)
    
    @_("',' Formal formal_list")
    def formal_list(self, p):
        return [p.Formal] + p.formal_list


    ###Simbolos###
    @_("OBJECTID ASSIGN expresion")
    def expresion(self, p):
        return Asignacion(nombre=p.OBJECTID, cuerpo=p.expresion)

    @_("expresion '+' expresion")
    def expresion(self, p):
        return Suma(izquierda=p[0], derecha=p[2])

    @_("expresion '-' expresion")
    def expresion(self, p):
        return Resta(izquierda=p[0], derecha=p[2])
    
    @_("expresion '*' expresion")
    def expresion(self, p):
        return Multiplicacion(izquierda=p[0], derecha=p[2])

    @_("expresion '/' expresion")
    def expresion(self, p):
        return Division(izquierda=p[0], derecha=p[2])
    
    @_("expresion '<' expresion")
    def expresion(self, p):
        return Menor(izquierda=p[0], derecha=p[2])

    @_("expresion DARROW expresion")
    def expresion(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])

    @_("expresion '=' expresion")
    def expresion(self, p):
        return Igual(izquierda=p[0], derecha=p[2])

    @_("'(' expresion ')'")
    def expresion(self, p):
        return p.expresion

    @_("NOT expresion")
    def expresion(self, p):
        return Not(expr=p.expresion)

    @_("ISVOID expresion")
    def expresion(self, p):
        return EsNulo(expr=p.expresion)

    @_("'~' expresion")
    def expresion(self, p):
        return Neg(expr=p.expresion)

    @_("expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0],clase=p.TYPEID,nombre_metodo=p.OBJECTID,argumentos=[])

    @_("expresion '@' TYPEID '.' OBJECTID '(' expresion expr_list ')'")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p[0],clase=p.TYPEID,nombre_metodo=p.OBJECTID,argumentos=[p[6]] + p.expr_list)

    @_("")
    def expr_list(self, p):
        return []

    @_("',' expresion expr_list")
    def expr_list(self, p):
        return [p.expresion] + p.expr_list

    @_("expresion '.' OBJECTID '(' expresion expr_list ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo=p[0],nombre_metodo=p.OBJECTID,argumentos=[p[4]] + p.expr_list)

    @_("expresion '.' OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo=p.expresion,nombre_metodo=p.OBJECTID,argumentos=[])
    
    @_("OBJECTID '(' expresion expr_list ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre="self"),nombre_metodo=p.OBJECTID,argumentos=[p[2]] + p.expr_list)

    @_("OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre="self"),nombre_metodo=p.OBJECTID,argumentos=[])

    @_("IF expresion THEN expresion ELSE expresion FI")
    def expresion(self, p):
        return Condicional(condicion=p[1],verdadero=p[3],falso=p[5])

    @_("WHILE expresion LOOP expresion POOL")
    def expresion(self, p):
        return Bucle(condicion=p[1],cuerpo=p[3])


    ####Let####
    @_("LET list_let IN expresion")
    def expresion(self, p):
        ultima_inicializacion = p.list_let[-1]
        temp = Let(nombre=ultima_inicializacion[0],
                tipo=ultima_inicializacion[1],
                inicializacion=ultima_inicializacion[2],
                cuerpo=p.expresion)
        for i in range(len(p.list_let)-2,-1,-1):
            ultima_inicializacion = p.list_let[i] 
            temp = Let(nombre=ultima_inicializacion[0],
                tipo=ultima_inicializacion[1],
                inicializacion=ultima_inicializacion[2],
                cuerpo=temp)
        return temp
    
    @_("")
    def list_let(self, p):
        return []

    @_("',' OBJECTID ':' TYPEID ASSIGN expresion list_let")
    def list_let(self, p):
        return [(p.OBJECTID,p.TYPEID,p.expresion)] + p.list_let

    @_("OBJECTID ':' TYPEID ASSIGN expresion list_let")
    def list_let(self, p):
        return [(p.OBJECTID,p.TYPEID,p.expresion)] + p.list_let

    @_("',' OBJECTID ':' TYPEID list_let")
    def list_let(self, p):
        return [(p.OBJECTID,p.TYPEID,NoExpr())] + p.list_let

    @_("OBJECTID ':' TYPEID list_let")
    def list_let(self, p):
        return [(p.OBJECTID,p.TYPEID,NoExpr())] + p.list_let
    
    ####Case####

    @_("CASE expresion OF list_case ESAC")
    def expresion(self, p):
        return Swicht(expr=p.expresion, casos=p.list_case) 

    @_("OBJECTID ':' TYPEID DARROW expresion ';'")
    def list_case(self, p):
        return [RamaCase(nombre_variable=p.OBJECTID, cast=p.TYPEID, cuerpo=p.expresion, tipo=p.TYPEID)]

    @_("OBJECTID ':' TYPEID DARROW expresion ';' list_case")
    def list_case(self, p):
        return [RamaCase(nombre_variable=p.OBJECTID, cast=p.TYPEID, cuerpo=p.expresion, tipo=p.TYPEID)] + p.list_case


    ###ULTIMAS LINEAS###
    
    @_("NEW TYPEID")
    def expresion(self, p):
        return Nueva(tipo=p.TYPEID)

    @_("'{' expr_list_pc '}'")
    def expresion(self, p):
        return Bloque(expresiones=p.expr_list_pc)
    
    @_("expresion ';'")
    def expr_list_pc(self, p):
        return [p.expresion]
    
    @_("expr_list_pc expresion ';'")
    def expr_list_pc(self, p):
        return p.expr_list_pc + [p.expresion]

    @_("OBJECTID")
    def expresion(self, p):
        return Objeto(nombre=p.OBJECTID)

    @_("INT_CONST")
    def expresion(self, p):
        return Entero(valor=p.INT_CONST)

    @_("STR_CONST")
    def expresion(self, p):
        return String(valor=p.STR_CONST)

    @_("BOOL_CONST")
    def expresion(self, p):
        return Booleano(valor=p.BOOL_CONST)
    
