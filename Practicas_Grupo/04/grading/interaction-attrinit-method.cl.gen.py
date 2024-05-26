from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.a: Int = Int(0)

        self.a: Int = self.f()

    @mutable_params
    def f(self, ) -> 'Int':
        return (self.a + Int(1))

    @mutable_params
    def main(self, ) -> 'Object':
        return self.out_int(self.a)

    def copy(self):
        c = Main()
        c.a = self.a
        return c

if __name__ == '__main__':
    bootstrap(Main)
