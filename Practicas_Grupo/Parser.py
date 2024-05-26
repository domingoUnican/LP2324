# coding: utf-8
from typing import Optional

from Clases import *
from Lexer import CoolLexer
from sly.lex import Token
from sly.yacc import YaccSymbol
from sly import Parser


# Placebo definition for PyCharm (since it doesn't understand the Parser metaclass)
def _(*_):
    return lambda _: _


class CoolParser(Parser):
    # error_token = TokenStr('error', r'error', {})
    nombre_fichero = ''
    tokens = CoolLexer.tokens #.union({
    #     error_token,
    # })
    debugfile = "salida.out"
    errores = []

    precedence = (
        ('right', 'NOT'),
        ('left', 'ASSIGN',),
        ('left', 'IN'),
        ('nonassoc', '<', 'LE', '='),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'ISVOID', '~'),
        ('left', '.', '@'),
    )

    def __init__(self):
        super().__init__()
        self.expected_next_error = False
        self.expected_error = False
        self.error_depth = 0

    @_("Clases")
    def Programa(self, p):
        return Programa(secuencia=p.Clases)

    @_("Clase",
       "Clase Clases")
    def Clases(self, p):
        if not p:
            return []
        return [p.Clase] + (p.Clases if len(p) > 1 else [])

    @_("CLASS TYPEID SuperClassDeclaration BlockCaracteristicas ';'")
    def Clase(self, p):
        return Clase(nombre=p.TYPEID, padre=p.SuperClassDeclaration,
                     nombre_fichero=self.nombre_fichero,
                     caracteristicas=p.BlockCaracteristicas)

    @_("CLASS error ';'",
       "CLASS TYPEID SuperClassDeclaration error ';'")
    def Clase(self, p):
        return ErrorNodo(p.error)

    @_("'{' Caracteristicas '}'")
    def BlockCaracteristicas(self, p):
        return p.Caracteristicas

    @_("'{' Caracteristicas error '}'",
       "'{' error '}'")
    def BlockCaracteristicas(self, p):
        return p.Caracteristicas if len(p) > 3 else []

    @_("",
       "INHERITS TYPEID")
    def SuperClassDeclaration(self, p):
        return p.TYPEID if len(p) > 0 else 'Object'

    @_(
        "",
        "Caracteristica Caracteristicas")
    def Caracteristicas(self, p):
        if not p:
            return []
        return [p.Caracteristica] + (p.Caracteristicas if len(p) > 1 else [])

    @_("Atributo", "Metodo")
    def Caracteristica(self, p):
        return p[0]

    @_("OBJECTID ':' TYPEID ';'")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=NoExpr())

    @_("OBJECTID ':' TYPEID")
    def Atributo(self, p):
        self._report_error(p, p.OBJECTID, 'OBJECTID')
        return ErrorNodo(p.OBJECTID)

    @_("OBJECTID ':' TYPEID ASSIGN Expresion ';'")
    def Atributo(self, p):
        return Atributo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion)

    @_("OBJECTID ':' error ';'",
       "OBJECTID ':' TYPEID error ';'",
       "OBJECTID ':' TYPEID ASSIGN error ';'")
    def Atributo(self, p):
        return ErrorNodo(p.error)

    @_("OBJECTID ParFormales ':' TYPEID BlockExpresion ';'")
    def Metodo(self, p):
        return Metodo(nombre=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.BlockExpresion, formales=p.ParFormales)


    @_("'(' ')'",
        "'(' Formales ')'")
    def ParFormales(self, p):
        return p.Formales if len(p) > 2 else []
    @_("'(' error ')'")
    def ParFormales(self, p):
        return ErrorNodo(p.error)

    @_("'{' Expresion '}'")
    def BlockExpresion(self, p):
        return p.Expresion
    @_("'{' error '}'")
    def BlockExpresion(self, p):
        return ErrorNodo(p.error)
    @_("'{' '}'")
    def BlockExpresion(self, p):
        self._report_error(p, p[1])
        return ErrorNodo(p[1])

    @_("Formal",
       "Formal ',' Formales")
    def Formales(self, p):
        if not p:
            return []
        return [p.Formal] + (p.Formales if len(p) > 1 else [])

    @_("OBJECTID ':' TYPEID")
    def Formal(self, p):
        return Formal(nombre_variable=p.OBJECTID, tipo=p.TYPEID)

    @_("OBJECTID ASSIGN Expresion")
    def Expresion(self, p):
        return Asignacion(nombre=p.OBJECTID, cuerpo=p.Expresion)

    @_("Expresion '+' Expresion")
    def Expresion(self, p):
        return Suma(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '-' Expresion")
    def Expresion(self, p):
        return Resta(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '*' Expresion")
    def Expresion(self, p):
        return Multiplicacion(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '/' Expresion")
    def Expresion(self, p):
        return Division(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '<' Expresion")
    def Expresion(self, p):
        return Menor(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion LE Expresion")
    def Expresion(self, p):
        return LeIgual(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("Expresion '=' Expresion")
    def Expresion(self, p):
        return Igual(izquierda=p.Expresion0, derecha=p.Expresion1)

    @_("'(' Expresion ')'")
    def Expresion(self, p):
        return p.Expresion

    @_("NOT Expresion")
    def Expresion(self, p):
        return Not(expr=p.Expresion)

    @_("ISVOID Expresion")
    def Expresion(self, p):
        return EsNulo(expr=p.Expresion)

    @_("'~' Expresion")
    def Expresion(self, p):
        return Neg(expr=p.Expresion)

    @_("Expresion '@' TYPEID '.' OBJECTID ParOptArgumentos")
    def Expresion(self, p):
        return LlamadaMetodoEstatico(cuerpo=p.Expresion, clase=p.TYPEID, nombre_metodo=p.OBJECTID,
                                     argumentos=p.ParOptArgumentos)

    @_("Expresion '.' OBJECTID ParOptArgumentos")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=p.Expresion, nombre_metodo=p.OBJECTID, argumentos=p.ParOptArgumentos)

    @_("OBJECTID ParOptArgumentos")
    def Expresion(self, p):
        return LlamadaMetodo(cuerpo=Objeto(nombre='self'), nombre_metodo=p.OBJECTID, argumentos=p.ParOptArgumentos)

    @_("'(' OptArgumentos ')'")
    def ParOptArgumentos(self, p):
        return p.OptArgumentos

    @_("'(' error ')'",
       "'(' Argumentos error ')'")
    def ParOptArgumentos(self, p):
        return ErrorNodo(p.error)

    @_("",
       "Argumentos")
    def OptArgumentos(self, p):
        if len(p) == 0:
            return []
        return p.Argumentos

    @_("Expresion",
       "Expresion ',' Argumentos")
    def Argumentos(self, p):
        if len(p) == 0:
            return []
        return [p.Expresion] + (p.Argumentos if len(p) > 1 else [])

    @_("IF Expresion THEN Expresion ELSE Expresion FI")
    def Expresion(self, p):
        return Condicional(condicion=p.Expresion0, verdadero=p.Expresion1, falso=p.Expresion2)

    @_("WHILE Expresion LOOP Expresion POOL")
    def Expresion(self, p):
        return Bucle(condicion=p.Expresion0, cuerpo=p.Expresion1)

    @_("LET Declaraciones IN Expresion")
    def Expresion(self, p):
        cuerpo = p.Expresion
        for decl in reversed(p.Declaraciones):
            if not isinstance(decl, ErrorNodo):
                cuerpo = Let(nombre=decl['nombre'], tipo=decl['tipo'], inicializacion=decl['cuerpo'], cuerpo=cuerpo)
        return cuerpo

    @_("Declaracion",
       "Declaracion ',' Declaraciones")
    def Declaraciones(self, p):
        return [p.Declaracion] + (p.Declaraciones if len(p) > 1 else [])

    @_("error ',' Declaraciones")
    def Declaraciones(self, p):
        return [ErrorNodo(p.error)] + (p.Declaraciones if len(p) > 1 else [])

    @_("OBJECTID ':' TYPEID",
       "OBJECTID ':' TYPEID ASSIGN Expresion")
    def Declaracion(self, p):
        return {'nombre': p.OBJECTID, 'tipo': p.TYPEID, 'cuerpo': p.Expresion if len(p) > 3 else NoExpr()}

    @_("CASE Expresion OF RamasCase ESAC",
       "CASE OF RamasCase ESAC",
       "CASE error OF RamasCase ESAC")
    def Expresion(self, p):
        if len(p) < 5:
            self._report_error(p, p.OF, 'OF')
            return ErrorNodo(p.OF)
        if isinstance(p[1], Expresion):
            return Switch(expr=p.Expresion, casos=p.RamasCase)
        return ErrorNodo(p.error)

    @_("RamaCase",
       "RamaCase RamasCase")
    def RamasCase(self, p):
        return [p.RamaCase] + (p.RamasCase if len(p) > 1 else [])

    @_("OBJECTID ':' TYPEID DARROW Expresion ';'")
    def RamaCase(self, p):
        return RamaCase(nombre_variable=p.OBJECTID, tipo=p.TYPEID, cuerpo=p.Expresion)

    @_("NEW TYPEID")
    def Expresion(self, p):
        return Nueva(tipo=p.TYPEID)

    @_("'{' Expresiones '}'")
    def Expresion(self, p):
        return Bloque(expresiones=p.Expresiones)

    @_("'{' error '}'")
    def Expresion(self, p):
        return ErrorNodo(p.error)

    @_("Expresion ';'",
       "Expresion ';' Expresiones")
    def Expresiones(self, p):
        return [p.Expresion] + (p.Expresiones if len(p) > 2 else [])

    @_("error ';'",
       "error ';' Expresiones")
    def Expresiones(self, p):
        return [ErrorNodo(p.error)] + (p.Expresiones if len(p) > 2 else [])

    @_("OBJECTID")
    def Expresion(self, p):
        return Objeto(nombre=p.OBJECTID)

    @_("INT_CONST")
    def Expresion(self, p):
        return Entero(valor=p.INT_CONST)

    @_("STR_CONST")
    def Expresion(self, p):
        return String(valor=p.STR_CONST)

    @_("BOOL_CONST")
    def Expresion(self, p):
        return Booleano(valor=p.BOOL_CONST)

    def error(self, token):
        self._report_error(token)
        return None

    def _report_error(self, token, value=None, type=None):
        if value is not None:
            s = YaccSymbol()
            s.value = value
            s.type = type if type is not None else value
            s.lineno = token.lineno
            s.index = token.index
            s.end = token.end
            token = s
        # print(f"  Error: {str(CoolParseError(self.nombre_fichero, token))}")
        self.errores.append(str(CoolParseError(self.nombre_fichero, token)))


class ErrorToken(Token):
    def __init__(self, value, lineno):
        self.type = 'error'
        self.value = value
        self.lineno = lineno


class ErrorNodo(Nodo):
    def __init__(self, token):
        print(f"    --- Error node: {token}, type: {type(token)}")
        self.token = token
        self.type = 'error'
        if isinstance(token, Token):
            self.lineno = token.lineno
            self.value = token.value

    def genera_codigo(self, indent: str = '', depth: int = 0) -> str:
        raise ValueError("Cannot generate code from invalid code.")


class CoolParseError:
    def __init__(self, file: str, token):
        self.file = file
        if token is not None:
            self.line = token.lineno
            self.token = token
            if token.type.isupper() and (token.type == token.value.upper() or token.value == '<='):
                self.mensaje = f"syntax error at or near {token.type}"
            elif token.type == token.value:
                self.mensaje = f"syntax error at or near '{token.value}'"
            else:
                self.mensaje = f"syntax error at or near {token.type} = {token.value}"
        else:
            self.line = 0
            self.mensaje = f"syntax error at or near EOF"

    def __str__(self):
        return f'"{self.file}", line {self.line}: {self.mensaje}'
