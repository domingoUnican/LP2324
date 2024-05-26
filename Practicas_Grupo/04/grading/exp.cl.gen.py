from Base_clases import *


class Main(IO):
    @mutable_params
    def exp(self, b: Par['Int'], x: Par['Int']) -> 'Int':
        @mutable_params
        def _let1(y: Par[Int]):
            return (y[:] * y[:])

        return (Int(1) if Bool(x[:] == Int(0)) else (_let1(self.exp(b[:], (x[:] / Int(2)))) if Bool(x[:] == (Int(2) * (x[:] / Int(2)))) else (b[:] * self.exp(b[:], (x[:] - Int(1))))))

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.out_int(self.exp(Int(2), Int(7)))
            self.out_string(String("\n"))
            self.out_int(self.exp(Int(3), Int(6)))
            self.out_string(String("\n"))
            self.out_int(self.exp(Int(8), Int(3)))
            return self.out_string(String("\n"))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
