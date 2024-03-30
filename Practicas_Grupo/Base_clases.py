from copy import deepcopy

class Objeto:
    def abort(self):
        exit()

    def copy(self):
        return deepcopy(self)

class Entero(Objeto):
    def __init__(self, numero):
        super().__init__()
        self.numero = numero

    def __add__(self, s):
        return Entero(self.numero + s.numero)
    
class String(Objeto):
    def __init__(self, cadena):
        super().__init__()
        self.cadena = cadena
    
    def __add__(self, s):
        return String(self.cadena + s.cadena)
    

class IO(Objeto):
    def out_string(self, s):
        s = String(s)
        print(s.cadena) # ¿Que habra que poner?

    def out_int(self, s):
        s = Entero(s)
        print(s.numero) # ¿Que habra que poner?

