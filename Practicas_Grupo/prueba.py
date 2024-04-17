class A:
    def imprime(self):
        print("Es clase A")

class B(A):
    def imprime(self):
        print("Es clase B")

from copy import deepcopy
from Base_clases import *

a = B()
a.imprime()
b = deepcopy(a)
b.__class__ = A
b.imprime()

class Bob(IO):
  x = Int(None)
  y = Int(4)
class Main(Bob):
  z = Int(23)
  def jack(self, q, z):
    temp = lambda z : self.print_z(self.z)
    temp(Int(self.z + self.y))

    self.y = self.y + 4
    temp = lambda y : self.y
    temp(Int(self.z + self.y))


  def print_z(self, z):
    self.out_string(String("z = "))
    self.out_int(self.z)
    self.out_string(String("\n"))

  def main(self):
    self.print_z(self.z)
    temp = lambda z : self.print_z(self.z)
    temp(Int(self.jack(5, self.z + 2)))


Main().main()