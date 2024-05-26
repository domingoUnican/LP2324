from Base_clases import *


class EvalObject(IO):
    @mutable_params
    def eval(self, ) -> 'EvalObject':
        def _block1():
            self.abort()
            return self

        return _block1()



class Closure(EvalObject):
    def __init__(self):
        super().__init__()
        self.parent: Closure = Void
        self.x: EvalObject = Void


    @mutable_params
    def get_parent(self, ) -> 'Closure':
        return self.parent

    @mutable_params
    def get_x(self, ) -> 'EvalObject':
        return self.x

    @mutable_params
    def init(self, p: Par['Closure']) -> 'Closure':
        def _block1():
            self.parent = _var1 = p[:]
            _var1
            return self

        return _block1()

    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.abort()
            return self

        return _block1()

    def copy(self):
        c = Closure()
        c.parent = self.parent
        c.x = self.x
        return c

class Main(Object):
    @mutable_params
    def main(self, ) -> 'EvalObject':
        @mutable_params
        def _let1(x: Par[EvalObject]):
            @mutable_params
            def _let2(y: Par[EvalObject]):
                _match1 = check_match(x[:])
                if isinstance(_match1, Closure):
                    c = _match1
                    _match_result1 = c.apply(y[:])
                elif isinstance(_match1, Object):
                    o = _match1
                    def _block1():
                        self.abort()
                        return EvalObject()

                    _match_result1 =                     _block1()
                else:
                    _match_result1 = Void
                return _match_result1

            return _let2((Closure8()).init(Closure()))

        @mutable_params
        def _let3(x: Par[EvalObject]):
            @mutable_params
            def _let4(y: Par[EvalObject]):
                _match2 = check_match(x[:])
                if isinstance(_match2, Closure):
                    c = _match2
                    _match_result2 = c.apply(y[:])
                elif isinstance(_match2, Object):
                    o = _match2
                    def _block2():
                        self.abort()
                        return EvalObject()

                    _match_result2 =                     _block2()
                else:
                    _match_result2 = Void
                return _match_result2

            return _let4((Closure7()).init(Closure()))

        @mutable_params
        def _let5(x: Par[EvalObject]):
            @mutable_params
            def _let6(y: Par[EvalObject]):
                _match3 = check_match(x[:])
                if isinstance(_match3, Closure):
                    c = _match3
                    _match_result3 = c.apply(y[:])
                elif isinstance(_match3, Object):
                    o = _match3
                    def _block3():
                        self.abort()
                        return EvalObject()

                    _match_result3 =                     _block3()
                else:
                    _match_result3 = Void
                return _match_result3

            return _let6((Closure6()).init(Closure()))

        @mutable_params
        def _let7(x: Par[EvalObject]):
            @mutable_params
            def _let8(y: Par[EvalObject]):
                _match4 = check_match(x[:])
                if isinstance(_match4, Closure):
                    c = _match4
                    _match_result4 = c.apply(y[:])
                elif isinstance(_match4, Object):
                    o = _match4
                    def _block4():
                        self.abort()
                        return EvalObject()

                    _match_result4 =                     _block4()
                else:
                    _match_result4 = Void
                return _match_result4

            return _let8((Closure5()).init(Closure()))

        @mutable_params
        def _let9(x: Par[EvalObject]):
            @mutable_params
            def _let10(y: Par[EvalObject]):
                _match5 = check_match(x[:])
                if isinstance(_match5, Closure):
                    c = _match5
                    _match_result5 = c.apply(y[:])
                elif isinstance(_match5, Object):
                    o = _match5
                    def _block5():
                        self.abort()
                        return EvalObject()

                    _match_result5 =                     _block5()
                else:
                    _match_result5 = Void
                return _match_result5

            return _let10((Closure4()).init(Closure()))

        @mutable_params
        def _let11(x: Par[EvalObject]):
            @mutable_params
            def _let12(y: Par[EvalObject]):
                _match6 = check_match(x[:])
                if isinstance(_match6, Closure):
                    c = _match6
                    _match_result6 = c.apply(y[:])
                elif isinstance(_match6, Object):
                    o = _match6
                    def _block6():
                        self.abort()
                        return EvalObject()

                    _match_result6 =                     _block6()
                else:
                    _match_result6 = Void
                return _match_result6

            return _let12((Closure3()).init(Closure()))

        @mutable_params
        def _let13(x: Par[EvalObject]):
            @mutable_params
            def _let14(y: Par[EvalObject]):
                _match7 = check_match(x[:])
                if isinstance(_match7, Closure):
                    c = _match7
                    _match_result7 = c.apply(y[:])
                elif isinstance(_match7, Object):
                    o = _match7
                    def _block7():
                        self.abort()
                        return EvalObject()

                    _match_result7 =                     _block7()
                else:
                    _match_result7 = Void
                return _match_result7

            return _let14((Closure2()).init(Closure()))

        @mutable_params
        def _let15(x: Par[EvalObject]):
            @mutable_params
            def _let16(y: Par[EvalObject]):
                _match8 = check_match(x[:])
                if isinstance(_match8, Closure):
                    c = _match8
                    _match_result8 = c.apply(y[:])
                elif isinstance(_match8, Object):
                    o = _match8
                    def _block8():
                        self.abort()
                        return EvalObject()

                    _match_result8 =                     _block8()
                else:
                    _match_result8 = Void
                return _match_result8

            return _let16((Closure1()).init(Closure()))

        return _let1(_let3(_let5(_let7(_let9(_let11(_let13(_let15((Closure0()).init(Closure())))))))))



