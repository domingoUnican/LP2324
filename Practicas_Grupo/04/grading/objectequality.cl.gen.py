from Base_clases import *


class A(Object):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)

        self.x: Int = Int(5)

    @mutable_params
    def foo(self, y: Par['Int']) -> 'A':
        def _block1():
            self.x = _var1 = y[:]
            _var1
            return self

        return _block1()

    def copy(self):
        c = A()
        c.x = self.x
        return c

class B(A):
    pass


class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(x: Par[B]):
                def _block2():
                    (Int(0) if Bool(x[:] == x[:]) else self.abort())
                    (self.abort() if Bool(x[:] == B()) else Int(0))
                    (self.abort() if Bool(A() == A()) else Int(0))
                    @mutable_params
                    def _let2(y: Par[A]):
                        def _block3():
                            (Int(0) if Bool(y[:] == x[:]) else self.abort())
                            return (Int(0) if Bool(y[:].foo(Int(3)) == x[:]) else self.abort())

                        return                         _block3()

                    return _let2(x[:])

                return                 _block2()

            _let1(B())
            @mutable_params
            def _let3(x: Par[A]):
                @mutable_params
                def _let4(y: Par[B]):
                    return (Int(0) if Bool(x[:] == y[:]) else self.abort())

                return _let4(Void)

            return _let3(Void)

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
