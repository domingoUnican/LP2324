# coding: utf-8
from dataclasses import dataclass, field
from typing import List
import pdb


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

    def Tipo(self,ambito):
        if self.nombre_variable == 'self':
            raise Exception("{}: '{}' cannot be the name of a formal parameter.\nCompilation halted due to static semantic errors.".format(self.linea,self.nombre_variable))


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

    def Tipo(self,ambito):
        self.cuerpo.Tipo(ambito)
        self.cast = self.cuerpo.cast
        if self.nombre == 'self':
            raise Exception("{}: Cannot assign to '{}'.\nCompilation halted due to static semantic errors.".format(self.linea,self.nombre))


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

    def Tipo(self,ambito):
        self.cuerpo.Tipo(ambito)
        argumentos = ambito.devuelve_tipo_metodo(self.nombre_metodo, self.clase)
        for arg, arg1 in zip(argumentos,self.argumentos):
            arg1.Tipo(ambito)
        self.cast = argumentos[-1]


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

    def Tipo(self,ambito):
        self.cuerpo.Tipo(ambito) ################################################################################################################################# NEG 2
        argumentos = ambito.devuelve_tipo_metodo(self.nombre_metodo, self.cuerpo.cast)
        for arg in self.argumentos:
            arg.Tipo(ambito)
        for arg, arg1 in zip(argumentos,self.argumentos):
            arg1.Tipo(ambito)
        self.cast = argumentos[-1]

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

    def Tipo(self,ambito):
        self.verdadero.Tipo(ambito)
        self.falso.Tipo(ambito)
        if self.condicion:
            self.cast = self.verdadero.cast
        else:
            self.cast = self.falso.cast


@dataclass
class Bucle(Expresion):
    condicion: Expresion = None
    cuerpo: Expresion = None  # Esto no debería ser un bloque ¿?

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        self.cuerpo.Tipo(ambito) 
        self.cast = self.cuerpo.cast

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

    def Tipo(self,ambito):
        self.cuerpo.Tipo(ambito)
        self.inicializacion.Tipo(ambito)
        self.cast = self.cuerpo.cast


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

    def Tipo(self,ambito):
        for i in self.expresiones:
            i.Tipo(ambito)
        self.cast = self.expresiones[-1].cast


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

    def Tipo(self,ambito):
        ambito.tipo_variable(self.nombre_variable,self.tipo)
        self.cuerpo.Tipo(ambito)
        self.cast = self.cuerpo.cast


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

    def Tipo(self,ambito):
        self.expr.Tipo(ambito)
        self.casos[0].Tipo(ambito)
        self.casos[1].Tipo(ambito)
        
        min_padre = ambito.minimo_ancestro(self.casos[0].cast,self.casos[1].cast)
        for i in range(2,len(self.casos)):
            self.casos[i].Tipo(ambito)
            min_padre = ambito.minimo_ancestro(min_padre,self.casos[i].cast)
        self.cast = min_padre.nombre
        

