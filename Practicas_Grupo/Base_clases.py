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
        return Entero(self.numero // s.numero)
    
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

class A (IO):
  def __init__(self):
    super().__init__()
    t = Entero(1)

    self.x = t
  def f(self,y):
    t = self.x

    t0 = t
    t = y

    t += t0

    self.x = t
    t = self.x

    t1 = t
    t = self

    t2 = t
    t = t2.out_int(t1)
    t = String1("\n")

    t3 = t
    t = self

    t4 = t
    t = t4.out_string(t3)
    t = self

    return t
  def g(self,y):
    t = self.x

    t5 = t
    t = y

    t = t5 - t

    self.x = t
    t = self.x

    t6 = t
    t = self

    t7 = t
    t = t7.out_int(t6)
    t = String1("\n")

    t8 = t
    t = self

    t9 = t
    t = t9.out_string(t8)
    t = self

    return t
class B (A):
  def __init__(self):
    super().__init__()
  def f(self,y):
    t = self.x

    t10 = t
    t = y

    t *= t10

    self.x = t
    t = self.x

    t11 = t
    t = self

    t12 = t
    t = t12.out_int(t11)
    t = String1("\n")

    t13 = t
    t = self

    t14 = t
    t = t14.out_string(t13)
    t = self

    return t
