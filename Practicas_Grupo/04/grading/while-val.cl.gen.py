from Base_clases import *


class Main(Object):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)


    @mutable_params
    def main(self, ) -> 'Object':
        _loop1 = Void
        while Bool(self.x < Int(10)):
            self.x = _var1 = (self.x + Int(1))
            _loop1 = _var1
        return (IO()).out_string((Void).type_name())

    def copy(self):
        c = Main()
        c.x = self.x
        return c

if __name__ == '__main__':
    bootstrap(Main)
