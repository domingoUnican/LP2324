# coding: utf-8
import collections
import keyword
import textwrap
from dataclasses import dataclass, field
from typing import List, Optional
from Base_clases import CoolBootstrapReservedNames 
import pdb


@dataclass
class Nodo:
    MAX_GEN_DEPTH = 150
    INDENT_STEP = '    '

    linea: int = 0

    def str(self, n):
        return f'{n * " "}#{self.linea}\n'

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        raise NotImplementedError()

    def Tipo(self, ambito):
        raise NotImplementedError()

    def traduce_tipo(self, tipo: str, var: bool = False, hint: bool = False):
        if tipo == 'SELF_TYPE':
            if Clase._last_generated_class is None:
                raise CodeGenError("Cannot reference SELF_TYPE outside of a class.")
            tipo = Clase._last_generated_class
        if var:
            tipo = f"Par['{tipo}']" if hint else f"Par[{tipo}]"
        elif hint:
            tipo = f"'{tipo}'"
        return tipo

    def traduce_nombre(self, nombre: str):
        strip = nombre.rstrip('_')
        if keyword.iskeyword(strip) or keyword.issoftkeyword(strip) or strip in CoolBootstrapReservedNames:
            return nombre + '_'
        return nombre


@dataclass
class Formal(Nodo):
    nombre_variable: str = '_no_set'
    tipo: str = '_no_type'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_formal\n'
        resultado += f'{(n + 2) * " "}{self.nombre_variable}\n'
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        return resultado

    def Tipo(self, ambito):
        if self.nombre_variable == 'self':
            raise Exception(
                "{}: '{}' cannot be the name of a formal parameter.\nCompilation halted due to static semantic errors.".format(
                    self.linea, self.nombre_variable))

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        return f"{self.traduce_nombre(self.nombre_variable)}: {self.traduce_tipo(self.tipo, var=True, hint=True)}"


class ExpresionCodeGenContext:
    def __init__(self, indent: str = '', depth: int = 0):
        self.indent = indent
        self.depth = depth
        self.free_variable_counter: dict[str, int] = collections.defaultdict(lambda: 1)
        self.initializations: list[str] = []
        self.names = {'self'}
        self.inlined_names: dict[str, str] = {}

    def free_variable_name(self, prefix: str = '_'):
        n = f'{prefix}{self.free_variable_counter[prefix]}'
        self.free_variable_counter[prefix] += 1
        return n

    def add_unique_name(self, name: str):
        nm = name
        c = 1
        while nm in self.names or nm in self.inlined_names:
            nm = name + f'_{c}'
            c += 1
        if c != 1:
            self.inlined_names[name] = nm
        else:
            self.names.add(nm)
        return nm

    def add_initialization(self, init: str):
        self.initializations.append(init)

    def add_var_name(self, name: str):
        self.inlined_names[name] = f"{name}[:]"

    def remove_var_name(self, name: str):
        if name in self.inlined_names:
            del self.inlined_names[name]

    def add_name(self, name: str):
        self.names.add(name)

    def remove_name(self, name: str):
        self.names.remove(name)

    def add_inlined_name(self, name: str, value: str):
        self.inlined_names[name] = value

    def remove_inlined_name(self, name: str):
        if name in self.inlined_names:
            del self.inlined_names[name]

    def initialization(self) -> str:
        return ''.join(f"{i}\n" for i in self.initializations)

    def sub_context(self, indent: Optional[str] = None, depth: Optional[int] = None) -> 'ExpresionCodeGenContext':
        if indent is None:
            indent = self.indent
        if depth is None:
            depth = self.depth
        sub = ExpresionCodeGenContext(indent, depth)
        sub.names |= self.names
        sub.inlined_names |= self.inlined_names
        # For clarity, it's better if all sub_expressions have the same variable counter
        sub.free_variable_counter = self.free_variable_counter
        return sub

class Expresion(Nodo):
    cast: str = '_no_type'

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        pass


@dataclass
class Asignacion(Expresion):
    nombre: str = '_no_set'
    cuerpo: Expresion = None

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        if context is None:
            raise CodeGenError("Cannot generate assignment without context.")
        nm = context.free_variable_name('_var')
        name = Objeto(self.linea, self.nombre).genera_codigo(indent, context.depth, context)
        s = f"{context.indent}{name} = {nm} = {self.cuerpo.genera_codigo(indent, context.depth, context)}"
        context.add_initialization(s)
        return f"{nm}"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_assign\n'
        resultado += f'{(n + 2) * " "}{self.nombre}\n'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cuerpo.Tipo(ambito)
        self.cast = self.cuerpo.cast
        if self.nombre == 'self':
            raise Exception(
                "{}: Cannot assign to '{}'.\nCompilation halted due to static semantic errors.".format(self.linea,
                                                                                                       self.nombre))


