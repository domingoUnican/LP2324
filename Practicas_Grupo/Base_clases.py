from copy import deepcopy

class Objeto():

    def __init__(self,init=None):
        self.init = init

    
    def abort(self):
        exit()
    
    def type_name(self):
        if self.init == None:
            return "Dispatch to void."
        nombre = self.__class__.__name__
        diccionario = {"Entero":"Int","String1":"String","Booleano":"Bool"}
        if nombre in diccionario:
            return diccionario[nombre]
        return nombre

    def copy(self): 
        return deepcopy(self)

class Entero(Objeto,int):
    def __init__(self, numero=0):
        super().__init__(True)
        
        self.numero = numero

    def __add__(self, s):
        return Entero(self.numero + s.numero)
    
    def __sub__(self, s):
        return Entero(self.numero - s.numero)
    
    def __mul__(self, s):
        return Entero(self.numero * s.numero)
    
    def __truediv__(self, s):
        return Entero(self.numero / s.numero)
    
class String1(Objeto,str):
    def __init__(self, cadena=""):
        super().__init__(True)
        
        self.cadena = cadena
    
    def length(self):
        return Entero(len(self.cadena))

    def concat(self, s):
        return String1(self.cadena + s.cadena)
    
    def substr(self, i, l):
        if i.numero < 0 or i.numero > len(self.cadena) or l.numero < 0:
            raise RuntimeError("Substring Index out of range")
        return String1(self.cadena[i.numero:i.numero+l.numero])

class Booleano(Objeto):
    def __init__(self, booleano=False):
        super().__init__(True)
        
        self.booleano = booleano
    
    def __eq__(self, s):
        return self.booleano == s.booleano
    
    def __not__(self):
        return Booleano(not self.booleano)

class IO(Objeto):
    def out_string(self, s):
        s = String1(s)
        print(s.cadena,end="") # ¿Que habra que poner?

    def out_int(self, s):
        s = Entero(s)
        print(s.numero,end="") # ¿Que habra que poner?
    
    def in_string(self):
        return String1(input())
    
    def in_int(self):
        return Entero(int(input()))
true = Booleano(True)
false = Booleano(False)

class Bob (IO):
  def __init__(self):
    super().__init__()
    self.x = Entero(0)
    t = Entero(4)

    self.y = t
class Main (Bob):
  def __init__(self):
    super().__init__()
    t = Entero(23)

    self.z = t
  def jack(self,q,z):
    t = self.z

    t0 = t
    t = self.y

    t += t0

    z = t
    t = self.z

    t1 = t
    t = self

    t2 = t
    t = t2.print_z(t1)
    t = self.y

    t3 = t
    t = Entero(4)

    t += t3

    self.y = t
    t = self.z

    t4 = t
    t = self.y

    t += t4

    y = t
    t = self.y

    return t
  def print_z(self,z):
    t = String1("z = ")

    t5 = t
    t = self

    t6 = t
    t = t6.out_string(t5)
    t = self.z

    t7 = t
    t = self

    t8 = t
    t = t8.out_int(t7)
    t = String1("\n")

    t9 = t
    t = self

    t10 = t
    t = t10.out_string(t9)

    return t
  def main(self):
    t = self.z

    t11 = t
    t = self

    t12 = t
    t = t12.print_z(t11)
    t = Entero(5)

    t13 = t
    t = self.z

    t14 = t
    t = Entero(2)

    t += t14

    t15 = t
    t = self

    t16 = t
    t = t16.jack(t13, t15)

    z = t
    t = self.z

    t17 = t
    t = self

    t18 = t
    t = t18.print_z(t17)

    return t
Main().main()