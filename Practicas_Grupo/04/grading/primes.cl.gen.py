from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.out: Int = Int(0)
        self.testee: Int = Int(0)
        self.divisor: Int = Int(0)
        self.stop: Int = Int(0)
        self.m: Object = Void

        def _block1():
            self.out_string(String("2 is trivially prime.\n"))
            return Int(2)

        self.out: Int = _block1()
        self.testee: Int = self.out
        self.stop: Int = Int(500)
        _loop1 = Void
        while true:
            def _block2():
                self.testee = _var1 = (self.testee + Int(1))
                _var1
                self.divisor = _var2 = Int(2)
                _var2
                _loop2 = Void
                while (false if Bool(self.testee < (self.divisor * self.divisor)) else (false if Bool((self.testee - (self.divisor * (self.testee / self.divisor))) == Int(0)) else true)):
                    self.divisor = _var3 = (self.divisor + Int(1))
                    _loop2 = _var3
                Void
                def _block3():
                    self.out = _var4 = self.testee
                    _var4
                    self.out_int(self.out)
                    return self.out_string(String(" is prime.\n"))

                (                _block3() if Bool(self.testee < (self.divisor * self.divisor)) else Int(0))
                return (String("halt").abort() if Bool(self.stop <= self.testee) else String("continue"))

            _loop1 = _block2()
        self.m: Object = Void

    @mutable_params
    def main(self, ) -> 'Int':
        return Int(0)

    def copy(self):
        c = Main()
        c.out = self.out
        c.testee = self.testee
        c.divisor = self.divisor
        c.stop = self.stop
        c.m = self.m
        return c

if __name__ == '__main__':
    bootstrap(Main)
