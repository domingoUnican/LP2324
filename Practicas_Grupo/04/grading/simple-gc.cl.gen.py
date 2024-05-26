from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.y: Int = Int(0)


    @mutable_params
    def f(self, x: Par['Int']) -> 'Int':
        self.y = _var1 = ((((x[:] + Int(6)) + Int(7)) + Int(8)) + Int(9))
        return _var1

    @mutable_params
    def main(self, ) -> 'Object':
        self.y = _var1 = ((((Int(1) + Int(2)) + Int(3)) + Int(4)) + self.f(Int(5)))
        return self.out_int(_var1)

    def copy(self):
        c = Main()
        c.y = self.y
        return c

if __name__ == '__main__':
    bootstrap(Main)
