from Base_clases import *


class Foo(Bazz):
    def __init__(self):
        super().__init__()
        self.a: Razz = Void
        self.b: Int = Int(0)

        _match1 = check_match(self)
        if isinstance(_match1, Razz):
            n = _match1
            _match_result1 = Bar()
        elif isinstance(_match1, Foo):
            n = _match1
            _match_result1 = Razz()
        elif isinstance(_match1, Bar):
            n = _match1
            _match_result1 = n
        else:
            _match_result1 = Void
        self.a: Razz = _match_result1
        self.b: Int = (((self.a.doh() + self.g.doh()) + self.doh()) + self.printh())

    @mutable_params
    def doh(self, ) -> 'Int':
        @mutable_params
        def _let1(i: Par[Int]):
            def _block1():
                self.h = _var1 = (self.h + Int(2))
                _var1
                return i[:]

            return             _block1()

        return _let1(self.h)

    def copy(self):
        c = Foo()
        c.a = self.a
        c.b = self.b
        return c

class Bar(Razz):
    def __init__(self):
        super().__init__()
        self.c: Int = Int(0)
        self.d: Object = Void

        self.c: Int = self.doh()
        self.d: Object = self.printh()

    def copy(self):
        c = Bar()
        c.c = self.c
        c.d = self.d
        return c

class Razz(Foo):
    def __init__(self):
        super().__init__()
        self.e: Bar = Void
        self.f: Int = Int(0)

        _match1 = check_match(self)
        if isinstance(_match1, Razz):
            n = _match1
            _match_result1 = Bar()
        elif isinstance(_match1, Bar):
            n = _match1
            _match_result1 = n
        else:
            _match_result1 = Void
        self.e: Bar = _match_result1
        self.f: Int = ((((Bazz.doh(self.a, ) + self.g.doh()) + self.e.doh()) + self.doh()) + self.printh())

    def copy(self):
        c = Razz()
        c.e = self.e
        c.f = self.f
        return c

class Bazz(IO):
    def __init__(self):
        super().__init__()
        self.h: Int = Int(0)
        self.g: Foo = Void
        self.i: Object = Void

        self.h: Int = Int(1)
        _match1 = check_match(self)
        if isinstance(_match1, Bazz):
            n = _match1
            _match_result1 = Foo()
        elif isinstance(_match1, Razz):
            n = _match1
            _match_result1 = Bar()
        elif isinstance(_match1, Foo):
            n = _match1
            _match_result1 = Razz()
        elif isinstance(_match1, Bar):
            n = _match1
            _match_result1 = n
        else:
            _match_result1 = Void
        self.g: Foo = _match_result1
        self.i: Object = self.printh()

    @mutable_params
    def printh(self, ) -> 'Int':
        def _block1():
            self.out_int(self.h)
            return Int(0)

        return _block1()

    @mutable_params
    def doh(self, ) -> 'Int':
        @mutable_params
        def _let1(i: Par[Int]):
            def _block1():
                self.h = _var1 = (self.h + Int(1))
                _var1
                return i[:]

            return             _block1()

        return _let1(self.h)

    def copy(self):
        c = Bazz()
        c.h = self.h
        c.g = self.g
        c.i = self.i
        return c

class Main(Object):
    def __init__(self):
        super().__init__()
        self.a: Bazz = Void
        self.b: Foo = Void
        self.c: Razz = Void
        self.d: Bar = Void

        self.a: Bazz = Bazz()
        self.b: Foo = Foo()
        self.c: Razz = Razz()
        self.d: Bar = Bar()

    @mutable_params
    def main(self, ) -> 'String':
        return String("do nothing")

    def copy(self):
        c = Main()
        c.a = self.a
        c.b = self.b
        c.c = self.c
        c.d = self.d
        return c

if __name__ == '__main__':
    bootstrap(Main)
