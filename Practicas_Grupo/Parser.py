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
        ('nonassoc', "<", "LE",'='),
        ('left', "+", "-"),
        ('left', "*", "/"),
        ('left', "ISVOID"),
        ('left', '~'),
        ('left', '@'),
        ('left', '.'),
        
    )
    
    @_("Clase ';'")
    def Programa(self, p):
        return Programa(secuencia = [p.Clase])
    
    @_("Programa Clase ';'")
    def Programa(self, p):
        return Programa(secuencia = p.Programa.secuencia + [p.Clase])

    @_("Programa error")
    def Programa(self, p):
        return Programa(secuencia = [p.Programa])

    @_("CLASS TYPEID '{' '}'")
    def Clase(self, p):
        return Clase(nombre=p[1], padre="Object",nombre_fichero=self.nombre_fichero, caracteristicas=[])

    @_("CLASS TYPEID '{' cuerpo_clase '}'")
    def Clase(self, p):
        return Clase(nombre=p[1], padre="Object",nombre_fichero=self.nombre_fichero, caracteristicas=p.cuerpo_clase)

    @_("CLASS TYPEID INHERITS TYPEID '{' '}'")
    def Clase(self, p):
        return Clase(nombre=p[1], padre=p[3],nombre_fichero=self.nombre_fichero, caracteristicas=[])

    @_("CLASS TYPEID INHERITS TYPEID '{' cuerpo_clase '}'")
    def Clase(self, p):
        return Clase(nombre=p[1], padre=p[3],nombre_fichero=self.nombre_fichero, caracteristicas=p.cuerpo_clase)

    @_("")
    def cuerpo_clase(self, p):
        return []

    @_("cuerpo_clase caracteristica ';'")
    def cuerpo_clase(self, p):
        return p.cuerpo_clase + [p.caracteristica]
    
    @_("cuerpo_clase error ';'")
    def cuerpo_clase(self, p):
        return []

    @_("Atributo")
    def caracteristica(self, p):
        return p.Atributo

    @_("Metodo")
    def caracteristica(self, p):
        return p.Metodo

    @_("OBJECTID ':' TYPEID")
    def Atributo(self, p):
        return Atributo(nombre=p[0], tipo=p[2], cuerpo=NoExpr())
    
    @_("OBJECTID ':' error")
    def Atributo(self, p):
        return NoExpr()

    @_("OBJECTID ':' TYPEID ASSIGN expr")
    def Atributo(self, p):
        return Atributo(nombre=p[0], tipo=p[2],cuerpo=p.expr)

    @_("OBJECTID '(' ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return Metodo(formales=[],nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expr)
    
    @_("OBJECTID '(' ')' ':' error")
    def Metodo(self, p):
        return p.error

    @_("OBJECTID '(' ')' ':' TYPEID '{' error '}'")
    def Metodo(self, p):
        return p.error

    @_("OBJECTID '(' formales ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID, tipo=p.TYPEID, formales=p.formales, cuerpo=p.expr)
    
    @_("OBJECTID '(' formales ')' ':' TYPEID '{' error '}'")
    def Metodo(self, p):
        return NoExpr()
    
    @_("OBJECTID '(' error ')' ':' TYPEID '{' expr '}'")
    def Metodo(self, p):
        return NoExpr()

    @_("formal")
    def formales(self, p):
        return [p.formal]
    
    @_("formal ',' formales")
    def formales(self, p):
        return [p.formal] + p.formales

    @_("OBJECTID ':' TYPEID")
    def formal(self, p):
        return Formal(nombre_variable=p.OBJECTID,tipo= p.TYPEID)

    @_("ISVOID expr")
    def expr(self, p):
        return EsNulo(expr=p.expr)
    
    @_("expr '*' expr")
    def expr(self, p):
        return Multiplicacion(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '/' expr")
    def expr(self, p):
        return Division(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '+' expr")
    def expr(self, p):
        return Suma(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr '-' expr")
    def expr(self, p):
        return Resta(izquierda=p.expr0, derecha=p.expr1)
    
    @_("expr LE expr")
    def expr(self, p):
        return LeIgual(izquierda=p.expr0, derecha=p.expr1)

    @_("expr '<' expr")
    def expr(self, p):
        return Menor(izquierda=p.expr0, derecha=p.expr1)

    @_("expr '=' expr")
    def expr(self, p):
        return Igual(izquierda=p.expr0, derecha=p.expr1)
    
    @_("NOT expr")
    def expr(self, p):
        return Not(expr=p.expr)
    
    @_("OBJECTID ASSIGN expr")
    def expr(self, p):
        return Asignacion(nombre=p.OBJECTID, cuerpo=p.expr)

    @_("'~' expr")
    def expr(self, p):
        return Neg(expr=p.expr)

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("expr '@' TYPEID '.' OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodoEstatico(cuerpo=p.expr,clase=p.TYPEID,nombre_metodo=p.OBJECTID,argumentos=[])

    @_("expr '@' TYPEID '.' OBJECTID '(' argumentos ')'")
    def expr(self, p):
        return LlamadaMetodoEstatico(cuerpo=p.expr,clase=p.TYPEID, nombre_metodo=p.OBJECTID, argumentos=p.argumentos)
    
    @_("expr")
    def argumentos(self, p):
        return [p.expr]

    @_("expr ',' argumentos")
    def argumentos(self, p):
        return [p.expr] + p.argumentos

    
    @_("OBJECTID '(' lista_argumentos ')'")
    def expr(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre="self"),nombre_metodo=p.OBJECTID, argumentos=p.lista_argumentos)

    @_("OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre="self"),nombre_metodo=p.OBJECTID, argumentos=[])
    
    @_("expr '.' OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodo(cuerpo=p.expr,nombre_metodo=p.OBJECTID, argumentos=[])
    
    @_("expr '.' OBJECTID '(' lista_argumentos ')'")
    def expr(self, p):
        return LlamadaMetodo(cuerpo=p.expr,nombre_metodo=p.OBJECTID, argumentos=p.lista_argumentos)
    
    @_("expr")
    def lista_argumentos(self, p):
        return [p.expr]

    @_("expr ',' lista_argumentos")
    def lista_argumentos(self, p):
        return [p.expr] + p.lista_argumentos

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        return Condicional(condicion=p.expr0,verdadero=p.expr1, falso=p.expr2)
    
    @_("IF expr THEN expr error FI")
    def expr(self, p):
        return NoExpr()

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        return Bucle(condicion=p.expr0, cuerpo=p.expr1)

    @_("LET OBJECTID ':' TYPEID opcionales lista_inicia IN expr")
    def expr(self, p):
        if p.lista_inicia != []:
            ultima_inicia = p.lista_inicia[-1]
            # Vamos a suponer que ultima_inicia = [nombre, tipo, inicializacion]
            temp = Let(nombre = ultima_inicia[0],
                        tipo = ultima_inicia[1], 
                        inicializacion=ultima_inicia[2], 
                        cuerpo = p.expr)
            
            for ultima_inicia in reversed(p.lista_inicia[:-1]):
                temp = Let(nombre=ultima_inicia[0],tipo = ultima_inicia[1], 
                        inicializacion=ultima_inicia[2], 
                        cuerpo = temp)
            return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=p.opcionales, cuerpo=temp)
        else:
            return Let(nombre=p.OBJECTID, tipo=p.TYPEID, inicializacion=p.opcionales, cuerpo=p.expr)
    
    @_("LET OBJECTID ':' TYPEID opcionales lista_inicia IN error")
    def expr(self, p):
        return NoExpr()

    @_("")
    def lista_inicia(self, p):
        return []
    
    @_("lista_inicia ',' OBJECTID ':' TYPEID opcionales")
    def lista_inicia(self, p):
        return p.lista_inicia + [(p.OBJECTID, p.TYPEID ,p.opcionales)]
    
    @_("ASSIGN expr")
    def opcionales(self, p):
        return p.expr
    
    @_("ASSIGN error")
    def opcionales(self, p):
        return NoExpr()
    
    @_("")
    def opcionales(self, p):
        return NoExpr()


    @_("CASE expr OF ESAC")
    def expr(self, p):
        return Swicht(expr=p.expr, casos=[])

    @_("CASE expr OF cuerpo_case ESAC")
    def expr(self, p):
        return Swicht(expr=p.expr, casos=p.cuerpo_case)

    @_("OBJECTID ':' TYPEID DARROW expr ';'")
    def cuerpo_case(self, p):
        return [RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expr)]
    
    @_("cuerpo_case OBJECTID ':' TYPEID DARROW expr ';'")
    def cuerpo_case(self, p):
        return p.cuerpo_case + [RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.expr)]
    
    @_("cuerpo_case OBJECTID ':' TYPEID DARROW error ';'")
    def cuerpo_case(self, p):
        return NoExpr()

    @_("NEW TYPEID")
    def expr(self, p):
        return Nueva(tipo=p.TYPEID)

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
        return Bloque(expresiones=p.bloque)
    
    # @_("'{' error '}'")
    # def expr(self, p):
    #     return NoExpr()
    
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
            self.errores.append(f"\"{self.nombre_fichero}\", line 0: syntax error at or near EOF")
        else:
            #print(p)
            if p.value in CoolLexer.literals:
                self.errores.append(f"\"{self.nombre_fichero}\", line {p.lineno}: syntax error at or near '{p.value}'")
            elif p.type == p.value.upper():
                self.errores.append(f"\"{self.nombre_fichero}\", line {p.lineno}: syntax error at or near {p.type}")
            elif p.type == "LE":
                self.errores.append(f"\"{self.nombre_fichero}\", line {p.lineno}: syntax error at or near {p.type}")
            else:
                self.errores.append(f"\"{self.nombre_fichero}\", line {p.lineno}: syntax error at or near {p.type} = {p.value}")
        

    