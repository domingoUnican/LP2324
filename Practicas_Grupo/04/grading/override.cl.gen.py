from Base_clases import *


class A(Object):
    @mutable_params
    def f(self, ) -> 'Int':
        return Int(1)

    @mutable_params
    def g(self, ) -> 'Int':
        return Int(2)



class B(A):
    @mutable_params
    def g(self, ) -> 'Int':
        return Int(3)



class C(B):
    @mutable_params
    def f(self, ) -> 'Int':
        return Int(4)



class D(C):
    @mutable_params
    def f(self, ) -> 'Int':
        return Int(5)

    @mutable_params
    def g(self, ) -> 'Int':
        return Int(6)



class Main(IO):
    def __init__(self):
        super().__init__()
        self.a: A = Void
        self.b: B = Void
        self.c: C = Void
        self.d: D = Void

        self.a: A = A()
        self.b: B = B()
        self.c: C = C()
        self.d: D = D()

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.out_int(self.a.f())
            self.out_int(self.a.g())
            self.out_int(self.b.f())
            self.out_int(self.b.g())
            self.out_int(self.c.f())
            self.out_int(self.c.g())
            self.out_int(self.d.f())
            self.out_int(self.d.g())
            self.out_int(A.f(self.a, ))
            self.out_int(A.g(self.a, ))
            self.out_int(A.f(self.b, ))
            self.out_int(A.g(self.b, ))
            self.out_int(B.f(self.c, ))
            self.out_int(B.g(self.c, ))
            self.out_int(C.f(self.d, ))
            self.out_int(C.g(self.d, ))
            self.a = _var1 = B()
            _var1
            self.b = _var2 = C()
            _var2
            self.c = _var3 = D()
            _var3
            self.out_int(self.a.f())
            self.out_int(self.a.g())
            self.out_int(self.b.f())
            self.out_int(self.b.g())
            self.out_int(self.c.f())
            self.out_int(self.c.g())
            return self.out_string(String("\n"))

        return _block1()

    def copy(self):
        c = Main()
        c.a = self.a
        c.b = self.b
        c.c = self.c
        c.d = self.d
        return c

if __name__ == '__main__':
    bootstrap(Main)
