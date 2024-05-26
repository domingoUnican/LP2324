from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.a: Int = Int(0)
        self.i: Int = Int(0)

        self.i: Int = Int(100)

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            _loop1 = Void
            while Bool(~(self.i) < Int(0)):
                def _block2():
                    self.a = _var1 = Int()
                    _var1
                    @mutable_params
                    def _let1(b: Par[IO]):
                        return b[:]

                    _let1(IO())
                    self.i = _var2 = (self.i - Int(1))
                    return _var2

                _loop1 = _block2()
            Void
            return self.out_int(self.i)

        return _block1()

    def copy(self):
        c = Main()
        c.a = self.a
        c.i = self.i
        return c

if __name__ == '__main__':
    bootstrap(Main)
