
class AST:
        pass 

class Assignment(AST):
    def __init__(self, location, value):
        self.location = location
        self.value = value
    def __str__(self):
        return f"Assignment({self.location}, {self.value})"

class BinOp(AST):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
    def __str__(self):
        return f"BinOp({self.operator}, {self.left}, {self.right})"

class Number(AST):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"Number({self.value})"
    
class Identifier(AST):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Identifier({self.name})"
