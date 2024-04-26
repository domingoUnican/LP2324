# coding: utf-8
from dataclasses import dataclass, field
from typing import List
import re



dict_global = {"padre": None}


@dataclass
class Nodo:
    linea: int = 0

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'
    
    #FIXME Nodo
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        return ""
    


@dataclass
class Formal(Nodo):
    nombre_variable: str = '_no_set'
    tipo: str = '_no_type'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        return f'{self.nombre_variable}'



class Expresion(Nodo):
    cast: str = '_no_type'
    
    

@dataclass
class Asignacion(Expresion):
    nombre: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        global dict_global
        codigo = ""
        # Recibir el diccionario local y ver si esta ahi, si no, mirar al "padre"
        nombre_variable = self.nombre
        diccionario = dict_recibido
        
        while(diccionario["padre"] is not None):
            if self.nombre in diccionario.keys():
                break
            else:
                diccionario = diccionario["padre"]
        
        if diccionario["padre"] is not None:
            nombre_usado = nombre_variable
        else:
            nombre_usado = "self." + nombre_variable

        codigo = f'{(n)*" "}{nombre_usado} = {self.cuerpo.genera_codigo(0, dict_recibido)}'
        #FIXME
        return codigo



@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion = None
    clase: str = '_no_type'
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: _no_type\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        variable = self.cuerpo.genera_codigo(0, dict_recibido)
        codigo += f'{" "*n}temp = {variable}\n'
        codigo += f'{" "*n}temp.__class__ = {self.clase}'
        codigo += f'{" "*n}temp.{self.nombre_metodo}('
        if len(self.argumentos) > 0:
            for arg in self.argumentos[:-1]:
                codigo += f'{arg.genera_codigo(0, dict_recibido)}, '
            codigo += f'{self.argumentos[-1].genera_codigo(0, dict_recibido)}'
        codigo += f')'
        return codigo
    
    



@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion = None
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{self.cuerpo.genera_codigo(n, dict_recibido)}.{self.nombre_metodo}('
        if len(self.argumentos) > 0:
            for arg in self.argumentos[:-1]:
                codigo += f'{arg.genera_codigo(0, dict_recibido)}, '
            codigo += f'{self.argumentos[-1].genera_codigo(0, dict_recibido)}'
        codigo += f')'
        return codigo


@dataclass
class Condicional(Expresion):
    condicion: Expresion = None
    verdadero: Expresion = None
    falso: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n+2)
        resultado += self.verdadero.str(n+2)
        resultado += self.falso.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo=""
        codigo += f'{(n)*" "}condicion = ({self.condicion.genera_codigo(0, dict_recibido)})\n'
        codigo += f'{(n)*" "}if (condicion == True):\n'
        codigo += f'{self.verdadero.genera_codigo(n+2, dict_recibido)}\n'
        codigo += f'{(n)*" "}else:\n'
        codigo += f'{self.falso.genera_codigo(n+2, dict_recibido)}\n'
        return codigo



@dataclass
class Bucle(Expresion):
    condicion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{(n)*" "}while {self.condicion.genera_codigo(0, dict_recibido)}:\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2, dict_recibido)}\n'
        return codigo


@dataclass
class Let(Expresion):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    inicializacion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_let\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.inicializacion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
    #     #similar to lambda expression
        variable = self.nombre
        dict_actual = {"padre": dict_recibido}
        dict_actual.update({self.nombre: None})
        codigo = ""
        # codigo += f'{n*" "}let {variable} : '
        # codigo += f'{self.tipo}'
        # codigo += f'({self.inicializacion.genera_codigo(0, dict_recibido)})'
        # codigo += f' in {self.cuerpo.genera_codigo(0, dict_actual)}\n'

        # codigo += f'{n*" "}temp = lambda {variable} : {self.cuerpo.genera_codigo(0, dict_recibido)}\n'
        # codigo += f'{n*" "}temp({self.tipo}({self.inicializacion.genera_codigo(0, dict_recibido)}))\n'

        codigo += f'{(n)*" "}def temp_func({self.nombre}):\n'
        # codigo += f'{(n+2)*" "}{self.inicializacion.genera_codigo(0)}\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2, dict_actual)}\n'
        codigo += f'{(n)*" "}variable = {self.tipo}({self.inicializacion.genera_codigo(0, dict_actual)})\n'
        codigo += f'{(n)*" "}temp_func(variable)\n'
        return codigo
    
        # codigo = ""
        # codigo += f'{(n)*" "}{self.nombre} = {self.inicializacion.genera_codigo(0)}\n'
        # codigo += f'{self.cuerpo.genera_codigo(n)}'
        # return codigo
    #FIXME Let


