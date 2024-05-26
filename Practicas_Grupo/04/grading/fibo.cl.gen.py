from Base_clases import *


class Main(IO):
    @mutable_params
    def fibo(self, i: Par['Int']) -> 'Int':
        return (Int(0) if Bool(i[:] == Int(0)) else (Int(1) if Bool(i[:] == Int(1)) else (self.fibo((i[:] - Int(1))) + self.fibo((i[:] - Int(2))))))

    @mutable_params
    def main(self, ) -> 'Object':
        return self.out_int(self.fibo(Int(15)))



if __name__ == '__main__':
    bootstrap(Main)
