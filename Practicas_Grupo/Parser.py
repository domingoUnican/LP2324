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
    reservados = CoolLexer._key_words
    debugfile = "salida.out"
    errores = []
    
    precedence = (
        ('right', 'DARROW'),
        ('left', 'NOT'),
        ('nonassoc', 'LE', '<', '='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'ISVOID'),
        ('left', '~'),
        ('left', '@'),
        ('left', '.'),
    )
    
    @_('clases')
    def program(self, p):
        return Programa(linea = 0, secuencia = p.clases)
    
    @_("clase ';'")
    def clases(self, p):
        return [p.clase]
        
    @_("clases clase ';'")
    def clases(self, p):
        lista_clases = p.clases
        lista_clases.append(p.clase)
        return lista_clases
    
    @_("CLASS TYPEID '{'  '}'")
    def clase(self, p):
        return Clase(linea = p.lineno, nombre = p.TYPEID, padre = 'OBJECT', nombre_fichero = self.nombre_fichero, caracteristicas = [])

    @_("CLASS TYPEID INHERITS TYPEID '{' '}'")
    def clase(self, p):
        return Clase(linea = p.lineno, nombre = p.TYPEID0, padre = p.TYPEID1, nombre_fichero = self.nombre_fichero, caracteristicas = [])
    
    @_("CLASS TYPEID '{' caracteristicas '}'")
    def clase(self, p):
        return Clase(linea = p.lineno, nombre = p.TYPEID, padre = 'OBJECT', nombre_fichero = self.nombre_fichero, caracteristicas = p.caracteristicas)
    
    @_("CLASS TYPEID '{' error '}'")
    def clase(self, p):
        return Clase(linea = p.lineno, nombre = p.TYPEID, padre = 'OBJECT', nombre_fichero = self.nombre_fichero, caracteristicas = NoExpr())
    
    @_("CLASS TYPEID INHERITS TYPEID '{' caracteristicas '}'")
    def clase(self, p):
        return Clase(linea = p.lineno, nombre = p.TYPEID0, padre = p.TYPEID1, nombre_fichero = self.nombre_fichero, caracteristicas = p.caracteristicas)
    
    @_("CLASS TYPEID INHERITS TYPEID '{' error '}'")
    def clase(self, p):
        return Clase(linea = p.lineno, nombre = p.TYPEID0, padre = p.TYPEID1, nombre_fichero = self.nombre_fichero, caracteristicas = NoExpr())
    
    @_("caracteristica ';'")
    def caracteristicas(self, p):
        return [p.caracteristica]
    
    @_("caracteristicas caracteristica ';'")
    def caracteristicas(self, p):
        lista_caracteristicas = p.caracteristicas
        lista_caracteristicas.append(p.caracteristica)
        return lista_caracteristicas
    
    @_("OBJECTID '(' ')' ':' TYPEID '{' expr '}'")
    def caracteristica(self, p):
        return Metodo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.expr, formales = [])
    
    @_("OBJECTID '(' ')' ':' TYPEID '{' error '}'")
    def caracteristica(self, p):
        return Metodo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = NoExpr(), formales = [])
    
    @_("OBJECTID '(' formales ')' ':' TYPEID '{' expr '}'")
    def caracteristica(self, p):
        return Metodo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.expr, formales = p.formales)
    
    @_("OBJECTID '(' formales ')' ':' TYPEID '{' error '}'")
    def caracteristica(self, p):
        return Metodo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = NoExpr(), formales = p.formales)
    
    @_("OBJECTID '(' error ')' ':' TYPEID '{' expr '}'")
    def caracteristica(self, p):
        return Metodo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.expr, formales = NoExpr())
    
    @_("OBJECTID ':' TYPEID")
    def caracteristica(self, p):
        return Atributo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = NoExpr())
    
    @_("OBJECTID ':' TYPEID ASSIGN expr")
    def caracteristica(self, p):
        return Atributo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.expr)
    
    @_("OBJECTID ':' TYPEID ASSIGN error")
    def caracteristica(self, p):
        return Atributo(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, cuerpo = NoExpr())
    
    @_("formal ")
    def formales(self, p):
        return [p.formal]
    
    @_("formales ',' formal")
    def formales(self, p):
        lista_formales = p.formales
        lista_formales.append(p.formal)
        return lista_formales
    
    @_('OBJECTID ":" TYPEID')
    def formal(self, p):
        return Formal(linea = p.lineno, nombre_variable = p.OBJECTID, tipo = p.TYPEID)
    
    @_('OBJECTID ASSIGN expr')
    def expr(self, p):
        return Asignacion(linea = p.lineno, nombre = p.OBJECTID, cuerpo = p.expr)
    
    @_('OBJECTID ASSIGN error')
    def expr(self, p):
        return Asignacion(linea = p.lineno, nombre = p.OBJECTID, cuerpo = NoExpr())
    
    @_("expr '.' OBJECTID '(' ')'") 
    def expr(self, p):
        return LlamadaMetodo(linea = p.lineno, cuerpo = p.expr, nombre_metodo = p.OBJECTID, argumentos = [])
    
    @_("expr '@' TYPEID '.' OBJECTID '(' ')'") 
    def expr(self, p):
        return LlamadaMetodoEstatico(linea = p.lineno, cuerpo = p.expr, clase = p.TYPEID, nombre_metodo = p.OBJECTID, argumentos = [])
    
    @_("expr '.' OBJECTID '(' parametros ')'") 
    def expr(self, p):
        return LlamadaMetodo(linea = p.lineno, cuerpo = p.expr, nombre_metodo = p.OBJECTID, argumentos = p.parametros)
    
    @_("expr '@' TYPEID '.' OBJECTID '(' parametros ')'") 
    def expr(self, p):
        return LlamadaMetodoEstatico(linea = p.lineno, cuerpo = p.expr, clase = p.TYPEID, nombre_metodo = p.OBJECTID, argumentos = p.parametros)
    
    @_("OBJECTID '(' ')'")
    def expr(self, p):
        return LlamadaMetodo(linea = p.lineno, cuerpo = Objeto(linea = p.lineno, nombre = 'self'), nombre_metodo = p.OBJECTID, argumentos = [])
    
    @_("OBJECTID '(' parametros ')'")
    def expr(self, p):
        return LlamadaMetodo(linea = p.lineno, cuerpo = Objeto(linea = p.lineno, nombre = 'self'), nombre_metodo = p.OBJECTID, argumentos = p.parametros)
    
    @_('expr')
    def parametros(self, p):
        return [p.expr]
    
    @_("parametros ',' expr")
    def parametros(self, p):
        lista_param = p.parametros
        lista_param.append(p.expr)
        return lista_param
    
    @_('IF expr THEN error FI')
    def expr(self, p):
        return Condicional(linea = p.lineno, condicion = p.expr, verdadero = NoExpr(), falso = NoExpr())
    
    @_('IF error THEN expr ELSE expr FI')
    def expr(self, p):
        return Condicional(linea = p.lineno, condicion = NoExpr(), verdadero = p.expr1, falso = p.expr2)
    
    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        return Condicional(linea = p.lineno, condicion = p.expr0, verdadero = p.expr1, falso = p.expr2)
    
    @_('WHILE expr LOOP expr POOL')
    def expr(self, p):
        return Bucle(linea = p.lineno, condicion = p.expr0, cuerpo = p.expr1)
    
    @_('WHILE error LOOP error POOL')
    def expr(self, p):
        return Bucle(linea = p.lineno, condicion = NoExpr(), cuerpo = NoExpr())
    
    @_('WHILE error LOOP expr POOL')
    def expr(self, p):
        return Bucle(linea = p.lineno, condicion = NoExpr(), cuerpo = p.expr)
    
    @_('WHILE expr LOOP error POOL')
    def expr(self, p):
        return Bucle(linea = p.lineno, condicion = p.expr, cuerpo = NoExpr())
    
    @_("expr ';'")
    def exprs(self, p):
        return [p.expr]
    
    @_("exprs expr ';'")
    def exprs(self, p):
        lista_expresiones = p.exprs
        lista_expresiones.append(p.expr)
        return lista_expresiones
    
    @_("'{' exprs '}'")
    def expr(self, p):
        return Bloque(linea = p.lineno, expresiones = p.exprs)
    
    @_("error ';'")
    def exprs(self, p):
        return []
    
    @_("LET OBJECTID ':' TYPEID IN expr")
    def expr(self, p):
        return Let(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, inicializacion = NoExpr(), cuerpo = p.expr)
    
    @_("LET OBJECTID ':' TYPEID ASSIGN expr IN expr")
    def expr(self, p):
        return Let(linea = p.lineno, nombre = p.OBJECTID, tipo = p.TYPEID, inicializacion = p.expr0, cuerpo = p.expr1)
    
    @_("LET OBJECTID ':' TYPEID tiposlet IN expr")
    def expr(self, p):
        Cuerpo = Let(nombre = tiposlet[-1][0],
            tipo = tiposlet[-1][1],
            inicializacion= tiposlet[-1][2],
            cuerpo = p.expr)
        tiposlet.pop()
        while tiposlet:
            Cuerpo = Let(nombre = tiposlet[-1][0],
            tipo = tiposlet[-1][1],
            inicializacion= tiposlet[-1][2],
            cuerpo = Cuerpo)
        cuerpo = ....__annotations__
        return Cuerpo
    
    @_("LET OBJECTID ':' TYPEID error IN expr")
    def expr(self, p):
        return NoExpr()
    
    @_("LET OBJECTID ':' TYPEID expr IN error")
    def expr(self, p):
        return NoExpr()
    
    @_("',' tipolet ")
    def tiposlet(self, p):
        return [p.inicializacion]
    
    @_("tiposlet ',' tipolet")
    def inicializaciones(self, p):
        lista_ini = p.inicializaciones
        lista_ini.append(p.inicializacion)
        return lista
    
    @_("OBJECTID ':' TYPEID ASSIGN expr")
    def tipolet(self, p):
        return [p.OBJECTID, p.TYPEID, p.expr]
    
    @_('OBJECTID ":" TYPEID ASSIGN error')
    def tipolet(self, p):
        return [p.OBJECTID, P.TYPEID, NoExpr()]
    
    @_("OBJECTID ':' TYPEID")
    def inicializacion(self, p):
        return [p.OBJECTID, p.TYPEID, NoExpr(nombre = '')]

    
    @_('CASE error OF darrowlist ESAC')
    def expr(self, p):
        return Swicht(linea = p.lineno, expr = NoExpr() , casos = p.darrowlist)
    
    @_('CASE expr OF error ESAC')
    def expr(self, p):
        return Swicht(linea = p.lineno, expr = p.expr , casos = NoExpr())
    
    @_('CASE expr OF darrowlist ESAC')
    def expr(self, p):
        return Swicht(linea = p.lineno, expr = p.expr , casos = p.darrowlist)
    
    @_("OBJECTID ':' TYPEID DARROW expr ';'")
    def darrowlist(self, p):
        return [RamaCase(linea = p.lineno, nombre_variable = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.expr)]
    
    @_("OBJECTID ':' TYPEID DARROW error ';'")
    def darrowlist(self, p):
        return [RamaCase(linea = p.lineno, nombre_variable = p.OBJECTID, tipo = p.TYPEID, cuerpo = NoExpr())]
    
    @_("darrowlist OBJECTID ':' TYPEID DARROW expr ';'")
    def darrowlist(self, p):
        lista = p.darrowlist
        lista.append(RamaCase(linea = p.lineno, nombre_variable = p.OBJECTID, tipo = p.TYPEID, cuerpo = p.expr))
        return lista
    
    @_('NEW TYPEID')
    def expr(self, p):
        return Nueva(linea = p.lineno, tipo = p.TYPEID)
    
    @_('error TYPEID')
    def expr(self, p):
        return Nueva(linea = p.lineno, tipo = p.TYPEID)
    
    @_('ISVOID expr')
    def expr(self, p):
        return EsNulo(linea = p.lineno, expr = p.expr)
    
    @_('ISVOID error')
    def expr(self, p):
        return EsNulo(linea = p.lineno, expr = NoExpr())
    
    @_("expr '+' expr")
    def expr(self, p):
        return Suma(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_("expr '-' expr")
    def expr(self, p):
        return Resta(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_("expr '*' expr")
    def expr(self, p):
        return Multiplicacion(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_("expr '/' expr")
    def expr(self, p):
        return Division(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_("'~' expr")
    def expr(self, p):
        return Neg(linea = p.lineno, expr = p.expr)
    
    @_("expr '<' expr")
    def expr(self, p):
        return Menor(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_('expr LE expr')
    def expr(self, p):
        return LeIgual(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_("expr '=' expr")
    def expr(self, p):
        return Igual(linea = p.lineno, izquierda = p.expr0, derecha = p.expr1)
    
    @_('NOT expr')
    def expr(self, p):
        return Not(linea = p.lineno, expr = p.expr)
    
    @_('NOT error')
    def expr(self, p):
        return Not(linea = p.lineno, expr = NoExpr())
    
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    @_('OBJECTID')
    def expr(self, p):
        return Objeto(linea = p.lineno, nombre = p.OBJECTID)

    @_('INT_CONST')
    def expr(self, p):
        return Entero(linea = p.lineno, valor = p.INT_CONST)

    @_('STR_CONST')
    def expr(self, p):
        return String(linea = p.lineno, valor = p.STR_CONST)
    
    @_("error INT_CONST")
    def expr(self, p):
        return Objeto(linea = p.lineno, nombre = 'basura')
    
    @_('BOOL_CONST')
    def expr(self, p):
        return Booleano(linea = p.lineno, valor = p.BOOL_CONST)
    
    def error(self, p):
        if p is None:
            resultado = f'"{self.nombre_fichero}", line 0: syntax error at or near EOF'
        elif p.value in self.reservados:
            resultado = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near {p.type}'
        elif p.value in self.literals:
            resultado = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near \'{p.type}\''
        else:
            resultado = f'"{self.nombre_fichero}", line {p.lineno}: syntax error at or near {p.type} = {p.value}'
        
        self.errores.append(resultado)