@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += ''.join([e.str(n+2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += '\n'
        return resultado
    #FIXME Bloque

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        temporal = None
        for expr in self.expresiones:
            codigo += f'{expr.genera_codigo(n, dict_recibido)}\n'
        
        return codigo


@dataclass
class RamaCase(Nodo):
    nombre_variable: str = '_no_set'
    cast: str = '_no_set'
    tipo: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    #FIXME RamaCase
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{(n)*" "}if {self.nombre_variable} is {self.tipo}:\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2, dict_recibido)}\n'
        return codigo

@dataclass
class Swicht(Expresion):
    expr: Expresion = None
    casos: List[RamaCase] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n+2)
        resultado += ''.join([c.str(n+2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
        
    #FIXME Swicht

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        
        #usamos un diccionario para hacer el switch
        codigo = ""
        codigo = f'{(n)*" "}match {self.expr.genera_codigo(0, dict_recibido)}:\n'
        for caso in self.casos:
            codigo += f'{(n+2)*" "}case {caso.genera_codigo(0, dict_recibido)}:\n'
            codigo += f'{caso.cuerpo.genera_codigo(n+4, dict_recibido)}\n'
        return codigo

        
        # codigo = ""
        # codigo = f'{(n)*" "}switch {self.expr.genera_codigo(0)}:\n'
        # for caso in self.casos:
        #     codigo += caso.genera_codigo(n+2)
            


@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        # codigo = f'{(n)*" "}new {self.tipo}'
        codigo = f'{(n)*" "}'
        return codigo
        #FIXME Nueva


@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion = None
    derecha: Expresion = None



@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp + temp0'
        codigo = f'{self.izquierda.genera_codigo(n, dict_recibido)} + {self.derecha.genera_codigo(0, dict_recibido)}'

         
        #si no existen las variables en el diccionario las creamos y inicializamos a 0?
    #    if(self.izquierda.genera_codigo(0, dict_recibido) not in dict_recibido.keys()):
    #        dict_recibido.update({self.izquierda.genera_codigo(0, dict_recibido): 0})
            
    #    if(self.derecha.genera_codigo(0, dict_recibido) not in dict_recibido.keys()):
    #        dict_recibido.update({self.derecha.genera_codigo(0, dict_recibido): 0})
            

        
        
        return codigo

@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):

        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n, dict_recibido)} - {self.derecha.genera_codigo(0, dict_recibido)}'
        return codigo



@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):    

        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n, dict_recibido)} * {self.derecha.genera_codigo(0, dict_recibido)}'
        return codigo

@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n, dict_recibido)} / {self.derecha.genera_codigo(0, dict_recibido)}'
        return codigo

@dataclass
class Menor(OperacionBinaria):
    operando: str = '<'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_lt\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n, dict_recibido)} < {self.derecha.genera_codigo(0, dict_recibido)}'
        return codigo



@dataclass
class LeIgual(OperacionBinaria):
    operando: str = '<='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n, dict_recibido)} <= {self.derecha.genera_codigo(0, dict_recibido)}'
        return codigo


@dataclass
class Igual(OperacionBinaria):
    operando: str = '='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):    
        codigo = ""
        codigo += f'{self.izquierda.genera_codigo(n, dict_recibido)} == {self.derecha.genera_codigo(0, dict_recibido)}'

        return codigo




@dataclass
class Neg(Expresion):
    expr: Expresion = None
    operador: str = '~'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):    
        codigo = ""
        codigo = f'not {self.expr.genera_codigo(0, dict_recibido)}'
        return codigo

@dataclass
class Not(Expresion):
    expr: Expresion = None
    operador: str = 'NOT'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'not {self.expr.genera_codigo(0, dict_recibido)}'
        return codigo

@dataclass
class EsNulo(Expresion):
    expr: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{self.expr.genera_codigo(0, dict_recibido)}.isVoid()'
        return codigo

@dataclass
class Objeto(Expresion):
    nombre: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""

        nombre_variable = self.nombre
        diccionario = dict_recibido
        
        while(diccionario["padre"] is not None):
            if self.nombre in diccionario.keys():
                break
            else:
                diccionario = diccionario["padre"]
        
        if (diccionario["padre"] is not None) or (nombre_variable is "self"):
            nombre_usado = nombre_variable
        else:
            nombre_usado = "self." + nombre_variable

        codigo += f'{(n)*" "}{nombre_usado}'

        # if self.nombre == "self":
        #     codigo = f'{(n)*" "}{self.nombre}'
        # else:
        #     codigo = f'{(n)*" "}self.{self.nombre}' 
        return codigo
    #FIXME que reciba el dict


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        return "None"