@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion = None
    clase: str = '_no_type'
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return (f"{self.clase}.{self.traduce_nombre(self.nombre_metodo)}("
                f"{self.cuerpo.genera_codigo(indent, depth+1, context)}, " +
                ', '.join(a.genera_codigo(indent, depth+1, context) for a in self.argumentos) + ')')

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_static_dispatch\n'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n + 2) * " "}{self.clase}\n'
        resultado += f'{(n + 2) * " "}{self.nombre_metodo}\n'
        resultado += f'{(n + 2) * " "}(\n'
        resultado += ''.join([c.str(n + 2) for c in self.argumentos])
        resultado += f'{(n + 2) * " "})\n'
        resultado += f'{n * " "}: _no_type\n'
        return resultado

    def Tipo(self, ambito):
        self.cuerpo.Tipo(ambito)
        argumentos = ambito.devuelve_tipo_metodo(self.nombre_metodo, self.clase)
        for arg, arg1 in zip(argumentos, self.argumentos):
            arg1.Tipo(ambito)
        self.cast = argumentos[-1]


@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion = None
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def _par(self, what: str, par: bool = True):
        if par:
            return f"({what})"
        return what

    def _should_par(self, nodo: Nodo):
        return all(not isinstance(nodo, what) for what in (
            Objeto, LlamadaMetodo, LlamadaMetodoEstatico, Entero, Booleano, String
        ))

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return (f'{self._par(self.cuerpo.genera_codigo(indent, depth+1, context), self._should_par(self.cuerpo))}.' +
                f'{self.traduce_nombre(self.nombre_metodo)}(' +
                ', '.join(a.genera_codigo(indent, depth+1, context) for a in self.argumentos) + ')')

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_dispatch\n'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{(n + 2) * " "}{self.nombre_metodo}\n'
        resultado += f'{(n + 2) * " "}(\n'
        resultado += ''.join([c.str(n + 2) for c in self.argumentos])
        resultado += f'{(n + 2) * " "})\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cuerpo.Tipo(ambito)  ################################################################################################################################# NEG 2
        argumentos = ambito.devuelve_tipo_metodo(self.nombre_metodo, self.cuerpo.cast)
        for arg in self.argumentos:
            arg.Tipo(ambito)
        for arg, arg1 in zip(argumentos, self.argumentos):
            arg1.Tipo(ambito)
        self.cast = argumentos[-1]


@dataclass
class Condicional(Expresion):
    condicion: Expresion = None
    verdadero: Expresion = None
    falso: Expresion = None

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return (f"({self.verdadero.genera_codigo(indent, depth+1, context)} if "
                f"{self.condicion.genera_codigo(indent, depth+1, context)} else "
                f"{self.falso.genera_codigo(indent, depth+1, context).lstrip()})")

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_cond\n'
        resultado += self.condicion.str(n + 2)
        resultado += self.verdadero.str(n + 2)
        resultado += self.falso.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
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

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        if context is None:
            raise CodeGenError("Cannot generate loops without context.")
        ctx = context.sub_context(indent)
        cond_name = ctx.free_variable_name('_cond')
        result_name = ctx.free_variable_name('_loop')
        cond = self.condicion.genera_codigo(ctx.indent, ctx.depth, ctx)
        init = f"{ctx.initialization()}"
        if init:
            init += f"{cond_name} = {cond}\n"
            cond = cond_name
        s = f"{init}{ctx.indent}{result_name} = Void\n"
        s += f"{ctx.indent}while {cond}:\n"
        wi = ctx.indent + Nodo.INDENT_STEP
        sub_ctx = context.sub_context(wi)
        gen = self.cuerpo.genera_codigo(wi, sub_ctx.depth, sub_ctx)
        s += sub_ctx.initialization()
        s += f"{wi}{result_name} = {gen.lstrip()}"
        if init:
            cond_update_ctx = context.sub_context(wi)
            cond_update = self.condicion.genera_codigo(wi, cond_update_ctx.depth, cond_update_ctx)
            s += f"{cond_update_ctx.initialization()}"
            s += f"{wi}{cond_name} = {cond_update.lstrip()}"
        context.add_initialization(s)
        return 'Void'  # while loops are meant to return nothing
        # return f"{result_name}"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_loop\n'
        resultado += self.condicion.str(n + 2)
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cuerpo.Tipo(ambito)
        self.cast = self.cuerpo.cast


