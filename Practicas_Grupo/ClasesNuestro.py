#Clases Del AST del parser

class AST(object):
    pass

class Programa(AST):
    # def __init__(self, clases):
    #     self.clases = clases

    def __init__(self,):
        print ("Programa")

class Clase(AST):
    def __init__(self):
        print ("Clase")

class Expression(AST):
    def __init__(self):
        print ("Expression")

class Metodo(AST):
    def __init__(self):
        print ("Metodo")

class Formal(AST):
    def __init__(self):
        print ("Formal")

class BinOp(AST):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class Number(AST):
    def __init__(self, value):
        self.value = value

class Identifier(AST):
    def __init__(self, name):
        self.name = name

class Formal(AST):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Assignment(AST):
    def __init__(self, location,value):
        self.location = location 
        self.value = value

class ObjectID(AST):
    def __init__(self, name):
        self.name = name

class TypeID(AST):
    def __init__(self, name):
        self.name = name

class UnOp(AST):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

class BoolConst(AST):
    def __init__(self, value):
        self.value = value

class IntConst(AST):
    def __init__(self, value):
        self.value = value

class StringConst(AST):
    def __init__(self, value):
        self.value = value