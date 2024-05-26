from Base_clases import *


class P(Object):
    def __init__(self):
        super().__init__()
        self.x: P = Void


    @mutable_params
    def foo(self, ) -> 'Object':
        def _block1():
            self.x = _var1 = P()
            _var1
            return self.abort()

        return _block1()

    @mutable_params
    def badGuy(self, ) -> 'Object':
        return self.x.foo()

    def copy(self):
        c = P()
        c.x = self.x
        return c

class C(P):
    @mutable_params
    def foo(self, ) -> 'Object':
        def _block1():
            (IO()).out_string(String("ok\n"))
            self.x = _var1 = C()
            return _var1

        return _block1()



class Main(Object):
    @mutable_params
    def f1(self, p: Par['P']) -> 'Object':
        def _block1():
            p[:] = _var1 = P()
            (_var1 if false else Int(0))
            return p[:].foo()

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(c: Par[C]):
            def _block1():
                self.f1(c[:])
                return c[:].badGuy()

            return             _block1()

        return _let1(C())



if __name__ == '__main__':
    bootstrap(Main)
