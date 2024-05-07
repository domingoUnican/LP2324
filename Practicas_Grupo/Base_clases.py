from copy import deepcopy
from collections import defaultdict

class Object:
    def abort(self):
        exit()

    def copy(self):
        return deepcopy(self)

    def type_name(self):
        d = {"<class 'Base_clases.Booleano'>" : "Bool", "<class 'Base_clases.Cadena_carac'>" : "String", 
                "<class 'Base_clases.Entero'>" : "Int"}
        if str(type(self))in d:
            return Cadena_carac(d[str(type(self))])
        else:
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
    
    def __truediv__(self, s):
        return Entero(self.numero // s.numero)

    def __eq__(self, value: object) -> bool:
        return self.numero == value.numero
    
    def __neg__(self):
        return Entero(-self.numero)
    
    def __lt__(self, value: object) -> bool:
        return self.numero < value.numero
    
    def __le__(self, value: object) -> bool:
        return self.numero <= value.numero

class Cadena_carac(Object):
    def __init__(self, cadena = ""):
        super().__init__()
        self.cadena = cadena

    def length(self):
        return len(self.cadena)

    def concat(self, s):
        return Cadena_carac(self.cadena + s.cadena)

    def substr(self, i, l):
        return Cadena_carac(self.cadena[i.numero:l.numero + i.numero])
    
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

'''class Main(IO):
    def __init__(self):
      temp = Cadena_carac("2 is trivially prime.\n")
      temp0 = temp
      temp = self
      temp = temp.out_string(temp0)
      temp = Entero(2)

      self.out = temp
      temp = self.out
      self.testee = temp
      self.divisor = Entero(0)
      temp = Entero(500)
      self.stop = temp
      temp = Booleano(True)
      while(temp == True):
        temp = self.testee
        tempsuma1 = temp
        temp = Entero(1)
        temp = tempsuma1 + temp
        self.testee = temp
        temp = Entero(2)
        self.divisor = temp
        temp = self.testee
        tempmenor = temp
        temp = self.divisor
        tempmul2 = temp
        temp = self.divisor
        temp = tempmul2 * temp
        temp = tempmenor < temp
        if True == temp:
          temp = Booleano(False)
        else:
          temp = self.testee
          tempresta3 = temp
          temp = self.divisor
          tempmul4 = temp
          temp = self.testee
          tempdiv5 = temp
          temp = self.divisor
          temp = tempdiv5 / temp
          temp = tempmul4 * temp
          temp = tempresta3 - temp
          temp6 = temp
          temp = Entero(0)
          temp7 = temp
          temp = (temp6 == temp7)
          if True == temp:
            temp = Booleano(False)
          else:
            temp = Booleano(True)
        while(temp == True):
          temp = self.divisor
          tempsuma8 = temp
          temp = Entero(1)
          temp = tempsuma8 + temp
          self.divisor = temp
          temp = self.testee
          tempmenor = temp
          temp = self.divisor
          tempmul9 = temp
          temp = self.divisor
          temp = tempmul9 * temp
          temp = tempmenor < temp
          if True == temp:
            temp = Booleano(False)
          else:
            temp = self.testee
            tempresta10 = temp
            temp = self.divisor
            tempmul11 = temp
            temp = self.testee
            tempdiv12 = temp
            temp = self.divisor
            temp = tempdiv12 / temp
            temp = tempmul11 * temp
            temp = tempresta10 - temp
            temp13 = temp
            temp = Entero(0)
            temp14 = temp
            temp = (temp13 == temp14)
            if True == temp:
              temp = Booleano(False)
            else:
              temp = Booleano(True)

        temp = self.testee
        tempmenor = temp
        temp = self.divisor
        tempmul15 = temp
        temp = self.divisor
        temp = tempmul15 * temp
        temp = tempmenor < temp
        if True == temp:
          temp = temp = self.testee
          self.out = temp
          temp = self.out
          temp16 = temp
          temp = self
          temp = temp.out_int(temp16)
          temp = Cadena_carac(" is prime.\n")
          temp17 = temp
          temp = self
          temp = temp.out_string(temp17)

        else:
          temp = Entero(0)

        if self.stop <= self.testee:
          Cadena_carac("halt").abort()
        else:
          temp = "continue"

        temp = Booleano(True)

      self.m = temp
    def main(self):
      temp = Entero(0)
      return temp
Main().main()

'''
