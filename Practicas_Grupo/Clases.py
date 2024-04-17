# coding: utf-8
from dataclasses import dataclass, field
from typing import List



@dataclass
class Nodo:
    linea: int = 0

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'
    
    def genera_codigo(self, n):
        return ''
    


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
        codigo = ''
        if self.tipo == 'Int':
            codigo = f"{' '*n}{self.nombre_variable} = 0\n"
        elif self.tipo == 'String':
            codigo = f"{' '*n}{self.nombre_variable} = ''\n"
        elif self.tipo == 'Bool':
            codigo = f"{' '*n}{self.nombre_variable} = False\n"
        else:
            codigo = f"{' '*n}{self.nombre_variable} = None\n"
        return codigo



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
        codigo += f"{self.cuerpo.genera_codigo(n)}\n"
        if self.nombre in Clase.atributos:
            codigo += f"{' '*n}self.{self.nombre} = t\n"
        else:
            codigo += f"{' '*n}{self.nombre} = t\n"
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
        global contador
        codigo = ""
        pila = []
        
        #Generamos codigo para cada argumento y se guarda en una variable temporal
        for pos, c in enumerate(self.argumentos):
            codigo += f"{c.genera_codigo(n)}\n"
            codigo += f"{' '*n}t{contador} = t\n"
            pila.append(f"t{contador}")
            contador += 1

        #Generamos codigo para la llamada al metodo de forma estatica
        argumentos_codigo = ', '.join(pila)
        codigo += f"{' '*n}t = {self.clase}().{self.nombre_metodo}({argumentos_codigo})\n"
        return codigo
        


