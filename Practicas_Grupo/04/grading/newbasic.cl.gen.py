from Base_clases import *


class Main(Object):
    def __init__(self):
        super().__init__()
        self.io: IO = Void

        self.io: IO = IO()

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.io.out_string(((Bool()).not_()).type_name())
            self.io.out_string(String("\n"))
            self.io.out_int((Int() + Int(1)))
            self.io.out_string(String("\n"))
            self.io.out_string((String()).substr(Int(0), Int(0)).type_name())
            return self.io.out_string(String("\n"))

        return _block1()

    def copy(self):
        c = Main()
        c.io = self.io
        return c

if __name__ == '__main__':
    bootstrap(Main)