@dataclass
class MultiLet(Expresion):
    declaraciones: list['DeclaracionMultiLet'] = None
    cuerpo: Expresion = None

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        if context is None:
            raise CodeGenError("Cannot generate loops without context.")
        nm = context.free_variable_name('_let')
        s = f"{indent}@mutable_params\n"
        s += f"{indent}def {nm}(" + ', '.join(
            f"{self.traduce_nombre(d.nombre)}: {self.traduce_tipo(d.tipo, var=True)}" for d in self.declaraciones
        ) + "):\n"
        mi = indent + Nodo.INDENT_STEP
        sub_ctx = context.sub_context(mi)
        for d in self.declaraciones:
            sub_ctx.add_var_name(self.traduce_nombre(d.nombre))
        gen = self.cuerpo.genera_codigo(mi, sub_ctx.depth, sub_ctx)
        s += f"{sub_ctx.initialization()}"
        s += f"{mi}return {gen.lstrip()}\n"
        context.add_initialization(s)
        inits = []
        for d in self.declaraciones:
            sub_ctx = context.sub_context()
            if isinstance(d.inicializacion, NoExpr):
                gen = d.inicializacion.genera_codigo(sub_ctx.indent, depth + 1, sub_ctx, context_type=d.tipo)
            else:
                gen = d.inicializacion.genera_codigo(sub_ctx.indent, depth + 1, sub_ctx)
            inits.append(gen)
            context.add_initialization(sub_ctx.initialization())
        return f"{nm}({', '.join(inits)})"


    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_multi_let\n'
        resultado += self.cuerpo.str(n + 2)
        for decl in self.declaraciones:
            resultado += decl.str(n + 2)
        return resultado

    def Tipo(self, ambito):
        self.cuerpo.Tipo(ambito)
        for decl in self.declaraciones:
            decl.Tipo(ambito)
        self.cast = self.cuerpo.cast


@dataclass
class DeclaracionMultiLet(Nodo):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    inicializacion: Expresion = None


@dataclass
class Let(Expresion):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    inicializacion: Expresion = None
    cuerpo: Expresion = None

    def flatten(self):
        """
        Compacta múltiples Let consecutivos en un solo MultiLet
        """
        if isinstance(self.cuerpo, Let):
            decls: list[DeclaracionMultiLet] = []
            c = [1]
            def patch_names(new_name):
                for d in decls:
                    if d.nombre == new_name:
                        d.nombre = f'_p{c[0]}'
                        c[0] += 1
            bod = self
            while isinstance(bod, Let):
                let, bod = bod, bod.cuerpo
                patch_names(let.nombre)
                decls.append(DeclaracionMultiLet(nombre=let.nombre, tipo=let.tipo, inicializacion=let.inicializacion))
            return MultiLet(declaraciones=decls, cuerpo=bod)
        return self

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        # if isinstance(self.cuerpo, Let):
        #     return self.flatten().genera_codigo(indent, depth, context)
        if context is None:
            raise CodeGenError("Cannot generate Let statement without context")
        nm = context.free_variable_name('_let')
        nombre = self.traduce_nombre(self.nombre)
        s = f"{indent}@mutable_params\n"
        s += f"{indent}def {nm}({nombre}: {self.traduce_tipo(self.tipo, var=True)}):\n"
        mi = indent + Nodo.INDENT_STEP
        sub_ctx = context.sub_context(mi)
        sub_ctx.add_var_name(nombre)
        gen = self.cuerpo.genera_codigo(mi, 0, sub_ctx)
        s += f"{sub_ctx.initialization()}"
        s += f"{mi}return {gen}\n"
        context.add_initialization(s)
        if isinstance(self.inicializacion, NoExpr):
            gen = self.inicializacion.genera_codigo(indent, depth + 1, context, context_type=self.tipo)
        else:
            gen = self.inicializacion.genera_codigo(indent, depth+1, context)
        return f"{nm}({gen})"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_let\n'
        resultado += f'{(n + 2) * " "}{self.nombre}\n'
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.inicializacion.str(n + 2) if self.inicializacion is not None else 'None'
        resultado += self.cuerpo.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cuerpo.Tipo(ambito)
        self.inicializacion.Tipo(ambito)
        self.cast = self.cuerpo.cast


@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion] = field(default_factory=list)

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        if context is None:
            raise CodeGenError("Cannot generate block without context")
        nm = context.free_variable_name('_block')
        s = f"{indent}def {nm}():\n"
        mi = indent + Nodo.INDENT_STEP
        for i, e in enumerate(self.expresiones):
            ctx = context.sub_context(mi)
            gen = e.genera_codigo(mi, 0, ctx)
            s += ctx.initialization()
            if i == len(self.expresiones) - 1:
                s += f"{mi}return {gen.lstrip()}\n"
            else:
                s += f"{mi}{gen}\n"
        context.add_initialization(s)
        return f"{indent}{nm}()"


    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n * " "}_block\n'
        resultado += ''.join([e.str(n + 2) for e in self.expresiones])
        resultado += f'{n * " "}: {self.cast}\n'
        resultado += '\n'
        return resultado

    def Tipo(self, ambito):
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
        resultado += f'{n * " "}_branch\n'
        resultado += f'{(n + 2) * " "}{self.nombre_variable}\n'
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n + 2)
        return resultado

    def Tipo(self, ambito):
        ambito.tipo_variable(self.nombre_variable, self.tipo)
        self.cuerpo.Tipo(ambito)
        self.cast = self.cuerpo.cast


