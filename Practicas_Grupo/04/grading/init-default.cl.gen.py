from Base_clases import *


class A(IO):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)
        self.b: Bool = false
        self.y: Int = Int(0)
        self.z: Int = Int(0)

        self.x: Int = (Int(1) if self.b else ~(Int(1)))
        self.b: Bool = true
        self.y: Int = (self.x + Int(3))
        self.z: Int = (self.z - Int(5))

    @mutable_params
    def print_attr(self, ) -> 'Object':
        def _block1():
            self.out_string(String("x: "))
            self.out_int(self.x)
            self.out_string(String("\nb: "))
            self.out_string((String("true") if self.b else String("false")))
            self.out_string(String("\ny: "))
            self.out_int(self.y)
            self.out_string(String("\nz: "))
            return self.out_int(self.z)

        return _block1()

    def copy(self):
        c = A()
        c.x = self.x
        c.b = self.b
        c.y = self.y
        c.z = self.z
        return c

class Main(Object):
    def __init__(self):
        super().__init__()
        self.a: A = Void

        self.a: A = A()

    @mutable_params
    def main(self, ) -> 'Object':
        return self.a.print_attr()

    def copy(self):
        c = Main()
        c.a = self.a
        return c

if __name__ == '__main__':
    bootstrap(Main)
