# coding: utf-8
from dataclasses import dataclass, field
from typing import List
from Base_clases import *

global lista

lista = []
@dataclass
class Nodo:
    linea: int = 0

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'


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

    def genera_codigo(self, n):
        return f"{' '*n}{self.nombre_variable}"



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

    def genera_codigo(self, n):
        codigo = ""
        if isinstance(self.cuerpo, Objeto) or isinstance(self.cuerpo, Nueva):
            codigo += f"{(' ')*n}temp = {self.cuerpo.genera_codigo(0)}\n"
        
        else: 
            codigo += f"{self.cuerpo.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}self.{self.nombre} = temp"
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

    def genera_codigo(self, n):
        codigo = f"{self.cuerpo.genera_codigo(n)}\n"
        codigo += f"{' '*n}temp.__class__ = {self.clase}\n"    
        codigo += f"{' '*n}temp.{self.nombre_metodo}("
        for formal in self.argumentos[:-1]:
            codigo += formal.genera_codigo(0) + ","
        if self.argumentos:
            codigo += self.argumentos[-1].genera_codigo(0) 
        codigo +=")"
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
    
    def genera_codigo(self, n):
        #*lista = trata la lista como puntero, accediendo a sus argumentos
        codigo = f"{' '*n}lst{self.nombre_metodo} = []\n"
        for formal in self.argumentos[:-1]:
            codigo += formal.genera_codigo(n) + "\n"
            codigo += f"{' '*n}lst{self.nombre_metodo}.append(temp)\n"
        if self.argumentos:
            codigo += self.argumentos[-1].genera_codigo(n) + "\n"
            codigo += f"{' '*n}lst{self.nombre_metodo}.append(temp)\n"
        codigo+=f"{self.cuerpo.genera_codigo(n)}.{self.nombre_metodo}(*lst{self.nombre_metodo})\n"
        """for formal in self.argumentos[:-1]:
            codigo += formal.genera_codigo(0) + ","
        if self.argumentos:
            codigo += self.argumentos[-1].genera_codigo(0)"""
        #codigo +=")"
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
    def genera_codigo(self, n):
        codigo = f"{self.condicion.genera_codigo(n)}\n"
        codigo += f"{' '*n}if Bool(b=True) == (temp):\n"
        
        codigo += f"{self.verdadero.genera_codigo(n+2)}\n"
        codigo += f"{' '*n}else:\n"
        codigo += f"{self.falso.genera_codigo(n+2)}\n"
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

    def genera_codigo(self, n):
        codigo =f"{self.condicion.genera_codigo(n)}"
        codigo =f"{' '*n}while temp:\n"
        codigo+=self.cuerpo.genera_codigo(n+2)
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
    def genera_codigo(self, n):
        codigo = f"{' '*n}"

        if (self.tipo == 'Booleano' and isinstance(self.inicializacion, NoExpr)):
            self.inicializacion = Booleano()
        elif (self.tipo == 'Entero' and isinstance(self.inicializacion, NoExpr)):
            self.inicializacion = Entero()
        elif (self.tipo == 'String' and isinstance(self.inicializacion, NoExpr)):
            self.inicializacion = String1(valor="")


        codigo += self.inicializacion.genera_codigo(0) + "\n"
        codigo += f"{' '*n}{self.nombre} = temp\n"
        codigo += self.cuerpo.genera_codigo(n)
        return codigo


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
    def genera_codigo(self, n):
        #codigo=f"{' '*n}"
        codigo=""
        for e in self.expresiones:
            codigo+= e.genera_codigo(n) +"\n" 
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
    def genera_codigo(self, n):
        codigo = f"{' '*(n+2)}{self.cuerpo.genera_codigo(0)}\n"
        codigo+= f"{' '*(n+2)}{self.nombre_variable}=temp\n"
        codigo+= f"{' '*(n+2)}return {self.nombre_variable}\n"
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
    def genera_codigo(self, n):
        #genera codigo de condicional
        codigo = f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{' '*n}variable = temp\n"
        codigo += f"{' '*n}if isinstance(variable, {self.casos[0].tipo}):\n"
        codigo += f"{self.casos[0].genera_codigo(n)}"
        for caso in self.casos[1:]:
            codigo += f"{' '*n}elif isinstance(variable, {self.caso.tipo}):\n"
            codigo += f"{self.caso.genera_codigo(n)}"
        return codigo
        

