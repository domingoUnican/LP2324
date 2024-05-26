from Base_clases import *


class A(Object):
    def __init__(self):
        super().__init__()
        self.x: A = Void


    @mutable_params
    def init(self, ) -> 'Object':
        self.x = _var1 = A()
        return _var1

    @mutable_params
    def foo(self, ) -> 'Int':
        return Int(1)

    @mutable_params
    def getx(self, ) -> 'A':
        return self.x

    def copy(self):
        c = A()
        c.x = self.x
        return c

class B(A):
    @mutable_params
    def foo(self, ) -> 'Int':
        return Int(2)



class Main(IO):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(a: Par[A]):
                def _block2():
                    a[:].init()
                    return self.out_int(a[:].getx().foo())

                return                 _block2()

            _let1(B())
            return self.out_string(String("\n"))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
