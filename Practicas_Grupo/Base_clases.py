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
        print(s.cadena,end='') #domingo nos dijo que debería de ser '' pero en otros sitios no funciona sin \n

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

    def __sub__(self, s):
        if (isinstance(s, Int)):
            return Int(self.numero - s.numero)
            # return Int(0)
        else:
            return Int(self.numero - s)
            
        
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

    def __eq__(self, e1):
        if (isinstance(e1, Bool)):
            return self.booleano == e1.booleano
        else:
            return self.booleano == e1

true = Bool(True)
false = Bool(False)

class Main(IO):
  def fact(self, n=Int(None)):
    temp = n
    temp0 = temp
    temp = Int(0)
    temp = temp == temp0
    condicion = temp
    if (condicion == True):
      temp = Int(1)
    else:
      temp = n
      temp0 = temp
      temp = n
      temp0 = temp
      temp = Int(1)
      temp = temp0 - temp
      arg0 = temp
      temp = self.fact(arg0)
      temp = temp0 * temp
    return temp
  def main(self):
    temp = Int(3)
    arg0 = temp
    temp = self.fact(arg0)
    arg0 = temp
    temp = self.out_int(arg0)
    temp = String("\n")
    arg0 = temp
    temp = self.out_string(arg0)
    temp = Int(7)
    arg0 = temp
    temp = self.fact(arg0)
    arg0 = temp
    temp = self.out_int(arg0)
    temp = String("\n")
    arg0 = temp
    temp = self.out_string(arg0)
    temp = Int(10)
    arg0 = temp
    temp = self.fact(arg0)
    arg0 = temp
    temp = self.out_int(arg0)
    temp = String("\n")
    temp = String("\n")
    arg0 = temp
    temp = self.out_string(arg0)
    return temp
Main().main()
