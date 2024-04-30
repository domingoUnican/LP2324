from copy import deepcopy

class Object:
    def abort(self):
        exit()

    def copy(self):
        return deepcopy(self)

    def type_name(self):
        return Cadena_carac(type(self).__qualname__)

class Entero(Object):
    def __init__(self, numero):
        super().__init__()
        self.numero = numero

    def __add__(self, s):
        return Entero(self.numero + s.numero)
    
    def __sub__(self, s):
        return Entero(self.numero - s.numero)

    def __mul__(self, s):
        return Entero(self.numero * s.numero)
    
    def __div__(self, s):
        return Entero(self.numero / s.numero)

    def __eq__(self, value: object) -> bool:
        return self.numero == value.numero
    
    def __neg__(self):
        return Entero(-self.numero)
    
    def __lt__(self, value: object) -> bool:
        return self.numero < value.numero

class Cadena_carac(Object):
    def __init__(self, cadena = ""):
        super().__init__()
        self.cadena = cadena

    def length(self):
        return len(self.cadena)

    def concat(self, s):
        return Cadena_carac(self.cadena + s.cadena)

    def substr(self, i, l):
        return Cadena_carac(self.cadena[i:l + i])
    
    def __eq__(self, value: object) -> bool:
        return self.cadena == value
    
class Booleano(Object):
    def __init__(self, booleano = False):
        super().__init__()
        self.booleano = booleano

    def __eq__(self, value: object) -> bool:
        if (isinstance(value, bool)):
            return self.booleano == value
        else:
            return self.booleano == value.booleano
    


class IO(Object):
    def out_string(self, s):
        print(s.cadena,end="") 
        return self 

    def out_int(self, s):
        print(s.numero,end="") 
        return self

    def in_string(self):
        a = input()
        return Cadena_carac(a)

    def in_int(self):
        a = input()
        return Entero(int(a))

def NOT(x):
    return Booleano(not x.booleano)
