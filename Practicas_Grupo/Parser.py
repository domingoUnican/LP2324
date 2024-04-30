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
    precedence = (('right', ASSIGN, IN), 
                 ('nonassoc', NOT, LE, '<', '=' ),
                 ('left', '+', '-'),
                 ('left', '*', '/', ISVOID),
                 ('left', '~'),
                 ('left', '@'),
                 ('left', '.')
                    )
   

    @_("Clase") #clase
    def Programa(self, p):

        return Programa(secuencia=[p.Clase])

    @_("Programa Clase") #subprograma u otra clase
    def Programa(self, p):
        
        return Programa(secuencia=p.Programa.secuencia + [p.Clase])

    @_("CLASS TYPEID opcional '{' lista_atr_metodos '}' ';'") #subprograma u otra clase
    def Clase(self, p):
        return Clase(nombre=p[1], padre = p[2], nombre_fichero= self.nombre_fichero, caracteristicas = p[4])
    
    @_("")
    def opcional(self, p):
        return 'Object'
    
    @_("INHERITS TYPEID")
    def opcional(self, p):
        return p[1]
  
    @_("")
    def lista_atr_metodos(self,p):
        return []
    

    @_("atributo  lista_atr_metodos")
    def lista_atr_metodos(self,p):
        return [p[0]] + p[1]
    

    @_("metodo  lista_atr_metodos")
    def lista_atr_metodos(self,p):
        return [p[0]] +p[1]

    @_("OBJECTID ':' TYPEID inicializacion ';'")
    def atributo (self,p):
        return Atributo(nombre= p[0], tipo = p[2], cuerpo= p[3])
    

    @_("")
    def inicializacion(self, p):
        return NoExpr()

    @_("ASSIGN expresion")
    def inicializacion(self, p):
        return p[1]

    @_("OBJECTID '(' ')' ':' TYPEID '{' expresion '}' ';'")
    def metodo (self,p):
         return Metodo(nombre= p[0], tipo= p[4], cuerpo= p[6], formales= [])
    
    @_("OBJECTID '(' formales  formal ')' ':' TYPEID '{' expresion '}' ';'")
    def metodo (self,p):
         return Metodo(nombre= p[0], tipo= p[6], cuerpo= p[8], formales= p[2] + [p[3]])
    
    @_("")
    def formales (self,p):
        return []
    
    @_("formales formal ','") 
    def formales (self,p):
        return p[0] + [p[1]]
    
    @_("OBJECTID ':' TYPEID")
    def formal(self, p):
        return Formal(nombre_variable= p[0], tipo= p[2])
    


    #hasta aqui se hizo en la tutoria
    #los nombres de los metodos en minusculas y los metodos que se retornan en mayuscula

    
    @_("OBJECTID ASSIGN expresion")
    def expresion(self, p):
        return Asignacion(nombre= p[0], cuerpo= p[2])
    

    @_("expresion '+' expresion")
    def expresion(self, p):
        return Suma(izquierda=  p[0], derecha= p[2])
    
    @_("expresion '-' expresion")
    def expresion(self, p):
        return Resta(izquierda=  p[0], derecha= p[2])
    
    @_("expresion '*' expresion")
    def expresion(self, p):
        return Multiplicacion(izquierda=  p[0], derecha= p[2])
    

    @_("expresion '/' expresion")
    def expresion(self, p):
        return Division(izquierda=  p[0], derecha= p[2])
    
    @_("expresion '<' expresion")
    def expresion(self, p):
        return Menor(izquierda=  p[0], derecha= p[2])
    
    @_("expresion LE expresion")
    def expresion(self, p):
        return LeIgual(izquierda=  p[0], derecha= p[2])
    

    @_("expresion '=' expresion")
    def expresion(self, p):
        return Igual(izquierda=  p[0], derecha= p[2])
    
    @_("'(' expresion ')'")
    def expresion(self, p):
        return p[1]
    
    
    @_("NOT expresion")
    def expresion(self, p):
        return Not(expr= p[1])
    
    @_("ISVOID expresion")
    def expresion(self, p):
        return EsNulo(expr= p[1])
    
    
    @_("'~' expresion")
    def expresion(self, p):
        return Neg(expr= p[1])
    
    @_("expresion '@' TYPEID '.' OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo= p[0], clase= p[2], nombre_metodo= p[4], argumentos= [])
    
    @_("expresion '@' TYPEID '.' OBJECTID '(' expresiones_metodos expresion ')'")
    def expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo= p[0], clase= p[2], nombre_metodo= p[4], argumentos= p[6] + [p[7]])
   
    @_("")
    def expresiones_metodos (self,p):
        return []
    
    @_("expresiones_metodos expresion  ','") 
    def expresiones_metodos (self,p):
        return p[0] + [p[1]]
    
    @_("OBJECTID '(' expresiones_metodos expresion ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= Objeto(nombre= "self" ) , nombre_metodo= p[0], argumentos= p[2] + [p[3]])
    
    @_("expresion '.' OBJECTID '(' expresiones_metodos expresion ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= p[0] , nombre_metodo= p[2], argumentos= p[4] + [p[5]])
    
    @_("expresion '.' OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= p[0], nombre_metodo= p[2], argumentos= [])
    
    @_("OBJECTID '(' ')'")
    def expresion(self, p):
        return LlamadaMetodo(cuerpo= Objeto(nombre= "self" ), nombre_metodo= p[0], argumentos= [])

    @_("IF expresion THEN expresion ELSE expresion FI") 
    def expresion(self, p):
        return Condicional (condicion= p[1], verdadero= p[3], falso= p[5])
    
    @_("WHILE expresion LOOP expresion POOL") 
    def expresion(self, p):
        return Bucle(condicion= p[1], cuerpo= p[3])
    

    ############################
    
    
    @_("LET  OBJECTID ':' TYPEID inicializacion expresiones_let IN expresion")
    def expresion(self, p):
       
        expresiones_in = p[7]
        expresiones_let_lista = [p[1], p[3], p[4]] + p[5]
        expresiones_lista = expresiones_let_lista[-3:]
           
        for elemento in expresiones_let_lista:
           
           del expresiones_let_lista[-3:]
          
           expresiones_in  = Let (nombre= expresiones_lista[0], tipo= expresiones_lista[1], 
                               inicializacion= expresiones_lista[2], cuerpo= expresiones_in)  
           
           expresiones_lista = expresiones_let_lista[-3:]
           
        return  expresiones_in


    #return Let (nombre= p[1], tipo= p[3], inicializacion= p[4], cuerpo= p[7])
    #Modificar el let este solo, devolver una lista con todos los lets y expresiones let hay que recorrerlo y generar funciones let y como el nested
    
    @_("")
    def expresiones_let(self, p):
        return []

    
    @_("',' OBJECTID ':' TYPEID inicializacion  expresiones_let ")
    def expresiones_let(self, p):
        return [p[1], p[3], p[4]] + p[5]
    

    ############################

    @_("CASE expresion OF case_lista  ESAC ") 
    def expresion(self, p):
        return Swicht(expr= p[1], casos= p[3]) 
    
    @_("OBJECTID ':' TYPEID DARROW expresion ';'") 
    def case_lista(self,p):
        return [RamaCase(nombre_variable= p[0], cast = p[2], tipo= p[2], cuerpo= p[4])]
    
    @_(" OBJECTID ':' TYPEID DARROW  expresion ';'  case_lista ") 
    def case_lista(self,p):
        return [RamaCase(nombre_variable= p[0], cast = p[2], tipo= p[2], cuerpo= p[4])] + p[6]


    @_("NEW TYPEID")
    def expresion(self, p):
        return Nueva(tipo= p[1])
    
  
    @_("'{' bloque '}'")
    def expresion(self, p):
        return Bloque(expresiones= p[1])
    

    @_("expresion ';'")
    def bloque(self, p):
        return [p[0]]

    @_("bloque expresion ';'")
    def bloque(self, p):
        return p[0] + [p[1]]
   
    @_("error ';'")
    def bloque(self, p):
        return list()

    @_("OBJECTID")
    def expresion(self, p):
        return Objeto(nombre= p[0])
    
    @_("INT_CONST")
    def expresion(self, p):
        return Entero(valor= p[0])
    
    @_("STR_CONST")
    def expresion(self, p):
        return String(valor= p[0])
    

    @_("BOOL_CONST")
    def expresion(self, p):
        return Booleano(valor= p[0])