@dataclass
class Switch(Expresion):
    expr: Expresion = None
    casos: List[RamaCase] = field(default_factory=list)

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        if context is None:
            raise CodeGenError("Cannot generate switch without context!")
        matched = context.free_variable_name('_match')
        result = context.free_variable_name('_match_result')
        s = f"{indent}{matched} = check_match({self.expr.genera_codigo(indent, context.depth, context)})\n"
        # TODO: Cool's switch statement picks the closest superclass, not the first in the list that matches
        # s += f"{indent}match {matched}:\n"
        # ci = indent + Nodo.INDENT_STEP
        # ei = ci + Nodo.INDENT_STEP
        # for caso in self.casos:
        #     caso_nombre = self.traduce_nombre(caso.nombre_variable)
        #     s += f'{ci}case {self.traduce_tipo(caso.tipo)}():\n'
        #     s += f'{ei}{caso_nombre} = {matched}\n'
        #     sub_ctx = context.sub_context(ei)
        #     sub_ctx.add_name(caso_nombre)
        #     gen = caso.cuerpo.genera_codigo(ei, sub_ctx.depth, sub_ctx)
        #     s += f'{sub_ctx.initialization()}'
        #     s += f'{ei}{result} = {gen}\n'
        # s += f'{ci}case _:\n'
        # s += f'{ei}{result} = Void'
        if_kw = 'if'
        ni = indent + Nodo.INDENT_STEP
        for caso in self.casos:
            caso_nombre = self.traduce_nombre(caso.nombre_variable)
            sub_ctx = context.sub_context(ni)
            caso_nombre = sub_ctx.add_unique_name(caso_nombre)
            s += f'{indent}{if_kw} isinstance({matched}, {self.traduce_tipo(caso.tipo)}):\n'
            s += f'{ni}{caso_nombre} = {matched}\n'
            gen = caso.cuerpo.genera_codigo(ni, sub_ctx.depth, sub_ctx)
            s += f'{sub_ctx.initialization()}'
            s += f'{ni}{result} = {gen}\n'
            if_kw = 'elif'
        if self.casos:
            s += f'{indent}else:\n'
        else:
            ni = indent
        s += f'{ni}{result} = Void'
        context.add_initialization(s)
        return f"{result}"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_typcase\n'
        resultado += self.expr.str(n + 2)
        resultado += ''.join([c.str(n + 2) for c in self.casos])
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.expr.Tipo(ambito)
        self.casos[0].Tipo(ambito)
        self.casos[1].Tipo(ambito)

        min_padre = ambito.minimo_ancestro(self.casos[0].cast, self.casos[1].cast)
        for i in range(2, len(self.casos)):
            self.casos[i].Tipo(ambito)
            min_padre = ambito.minimo_ancestro(min_padre, self.casos[i].cast)
        self.cast = min_padre.nombre


@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return f"{self.traduce_tipo(self.tipo)}()"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_new\n'
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cast = self.tipo


@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion = None
    derecha: Expresion = None

    operando = NotImplemented
    def genera_operando(self) -> str:
        if self.operando == NotImplemented:
            raise NotImplementedError()
        return self.operando

    def genera_prefijo(self) -> Optional[str]:
        return None

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        if depth > Nodo.MAX_GEN_DEPTH:
            if context is None:
                raise CodeGenError("Expression is too deep to be generated without context!")
            nm = context.free_variable_name('_bin')
            s = f"{context.indent}{nm} = {self.genera_codigo(indent, context.depth, context)}\n"
            context.add_initialization(s)
            return f"{nm}"
        pre = self.genera_prefijo()
        if pre is None:
            pre = ''
        return (f"{pre}({self.izquierda.genera_codigo(indent, depth+1, context)} {self.genera_operando()} "
                f"{self.derecha.genera_codigo(indent, depth+1, context)})")