@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        self.cast = self.tipo


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
    
    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast == 'Int' and self.derecha.cast == 'Int'):
            self.cast='Int'
            return ''
        else:
            self.cast='Object'
            raise Exception(f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')

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

    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast == 'Int' and self.derecha.cast == 'Int'):
            self.cast='Int'
            return ''
        else:
            self.cast='Object'
            raise Exception(f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')


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

    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast == 'Int' and self.derecha.cast == 'Int'):
            self.cast='Int'
        else:
            self.cast='Object'
            raise Exception(f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')


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

    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast == 'Int' and self.derecha.cast == 'Int'):
            self.cast='Int'
        else:
            self.cast='Object'
            raise Exception(f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')

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

    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast in ["Int","String","Bool"] and self.derecha.cast == self.izquierda.cast):
            self.cast='Bool'
        elif (self.izquierda.cast not in ["Int","String","Bool"] and self.derecha.cast not in ["Int","String","Bool"]):
            self.cast='Bool'
        else:
            self.cast='Object'
            return 'Error de tipos'

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

    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast in ["Int","String","Bool"] and self.derecha.cast == self.izquierda.cast):
            self.cast='Bool'
        elif (self.izquierda.cast not in ["Int","String","Bool"] and self.derecha.cast not in ["Int","String","Bool"]):
            self.cast='Bool'
        else:
            self.cast='Object'
            return 'Error de tipos'


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

    def Tipo(self,ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if(self.izquierda.cast in ["Int","String","Bool"] and self.derecha.cast == self.izquierda.cast):
            self.cast='Bool'
        elif (self.izquierda.cast not in ["Int","String","Bool"] and self.derecha.cast not in ["Int","String","Bool"]):
            self.cast='Bool'
        else:
            self.cast='Object'
            return 'Error de tipos'



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

    def Tipo(self,ambito):
        self.expr.Tipo(ambito) ########################################################################################################## NEG 1
        
        if(self.expr.cast == 'Int'):
            self.cast='Int'
        else:
            self.cast='Object'
            return 'Error de tipos'

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

    def Tipo(self,ambito):
        self.expr.Tipo(ambito)
        if(self.expr.cast == 'Bool'):
            self.cast='Bool'
        else:
            self.cast='Object'
            return 'Error de tipos'

@dataclass
class EsNulo(Expresion):
    expr: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        self.expr.Tipo(ambito)
        self.cast = self.expr.cast    


@dataclass
class Objeto(Expresion):
    nombre: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        ################################################################################################################### NEG 3

        if self.nombre == "self":
            self.cast="SELF_TYPE"
        else:
            self.cast=ambito.get_tipo_variable(self.nombre)


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        self.cast='_no_type'


@dataclass
class Entero(Expresion):
    valor: int = 0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def Tipo(self,ambito):
        self.cast='Int'

@dataclass
class String(Expresion):
    valor: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        self.cast= 'String'
        return ""  # Retorna vacío para devolver siempre algo


@dataclass
class Booleano(Expresion):
    valor: bool = False
    
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def Tipo(self,ambito):
        self.cast = 'Bool'

@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado

    def Tipo(self):
        nombres = []
        ambito = Ambito([], {}, {})
        e_main = False
        for clase in self.secuencia:
            if clase.nombre in nombres:
                raise Exception(str(clase.linea+1) + ':' + " Class " + clase.nombre + " was previously defined.\nCompilation halted due to static semantic errors.")
            else:
                nombres.append(clase.nombre)
            if clase.nombre == 'SELF_TYPE':
                raise Exception(str(clase.linea+3) + ': ' + "Redefinition of basic class " + clase.nombre + '.\n' + "Compilation halted due to static semantic errors.")
            elif clase.nombre == 'Int':
                raise Exception(str(clase.linea+1) + ': ' + "Redefinition of basic class " + clase.nombre + '.\n' + "Compilation halted due to static semantic errors.")
            if clase.nombre == 'Main':
                for carac in clase.caracteristicas:
                    if carac.nombre == 'main':
                        e_main = True
            clase.Tipo(ambito)
        for clase in self.secuencia:
            for caracteristica in clase.caracteristicas:
                if isinstance(caracteristica,Metodo):
                    ambito.meter_funcion(clase.nombre,caracteristica.nombre,[[x.nombre_variable,x.tipo] for x in caracteristica.formales],caracteristica.tipo)# Hay que meter los parametros que sean
        # ERRORES
        for clase in self.secuencia:

            for caracteristica in clase.caracteristicas:
                if caracteristica.tipo not in ["Int", "Bool", "String", "SELF_TYPE", "Object"] and caracteristica.tipo not in ambito.variables.values():
                        raise Exception(str(self.linea+2) +":"+ " Undefined return type " + caracteristica.tipo + " in method main." + "\n" + "returntypenoexist.test:" +
                                        str(self.linea+2) +":"+ " 'new' used with undefined class " + caracteristica.tipo + ".\nCompilation halted due to static semantic errors.")
                if isinstance(caracteristica,Metodo) and not ambito.es_subtipo(caracteristica.tipo,caracteristica.cuerpo.cast) and not ambito.es_subtipo(caracteristica.cuerpo.cast,caracteristica.tipo):
                    raise Exception(str(self.linea+4) + ':' + " Incompatible number of formal parameters in redefined method " + caracteristica.nombre + ".\nCompilation halted due to static semantic errors.")
    
        if e_main == False:
            raise Exception("Class Main is not defined.\nCompilation halted due to static semantic errors.")

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

    def Tipo(self,ambito):
        if self.nombre not in ambito.clases:
            ambito.meter_clase(self)
        self.cast = 'Object'
        ambito.tipo_variable('self',self.nombre)
        for caracteristica in self.caracteristicas:
            if isinstance(caracteristica,Atributo):
                caracteristica.Tipo(ambito)
                ambito.tipo_variable(caracteristica.nombre,caracteristica.tipo)
            else:
                # Hace falta meter los metodos aquí llamando al nuevo metodo que hay abajo
                caracteristica.Tipo(ambito)
                ambito.meter_funcion(self.nombre,caracteristica.nombre,[[x.nombre_variable,x.tipo] for x in caracteristica.formales],caracteristica.tipo)# Hay que meter los parametros que sean
        """for caracteristica in self.caracteristicas:
            if caracteristica.tipo not in ["Int", "Bool", "String", "SELF_TYPE", "Object"] and caracteristica.tipo not in ambito.variables.values():
                    raise Exception(str(self.linea+1) +":"+ " Undefined return type " + caracteristica.tipo + " in method main." + "\n" + "returntypenoexist.test:" +
                                    str(self.linea+1) +":"+ " 'new' used with undefined class " + caracteristica.tipo + ".\nCompilation halted due to static semantic errors.")"""
        for caracteristica in self.caracteristicas:
            caracteristica.Tipo(ambito)
            

@dataclass
class Metodo(Caracteristica):
    formales: List[Formal] = field(default_factory=list)

    def Tipo(self,ambito):
        for formal in self.formales:
            formal.Tipo(ambito)
        self.cuerpo.Tipo(ambito)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)

        return resultado


