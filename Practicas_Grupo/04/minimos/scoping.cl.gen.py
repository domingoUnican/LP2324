from Base_clases import *


class Bob(IO):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)
        self.y: Int = Int(0)

        self.y: Int = Int(4)

    def copy(self):
        c = Bob()
        c.x = self.x
        c.y = self.y
        return c

class Main(Bob):
    def __init__(self):
        super().__init__()
        self.z: Int = Int(0)

        self.z: Int = Int(23)

    @mutable_params
    def jack(self, q: Par['Int'], z: Par['Int']) -> 'Int':
        def _block1():
            @mutable_params
            def _let1(z: Par[Int]):
                return self.print_z(z[:])

            _let1((z[:] + self.y))
            self.y = _var1 = (self.y + Int(4))
            _var1
            @mutable_params
            def _let2(y: Par[Int]):
                return y[:]

            return _let2((z[:] + self.y))

        return _block1()

    @mutable_params
    def print_z(self, z: Par['Int']) -> 'Main':
        def _block1():
            self.out_string(String("z = "))
            self.out_int(z[:])
            return self.out_string(String("\n"))

        return _block1()

    @mutable_params
    def main(self, ) -> 'Bob':
        def _block1():
            self.print_z(self.z)
            @mutable_params
            def _let1(z: Par[Int]):
                return self.print_z(z[:])

            return _let1(self.jack(Int(5), (self.z + Int(2))))

        return _block1()

    def copy(self):
        c = Main()
        c.z = self.z
        return c

if __name__ == '__main__':
    bootstrap(Main)