@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_plus\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast == 'Int' and self.derecha.cast == 'Int':
            self.cast = 'Int'
            return ''
        else:
            self.cast = 'Object'
            raise Exception(
                f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')


@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_sub\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast == 'Int' and self.derecha.cast == 'Int':
            self.cast = 'Int'
            return ''
        else:
            self.cast = 'Object'
            raise Exception(
                f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')


@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_mul\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast == 'Int' and self.derecha.cast == 'Int':
            self.cast = 'Int'
        else:
            self.cast = 'Object'
            raise Exception(
                f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')


@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_divide\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast == 'Int' and self.derecha.cast == 'Int':
            self.cast = 'Int'
        else:
            self.cast = 'Object'
            raise Exception(
                f'{self.linea}: non-Int arguments: {self.izquierda.cast} + {self.derecha.cast} \n Compilation halted due to static semantic errors.')


@dataclass
class Menor(OperacionBinaria):
    operando: str = '<'

    def genera_prefijo(self) -> Optional[str]:
        return 'Bool'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_lt\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast in ["Int", "String", "Bool"] and self.derecha.cast == self.izquierda.cast:
            self.cast = 'Bool'
        elif (self.izquierda.cast not in ["Int", "String", "Bool"] and self.derecha.cast not in ["Int", "String",
                                                                                                 "Bool"]):
            self.cast = 'Bool'
        else:
            self.cast = 'Object'
            return 'Error de tipos'


@dataclass
class LeIgual(OperacionBinaria):
    operando: str = '<='

    def genera_prefijo(self) -> Optional[str]:
        return 'Bool'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_leq\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast in ["Int", "String", "Bool"] and self.derecha.cast == self.izquierda.cast:
            self.cast = 'Bool'
        elif (self.izquierda.cast not in ["Int", "String", "Bool"] and self.derecha.cast not in ["Int", "String",
                                                                                                 "Bool"]):
            self.cast = 'Bool'
        else:
            self.cast = 'Object'
            return 'Error de tipos'


@dataclass
class Igual(OperacionBinaria):
    operando: str = '='

    def genera_operando(self) -> str:
        return '=='

    def genera_prefijo(self) -> Optional[str]:
        return 'Bool'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_eq\n'
        resultado += self.izquierda.str(n + 2)
        resultado += self.derecha.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.izquierda.Tipo(ambito)
        self.derecha.Tipo(ambito)
        if self.izquierda.cast in ["Int", "String", "Bool"] and self.derecha.cast == self.izquierda.cast:
            self.cast = 'Bool'
        elif (self.izquierda.cast not in ["Int", "String", "Bool"] and self.derecha.cast not in ["Int", "String",
                                                                                                 "Bool"]):
            self.cast = 'Bool'
        else:
            self.cast = 'Object'
            return 'Error de tipos'


@dataclass
class Neg(Expresion):
    expr: Expresion = None
    operador: str = '~'

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return f'~({self.expr.genera_codigo(indent, depth+1, context)})'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_neg\n'
        resultado += self.expr.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.expr.Tipo(
            ambito)  ########################################################################################################## NEG 1

        if self.expr.cast == 'Int':
            self.cast = 'Int'
        else:
            self.cast = 'Object'
            return 'Error de tipos'


@dataclass
class Not(Expresion):
    expr: Expresion = None
    operador: str = 'NOT'

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return '(' + self.expr.genera_codigo(indent, depth+1, context) + ').not_()'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_comp\n'
        resultado += self.expr.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.expr.Tipo(ambito)
        if self.expr.cast == 'Bool':
            self.cast = 'Bool'
        else:
            self.cast = 'Object'
            return 'Error de tipos'


@dataclass
class EsNulo(Expresion):
    expr: Expresion = None

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return f'Bool({self.expr.genera_codigo(indent, depth+1, context)} is Void)'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_isvoid\n'
        resultado += self.expr.str(n + 2)
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.expr.Tipo(ambito)
        self.cast = self.expr.cast


@dataclass
class Objeto(Expresion):
    nombre: str = '_no_set'

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        name = self.traduce_nombre(self.nombre)
        if name.startswith('_'):
            raise CodeGenError("Cannot generate reserved name")
        if name in context.inlined_names:
            return context.inlined_names[name]
        if name in context.names:
            return name
        return f"self.{name}"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_object\n'
        resultado += f'{(n + 2) * " "}{self.nombre}\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        ################################################################################################################### NEG 3

        if self.nombre == "self":
            self.cast = "SELF_TYPE"
        else:
            self.cast = ambito.get_tipo_variable(self.nombre)


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def genera_codigo(self, indent: str = '', depth: int = 0,
                      context: Optional[ExpresionCodeGenContext] = None,
                      context_type: Optional[str] = None) -> str:
        if context_type == 'Int':
            return Entero(self.linea).genera_codigo(indent, depth, context)
        elif context_type == 'Bool':
            return Booleano(self.linea).genera_codigo(indent, depth, context)
        elif context_type == 'String':
            return String(self.linea, '').genera_codigo(indent, depth, context)
        return 'Void'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_no_expr\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cast = '_no_type'


@dataclass
class Entero(Expresion):
    valor: int = 0

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return f"Int({str(self.valor)})"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_int\n'
        resultado += f'{(n + 2) * " "}{self.valor}\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cast = 'Int'


@dataclass
class String(Expresion):
    valor: str = '_no_set'

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return f"String({self.valor})"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_string\n'
        resultado += f'{(n + 2) * " "}{self.valor}\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cast = 'String'
        return ""  # Retorna vacío para devolver siempre algo


@dataclass
class Booleano(Expresion):
    valor: bool = False

    def genera_codigo(self, indent: str = '', depth: int = 0, context: Optional[ExpresionCodeGenContext] = None) -> str:
        return "true" if self.valor else "false"

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_bool\n'
        resultado += f'{(n + 2) * " "}{1 if self.valor else 0}\n'
        resultado += f'{n * " "}: {self.cast}\n'
        return resultado

    def Tipo(self, ambito):
        self.cast = 'Bool'


@dataclass
class IterableNodo(Nodo):
    secuencia: list[Nodo] = field(default_factory=list)

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        return '\n'.join(n.genera_codigo(indent, depth) for n in self.secuencia)


class Programa(IterableNodo):
    bootstrap = textwrap.dedent("""
        from Base_clases import *
    """).lstrip()
    footer = textwrap.dedent("""
        if __name__ == '__main__':
            bootstrap(Main)
    """).lstrip()

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        assert indent == ''
        return Programa.bootstrap + '\n\n' + super().genera_codigo(indent, depth) + '\n' + Programa.footer

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" " * n}_program\n'
        resultado += ''.join([c.str(n + 2) for c in self.secuencia])
        return resultado

    def Tipo(self, ambito: None = None):
        if ambito is not None:
            raise ValueError("Received unsupported parameter!")
        nombres = []
        ambito = Ambito([], {}, {})
        e_main = False
        for clase in self.secuencia:
            assert isinstance(clase, Clase)
            if clase.nombre in nombres:
                raise Exception(
                    str(clase.linea + 1) + ':' + " Class " + clase.nombre + " was previously defined.\nCompilation halted due to static semantic errors.")
            else:
                nombres.append(clase.nombre)
            if clase.nombre == 'SELF_TYPE':
                raise Exception(
                    str(clase.linea + 3) + ': ' + "Redefinition of basic class " + clase.nombre + '.\n' + "Compilation halted due to static semantic errors.")
            elif clase.nombre == 'Int':
                raise Exception(
                    str(clase.linea + 1) + ': ' + "Redefinition of basic class " + clase.nombre + '.\n' + "Compilation halted due to static semantic errors.")
            if clase.nombre == 'Main':
                for carac in clase.caracteristicas:
                    if carac.nombre == 'main':
                        e_main = True
            clase.Tipo(ambito)
        for clase in self.secuencia:
            assert isinstance(clase, Clase)
            for caracteristica in clase.caracteristicas:
                if isinstance(caracteristica, Metodo):
                    ambito.meter_funcion(clase.nombre, caracteristica.nombre,
                                         [[x.nombre_variable, x.tipo] for x in caracteristica.formales],
                                         caracteristica.tipo)  # Hay que meter los parametros que sean
        # ERRORES
        for clase in self.secuencia:
            assert isinstance(clase, Clase)
            for caracteristica in clase.caracteristicas:
                if caracteristica.tipo not in ["Int", "Bool", "String", "SELF_TYPE",
                                               "Object"] and caracteristica.tipo not in ambito.variables.values():
                    raise Exception(
                        str(self.linea + 2) + ":" + " Undefined return type " + caracteristica.tipo + " in method main." + "\n" + "returntypenoexist.test:" +
                        str(self.linea + 2) + ":" + " 'new' used with undefined class " + caracteristica.tipo + ".\nCompilation halted due to static semantic errors.")
                if isinstance(caracteristica, Metodo) and not ambito.es_subtipo(caracteristica.tipo,
                                                                                caracteristica.cuerpo.cast) and not ambito.es_subtipo(
                        caracteristica.cuerpo.cast, caracteristica.tipo):
                    raise Exception(
                        str(self.linea + 4) + ':' + " Incompatible number of formal parameters in redefined method " + caracteristica.nombre + ".\nCompilation halted due to static semantic errors.")

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

    # Should be moved into the context
    _last_generated_class = None

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        nombre = self.traduce_nombre(self.nombre)
        Clase._last_generated_class = nombre
        s = f"{indent}class {nombre}"
        if self.padre != '_no_set':
            s += '(' + self.padre + '):\n'
        else:
            s += ':\n'
        indent += Nodo.INDENT_STEP
        if not self.caracteristicas:
            s += f"{indent}pass\n"
        atributos = [a for a in self.caracteristicas if isinstance(a, Atributo)]
        otros = [c for c in self.caracteristicas if not isinstance(c, Atributo)]
        if atributos:
            s += f'{indent}def __init__(self):\n'
            mi = indent + Nodo.INDENT_STEP
            s += f'{mi}super().__init__()\n'
            attr_context = ExpresionCodeGenContext(mi)
            for attr in atributos:
                attr_name = self.traduce_nombre(attr.nombre)
                s += f"{mi}self.{attr_name}: {self.traduce_tipo(attr.tipo)} = "
                s += NoExpr().genera_codigo(mi, attr_context.depth, attr_context,
                                            context_type=self.traduce_tipo(attr.tipo)) + '\n'
            if atributos:
                s += '\n'
            for attr in atributos:
                ctx = attr_context.sub_context()
                if isinstance(attr.cuerpo, NoExpr):
                    continue
                gen = attr.cuerpo.genera_codigo(mi, ctx.depth, ctx)
                s += f"{ctx.initialization()}"
                attr_name = self.traduce_nombre(attr.nombre)
                s += f"{mi}self.{attr_name}: {self.traduce_tipo(attr.tipo)} = {gen.lstrip()}\n"
            s += '\n'
        for car in otros:
            if isinstance(car, Metodo) and car.nombre == 'copy':
                raise CodeGenError("Cannot define reserved method: 'copy'")
            s += car.genera_codigo(indent, depth)
        if atributos:
            s += f"{indent}def copy(self):\n"
            mi = indent + Nodo.INDENT_STEP
            s += f"{mi}c = {nombre}()\n"
            for attr in atributos:
                s += f"{mi}c.{self.traduce_nombre(attr.nombre)} = self.{attr.nombre}\n"
            s += f"{mi}return c"
        return s + '\n'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_class\n'
        resultado += f'{(n + 2) * " "}{self.nombre}\n'
        resultado += f'{(n + 2) * " "}{self.padre}\n'
        resultado += f'{(n + 2) * " "}"{self.nombre_fichero}"\n'
        resultado += f'{(n + 2) * " "}(\n'
        resultado += ''.join([c.str(n + 2) for c in self.caracteristicas])
        resultado += '\n'
        resultado += f'{(n + 2) * " "})\n'
        return resultado

    def Tipo(self, ambito):
        if self.nombre not in ambito.clases:
            ambito.meter_clase(self)
        self.cast = 'Object'
        ambito.tipo_variable('self', self.nombre)
        for caracteristica in self.caracteristicas:
            if isinstance(caracteristica, Atributo):
                caracteristica.Tipo(ambito)
                ambito.tipo_variable(caracteristica.nombre, caracteristica.tipo)
            else:
                assert isinstance(caracteristica, Metodo)
                # Hace falta meter los metodos aquí llamando al nuevo metodo que hay abajo
                caracteristica.Tipo(ambito)
                ambito.meter_funcion(self.nombre, caracteristica.nombre,
                                     [[x.nombre_variable, x.tipo] for x in caracteristica.formales],
                                     caracteristica.tipo)  # Hay que meter los parametros que sean
        """for caracteristica in self.caracteristicas:
            if caracteristica.tipo not in ["Int", "Bool", "String", "SELF_TYPE", "Object"] and caracteristica.tipo not in ambito.variables.values():
                    raise Exception(str(self.linea+1) +":"+ " Undefined return type " + caracteristica.tipo + " in method main." + "\n" + "returntypenoexist.test:" +
                                    str(self.linea+1) +":"+ " 'new' used with undefined class " + caracteristica.tipo + ".\nCompilation halted due to static semantic errors.")"""
        for caracteristica in self.caracteristicas:
            caracteristica.Tipo(ambito)


@dataclass
class Metodo(Caracteristica):
    formales: List[Formal] = field(default_factory=list)

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        s = f"{indent}@mutable_params\n"
        s += f"{indent}def {self.traduce_nombre(self.nombre)}(self, "
        s += ', '.join(f.genera_codigo(indent, depth+1) for f in self.formales)
        s += f") -> {self.traduce_tipo(self.tipo, hint=True)}:\n"
        indent += Nodo.INDENT_STEP
        ctx = ExpresionCodeGenContext(indent)
        for f in self.formales:
            ctx.add_var_name(self.traduce_nombre(f.nombre_variable))
        gen = self.cuerpo.genera_codigo(indent, ctx.depth, ctx)
        s += ctx.initialization()
        s += f'{indent}return ' + gen.lstrip() + '\n'
        return s + '\n'

    def Tipo(self, ambito):
        for formal in self.formales:
            formal.Tipo(ambito)
        self.cuerpo.Tipo(ambito)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_method\n'
        resultado += f'{(n + 2) * " "}{self.nombre}\n'
        resultado += ''.join([c.str(n + 2) for c in self.formales])
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n + 2)

        return resultado


class Atributo(Caracteristica):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{n * " "}_attr\n'
        resultado += f'{(n + 2) * " "}{self.nombre}\n'
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n + 2) if self.cuerpo is not None else 'None'
        return resultado

    def Tipo(self, ambito):
        self.cast = 'Object'
        self.cuerpo.Tipo(ambito)
        reserved_names = ['self']
        if self.nombre in reserved_names:
            raise Exception(
                "{}: '{}' cannot be the name of an attribute.\nCompilation halted due to static semantic errors.".format(
                    self.linea, self.nombre))


