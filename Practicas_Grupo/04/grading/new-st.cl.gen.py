from Base_clases import *


class A(Object):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)

        self.x: Int = (self.x + Int(1))

    @mutable_params
    def printX(self, ) -> 'Object':
        def _block1():
            (IO()).out_string(String("x is "))
            (IO()).out_int(self.x)
            return (IO()).out_string(String("\n"))

        return _block1()

    @mutable_params
    def new_st(self, ) -> 'A':
        return A()

    @mutable_params
    def bump(self, ) -> 'Object':
        self.x = _var1 = (self.x + Int(1))
        return _var1

    def copy(self):
        c = A()
        c.x = self.x
        return c

class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(a1: Par[A]):
            @mutable_params
            def _let2(a2: Par[A]):
                def _block1():
                    a1[:].printX()
                    a1[:].bump()
                    a1[:].bump()
                    a1[:].bump()
                    a1[:].printX()
                    a2[:] = _var1 = a1[:].new_st()
                    _var1
                    a2[:].printX()
                    return a1[:].printX()

                return                 _block1()

            return _let2(Void)

        return _let1(A())



if __name__ == '__main__':
    bootstrap(Main)
