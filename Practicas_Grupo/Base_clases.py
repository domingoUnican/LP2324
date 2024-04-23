from copy import deepcopy

class Object:
    # def __init__(self,s) -> None:
    #     pass
    estaInicializado = False
    
    def abort(self):
        # exit()
        print("error")

    def copy(self):
        return deepcopy(self)

    def isVoid(self):
        return not self.estaInicializado

class IO(Object):

    

    def out_string(self, s):
        print(s.cadena,end='')

    def out_int(self, s):
        print(s.numero,end='')

    def in_string(self):
        return String(input())
    
    def in_int(self):
        return Int(int(input()))

class Int(Object):
    def __init__(self, s):
        super().__init__()
        self.estaInicializado = True
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
        super().__init__()
        self.estaInicializado = True
        
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
    
    def __eq__(self, e1):
        if (isinstance(e1, String)):
            return self.cadena == e1.cadena
        else:
            return self.cadena == e1
          
       
    
class Bool(Object):
    def __init__(self, s):
        super().__init__()
        self.estaInicializado = True
        if s is None:
            self.booleano = False
        else:
            self.booleano = s

true = Bool(True)
false = Bool(False)



class Main(Object):
  def main(self):
    condicion = (True == False)
    if (condicion == true):
      print("1")
      self.abort()
    else:
       0
    condicion = (True == True)
    if (condicion == true):
      0
    else:
      print("2")
      self.abort()

    condicion = (String("hello") == String("hello").copy())
    if (condicion == true):
      0
    else:
      print("3")
      self.abort()

    def temp_func(a):
      condicion = (a == String(""))
      if (condicion == true):
        0
      else:
        print("4")
        self.abort()

    variable = String(None)
    temp_func(variable)

    condicion = (5 == 6)
    if (condicion == true):
      print("5")
      self.abort()
    else:
      0


Main().main()