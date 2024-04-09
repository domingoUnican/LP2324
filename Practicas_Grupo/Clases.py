# coding: utf-8
from dataclasses import dataclass, field
from typing import List



@dataclass
class Nodo:
    linea: int = 0

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'
    
    #FIXME Nodo
    def genera_codigo(self, n=0):
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
    
    def genera_codigo(self, n=0):
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{self.nombre} = {self.cuerpo.genera_codigo(0)}'
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
    

    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{self.cuerpo.genera_codigo(n)}.{self.nombre_metodo}('
        if len(self.argumentos) > 0:
            for arg in self.argumentos[:-1]:
                codigo += f'{arg.genera_codigo(0)} ,'
            codigo += f'{self.argumentos[-1].genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):
        codigo=""
        codigo = f'{(n)*" "}if {self.condicion.genera_codigo(0)}:\n'
        codigo += f'{self.verdadero.genera_codigo(n+2)}\n'
        codigo += f'{(n)*" "}else:\n'
        codigo += f'{self.falso.genera_codigo(n+2)}\n'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}while {self.condicion.genera_codigo(0)}:\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2)}\n'
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
    
    # def genera_codigo(self, n=0):
    #     #similar to lambda expression
    #     codigo = ""
    #     codigo = f'{(n)*" "}def {self.nombre}({self.tipo}):\n'
    #     codigo += f'{(n+2)*" "}{self.inicializacion.genera_codigo(0)}\n'
    #     codigo += f'{self.cuerpo.genera_codigo(n+2)}\n'
    #     return codigo
    
        # codigo = ""
        # codigo = f'{(n)*" "}{self.nombre} = {self.inicializacion.genera_codigo(0)}\n'
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

    def genera_codigo(self, n=0):
        codigo = ""
        for expr in self.expresiones:
            codigo += f'{expr.genera_codigo(n)}\n'
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
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}if {self.nombre_variable} is {self.tipo}:\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2)}\n'
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
    
    # def genera_codigo(self, n=0):
    #     codigo = ""
    #     codigo = f'{(n)*" "}if {self.expr.genera_codigo(0)}:\n'
    #TODO Swicht


@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}new {self.tipo}'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} + {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} - {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} * {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} / {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} < {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} <= {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'{self.izquierda.genera_codigo(n)} == {self.derecha.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'not {self.expr.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'not {self.expr.genera_codigo(0)}'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{self.expr.genera_codigo(0)} is None'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        if self.nombre == "self":
            codigo = f'{(n)*" "}{self.nombre}'
        else:
            codigo = f'{(n)*" "}self.{self.nombre}' 
        return codigo


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0):
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}{self.valor}'
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
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}{self.valor}'
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

    def genera_codigo(self, n=0):
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
    
    def genera_codigo(self, n=0): # genera codigo tiene que tener un indentado 
        #----------------------------------
        codigo =""
        for clase in self.secuencia:
            codigo += clase.genera_codigo(n)
            codigo+= f"{' '*n}Main().main()\n"

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
    def genera_codigo(self,n=0):
        codigo =""
        codigo = f"{' '*n}class {self.nombre}({self.padre}):\n"
        lista_atributos = []
        for caracteristica in self.caracteristicas:
            if (isinstance(caracteristica, Atributo)):
                lista_atributos.append(caracteristica.nombre)
        for caracteristica in self.caracteristicas:
            codigo += caracteristica.genera_codigo(n+2, lista_atributos)
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
    
    def genera_codigo(self,n=0):
        codigo = ""
        codigo = f'{(n)*" "}def {self.nombre}(self'
        for formal in self.formales:
            codigo +=  ',' + formal.genera_codigo(0)
        codigo += '):\n'
        codigo += self.cuerpo.genera_codigo(n+2)
        return codigo


class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    
    def genera_codigo(self,n=0):
        if (self.tipo == "Int" and self.cuerpo.genera_codigo(0) == "None"):
            codigo = f"{' '*n}{self.nombre} = 0\n"
        elif (self.tipo == "Bool" and self.cuerpo.genera_codigo(0) == "None"):
            codigo = f"{' '*n}{self.nombre} = False\n"
        elif (self.tipo == "String" and self.cuerpo.genera_codigo(0) == "None"):
            codigo = f"{' '*n}{self.nombre} = ''\n"
        else:
            codigo = f"{' '*n}{self.nombre} = {self.cuerpo.genera_codigo(0)}\n"
        return codigo
