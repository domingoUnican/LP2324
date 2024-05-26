from Base_clases import *


class A(IO):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)

        self.x: Int = Int(1)

    @mutable_params
    def f(self, y: Par['Int']) -> 'A':
        def _block1():
            self.x = _var1 = (self.x + y[:])
            _var1
            self.out_int(self.x)
            self.out_string(String("\n"))
            return self

        return _block1()

    @mutable_params
    def g(self, y: Par['Int']) -> 'A':
        def _block1():
            self.x = _var1 = (self.x - y[:])
            _var1
            self.out_int(self.x)
            self.out_string(String("\n"))
            return self

        return _block1()

    def copy(self):
        c = A()
        c.x = self.x
        return c

class B(A):
    @mutable_params
    def f(self, y: Par['Int']) -> 'B':
        def _block1():
            self.x = _var1 = (self.x * y[:])
            _var1
            self.out_int(self.x)
            self.out_string(String("\n"))
            return self

        return _block1()



class Main(IO):
    def __init__(self):
        super().__init__()
        self.b: B = Void

        self.b: B = B()

    @mutable_params
    def main(self, ) -> 'Object':
        return A.g(A.f(self.b.g(~(Int(4))), Int(8)).f(Int(5)), Int(3))

    def copy(self):
        c = Main()
        c.b = self.b
        return c

if __name__ == '__main__':
    bootstrap(Main)
