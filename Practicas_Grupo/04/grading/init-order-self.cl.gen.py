from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.x: Object = Void
        self.y: Object = Void
        self.z: Object = Void
        self.c: Object = Void
        self.b: Object = Void
        self.a: Object = Void

        self.x: Object = self.recite(Int(1))
        self.y: Object = self.recite(Int(2))
        self.z: Object = self.recite(Int(3))
        self.c: Object = self.recite(Int(4))
        self.b: Object = self.recite(Int(5))
        self.a: Object = self.recite(Int(6))

    @mutable_params
    def recite(self, value: Par['Int']) -> 'Object':
        def _block1():
            self.out_int(value[:])
            self.out_string(String("\n"))
            return self

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        return self

    def copy(self):
        c = Main()
        c.x = self.x
        c.y = self.y
        c.z = self.z
        c.c = self.c
        c.b = self.b
        c.a = self.a
        return c

if __name__ == '__main__':
    bootstrap(Main)
