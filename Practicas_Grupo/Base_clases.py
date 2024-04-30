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

class Main (IO):
  def __init__(self):
    super().__init__()
    t = String1("2 is trivially prime.\n")

    t0 = t
    t = self

    t1 = t
    t = t1.out_string(t0)
    t = Entero(2)

    self.out = t
    t = self.out

    self.testee = t
    self.divisor = Entero(0)
    t = Entero(500)

    self.stop = t
    t = Booleano(True)

    t2 = t
    if t == false:
      t = Objeto()
    while t2 == true:
      t = self.testee

      t3 = t
      t = Entero(1)

      t += t3

      self.testee = t
      t = Entero(2)

      self.divisor = t
      t = self.testee
      t4 = t
      t = self.divisor

      t5 = t
      t = self.divisor

      t *= t5

      t = t4 < t
      t = Booleano(t)

      if t == true:
          t = Booleano(False)

      else:
          t = self.testee

          t6 = t
          t = self.divisor

          t7 = t
          t = self.testee

          t8 = t
          t = self.divisor

          t = t8 / t
          t *= t7

          t = t6 - t
          t9 = t
          t = Entero(0)

          t = t9 == t
          t = Booleano(t)

          if t == true:
              t = Booleano(False)

          else:
              t = Booleano(True)



      t10 = t
      if t == false:
        t = Objeto()
      while t10 == true:
        t = self.divisor

        t11 = t
        t = Entero(1)

        t += t11

        self.divisor = t

        t = self.testee
        t10 = t
        t = self.divisor

        t11 = t
        t = self.divisor

        t *= t11

        t = t10 < t
        t = Booleano(t)

        if t == true:
            t = Booleano(False)

        else:
            t = self.testee

            t12 = t
            t = self.divisor

            t13 = t
            t = self.testee

            t14 = t
            t = self.divisor

            t = t14 / t
            t *= t13

            t = t12 - t
            t15 = t
            t = Entero(0)

            t = t15 == t
            t = Booleano(t)

            if t == true:
                t = Booleano(False)

            else:
                t = Booleano(True)



        t10 = t
      t = self.testee
      t9 = t
      t = self.divisor

      t10 = t
      t = self.divisor

      t *= t10

      t = t9 < t
      t = Booleano(t)

      if t == true:
          t = self.testee

          self.out = t
          t = self.out

          t11 = t
          t = self

          t12 = t
          t = t12.out_int(t11)
          t = String1(" is prime.\n")

          t13 = t
          t = self

          t14 = t
          t = t14.out_string(t13)

      else:
          t = Entero(0)

      t = self.stop
      t15 = t
      t = self.testee

      t = t15 <= t
      t = Booleano(t)

      if t == true:
          t = String1("halt")

          t16 = t
          t = t16.abort()

      else:
          t = String1("continue")


      t = Booleano(True)

      t2 = t

    self.m = t
  def main(self):
    t = Entero(0)

    return t
Main().main()