from Base_clases import *


class Main(IO):
    @mutable_params
    def f(self, x: Par['Int'], y: Par['Int']) -> 'Object':
        def _block1():
            self.out_string(String("x: "))
            self.out_int(x[:])
            self.out_string(String("\ny: "))
            self.out_int(y[:])
            return self.out_string(String("\n"))

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(x: Par[Int]):
            def _block1():
                x[:] = _var1 = Int(3)
                x[:] = _var2 = Int(4)
                self.f(_var1, _var2)
                return self.out_int(x[:])

            return             _block1()

        return _let1(Int(2))



if __name__ == '__main__':
    bootstrap(Main)