class Closure8(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 8\n"))
            self.x = _var1 = y[:]
            _var1
            return self.get_x()

        return _block1()



class Closure7(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 7\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure9()).init(self)

        return _block1()



class Closure9(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 9\n"))
            self.x = _var1 = y[:]
            _var1
            return self.get_parent().get_x()

        return _block1()



class Closure6(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 6\n"))
            self.x = _var1 = y[:]
            _var1
            return self.get_x()

        return _block1()



class Closure5(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 5\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure10()).init(self)

        return _block1()



class Closure10(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 10\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure11()).init(self)

        return _block1()



class Closure11(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 11\n"))
            self.x = _var1 = y[:]
            _var1
            @mutable_params
            def _let1(x: Par[EvalObject]):
                @mutable_params
                def _let2(y: Par[EvalObject]):
                    _match1 = check_match(x[:])
                    if isinstance(_match1, Closure):
                        c = _match1
                        _match_result1 = c.apply(y[:])
                    elif isinstance(_match1, Object):
                        o = _match1
                        def _block2():
                            self.abort()
                            return EvalObject()

                        _match_result1 =                         _block2()
                    else:
                        _match_result1 = Void
                    return _match_result1

                @mutable_params
                def _let3(x: Par[EvalObject]):
                    @mutable_params
                    def _let4(y: Par[EvalObject]):
                        _match2 = check_match(x[:])
                        if isinstance(_match2, Closure):
                            c = _match2
                            _match_result2 = c.apply(y[:])
                        elif isinstance(_match2, Object):
                            o = _match2
                            def _block3():
                                self.abort()
                                return EvalObject()

                            _match_result2 =                             _block3()
                        else:
                            _match_result2 = Void
                        return _match_result2

                    return _let4(self.get_x())

                return _let2(_let3(self.get_parent().get_x()))

            @mutable_params
            def _let5(x: Par[EvalObject]):
                @mutable_params
                def _let6(y: Par[EvalObject]):
                    _match3 = check_match(x[:])
                    if isinstance(_match3, Closure):
                        c = _match3
                        _match_result3 = c.apply(y[:])
                    elif isinstance(_match3, Object):
                        o = _match3
                        def _block4():
                            self.abort()
                            return EvalObject()

                        _match_result3 =                         _block4()
                    else:
                        _match_result3 = Void
                    return _match_result3

                return _let6(self.get_x())

            return _let1(_let5(self.get_parent().get_parent().get_x()))

        return _block1()



class Closure4(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 4\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure12()).init(self)

        return _block1()



class Closure12(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 12\n"))
            self.x = _var1 = y[:]
            _var1
            return self.get_parent().get_x()

        return _block1()



class Closure3(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 3\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure13()).init(self)

        return _block1()



class Closure13(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 13\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure14()).init(self)

        return _block1()



class Closure14(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 14\n"))
            self.x = _var1 = y[:]
            _var1
            @mutable_params
            def _let1(x: Par[EvalObject]):
                @mutable_params
                def _let2(y: Par[EvalObject]):
                    _match1 = check_match(x[:])
                    if isinstance(_match1, Closure):
                        c = _match1
                        _match_result1 = c.apply(y[:])
                    elif isinstance(_match1, Object):
                        o = _match1
                        def _block2():
                            self.abort()
                            return EvalObject()

                        _match_result1 =                         _block2()
                    else:
                        _match_result1 = Void
                    return _match_result1

                @mutable_params
                def _let3(x: Par[EvalObject]):
                    @mutable_params
                    def _let4(y: Par[EvalObject]):
                        _match2 = check_match(x[:])
                        if isinstance(_match2, Closure):
                            c = _match2
                            _match_result2 = c.apply(y[:])
                        elif isinstance(_match2, Object):
                            o = _match2
                            def _block3():
                                self.abort()
                                return EvalObject()

                            _match_result2 =                             _block3()
                        else:
                            _match_result2 = Void
                        return _match_result2

                    return _let4(self.get_x())

                return _let2(_let3(self.get_parent().get_x()))

            @mutable_params
            def _let5(x: Par[EvalObject]):
                @mutable_params
                def _let6(y: Par[EvalObject]):
                    _match3 = check_match(x[:])
                    if isinstance(_match3, Closure):
                        c = _match3
                        _match_result3 = c.apply(y[:])
                    elif isinstance(_match3, Object):
                        o = _match3
                        def _block4():
                            self.abort()
                            return EvalObject()

                        _match_result3 =                         _block4()
                    else:
                        _match_result3 = Void
                    return _match_result3

                return _let6(self.get_x())

            return _let1(_let5(self.get_parent().get_parent().get_x()))

        return _block1()



class Closure2(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 2\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure15()).init(self)

        return _block1()



class Closure15(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 15\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure16()).init(self)

        return _block1()



class Closure16(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 16\n"))
            self.x = _var1 = y[:]
            _var1
            @mutable_params
            def _let1(x: Par[EvalObject]):
                @mutable_params
                def _let2(y: Par[EvalObject]):
                    _match1 = check_match(x[:])
                    if isinstance(_match1, Closure):
                        c = _match1
                        _match_result1 = c.apply(y[:])
                    elif isinstance(_match1, Object):
                        o = _match1
                        def _block2():
                            self.abort()
                            return EvalObject()

                        _match_result1 =                         _block2()
                    else:
                        _match_result1 = Void
                    return _match_result1

                @mutable_params
                def _let3(x: Par[EvalObject]):
                    @mutable_params
                    def _let4(y: Par[EvalObject]):
                        _match2 = check_match(x[:])
                        if isinstance(_match2, Closure):
                            c = _match2
                            _match_result2 = c.apply(y[:])
                        elif isinstance(_match2, Object):
                            o = _match2
                            def _block3():
                                self.abort()
                                return EvalObject()

                            _match_result2 =                             _block3()
                        else:
                            _match_result2 = Void
                        return _match_result2

                    return _let4(self.get_x())

                return _let2(_let3(self.get_parent().get_x()))

            @mutable_params
            def _let5(x: Par[EvalObject]):
                @mutable_params
                def _let6(y: Par[EvalObject]):
                    _match3 = check_match(x[:])
                    if isinstance(_match3, Closure):
                        c = _match3
                        _match_result3 = c.apply(y[:])
                    elif isinstance(_match3, Object):
                        o = _match3
                        def _block4():
                            self.abort()
                            return EvalObject()

                        _match_result3 =                         _block4()
                    else:
                        _match_result3 = Void
                    return _match_result3

                return _let6(self.get_x())

            return _let1(_let5(self.get_parent().get_parent().get_x()))

        return _block1()



class Closure1(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 1\n"))
            self.x = _var1 = y[:]
            _var1
            return (Closure17()).init(self)

        return _block1()



class Closure17(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 17\n"))
            self.x = _var1 = y[:]
            _var1
            return self.get_parent().get_x()

        return _block1()



class Closure0(Closure):
    @mutable_params
    def apply(self, y: Par['EvalObject']) -> 'EvalObject':
        def _block1():
            self.out_string(String("Applying closure 0\n"))
            self.x = _var1 = y[:]
            _var1
            return self.get_x()

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
