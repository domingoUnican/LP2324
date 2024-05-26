from Base_clases import *


class Base(IO):
    def __init__(self):
        super().__init__()
        self.baseAttr: Int = Int(0)

        def _block1():
            self.report(Int(1))
            return Int(1)

        self.baseAttr: Int = _block1()

    @mutable_params
    def report(self, value: Par['Int']) -> 'Base':
        def _block1():
            self.out_int(value[:])
            self.out_string(String("\n"))
            return self

        return _block1()

    @mutable_params
    def duplicate(self, ) -> 'Base':
        return Base()

    def copy(self):
        c = Base()
        c.baseAttr = self.baseAttr
        return c

class Derived(Base):
    def __init__(self):
        super().__init__()
        self.derivedAttr: Int = Int(0)

        def _block1():
            self.report(Int(2))
            return Int(2)

        self.derivedAttr: Int = _block1()

    @mutable_params
    def report(self, value: Par['Int']) -> 'Derived':
        def _block1():
            self.out_string(String("old: "))
            self.out_int(self.derivedAttr)
            self.out_string(String(".  new: "))
            self.derivedAttr = _var1 = value[:]
            _var1
            return Base.report(self, self.derivedAttr)

        return _block1()

    def copy(self):
        c = Derived()
        c.derivedAttr = self.derivedAttr
        return c

class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        return (Derived()).report(Int(5)).duplicate().report(Int(29))



if __name__ == '__main__':
    bootstrap(Main)