@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def genera_codigo(self, n):
        return f"{' '*n}temp = {self.tipo}()"

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
    def genera_codigo(self, n):
        codigo = ""
        codigo+= self.izquierda.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}sumando = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = sumando + temp \n"
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

    def genera_codigo(self, n):
        #return f"{' '*n}{self.izquierda}-{self.derecha}"
        codigo = ""
        codigo+= self.izquierda.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}restando = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = restando - temp \n"
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
    def genera_codigo(self, n):
        codigo = ""
        codigo+= self.izquierda.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}multiplicando = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = multiplicando * temp \n"
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
    def genera_codigo(self, n):

        codigo = ""
        codigo+= self.izquierda.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}dividendo = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = dividendo / temp \n"
        return codigo
        #return f"{' '*n}{self.izquierda}/{self.derecha}"


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
    def genera_codigo(self, n):
        codigo = ""
        codigo =f"{self.izquierda.genera_codigo(n)}\n"
        codigo = f"{(n)*' '}temp1 = temp\n"
        codigo =f"{self.derecha.genera_codigo(n)}\n"
        codigo = f"{(n)*' '}temp = (temp < temp1)\n"
        codigo = "temp"
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
    def genera_codigo(self, n):
        codigo = ""
        codigo =f"{self.izquierda.genera_codigo(n)}\n"
        codigo = f"{(n)*' '}temp1 = temp\n"
        codigo =f"{self.derecha.genera_codigo(n)}\n"
        codigo = f"{(n)*' '}temp = (temp <= temp1)\n"
        codigo = "temp"
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
    
    def genera_codigo(self, n):
        codigo =f"{self.izquierda.genera_codigo(n)}\n"
        codigo += f"{(n)*' '}temp1 = temp\n"
        codigo +=f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(n)*' '}temp = (temp == temp1)\n"
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
    
    def genera_codigo(self, n):
        stringAQuitar = "temp="
        stringOriginal = f"{self.expr.genera_codigo(0)}"
        new_string = stringOriginal.replace(stringAQuitar, "")
        codigo = f"{' '*(n)}temp = not {new_string}"
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
    
    def genera_codigo(self, n):
        codigo = f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{' '*n}temp = not temp"
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
    
    def genera_codigo(self, n):
        return f"{' '*n}{self.expr.genera_codigo(0)}.EsNulo()"

@dataclass
class Objeto(Expresion):
    nombre: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def genera_codigo(self, n):
        global lista
        if self.nombre in lista:
            return f"{' '*n}temp = self.{self.nombre}"
        else:
            return f"{' '*n}temp = {self.nombre}"


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def genera_codigo(self, n):
        return f"{' '*n}"


@dataclass
class Entero(Expresion):
    valor: int = 0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def genera_codigo(self, n):
        return f"{' '*n}temp={self.valor}"

@dataclass
class String1(Expresion):
    valor: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n):
        return f"{' '*n}temp = String({self.valor})"
        


@dataclass
class Booleano(Expresion):
    valor: bool = False
    
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    def genera_codigo(self, n):
        return f"{' '*n}temp = {self.valor}"
    

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
            #codigo += clase.genera_codigo(n)

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
    def genera_codigo(self,n):
        codigo =""
        if self.padre == "" :
            codigo = f"{' '*n}class {self.nombre}(Object):\n"
        else:
            codigo = f"{' '*n}class {self.nombre}({self.padre}):\n"""
            codigo += f""
        codigo += f"{' '*(n+2)}def __init__(self):\n"
        counter = 0
        for caracteristica in self.caracteristicas:
            if isinstance(caracteristica, Atributo):
                codigo += caracteristica.genera_codigo(n+4)
                counter += 1
        if counter == 0:
            codigo += f"{' '*(n+4)}pass\n"
        for caracteristica in self.caracteristicas:
            if not isinstance(caracteristica, Atributo):
                codigo += caracteristica.genera_codigo(n+2)
        
        
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

    def genera_codigo(self, n):
        codigo = ""
        if self.formales == []:
            codigo += f"{' '*n}def {self.nombre}(self"
        else:
            codigo += f"{' '*n}def {self.nombre}(self,"
        for formal in self.formales[:-1]:
            codigo += formal.genera_codigo(0) + ","
        if self.formales:
            codigo += self.formales[-1].genera_codigo(0) 
        codigo +="):\n"
        codigo +=self.cuerpo.genera_codigo(n+2)
        codigo += f"{' '*(n+2)}return temp\n"
        return codigo


class Atributo(Caracteristica):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado

    def genera_codigo(self, n):
        #else:
        global lista
        lista.append(self.nombre)
        codigo = f"{self.cuerpo.genera_codigo(n)}\n"
        if (self.tipo == 'Booleano' and isinstance(self.cuerpo, NoExpr)):
            codigo += f"{' '*n}self.{self.nombre}={self.tipo}()\n"
        elif (self.tipo == 'Entero' and isinstance(self.cuerpo, NoExpr)):
            codigo += f"{' '*n}self.{self.nombre}={self.tipo}()\n"
        elif (self.tipo == 'String' and isinstance(self.cuerpo, NoExpr)):
            codigo += f"{' '*n}self.{self.nombre}={self.tipo}()\n"
        elif (not isinstance(self.cuerpo, NoExpr)):
            codigo += self.cuerpo.genera_codigo(n)
            codigo+="\n"
            codigo += f"{' '*n}self.{self.nombre}=temp\n"
        else:
            codigo += f"{' '*n}self.{self.nombre}=None\n"
        #aqui pendejo
        #codigo += f"{' '*n}self.{self.nombre}={self.tipo}()\n"
        return codigo
        #return f"{' '*n}{self.nombre}={self.tipo}({self.cuerpo.genera_codigo(n)})\n"