class Arbol:
    def __init__(self, nombre, padre, funciones, hijos):
        self.nombre = nombre
        self.padre = padre
        self.funciones = funciones
        self.hijos = hijos

    def meter_funcion(self, nombre_funcion, parametro_formales, retorno):
        self.funciones[nombre_funcion] = [parametro_formales, retorno]


class Ambito:
    def __init__(self, arbol, metodos, variables):
        self.metodos = metodos
        self.variables = variables
        self.clases = ["Object", 'Int', 'IO', 'String']
        raiz = Arbol('Object', '', {'abort': [[[]], 'Object'],
                                    'typename': [[[]], 'String'],
                                    'copy': [[[]], 'SELF_TYPE'],
                                    'self': [[[]], 'SELF_TYPE']}
                     , []  # Añadir hijos
                     )
        integer = Arbol('Int', 'Object', {'new': [[[]], 'Int']}, [])  # (Int no tiene metodos)
        io = Arbol('IO', 'Object',
                   {'out_string': [[['x', 'String']], 'SELF_TYPE'], 'out_int': [[['x', 'Int']], 'SELF_TYPE'],
                    'in_string': [[[]], 'String'], 'in_int': [[[]], 'Int']}, [])
        string = Arbol('String', 'Object', {'length': [[[]], 'Int'], 'concat': [[['s', 'String']], 'String'],
                                            'substr': [[['i', 'Int'], ['l', 'Int']], 'String']}, [])

        boolean = Arbol('Bool', 'Object', {'new': [[[]], 'Bool']}, [])  # (Bool no tiene metodos) default = false
        """raiz.meter_funcion('abort', [], 'Object')
        raiz.meter_funcion('typename', [], 'String')
        raiz.meter_funcion('copy', [], 'SELF_TYPE')"""
        raiz.hijos.append(integer)
        raiz.hijos.append(boolean)
        raiz.hijos.append(io)
        raiz.hijos.append(string)
        self.Arbol = raiz

    def clase_tiene_metodo_x(self, hijo_clase, nombre_metodo):
        if isinstance(hijo_clase, str):
            hijo_clase = self.get_nodo(hijo_clase)

        if nombre_metodo in hijo_clase.funciones:

            return hijo_clase.funciones[
                nombre_metodo]  ## Devuelve una lista de los tipos de los argumentos y del return
        else:
            # if self.get_nodo(hijo_clase) is not False:
            #    if self.get_nodo(hijo_clase).padre:

            if hijo_clase.padre:

                return self.clase_tiene_metodo_x(hijo_clase.padre, nombre_metodo)
            else:

                return False

    def devuelve_tipo_metodo(self, nombre_metodo, cast):

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
            if nombre_metodo != 'self' and metodos[-1] == "SELF_TYPE":
                metodos = [metodos[:-1], cast]
            return metodos
        else:
            return False

    def es_subtipo(self, claseA, claseB):
        if claseA == claseB:
            return True
        elif claseB == "Object":
            return claseA == claseB
        else:
            return self.es_subtipo(self.padreada(claseB), claseA)

    def padreada(self, nombreN):
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombreN:
                return nodo_temp.padre
            else:
                l.extend(nodo_temp.hijos)
        return "ERROR"

    def minimo_ancestro(self, nodoA, nodoB):
        if isinstance(nodoA, str):
            nodoA = self.get_nodo(nodoA)
        if isinstance(nodoB, str):
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
            return self.minimo_ancestro(nodoA, nodoB)

    def profundidad(self, nodo):
        if self.Arbol == nodo:
            return 0
        else:
            return 1 + self.profundidad(self.get_nodo(nodo.padre))

    def nodoArbol(self, nombreN):
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombreN:
                return nodo_temp
            else:
                l.extend(nodo_temp.hijos)
        return self.Arbol

    def tipo_variable(self, nombre, tipo):
        self.variables[nombre] = tipo

    def get_tipo_variable(self, nombre):
        return self.variables[nombre]

    def meter_funcion(self, nombre_clase, nombre_funcion, parametro_formales, retorno):
        # Hay que enganchar la funcion al arbol que se define arriba en el __init__ de ambito
        # No se donde se engancha lol
        # Pero es como el diccionario este que hay encima. Ejemplo: string = Arbol('String','Object',{'length':[[[]],'Int'],'concat':[[['s','String']],'String'],'substr':[[['i','Int'],['l','Int']],'String']},[])
        nodo = self.Arbol
        nodo_temp = nodo
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombre_clase:
                break
            l.extend(nodo_temp.hijos)
        nodo_temp.meter_funcion(nombre_funcion, parametro_formales, retorno)

    def existe_clase(self, nombreN):
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombreN:
                return True
            else:
                l.extend(nodo_temp.hijos)
        return False

    def get_nodo(self, nombre_nodo):
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            if nodo_temp.nombre == nombre_nodo:
                return nodo_temp
            else:
                l.extend(nodo_temp.hijos)
        return False

    def mostrar_arbol(self):  # metodo de debug
        nodo = self.Arbol
        l = [nodo]
        while l:
            nodo_temp = l.pop()
            l.extend(nodo_temp.hijos)
        return False

    def meter_clase(self, clase):
        self.clases.append(clase)
        nodoPadre = self.get_nodo(clase.padre)
        nodoPadre.hijos.append(Arbol(clase.nombre, clase.padre, {}, []))


class CodeGenError(Exception):
    def __init__(self, message: str):
        self.message = message
    def __str__(self):
        return self.message
