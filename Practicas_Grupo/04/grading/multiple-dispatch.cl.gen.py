from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)


    @mutable_params
    def f(self, y: Par['Int']) -> 'Main':
        def _block1():
            self.out_int((self.x + y[:]))
            self.out_string(String("\n"))
            return self

        return _block1()

    @mutable_params
    def g(self, z: Par['Int']) -> 'Int':
        def _block1():
            self.x = _var1 = (self.x + Int(1))
            _var1
            return (z[:] + self.x)

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        return self.f(self.g(Int(1))).f(self.g(self.g(Int(5)))).f(self.g(self.g(self.g(Int(10)))))

    def copy(self):
        c = Main()
        c.x = self.x
        return c

if __name__ == '__main__':
    bootstrap(Main)
