# coding: utf-8
from dataclasses import dataclass, field
from typing import List


ATRIBUTOS = []
INDICE = 0

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
        codigo = ""
        codigo += f"{self.nombre_variable}"
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
    
    def genera_codigo(self,n):
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
        global INDICE
        codigo = ""
        temp = ""
        lista_ind = []
        

        if not(len(self.argumentos) == 0):
            for i in range(len(self.argumentos)):
                codigo += f"{self.argumentos[i].genera_codigo(n)}\n"
                codigo += f"{(' ')*n}temp{INDICE} = temp\n"
                lista_ind.append(INDICE)
                
                INDICE += 1

        codigo += f"{(' ')*n}{self.cuerpo.genera_codigo(0)}\n"
        codigo += f"{(' ')*n}clase = deepcopy(temp)\n"
        codigo += f"{(' ')*n}clase.__class__ = {self.clase}\n"
        codigo += f"{(' ')*n}temp = clase.{self.nombre_metodo}("
        if len(self.argumentos) == 1:
            codigo+= f"temp{lista_ind[0]}"
        elif (len(self.argumentos) > 1):
            for i in lista_ind[:-1]:
                codigo += f"temp{i}, "
            codigo+= f"temp{lista_ind[-1]}"
        
        codigo += ")"

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
        global INDICE
        codigo = ""
        temp = ""
        lista_ind = []
        if not(len(self.argumentos) == 0):
            for i in range(len(self.argumentos)):
                codigo += f"{self.argumentos[i].genera_codigo(n)}\n"
                codigo += f"{(' ')*n}temp{INDICE} = temp\n"
                lista_ind.append(INDICE)
                
                INDICE += 1
        
        codigo += f"{self.cuerpo.genera_codigo(n)}  \n"
        codigo += f"{n*(' ')}temp = temp.{self.nombre_metodo}("
        if len(self.argumentos) == 1:
            codigo+= f"temp{lista_ind[0]}"
        elif (len(self.argumentos) > 1):
            for i in lista_ind[:-1]:
                codigo += f"temp{i}, "
            codigo+= f"temp{lista_ind[-1]}"
        
        codigo += ")"
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
        codigo = ""
        codigo += f"{self.condicion.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}if True == temp:\n"
        codigo += f"{self.verdadero.genera_codigo(n+2)}\n"
        codigo += f"{(' ')*n}else:\n{self.falso.genera_codigo(n+2)}"
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
        codigo = ""
        codigo +=f"{self.condicion.genera_codigo(n)}\n"
        codigo += f"{(n)*(' ')}while(temp == True):\n"
        codigo += f"{self.cuerpo.genera_codigo(n+2)}"
        codigo +=f"{self.condicion.genera_codigo(n+2)}\n"
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
        codigo = f""
        inicializa = f"{(' ')*n}temp = "
        if (self.tipo == "Int"):
            inicializa += "Entero(0)"
        elif (self.tipo == "String"):
            inicializa += "Cadena_carac()"
        elif (self.tipo == "Bool"):
            inicializa += "Booleano(False)"
        else:
            inicializa += f"{self.inicializacion.genera_codigo(n)}"
        codigo += f"{inicializa}\n"
        codigo += f"{(' ')*n}{self.nombre} = temp\n"
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
        codigo = f""
        for expr in self.expresiones:
            codigo += f"{expr.genera_codigo(n)}\n"
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
        codigo = ""
        codigo += f"{self.tipo}):\n"
        codigo += f"{(n)*' '}{self.nombre_variable} = {self.tipo}()\n"
        codigo += f"{self.cuerpo.genera_codigo(n)}\n"
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
        codigo = ""

        codigo += f"{(n)*' '}if isinstance({self.expr.genera_codigo(0)}, {self.casos[0].genera_codigo(n + 2)}"
        for i in range(len(self.casos) - 1):
            codigo += f"elif ({self.expr.genera_codigo(0)} == {self.casos[i+1].genera_codigo(n + 2)}"
        codigo += f"{(n)*' '}else:\n"
        codigo += f"{(n+2)*' '}temp = None\n"
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
        codigo = f"{n*(' ')}temp = "
        if (self.tipo == "Int"):
            codigo += f"Entero(0)"
        elif (self.tipo == "String"):
            codigo += f"Cadena_carac("")"
        elif (self.tipo == "Bool"):
            codigo += f"Booleano()"
        elif (self.tipo == "IO"):
            codigo += f"IO()"
        else:
            codigo+=f"{self.tipo}()"
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
        global INDICE
        indiceloc = INDICE
        codigo = ""
        INDICE += 1
        codigo = f"{self.izquierda.genera_codigo(n)}\n" 
        codigo += f"{(' ')*n}tempsuma{indiceloc} = temp\n"
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}temp = tempsuma{indiceloc} + temp"
        
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
        global INDICE
        indiceloc = INDICE 
        codigo = ""
        INDICE += 1
        codigo += f"{self.izquierda.genera_codigo(n)}\n" 
        codigo += f"{(' ')*n}tempresta{indiceloc} = temp\n"
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}temp = tempresta{indiceloc} - temp"
        
        
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
        global INDICE
        indiceloc = INDICE 
        codigo = ""
        INDICE += 1
        codigo = f"{self.izquierda.genera_codigo(n)}\n" 
        codigo += f"{(' ')*n}tempmul{indiceloc} = temp\n"
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}temp = tempmul{indiceloc} * temp"
        
        
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
        global INDICE
        indiceloc = INDICE 
        codigo = ""
        INDICE += 1
        codigo = f"{self.izquierda.genera_codigo(n)}\n" 
        codigo += f"{(' ')*n}tempdiv{indiceloc} = temp\n"
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}temp = tempdiv{indiceloc} / temp"
        
        
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
        codigo = ""
        codigo = f"{self.izquierda.genera_codigo(n)}\n" 
        codigo += f"{(' ')*n}tempmenor = temp\n"
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(' ')*n}temp = tempmenor < temp"
        
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
        global INDICE
        
        codigo = ""
        codigo += f"{self.izquierda.genera_codigo(n)}\n"
        codigo += f"{(n)*' '}temp{INDICE} = temp\n"
        indice1 = INDICE
        INDICE += 1
        codigo += f"{self.derecha.genera_codigo(n)}\n"
        codigo += f"{(n)*' '}temp{INDICE} = temp\n"
        indice2 = INDICE
        INDICE += 1
        codigo += f"{(n)*' '}temp = (temp{indice1} == temp{indice2})"
        return codigo


