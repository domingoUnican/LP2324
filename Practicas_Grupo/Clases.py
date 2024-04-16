# coding: utf-8
from dataclasses import dataclass, field
from typing import List
import Base_clases



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
        return f"{' '*n}{self.nombre}={self.cuerpo.genera_codigo(0)}"



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
        codigo = ""
        codigo += f"{' '*n}temp = self.{self.nombre_metodo}("
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
        codigo = ""
        codigo += f"{' '*n}{self.cuerpo.genera_codigo(0)}.{self.nombre_metodo}("
        for formal in self.argumentos[:-1]:
            codigo += formal.genera_codigo(0) + ","
        if self.argumentos:
            codigo += self.argumentos[-1].genera_codigo(0) 
        codigo +=")"
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
        codigo += f"{self.falso.genera_codigo(n+2)}"
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
        if (self.tipo == 'Booleano' and self.inicializacion == NoExpr()):
            self.inicializacion = Booleano()
        elif (self.tipo == 'Entero' and self.inicializacion == NoExpr()):
            self.inicializacion = Entero()
        elif (self.tipo == 'String' and self.inicializacion == NoExpr()):
            self.inicializacion = String(s="")
        
        codigo += self.nombre + "=" + self.inicializacion.genera_codigo(0) + "\n"
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
        return Condicional(condicion=self.expr, verdadero=self.casos[0], falso=False).genera_codigo(n)
        

@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado


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
        codigo+= f"{' '*n}temporal = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = temporal + temp \n"
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
        codigo+= f"{' '*n}temporal = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = temporal - temp \n"
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
        codigo+= f"{' '*n}temporal = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = temporal * temp \n"
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
        codigo+= f"{' '*n}temporal = temp \n"
        codigo+= self.derecha.genera_codigo(n) + "\n"
        codigo+= f"{' '*n}temp = temporal / temp \n"
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
        return f"{' '*n}not{self.expr}"

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
        return f"{' '*n}not{self.expr}"
        
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
        """if self.nombre == "self":
            return f"{' '*n}temp = {self.nombre}"""
        return f"{' '*n}temp = self.{self.nombre}"


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
class String(Expresion):
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
        for caracteristica in self.caracteristicas:
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
        codigo += f"{' '*n}def {self.nombre}(self"
        for formal in self.formales[:-1]:
            codigo += formal.genera_codigo(0) + ","
        if self.formales:
            codigo += self.formales[-1].genera_codigo(0) 
        codigo +="):\n"
        codigo +=self.cuerpo.genera_codigo(n+2)
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
        """if isinstance (self.cuerpo, NoExpr):
            #return f"{' '*n}{self.nombre}=0\n"
            if self.tipo == 'Int':
                return f"{' '*n}{self.nombre}={Entero().genera_codigo(0)}\n"
            elif self.tipo == 'String':
                return f"{' '*n}{self.nombre}={String(valor='').genera_codigo(0)}\n"
            elif self.tipo == 'Bool':
                return f"{' '*n}{self.nombre}={Booleano().genera_codigo(0)}\n"
            elif self.tipo == 'IO':
                return f"{' '*n}{self.nombre}={Base_clases.IO().out_string(None)}\n"""
        #else:
        return f"{' '*n}{self.nombre}={self.tipo}({self.cuerpo.genera_codigo(n)})\n"