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


class IO(Objeto):
    def out_string(self, s):
        print(s,flush=false) # ¿Que habra que poner?

    def out_int(self, s):
        print("") # ¿Que habra que poner?