@dataclass
class Neg(Expresion):
    expr: Expresion = None
    operador: str = '~'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n+2)
        resultado += f'{n*(" ")}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n):
        codigo = ""
        codigo += f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{n*(' ')}temp = -temp"
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
        codigo = ""
        codigo += f"{self.expr.genera_codigo(n)}\n"
        codigo += f"{n*(' ')}temp = NOT(temp)"
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
        codigo = ""
        codigo = f"{self.expr.genera_codigo(n)} is None"
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
        global ATRIBUTOS
        codigo = f"{(' ')*n}temp = {self.nombre}" if self.nombre not in ATRIBUTOS else f"{(' ')*n}temp = self.{self.nombre}"
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
        
        codigo = f"{(' ')*n}None" 
        return codigo


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
        codigo = ""
        codigo += f"{(' ')*n}temp = Entero({self.valor})"
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
        codigo = f"{(' ')*n}temp = Cadena_carac({self.valor})"
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

    def genera_codigo(self,n):
        codigo = f"{(n)*' '}temp = Booleano({self.valor})"
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
    def genera_codigo(self, n = 0):
        codigo = ""
        for sec in self.secuencia:
            codigo += sec.genera_codigo(n + 2)
            
        codigo += f"Main().main()"
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
    
    def genera_codigo(self, n):
        global ATRIBUTOS
        codigo = ""
        if self.padre == '_no_set':
            codigo += f"class {self.nombre}:\n"
        else:
            codigo += f"class {self.nombre}({self.padre}):\n"
        codigo += f"{(n+2)*' '}def __init__(self):\n"
        for caracteristica in self.caracteristicas:
            ATRIBUTOS.append(caracteristica.nombre)
            if isinstance(caracteristica,Atributo):
                codigo += f"{caracteristica.genera_codigo(n+2)}\n"
        for caracteristica in self.caracteristicas:
            if isinstance(caracteristica,Metodo):
                codigo += f"{caracteristica.genera_codigo(n+2)}\n"
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
        codigo += f"{(' ')*n}def {self.nombre}(self"
        for i in range(len(self.formales)):
            codigo += f", {self.formales[i].genera_codigo(0)}"
        codigo += '):\n'
        codigo += self.cuerpo.genera_codigo(n+2)
        codigo += f"\n{(' ')*(n+2)}return temp"
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
        codigo = ""
        if isinstance(self.cuerpo, NoExpr):
            if (self.tipo == "Int"):
                codigo += f"{(' ')*n}self.{self.nombre} = Entero(0)"
            elif (self.tipo == "String"):
                codigo += f"{(' ')*n}self.{self.nombre} = Cadena_carac("")"
            elif (self.tipo == "Bool"):
                codigo += f"{(' ')*n}self.{self.nombre} = Booleano()"
            elif (self.tipo == "IO"):
                codigo += f"{(' ')*n}self.{self.nombre} = None"
            else:
                codigo += f"{(' ')*n}self.{self.nombre} = None"
        elif (self.tipo == "Int" or self.tipo == "String" or self.tipo == "Bool" or self.tipo == "IO"):
            codigo += f"{self.cuerpo.genera_codigo(n+2)}\n"
            codigo += f"{(' ')*(n+2)}{self.nombre} = temp"
        else:
            codigo += f"{(' ')*(n+2)}{self.nombre} = {self.tipo}()"
            
            

        return codigo