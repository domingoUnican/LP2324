from copy import deepcopy

class Objeto:
    
    def abort(self):
        exit()

    def copy(self): 
        return deepcopy(self)

class Entero(Objeto,int):
    def __init__(self, numero):
        super().__init__()
        if numero == None:
            self.numero = Entero(0)
        else:
            self.numero = numero

    def __add__(self, s):
        return Entero(self.numero + s.numero)
    
class String(Objeto,str):
    def __init__(self, cadena):
        super().__init__()
        if cadena == None:
            self.cadena = ""
        else:
            self.cadena = cadena
    
    def __add__(self, s):
        return String(self.cadena + s.cadena)

class Booleano(Objeto):
    def __init__(self, booleano):
        super().__init__()
        if booleano == None:
            self.booleano = Booleano(False)
        else:
            self.booleano = booleano

class IO(Objeto):
    def out_string(self, s):
        s = String(s)
        print(s.cadena,end="") # ¿Que habra que poner?

    def out_int(self, s):
        s = Entero(s)
        print(s.numero,end="") # ¿Que habra que poner?

