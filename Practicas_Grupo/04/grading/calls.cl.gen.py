from Base_clases import *


class Main(Object):
    def __init__(self):
        super().__init__()
        self.io: IO = Void

        self.io: IO = IO()

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.io.out_int(self.f(self.g(Int(1)), self.h(Int(2))))
            return self.io.out_string(String("\n"))

        return _block1()

    @mutable_params
    def f(self, x: Par['Int'], y: Par['Int']) -> 'Int':
        return (x[:] + y[:])

    @mutable_params
    def g(self, x: Par['Int']) -> 'Int':
        return (x[:] + Int(5))

    @mutable_params
    def h(self, x: Par['Int']) -> 'Int':
        return (x[:] + Int(7))

    def copy(self):
        c = Main()
        c.io = self.io
        return c

if __name__ == '__main__':
    bootstrap(Main)
