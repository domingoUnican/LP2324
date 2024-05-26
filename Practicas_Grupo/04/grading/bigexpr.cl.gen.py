from Base_clases import *


class Main(IO):
    @mutable_params
    def main(self, ) -> 'IO':
        @mutable_params
        def _let1(x: Par[Int]):
            x[:] = _var1 = Int(1)
            x[:] = _var2 = (x[:] + Int(1))
            return self.out_int((_var1 + (_var2 + (Int(3) + (Int(4) + (Int(5) + (Int(6) + (Int(7) + (x[:] + Int(6))))))))))

        return _let1(Int(5))



if __name__ == '__main__':
    bootstrap(Main)
