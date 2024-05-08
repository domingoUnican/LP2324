from copy import deepcopy

class Object:
    def abort(self):
        exit()

    def copy(self):
        return deepcopy(self)
    
    def EsNulo(self):
        return True

class Int(Object, int):
    def __init__(self, numero=None):
        super().__init__()
        if numero is None:
            self.numero = 0
        else:
            self.numero = numero

    def __add__(self, s):
        return Entero(self.numero + s.numero)

    def EsNulo(self):
        return False


class IO(Object):

    def out_string(self, s):
        print(s.s, end='') # ¿Que habra que poner?,flush=False
        
    def out_int(self, s):
        print(s, end='') # ¿Que habra que poner?
        

class String(Object):#str
    def __init__(self, s=""):
        super().__init__()
        if s is None:
            self.s = ""
        else:
            self.s = s

    def __eq__(self, b):
        if isinstance(b, str):
            return self.s == b
        if self.s == b.s:
            return True
        else:
            return False
    def EsNulo(self):
        if self.s != None:
            return False
        return True

class Bool(Object):
    def __init__(self, b=None):
        super().__init__()
        if b == None:
            self.b = False
        else:
            self.b = b
    def EsNulo(self):
        return False

    def __eq__(self, b):
        if isinstance(b, bool):
            return self.b == b
        if self.b == b.b:
            return True
        else:
            return False

class Main(IO):
  def __init__(self):
    pass
  def print(self,x):
    lstout_int = []
    temp = x
    lstout_int.append(temp)
    temp = self.out_int(*lstout_int)

    lstout_string = []
    temp = String("\n")
    lstout_string.append(temp)
    temp = self.out_string(*lstout_string)

    return temp
  def main(self):
    temp=5
    foo = temp
    temp = not Entero(linea=0, valor='1')
    foo = temp

    foo = temp
    temp = not Objeto(linea=0, nombre='foo')
    if Bool(b=True) == (temp):

      foo = temp
      lstprint = []
      temp = foo
      sumando = temp
      temp=1
      temp = sumando + temp

      lstprint.append(temp)
      temp = self.print(*lstprint)

    else:
      temp=5
    return temp
Main().main()