class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado

    def Tipo(self,ambito):
        self.cast = 'Object'
        self.cuerpo.Tipo(ambito)
        reserved_names = ['self']
        if self.nombre in reserved_names:
            raise Exception("{}: '{}' cannot be the name of an attribute.\nCompilation halted due to static semantic errors.".format(self.linea,self.nombre))

class Arbol:
    def __init__(self, nombre, padre, funciones, hijos):
        self.nombre = nombre
        self.padre = padre
        self.funciones = funciones
        self.hijos = hijos

    def meter_funcion(self, nombre_funcion, parametro_formales, retorno):
        self.funciones[nombre_funcion] = [parametro_formales,retorno]
    

class Ambito:
    def __init__(self, arbol, metodos, variables):
        self.metodos = metodos
        self.variables = variables
        self.clases = ["Object",'Int','IO','String']
        raiz = Arbol('Object','', {'abort':[[[]],'Object'],
                                'typename': [[[]], 'String'],
                                  'copy': [[[]], 'SELF_TYPE'],
                                   'self': [[[]], 'SELF_TYPE']}
                     , [] #Añadir hijos
                     )
        integer = Arbol('Int','Object',{'new':[[[]],'Int']},[]) #(Int no tiene metodos)
        io = Arbol('IO','Object', {'out_string':[[['x','String']],'SELF_TYPE'],'out_int':[[['x','Int']],'SELF_TYPE'],'in_string':[[[]],'String'],'in_int':[[[]],'Int']},[])
        string = Arbol('String','Object',{'length':[[[]],'Int'],'concat':[[['s','String']],'String'],'substr':[[['i','Int'],['l','Int']],'String']},[])
      
        boolean = Arbol('Bool','Object',{'new':[[[]],'Bool']},[]) #(Bool no tiene metodos) default = false
        """raiz.meter_funcion('abort', [], 'Object')
        raiz.meter_funcion('typename', [], 'String')
        raiz.meter_funcion('copy', [], 'SELF_TYPE')"""
        raiz.hijos.append(integer)
        raiz.hijos.append(boolean)
        raiz.hijos.append(io)
        raiz.hijos.append(string)
        self.Arbol = raiz

    def clase_tiene_metodo_x(self, hijo_clase, nombre_metodo):
        if isinstance(hijo_clase,str):
            hijo_clase = self.get_nodo(hijo_clase)

        if nombre_metodo in hijo_clase.funciones:

            return hijo_clase.funciones[nombre_metodo] ## Devuelve una lista de los tipos de los argumentos y del return
        else:
            #if self.get_nodo(hijo_clase) is not False:
            #    if self.get_nodo(hijo_clase).padre:

            if hijo_clase.padre:

                return self.clase_tiene_metodo_x(hijo_clase.padre, nombre_metodo)
            else:

                return False
    
    def devuelve_tipo_metodo(self,nombre_metodo,cast):

        nodo_temp = self.Arbol
        l = [nodo_temp]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == cast:
                break
            l.extend(nodo_temp.hijos)


        metodos = self.clase_tiene_metodo_x(nodo_temp, nombre_metodo)
        if metodos is not False:

            """nodo = self.Arbol
            l = [nodo]
            while l:
                nodo_temp = l.pop()
                if nodo_temp.nombre == cast:
                    break
                l.extend(nodo_temp.hijos)"""
            if nombre_metodo is not 'self' and metodos[-1] == "SELF_TYPE":
                metodos = [metodos[:-1],cast]
            return metodos
        else:
            return False


    def es_subtipo(self,claseA,claseB):
        if claseA == claseB:
            return True
        elif claseB == "Object":
            return claseA == claseB
        else:
            return self.es_subtipo(self.padreada(claseB),claseA)

    def padreada(self,nombreN):
      nodo = self.Arbol
      l = [nodo]
      while l:
        nodo_temp = l.pop()
        if nodo_temp.nombre == nombreN:
          return nodo_temp.padre
        else:
          l.extend(nodo_temp.hijos)
      return "ERROR"

    def minimo_ancestro(self,nodoA,nodoB):
        if isinstance(nodoA,str):
            nodoA = self.get_nodo(nodoA)
        if isinstance(nodoB,str):
            nodoB = self.get_nodo(nodoB)
        if nodoA is nodoB:
            return nodoA
        elif nodoB is nodoA.padre:
            return nodoB
        elif nodoA is nodoB.padre:
            return nodoA
        else:
            if self.profundidad(nodoA) >= self.profundidad(nodoB) and nodoA.padre != '':
                nodoA = nodoA.padre
            else:
                nodoB = nodoB.padre
            return self.minimo_ancestro(nodoA,nodoB)

    def profundidad(self,nodo):
        if (self.Arbol == nodo):
            return 0
        else:
            return 1+self.profundidad(self.get_nodo(nodo.padre))

    def nodoArbol(self,nombreN):
      nodo = self.Arbol
      l = [nodo]
      while l:
        nodo_temp = l.pop()
        if nodo_temp.nombre == nombreN:
          return nodo_temp
        else:
          l.extend(nodo_temp.hijos)
      return self.Arbol

    def tipo_variable(self,nombre,tipo):
        self.variables[nombre] = tipo

    def get_tipo_variable(self,nombre):
        return self.variables[nombre]

    def meter_funcion(self, nombre_clase, nombre_funcion, parametro_formales, retorno):
        # Hay que enganchar la funcion al arbol que se define arriba en el __init__ de ambito
        # No se donde se engancha lol
        # Pero es como el diccionario este que hay encima. Ejemplo: string = Arbol('String','Object',{'length':[[[]],'Int'],'concat':[[['s','String']],'String'],'substr':[[['i','Int'],['l','Int']],'String']},[])
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombre_clase:
                break
            l.extend(nodo_temp.hijos)

        nodo_temp.meter_funcion(nombre_funcion, parametro_formales, retorno)

    def existe_clase(self,nombreN):
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombreN:
              return True
            else:
              l.extend(nodo_temp.hijos)
        return False

    def get_nodo(self,nombre_nodo):
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombre_nodo:
              return nodo_temp
            else:
              l.extend(nodo_temp.hijos)
        return False

    def mostrar_arbol(self): # metodo de debug
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            l.extend(nodo_temp.hijos)
        return False

    def meter_clase(self,clase):
        self.clases.append(clase)
        nodoPadre = self.get_nodo(clase.padre)
        nodoPadre.hijos.append(Arbol(clase.nombre,clase.padre,{},[]))
