from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.i: Int = Int(0)
        self.s: String = String()
        self.b: Bool = false
        self.io: IO = Void


    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.out_int(self.i)
            self.out_string(self.s)
            (self.out_string(String("true")) if self.b else self.out_string(String("false")))
            return (self.out_string(String("void")) if Bool(self.io is Void) else self.out_string(String("not void")))

        return _block1()

    def copy(self):
        c = Main()
        c.i = self.i
        c.s = self.s
        c.b = self.b
        c.io = self.io
        return c

if __name__ == '__main__':
    bootstrap(Main)
