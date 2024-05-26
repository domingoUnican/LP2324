from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.s: String = String()

        self.s: String = String("this is a")

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.out_int(self.s.length())
            self.out_string(String("\n").concat(self.s.concat(String(" string\n"))))
            return self.out_string(self.s.substr(Int(5), Int(2)).concat(String("\n")))

        return _block1()

    def copy(self):
        c = Main()
        c.s = self.s
        return c

if __name__ == '__main__':
    bootstrap(Main)