@dataclass
class Entero(Expresion):
    valor: int = 0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{(n)*" "}Int({self.valor})'
        return codigo

@dataclass
class String(Expresion):
    valor: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{(n)*" "}String({self.valor})'
        return codigo


@dataclass
class Booleano(Expresion):
    valor: bool = False
    
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{(n)*" "}{True if self.valor else False}'
        return codigo
        

@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global): # genera codigo tiene que tener un indentado 
        #----------------------------------
        codigo =""
        for clase in self.secuencia:
            codigo += clase.genera_codigo(n, dict_recibido)
        codigo += f"{' '*n}Main().main()\n"

        return codigo
        #----------------------------------

@dataclass
class Caracteristica(Nodo):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    cuerpo: Expresion = None
    

@dataclass
class Clase(Nodo):
    nombre: str = '_no_set'
    padre: str = '_no_set'
    nombre_fichero: str = '_no_set'
    caracteristicas: List[Caracteristica] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.caracteristicas])
        resultado += '\n'
        resultado += f'{(n+2)*" "})\n'
        return resultado
    
    #------------------
    def genera_codigo(self,n=0, dict_recibido=dict_global):
        codigo =""
        codigo = f"{' '*n}class {self.nombre}({self.padre}):\n"
        global dict_global
        for caracteristica in self.caracteristicas:
            if (isinstance(caracteristica, Atributo)):
                # lista_atributos.append(caracteristica.nombre)
                dict_global.update({caracteristica.nombre: None}) # FIXME
        for caracteristica in self.caracteristicas:
            codigo += caracteristica.genera_codigo(n+2, dict_global) # FIXME
        return codigo
    #-------------------

@dataclass
class Metodo(Caracteristica):
    formales: List[Formal] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)

        return resultado
    
    def genera_codigo(self,n=0, dict_recibido=dict_global):      
        # global lista_atributos
        nuevo_ambito = {"padre": dict_recibido}
        codigo = ""
        codigo = f'{(n)*" "}def {self.nombre}(self'
        for formal in self.formales:
            nombre_formal = formal.genera_codigo(0, dict_recibido)
            codigo +=  ', ' + nombre_formal
            codigo += f'={formal.tipo}(None)'
            nuevo_ambito.update({nombre_formal: "None"})
        codigo += '):\n'
        #codigo += self.cuerpo.genera_codigo(n+2, nuevo_ambito)
        #codigo += f'{(n+2)*" "}return {self.cuerpo.genera_codigo(0, nuevo_ambito)[-1]}\n'
        #bucle que recorre el cuerpo por detras hasta encontrar un salto de linea
        #TODO
        lista_retorno = []
        contador = 0
        if self.nombre == "main":
            codigo += self.cuerpo.genera_codigo(n+2, nuevo_ambito)
        else:
            for elemento in reversed(self.cuerpo.genera_codigo(0, nuevo_ambito)):
                    if elemento == '\n':
                        break
                    else:
                        lista_retorno.append(elemento)
                        contador += 1
            codigo += self.cuerpo.genera_codigo(n+2, nuevo_ambito)[0:-contador]
            codigo += f'{(n+2)*" "}return ({"".join(reversed(lista_retorno))})\n'
        codigo += '\n'
        return codigo


class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    
    def genera_codigo(self,n=0,dict_recibido=dict_global):
        if (self.tipo == "IO" and self.cuerpo.genera_codigo(0) == "None"):
            codigo = f"{' '*n}{self.nombre} = {self.tipo}()\n"
        else:
            codigo = f"{' '*n}{self.nombre} = {self.tipo}({self.cuerpo.genera_codigo(0, dict_recibido)})\n"
        # dict_recibido.update(self.nombre, self.tipo(self.cuerpo.genera_codigo(0)))
        #FIXME cambios con el diccionario
        # if (self.tipo == "Int" and self.cuerpo.genera_codigo(0) == "None"):
        #     codigo = f"{' '*n}{self.nombre} = 0\n"
        # elif (self.tipo == "Bool" and self.cuerpo.genera_codigo(0) == "None"):
        #     codigo = f"{' '*n}{self.nombre} = False\n"
        # elif (self.tipo == "String" and self.cuerpo.genera_codigo(0) == "None"):
        #     codigo = f"{' '*n}{self.nombre} = ''\n"
        # else:
        #     codigo = f"{' '*n}{self.nombre} = {self.cuerpo.genera_codigo(0)}\n"
        # codigo = f"{' '*n}{self.nombre} = {self.cuerpo.genera_codigo(0)}\n"
        
        return codigo
