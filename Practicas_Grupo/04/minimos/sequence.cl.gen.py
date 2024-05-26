from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.a: Int = Int(0)
        self.b: Int = Int(0)

        self.a: Int = Int(0)
        self.b: Int = Int(1)

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.a = _var1 = (self.b + Int(1))
            _var1
            self.b = _var2 = (self.a + Int(1))
            _var2
            self.a = _var3 = (self.b + Int(1))
            _var3
            self.b = _var4 = (self.a + Int(1))
            _var4
            self.a = _var5 = (self.b + Int(1))
            _var5
            self.b = _var6 = (self.a + Int(1))
            _var6
            self.a = _var7 = (self.b + Int(1))
            _var7
            self.b = _var8 = (self.a + Int(1))
            _var8
            self.a = _var9 = (self.b + Int(1))
            _var9
            self.b = _var10 = (self.a + Int(1))
            _var10
            return self.out_int((self.a + self.b))

        return _block1()

    def copy(self):
        c = Main()
        c.a = self.a
        c.b = self.b
        return c

if __name__ == '__main__':
    bootstrap(Main)
