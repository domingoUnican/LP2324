from Base_clases import *


class Main(IO):
    @mutable_params
    def recite(self, value: Par['Int']) -> 'Int':
        def _block1():
            self.out_int(value[:])
            self.out_string(String("\n"))
            return value[:]

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            (self.recite(Int(1)) + self.recite(Int(2)))
            (self.recite(Int(3)) - self.recite(Int(4)))
            (self.recite(Int(5)) * self.recite(Int(6)))
            (self.recite(Int(7)) / self.recite(Int(8)))
            Bool(self.recite(Int(9)) < self.recite(Int(10)))
            Bool(self.recite(Int(11)) == self.recite(Int(12)))
            return Bool(self.recite(Int(13)) <= self.recite(Int(14)))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
