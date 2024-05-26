from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.a: Int = Int(0)


    @mutable_params
    def f(self, i: Par['Int']) -> 'Object':
        i[:] = _var1 = Int(1)
        return _var1

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.f(self.a)
            return self.out_int(self.a)

        return _block1()

    def copy(self):
        c = Main()
        c.a = self.a
        return c

if __name__ == '__main__':
    bootstrap(Main)
