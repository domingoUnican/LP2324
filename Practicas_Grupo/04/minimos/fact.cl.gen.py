from Base_clases import *


class Main(IO):
    @mutable_params
    def fact(self, n: Par['Int']) -> 'Int':
        return (Int(1) if Bool(n[:] == Int(0)) else (n[:] * self.fact((n[:] - Int(1)))))

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.out_int(self.fact(Int(3)))
            self.out_string(String("\n"))
            self.out_int(self.fact(Int(7)))
            self.out_string(String("\n"))
            self.out_int(self.fact(Int(10)))
            return self.out_string(String("\n"))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
