from Base_clases import *


class Base(IO):
    def __init__(self):
        super().__init__()
        self.x: Object = Void
        self.b: Object = Void

        self.x: Object = self.recite(Int(1))
        self.b: Object = self.recite(Int(2))

    @mutable_params
    def recite(self, value: Par['Int']) -> 'Object':
        def _block1():
            self.out_int(value[:])
            self.out_string(String("\n"))
            return self

        return _block1()

    def copy(self):
        c = Base()
        c.x = self.x
        c.b = self.b
        return c

class Main(Base):
    def __init__(self):
        super().__init__()
        self.y: Object = Void
        self.z: Object = Void
        self.c: Object = Void

        self.y: Object = self.recite(Int(3))
        self.z: Object = self.recite(Int(4))
        self.c: Object = self.recite(Int(5))

    @mutable_params
    def main(self, ) -> 'Object':
        return self

    def copy(self):
        c = Main()
        c.y = self.y
        c.z = self.z
        c.c = self.c
        return c

if __name__ == '__main__':
    bootstrap(Main)
