from Base_clases import *


class List(IO):
    @mutable_params
    def isNil(self, ) -> 'Bool':
        def _block1():
            self.abort()
            return true

        return _block1()

    @mutable_params
    def cons(self, hd: Par['Int']) -> 'Cons':
        @mutable_params
        def _let1(new_cell: Par[Cons]):
            return new_cell[:].init(hd[:], self)

        return _let1(Cons())

    @mutable_params
    def car(self, ) -> 'Int':
        def _block1():
            self.abort()
            return Int()

        return _block1()

    @mutable_params
    def cdr(self, ) -> 'List':
        def _block1():
            self.abort()
            return List()

        return _block1()

    @mutable_params
    def rev(self, ) -> 'List':
        return self.cdr()

    @mutable_params
    def sort(self, ) -> 'List':
        return self.cdr()

    @mutable_params
    def insert(self, i: Par['Int']) -> 'List':
        return self.cdr()

    @mutable_params
    def rcons(self, i: Par['Int']) -> 'List':
        return self.cdr()

    @mutable_params
    def print_list(self, ) -> 'Object':
        return self.abort()



class Cons(List):
    def __init__(self):
        super().__init__()
        self.xcar: Int = Int(0)
        self.xcdr: List = Void


    @mutable_params
    def isNil(self, ) -> 'Bool':
        return false

    @mutable_params
    def init(self, hd: Par['Int'], tl: Par['List']) -> 'Cons':
        def _block1():
            self.xcar = _var1 = hd[:]
            _var1
            self.xcdr = _var2 = tl[:]
            _var2
            return self

        return _block1()

    @mutable_params
    def car(self, ) -> 'Int':
        return self.xcar

    @mutable_params
    def cdr(self, ) -> 'List':
        return self.xcdr

    @mutable_params
    def rev(self, ) -> 'List':
        return self.xcdr.rev().rcons(self.xcar)

    @mutable_params
    def sort(self, ) -> 'List':
        return self.xcdr.sort().insert(self.xcar)

    @mutable_params
    def insert(self, i: Par['Int']) -> 'List':
        return ((Cons()).init(i[:], self) if Bool(i[:] < self.xcar) else (Cons()).init(self.xcar, self.xcdr.insert(i[:])))

    @mutable_params
    def rcons(self, i: Par['Int']) -> 'List':
        return (Cons()).init(self.xcar, self.xcdr.rcons(i[:]))

    @mutable_params
    def print_list(self, ) -> 'Object':
        def _block1():
            self.out_int(self.xcar)
            self.out_string(String("\n"))
            return self.xcdr.print_list()

        return _block1()

    def copy(self):
        c = Cons()
        c.xcar = self.xcar
        c.xcdr = self.xcdr
        return c

class Nil(List):
    @mutable_params
    def isNil(self, ) -> 'Bool':
        return true

    @mutable_params
    def rev(self, ) -> 'List':
        return self

    @mutable_params
    def sort(self, ) -> 'List':
        return self

    @mutable_params
    def insert(self, i: Par['Int']) -> 'List':
        return self.rcons(i[:])

    @mutable_params
    def rcons(self, i: Par['Int']) -> 'List':
        return (Cons()).init(i[:], self)

    @mutable_params
    def print_list(self, ) -> 'Object':
        return true



class Main(IO):
    def __init__(self):
        super().__init__()
        self.l: List = Void


    @mutable_params
    def iota(self, i: Par['Int']) -> 'List':
        def _block1():
            self.l = _var1 = Nil()
            _var1
            @mutable_params
            def _let1(j: Par[Int]):
                _loop1 = Void
                while Bool(j[:] < i[:]):
                    def _block2():
                        self.l = _var2 = (Cons()).init(j[:], self.l)
                        _var2
                        j[:] = _var3 = (j[:] + Int(1))
                        return _var3

                    _loop1 = _block2()
                return Void

            _let1(Int(0))
            return self.l

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            return self.iota(Int(20)).rev().sort().print_list()

        return _block1()

    def copy(self):
        c = Main()
        c.l = self.l
        return c

if __name__ == '__main__':
    bootstrap(Main)