contador = 0  # Contador global para generar nombres de variables temporales únicos
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
        global contador
        codigo = ""
        pila = []
        
        # Generamos codigo para cada argumento y se guarda en una variable temporal
        for c in self.argumentos:
            codigo += f"{c.genera_codigo(n)}\n"
            codigo += f"{' '*n}t{contador} = t\n"
            pila.append(f"t{contador}")
            contador += 1
        
        # Generamos codigo para el cuerpo de la llamada
        codigo += f"{self.cuerpo.genera_codigo(n)}\n"
        codigo += f"{' '*n}t{contador} = t\n"
        contador += 1
        
        # Generamos codigo para la llamada al metodo
        argumentos_codigo = ', '.join(pila)
        codigo += f"{' '*n}t = t{contador-1}.{self.nombre_metodo}({argumentos_codigo})\n"
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
        codigo = ''
        codigo += f"{self.condicion.genera_codigo(n)}\n"
        codigo += f"{' '*n}if t:\n"
        codigo += f"{self.verdadero.genera_codigo(n+4)}\n"
        codigo += f"{' '*n}else:\n"
        codigo += f"{self.falso.genera_codigo(n+4)}\n"
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
        codigo = ''
        codigo += f"{self.condicion.genera_codigo(n)}\n"
        codigo += f"{' '*n}t1 = t\n"
        codigo += f"{' '*n}if t == false:\n"
        codigo += f"{' '*(n+2)}t = Objeto()\n"
        codigo += f"{' '*n}while t1 == true:\n"
        codigo += f"{self.cuerpo.genera_codigo(n+2)}\n"
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
        codigo = ""
        if isinstance(self.inicializacion,NoExpr):
            if self.tipo == 'Int':
                codigo += f"{' '*n}{self.nombre} = Entero(0)\n"
            elif self.tipo == 'String':
                codigo += f"{' '*n}{self.nombre} = String1("")\n"
            elif self.tipo == 'Bool':
                codigo += f"{' '*n}{self.nombre} = Booleano(False)\n"
        else:
            codigo += f"{self.inicializacion.genera_codigo(n)}\n"
            codigo += f"{' '*n}{self.nombre} = t\n"
        
        codigo += f"{self.cuerpo.genera_codigo(n)}"
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
        codigo = ""
        for e in self.expresiones:
            codigo += e.genera_codigo(n)
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
        codigo = ''
        codigo += f"{' '*n}if isinstance(t, {self.tipo}):\n"
        codigo += f"{self.cuerpo.genera_codigo(n+2)}\n"
        codigo += f"{' '*(n+2)}return t\n"
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
        codigo = ''
        codigo += f"{self.expr.genera_codigo(n)}\n"
        for c in self.casos:
            codigo += f"{c.genera_codigo(n)}\n"
        codigo += f"{' '*n}print('Match on void in case statement.')\n"
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
        codigo = ''
        if self.tipo == 'Int':
            codigo += f"{' '*n}t = Entero(None)\n"
        elif self.tipo == 'String':
            codigo += f"{' '*n}t = String(None)\n"
        elif self.tipo == 'Bool':
            codigo += f"{' '*n}t = Booleano(None)\n"
        else:
            codigo += f"{' '*n}t = {self.tipo}()\n"

        return codigo

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
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}\n"
        codigo += f"{' '*(n)}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*(n)}t += t{numero}\n"
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
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}\n"
        codigo += f"{' '*(n)}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t{numero} - t"
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
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}\n"
        codigo += f"{' '*n}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*n}t *= t{numero}\n"
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
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}\n"
        codigo += f"{' '*n}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t{contador} / t"
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
    
    def genera_codigo(self, n):
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}"
        codigo += f"{' '*n}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t{numero} < t"
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
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}"
        codigo += f"{' '*n}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t{numero} <= t"
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
        global contador
        codigo = f"{self.izquierda.genera_codigo(n)}"
        codigo += f"{' '*n}t{contador} = t\n"
        numero = contador
        contador += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t{numero} == t"
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
        codigo = ''
        codigo += f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = {self.operador} t\n"
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
        codigo = ''
        codigo += f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t.__not__()\n"
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
        codigo = ''
        codigo += f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{' '*n}t = t is None"
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

    def genera_codigo(self, n):
        codigo = f"{' '*n}t = {self.nombre}\n"
        if self.nombre in Clase.atributos:
            codigo = f"{' '*n}t = self.{self.nombre}\n"
        elif self.nombre == 'self':
            codigo = f"{' '*n}t = self\n"
        return codigo


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n):
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
        
    def genera_codigo(self, n):
        codigo = f"{' '*n}t = Entero({self.valor})\n"
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

    def genera_codigo(self, n):
        return f"{' '*n}t = String1({self.valor})\n"


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
        codigo = ''
        if self.valor:
            codigo = f"{' '*n}t = Booleano(True)\n"
        else:
            codigo = f"{' '*n}t = Booleano(False)\n"
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
        codigo = ''
        for c in self.secuencia:
            codigo += c.genera_codigo(n)
        codigo += f"{' '*n}Main().main()\n"
        return codigo


        


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
    atributos = set()
    def genera_codigo(self, n):
        
        codigo = ""
        codigo += f"{' '*n}class {self.nombre} ("
        if self.padre == 'Object':
            codigo += "Objeto):\n"
        else:
            codigo += f"{self.padre}):\n"
        
        for c in self.caracteristicas:
            if isinstance(c, Atributo):
                self.atributos.add(c.nombre)
        
        if len(self.atributos) > 0:
            codigo += f"{' '*(n+2)}def __init__(self):\n"
            for c in self.caracteristicas:
                if isinstance(c, Atributo):
                    codigo += c.genera_codigo(n+4)

        for c in self.caracteristicas:
            if not isinstance(c, Atributo):
                codigo += c.genera_codigo(n+2)
        return codigo

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
        codigo += f"{' '*n}def {self.nombre}(self"
        for formal in self.formales:
            codigo +="," + formal.nombre_variable
        codigo += "):\n"
        
        codigo += f"{self.cuerpo.genera_codigo(n+2)}\n"
        codigo += f"{' '*(n+2)}return t\n"
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
        codigo = ''
        if not isinstance(self.cuerpo,NoExpr):
            codigo += f"{self.cuerpo.genera_codigo(n)}\n"
            codigo += f"{' '*n}self.{self.nombre} = t\n"
        elif self.tipo == 'Int':
            codigo = f"{' '*n}self.{self.nombre} = 0\n"
        elif self.tipo == 'String':
            codigo = f"{' '*n}self.{self.nombre} = ''\n"
        elif self.tipo == 'Bool':
            codigo = f"{' '*n}self.{self.nombre} = False\n"
        # elif self.tipo == 'IO':
        #     codigo = f"{' '*n}{self.nombre} = IO()\n"
        else:
            codigo = f"{' '*n}self.{self.nombre} = None\n"
        return codigo

