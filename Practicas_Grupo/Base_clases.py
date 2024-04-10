from copy import deepcopy

class Object:
    # def __init__(self,s) -> None:
    #     pass
    
    def abort(self):
        # exit()
        print("error")

    def copy(self):
        return deepcopy(self)

class IO(Object):
    def out_string(self, s):
        print(s.cadena,end='')

    def out_int(self, s):
        print(s.numero,end='')

    def in_string(self):
        return String(input())
    
    def in_int(self):
        return Int(int(input()))

class Int(Object, int):
    def __init__(self, s):
        super().__init__()
        if s is None:
            self.numero = 0
        else:
            self.numero = s

    def __add__(self, s):
        if (isinstance(s, Int)):
            return Int(self.numero + s.numero)
        else:
            return Int(self.numero + s)
            

class String(Object):
    def __init__(self, s):
        if s is None:
            self.cadena = ""
        else:
            self.cadena = s
        
    def length(self):
        return len(self.cadena)
        
    def concatenate(self, s):
        return String(self.cadena + s.cadena)
    
    def substr(self, e1, e2):
        return String(self.cadena[e1:e1+e2+1])
    
class Bool(Object):
    def __init__(self, s):
        super().__init__()
        if s is None:
            self.booleano = False
        else:
            self.booleano = s
    



