from Base_clases import *


class P(Object):
    def __init__(self):
        super().__init__()
        self.x: Int = Int(0)

        self.x: Int = Int(3)

    def copy(self):
        c = P()
        c.x = self.x
        return c

class C1(P):
    pass


class C2(P):
    @mutable_params
    def getX(self, ) -> 'Int':
        return self.x

    @mutable_params
    def setX(self, i: Par['Int']) -> 'Int':
        self.x = _var1 = i[:]
        return _var1



class Blah(Object):
    def __init__(self):
        super().__init__()
        self.i: Int = Int(0)
        self.b: Bool = false
        self.s: String = String()
        self.j: Int = Int(0)
        self.c: Bool = false
        self.t: String = String()
        self.io: IO = Void
        self.void: Object = Void

        self.j: Int = self.tiny()
        self.c: Bool = true
        def _block1():
            Blah.add(self, )
            return String("whassup?!")

        self.t: String = _block1()
        self.io: IO = IO()

    @mutable_params
    def tiny(self, ) -> 'Int':
        def _block1():
            String("Hi")
            false
            return Int(0)

        return _block1()

    @mutable_params
    def add(self, ) -> 'Int':
        return (Int(1) + Int(2))

    @mutable_params
    def compare(self, ) -> 'Bool':
        return Bool(Int(1) < Int(2))

    @mutable_params
    def compareEq(self, ) -> 'Bool':
        return Bool(Int(1) == Int(2))

    @mutable_params
    def isv(self, ) -> 'Bool':
        return Bool(Int(1) is Void)

    @mutable_params
    def divByZero(self, ) -> 'Int':
        return (Int(1) / Int(0))

    @mutable_params
    def cmp(self, ) -> 'Bool':
        return (true).not_()

    @mutable_params
    def ng(self, ) -> 'Int':
        return ~(Int(5))

    @mutable_params
    def caller(self, ) -> 'Int':
        return (Blah.callee(self, Int(6), Int(13)) + Blah.callee(self, Int(9), Int(2)))

    @mutable_params
    def callee(self, x: Par['Int'], y: Par['Int']) -> 'Int':
        return (x[:] + y[:])

    @mutable_params
    def get_t(self, ) -> 'String':
        return self.t

    @mutable_params
    def useLet(self, ) -> 'Int':
        @mutable_params
        def _let1(q: Par[Int]):
            @mutable_params
            def _let2(r: Par[Int]):
                @mutable_params
                def _let3(s: Par[Int]):
                    return ((q[:] + r[:]) + s[:])

                return _let3(self.j)

            return _let2(Int(99))

        return _let1(Int(0))

    @mutable_params
    def useIf(self, ) -> 'Int':
        return (self.ng() if self.cmp() else self.tiny())

    @mutable_params
    def useWhile(self, ) -> 'Object':
        _loop1 = Void
        while self.cmp():
            _loop1 = self.get_t()
        return Void

    @mutable_params
    def useCase(self, ) -> 'Int':
        _match1 = check_match(self)
        if isinstance(_match1, P):
            p = _match1
            _match_result1 = Int(3)
        elif isinstance(_match1, C):
            c = _match1
            _match_result1 = Int(4)
        elif isinstance(_match1, Blah):
            b = _match1
            _match_result1 = Int(5)
        else:
            _match_result1 = Void
        return _match_result1

    @mutable_params
    def useNew(self, ) -> 'Object':
        def _block1():
            Int()
            Bool()
            C()
            Main()
            return Blah()

        return _block1()

    @mutable_params
    def doThemAll(self, ) -> 'Int':
        def _block1():
            IO.out_string(self.io, String("basics:\n"))
            self.tiny()
            self.add()
            self.compare()
            self.compareEq()
            self.isv()
            self.cmp()
            self.ng()
            self.caller()
            self.callee(Int(3), Int(4))
            self.get_t()
            self.useLet()
            self.useIf()
            self.useWhile()
            self.useCase()
            self.useNew()
            IO.out_string(self.io, String("more advanced:\n"))
            self.bigIf()
            self.bigMath()
            self.bigAssign()
            self.bigWhile()
            self.bigSelf()
            self.bigStrCompare()
            self.bigCase()
            self.bigAttrAccess()
            return Int(0)

        return _block1()

    @mutable_params
    def bigIf(self, ) -> 'Int':
        def _block1():
            self.io.out_string(String("bigIf\n"))
            ((Object.abort(self, ) if false else Int(0)) if true else Object.abort(self, ))
            (Object.abort(self, ) if false else (Object.abort(self, ) if false else Int(0)))
            ((Int(0) if true else Object.abort(self, )) if true else Object.abort(self, ))
            (Object.abort(self, ) if false else (Int(0) if true else Object.abort(self, )))
            return Int(0)

        return _block1()

    @mutable_params
    def bigWhile(self, ) -> 'Object':
        def _block1():
            self.io.out_string(String("bigWhile\n"))
            @mutable_params
            def _let1(x: Par[Int]):
                @mutable_params
                def _let2(ct: Par[Int]):
                    def _block2():
                        _loop1 = Void
                        while (Bool(x[:] <= Int(10))).not_():
                            def _block3():
                                x[:] = _var1 = (x[:] - Int(1))
                                _var1
                                ct[:] = _var2 = (ct[:] + Int(1))
                                return _var2

                            _loop1 = _block3()
                        Void
                        return (self.abort() if (Bool(x[:] == Int(10))).not_() else (self.abort() if (Bool(ct[:] == Int(24))).not_() else self))

                    return                     _block2()

                return _let2(Int(0))

            _let1(Int(34))
            @mutable_params
            def _let3(i: Par[Int]):
                @mutable_params
                def _let4(j: Par[Int]):
                    @mutable_params
                    def _let5(k: Par[Int]):
                        @mutable_params
                        def _let6(ctI: Par[Int]):
                            @mutable_params
                            def _let7(ctJ: Par[Int]):
                                @mutable_params
                                def _let8(ctK: Par[Int]):
                                    def _block4():
                                        i[:] = _var3 = Int(0)
                                        _var3
                                        _loop2 = Void
                                        while Bool(i[:] < Int(10)):
                                            def _block5():
                                                j[:] = _var4 = Int(0)
                                                _var4
                                                _loop3 = Void
                                                while Bool(j[:] < Int(10)):
                                                    def _block6():
                                                        k[:] = _var5 = Int(0)
                                                        _var5
                                                        _loop4 = Void
                                                        while Bool(k[:] < Int(10)):
                                                            def _block7():
                                                                k[:] = _var6 = (k[:] + Int(1))
                                                                _var6
                                                                ctK[:] = _var7 = (ctK[:] + Int(1))
                                                                return _var7

                                                            _loop4 = _block7()
                                                        Void
                                                        j[:] = _var8 = (j[:] + Int(1))
                                                        _var8
                                                        ctJ[:] = _var9 = (ctJ[:] + Int(1))
                                                        return _var9

                                                    _loop3 = _block6()
                                                Void
                                                i[:] = _var10 = (i[:] + Int(1))
                                                _var10
                                                ctI[:] = _var11 = (ctI[:] + Int(1))
                                                return _var11

                                            _loop2 = _block5()
                                        Void
                                        self.assert_(Bool(ctI[:] == Int(10)), Int(12))
                                        self.assert_(Bool(ctJ[:] == Int(100)), Int(123))
                                        return self.assert_(Bool(ctK[:] == Int(1000)), Int(1234))

                                    return                                     _block4()

                                return _let8(Int(0))

                            return _let7(Int(0))

                        return _let6(Int(0))

                    return _let5(Int(0))

                return _let4(Int(0))

            return _let3(Int(0))

        return _block1()

    @mutable_params
    def bail(self, i: Par['Int']) -> 'Object':
        def _block1():
            self.io.out_string(String("failed: "))
            self.io.out_int(i[:])
            self.io.out_string(String("\n"))
            return self.abort()

        return _block1()

    @mutable_params
    def bigMath(self, ) -> 'Object':
        def _block1():
            (Int(0) if Bool((Int(1) + Int(2)) == Int(3)) else self.bail(Int(55)))
            self.io.out_string(String("bigMath\n"))
            ((((((((((true if Bool((Int(1) + (Int(2) + (Int(3) + (Int(4) + (Int(5) + (Int(6) + (Int(7) + (Int(8) + (Int(9) + Int(10)))))))))) == Int(55)) else self.bail(Int(1))) if Bool((Int(1) + (Int(2) + (Int(3) + (Int(4) + Int(5))))) == Int(15)) else self.bail(Int(2))) if Bool((Int(1) + (Int(2) + Int(3))) == Int(6)) else self.bail(Int(3))) if Bool((((((Int(100) / Int(2)) / Int(2)) / Int(2)) / Int(2)) / Int(2)) == Int(3)) else self.bail(Int(4))) if Bool((((Int(45) + Int(14)) - (Int(75) * Int(2))) + Int(100)) == Int(9)) else self.bail(Int(5))) if Bool((Int(99) / Int(11)) == Int(9)) else self.bail(Int(6))) if Bool((Int(11) * Int(2)) == Int(22)) else self.bail(Int(7))) if Bool((Int(5) - Int(3)) == Int(2)) else self.bail(Int(8))) if Bool((Int(1) + Int(2)) == Int(3)) else self.bail(Int(9))) if Bool(Int(1) == Int(1)) else self.bail(Int(10)))
            self.assert_((false).not_(), Int(250))
            self.assert_(((true).not_()).not_(), Int(251))
            self.assert_(Bool(Int(3) < Int(4)), Int(253))
            self.assert_((Bool(Int(3) < Int(3))).not_(), Int(254))
            self.assert_(Bool(Int(65) <= Int(66)), Int(255))
            self.assert_(Bool(Int(65) <= Int(65)), Int(255))
            self.assert_(Bool(~(Int(2)) == (Int(0) - Int(2))), Int(257))
            self.assert_(Bool(~(Int(2)) < Int(2)), Int(258))
            return self.assert_(Bool(~(Int(0)) == Int(0)), Int(259))

        return _block1()

    @mutable_params
    def assert_(self, b: Par['Bool'], line: Par['Int']) -> 'Object':
        def _block1():
            self.io.out_string(String("assertion failed: "))
            self.io.out_int(line[:])
            self.io.out_string(String("\n"))
            return self.abort()

        return (true if b[:] else _block1())

    @mutable_params
    def bigAssign(self, ) -> 'Object':
        @mutable_params
        def _let1(x: Par[Int]):
            @mutable_params
            def _let2(y: Par[Int]):
                @mutable_params
                def _let3(z: Par[Int]):
                    def _block1():
                        self.io.out_string(String("bigAssign\n"))
                        self.assert_(Bool(x[:] == Int(0)), Int(1))
                        self.assert_(Bool(y[:] == Int(0)), Int(2))
                        self.assert_(Bool(z[:] == Int(0)), Int(3))
                        x[:] = _var1 = Int(1)
                        _var1
                        y[:] = _var2 = Int(2)
                        _var2
                        z[:] = _var3 = Int(3)
                        _var3
                        self.assert_(Bool(x[:] == Int(1)), Int(4))
                        self.assert_(Bool(y[:] == Int(2)), Int(5))
                        self.assert_(Bool(z[:] == Int(3)), Int(6))
                        z[:] = _var4 = Int(1)
                        _var4
                        y[:] = _var5 = Int(2)
                        _var5
                        x[:] = _var6 = Int(3)
                        _var6
                        self.assert_(Bool(z[:] == Int(1)), Int(14))
                        self.assert_(Bool(y[:] == Int(2)), Int(15))
                        self.assert_(Bool(x[:] == Int(3)), Int(16))
                        y[:] = _var8 = Int(6)
                        x[:] = _var7 = _var8
                        _var7
                        self.assert_(Bool(x[:] == Int(6)), Int(114))
                        self.assert_(Bool(y[:] == Int(6)), Int(115))
                        self.assert_(Bool(z[:] == Int(1)), Int(116))
                        x[:] = _var9 = (y[:] + Int(4))
                        _var9
                        y[:] = _var10 = (x[:] - Int(3))
                        _var10
                        z[:] = _var11 = ((x[:] * y[:]) + Int(14))
                        _var11
                        y[:] = _var12 = (y[:] + Int(1))
                        _var12
                        self.assert_(Bool(x[:] == Int(10)), Int(2114))
                        self.assert_(Bool(y[:] == Int(8)), Int(3114))
                        self.assert_(Bool(z[:] == Int(84)), Int(2116))
                        x[:] = _var13 = y[:]
                        _var13
                        y[:] = _var14 = z[:]
                        _var14
                        z[:] = _var15 = x[:]
                        _var15
                        self.assert_(Bool(x[:] == Int(8)), Int(101))
                        self.assert_(Bool(y[:] == Int(84)), Int(102))
                        self.assert_(Bool(z[:] == Int(8)), Int(103))
                        self.assert_(Bool((x[:] + y[:]) == Int(92)), Int(104))
                        self.assert_(Bool(x[:] == Int(8)), Int(105))
                        return self.assert_(Bool(y[:] == Int(84)), Int(106))

                    return                     _block1()

                return _let3(Int(0))

            return _let2(Int(0))

        return _let1(Int(0))

    @mutable_params
    def setI(self, newI: Par['Int']) -> 'Int':
        self.i = _var1 = newI[:]
        return _var1

    @mutable_params
    def getI(self, ) -> 'Int':
        return self.i

    @mutable_params
    def bigSelf(self, ) -> 'Object':
        @mutable_params
        def _let1(v: Par[Blah]):
            @mutable_params
            def _let2(s: Par[Blah]):
                @mutable_params
                def _let3(t: Par[Blah]):
                    def _block1():
                        self.io.out_string(String("bigSelf\n"))
                        self.assert_(Bool(v[:] is Void), Int(310))
                        self.assert_((Bool(v[:] == s[:])).not_(), Int(311))
                        self.assert_((Bool(s[:] == t[:])).not_(), Int(312))
                        self.assert_((Bool(v[:] == t[:])).not_(), Int(313))
                        s[:].setI(Int(3))
                        t[:].setI(Int(4))
                        self.assert_((Bool(s[:].getI() == t[:].getI())).not_(), Int(320))
                        t[:] = _var1 = self
                        _var1
                        self.assert_(Bool(s[:] == t[:]), Int(314))
                        s[:].setI(Int(5))
                        t[:].setI(Int(6))
                        return self.assert_(Bool(s[:].getI() == t[:].getI()), Int(327))

                    return                     _block1()

                return _let3(Blah())

            return _let2(self)

        return _let1(Void)

    @mutable_params
    def bigStrCompare(self, ) -> 'Object':
        @mutable_params
        def _let1(s: Par[String]):
            @mutable_params
            def _let2(t: Par[String]):
                @mutable_params
                def _let3(u: Par[String]):
                    @mutable_params
                    def _let4(v: Par[String]):
                        @mutable_params
                        def _let5(w: Par[String]):
                            def _block1():
                                self.io.out_string(String("bigStrCompare\n"))
                                self.assert_((Bool(s[:] == t[:])).not_(), Int(339))
                                self.assert_(Bool(s[:] == String("foo")), Int(340))
                                self.assert_(Bool(t[:] == String("bar")), Int(341))
                                self.assert_(Bool(v[:] == w[:]), Int(342))
                                self.assert_((Bool(v[:] == u[:])).not_(), Int(346))
                                v[:] = _var1 = u[:].substr(Int(0), Int(3))
                                _var1
                                w[:] = _var2 = u[:].substr(Int(3), Int(3))
                                _var2
                                self.assert_((Bool(v[:] == w[:])).not_(), Int(350))
                                self.assert_(Bool(v[:] == s[:]), Int(351))
                                self.assert_(Bool(w[:] == t[:]), Int(352))
                                self.assert_((Bool(v[:] == t[:])).not_(), Int(353))
                                return self.assert_(Bool(s[:].substr(Int(1), Int(1)) == s[:].substr(Int(2), Int(1))), Int(355))

                            return                             _block1()

                        return _let5(String())

                    return _let4(String())

                return _let3(String("foobar"))

            return _let2(String("bar"))

        return _let1(String("foo"))

    @mutable_params
    def bigCase(self, ) -> 'Object':
        @mutable_params
        def _let1(a: Par[A]):
            @mutable_params
            def _let2(b: Par[B]):
                @mutable_params
                def _let3(c: Par[C]):
                    @mutable_params
                    def _let4(p: Par[P]):
                        @mutable_params
                        def _let5(c1: Par[C1]):
                            @mutable_params
                            def _let6(c2: Par[C2]):
                                @mutable_params
                                def _let7(i: Par[Int]):
                                    @mutable_params
                                    def _let8(o: Par[Object]):
                                        def _block1():
                                            self.io.out_string(String("bigCase\n"))
                                            o[:] = _var1 = c1[:]
                                            _var1
                                            _match1 = check_match(o[:])
                                            if isinstance(_match1, A):
                                                x = _match1
                                                _match_result1 = Int(1)
                                            elif isinstance(_match1, C1):
                                                y = _match1
                                                _match_result1 = Int(2)
                                            elif isinstance(_match1, C2):
                                                z = _match1
                                                _match_result1 = Int(3)
                                            elif isinstance(_match1, Object):
                                                k = _match1
                                                _match_result1 = Int(4)
                                            else:
                                                _match_result1 = Void
                                            i[:] = _var2 = _match_result1
                                            _var2
                                            self.assert_(Bool(i[:] == Int(2)), Int(381))
                                            o[:] = _var3 = c1[:]
                                            _var3
                                            _match2 = check_match(o[:])
                                            if isinstance(_match2, A):
                                                x = _match2
                                                _match_result2 = Int(1)
                                            elif isinstance(_match2, P):
                                                y = _match2
                                                _match_result2 = Int(2)
                                            elif isinstance(_match2, C2):
                                                z = _match2
                                                _match_result2 = Int(3)
                                            elif isinstance(_match2, Object):
                                                k = _match2
                                                _match_result2 = Int(4)
                                            else:
                                                _match_result2 = Void
                                            i[:] = _var4 = _match_result2
                                            _var4
                                            self.assert_(Bool(i[:] == Int(2)), Int(390))
                                            o[:] = _var5 = c2[:]
                                            _var5
                                            _match3 = check_match(o[:])
                                            if isinstance(_match3, A):
                                                x = _match3
                                                _match_result3 = Int(1)
                                            elif isinstance(_match3, P):
                                                y = _match3
                                                _match_result3 = Int(2)
                                            elif isinstance(_match3, C2):
                                                z = _match3
                                                _match_result3 = Int(3)
                                            elif isinstance(_match3, Object):
                                                k = _match3
                                                _match_result3 = Int(4)
                                            else:
                                                _match_result3 = Void
                                            i[:] = _var6 = _match_result3
                                            _var6
                                            self.assert_(Bool(i[:] == Int(3)), Int(399))
                                            o[:] = _var7 = c1[:]
                                            _var7
                                            _match4 = check_match(b[:])
                                            if isinstance(_match4, A):
                                                x = _match4
                                                _match_result4 = Int(1)
                                            elif isinstance(_match4, C1):
                                                y = _match4
                                                _match_result4 = Int(2)
                                            elif isinstance(_match4, C2):
                                                z = _match4
                                                _match_result4 = Int(3)
                                            elif isinstance(_match4, Object):
                                                k = _match4
                                                _match_result4 = Int(4)
                                            else:
                                                _match_result4 = Void
                                            i[:] = _var8 = _match_result4
                                            _var8
                                            self.assert_(Bool(i[:] == Int(1)), Int(408))
                                            o[:] = _var9 = b[:]
                                            _var9
                                            _match5 = check_match(o[:])
                                            if isinstance(_match5, A):
                                                x = _match5
                                                _match_result5 = Int(1)
                                            elif isinstance(_match5, B):
                                                x = _match5
                                                _match_result5 = Int(2)
                                            elif isinstance(_match5, C):
                                                x = _match5
                                                _match_result5 = Int(3)
                                            else:
                                                _match_result5 = Void
                                            i[:] = _var10 = _match_result5
                                            _var10
                                            self.assert_(Bool(i[:] == Int(2)), Int(417))
                                            o[:] = _var11 = c[:]
                                            _var11
                                            _match6 = check_match(o[:])
                                            if isinstance(_match6, A):
                                                x = _match6
                                                _match_result6 = Int(1)
                                            elif isinstance(_match6, B):
                                                x = _match6
                                                _match_result6 = Int(2)
                                            elif isinstance(_match6, C):
                                                x = _match6
                                                _match_result6 = Int(3)
                                            elif isinstance(_match6, Object):
                                                k = _match6
                                                _match_result6 = Int(4)
                                            else:
                                                _match_result6 = Void
                                            i[:] = _var12 = _match_result6
                                            _var12
                                            self.assert_(Bool(i[:] == Int(3)), Int(426))
                                            o[:] = _var13 = c1[:]
                                            _var13
                                            _match7 = check_match(o[:])
                                            if isinstance(_match7, A):
                                                x = _match7
                                                _match_result7 = Int(1)
                                            elif isinstance(_match7, B):
                                                x = _match7
                                                _match_result7 = Int(2)
                                            elif isinstance(_match7, C):
                                                x = _match7
                                                _match_result7 = Int(3)
                                            elif isinstance(_match7, Object):
                                                k = _match7
                                                _match_result7 = Int(4)
                                            else:
                                                _match_result7 = Void
                                            i[:] = _var14 = _match_result7
                                            _var14
                                            self.assert_(Bool(i[:] == Int(4)), Int(438))
                                            o[:] = _var15 = b[:]
                                            _var15
                                            _match8 = check_match(o[:])
                                            if isinstance(_match8, Object):
                                                k = _match8
                                                _match_result8 = Int(4)
                                            else:
                                                _match_result8 = Void
                                            i[:] = _var16 = _match_result8
                                            _var16
                                            self.assert_(Bool(i[:] == Int(4)), Int(444))
                                            o[:] = _var17 = true
                                            _var17
                                            _match9 = check_match(o[:])
                                            if isinstance(_match9, Bool):
                                                x = _match9
                                                _match_result9 = Int(1)
                                            elif isinstance(_match9, B):
                                                x = _match9
                                                _match_result9 = Int(2)
                                            elif isinstance(_match9, C):
                                                x = _match9
                                                _match_result9 = Int(3)
                                            else:
                                                _match_result9 = Void
                                            i[:] = _var18 = _match_result9
                                            _var18
                                            self.assert_(Bool(i[:] == Int(1)), Int(453))
                                            o[:] = _var19 = Int(2)
                                            _var19
                                            _match10 = check_match(Int(3))
                                            if isinstance(_match10, Object):
                                                k = _match10
                                                _match_result10 = Int(4)
                                            else:
                                                _match_result10 = Void
                                            i[:] = _var20 = _match_result10
                                            _var20
                                            self.assert_(Bool(i[:] == Int(4)), Int(459))
                                            o[:] = _var21 = String("foobar")
                                            _var21
                                            _match11 = check_match(String("foobar").substr(Int(2), Int(2)))
                                            if isinstance(_match11, Bool):
                                                x = _match11
                                                _match_result11 = Int(1)
                                            elif isinstance(_match11, String):
                                                y = _match11
                                                _match_result11 = Int(2)
                                            elif isinstance(_match11, C):
                                                x = _match11
                                                _match_result11 = Int(3)
                                            elif isinstance(_match11, Object):
                                                k = _match11
                                                _match_result11 = Int(4)
                                            else:
                                                _match_result11 = Void
                                            i[:] = _var22 = _match_result11
                                            _var22
                                            return self.assert_(Bool(i[:] == Int(2)), Int(468))

                                        return                                         _block1()

                                    return _let8(Void)

                                return _let7(Int(0))

                            return _let6(C2())

                        return _let5(C1())

                    return _let4(P())

                return _let3(C())

            return _let2(B())

        return _let1(A())

    @mutable_params
    def bigAttrAccess(self, ) -> 'Object':
        @mutable_params
        def _let1(c: Par[C2]):
            def _block1():
                self.io.out_string(String("bigAttrAccess\n"))
                self.assert_(Bool(c[:].getX() == Int(3)), Int(496))
                c[:].setX(Int(5))
                return self.assert_(Bool(c[:].getX() == Int(5)), Int(498))

            return             _block1()

        return _let1(C2())

    def copy(self):
        c = Blah()
        c.i = self.i
        c.b = self.b
        c.s = self.s
        c.j = self.j
        c.c = self.c
        c.t = self.t
        c.io = self.io
        c.void = self.void
        return c

class A(Object):
    @mutable_params
    def e(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def f(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def g(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def i(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def j(self, ) -> 'Int':
        return Int(0)



class B(A):
    @mutable_params
    def e(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def g(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def h(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def k(self, ) -> 'Int':
        return Int(0)



class C(B):
    @mutable_params
    def e(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def h(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def i(self, ) -> 'Int':
        return Int(0)

    @mutable_params
    def ell(self, ) -> 'Int':
        return Int(0)



class Base(Object):
    def __init__(self):
        super().__init__()
        self.a: Int = Int(0)
        self.b: String = String()
        self.c: Bool = false


    def copy(self):
        c = Base()
        c.a = self.a
        c.b = self.b
        c.c = self.c
        return c

class Grandparent(Base):
    def __init__(self):
        super().__init__()
        self.d: Base = Void
        self.e: Int = Int(0)
        self.f: Grandparent = Void


    def copy(self):
        c = Grandparent()
        c.d = self.d
        c.e = self.e
        c.f = self.f
        return c

class Parent(Grandparent):
    def __init__(self):
        super().__init__()
        self.g: Parent = Void
        self.h: Int = Int(0)
        self.i: Bool = false


    def copy(self):
        c = Parent()
        c.g = self.g
        c.h = self.h
        c.i = self.i
        return c

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.j: Base = Void
        self.k: Grandparent = Void
        self.l: Main = Void
        self.m: String = String()


    def copy(self):
        c = Child()
        c.j = self.j
        c.k = self.k
        c.l = self.l
        c.m = self.m
        return c

class Main(Object):
    @mutable_params
    def main(self, ) -> 'IO':
        @mutable_params
        def _let1(io: Par[IO]):
            @mutable_params
            def _let2(b: Par[Blah]):
                def _block1():
                    IO.out_string(io[:], String("hello, world\n"))
                    io[:].out_string(String("printed via dynamic dispatch\n"))
                    IO.out_string(io[:], String("tested static dispatch and 'new IO'\n"))
                    @mutable_params
                    def _let3(i: Par[Int]):
                        def _block2():
                            IO.out_string(io[:], String("an int: "))
                            IO.out_int(io[:], i[:])
                            return IO.out_string(io[:], String("\n"))

                        return                         _block2()

                    _let3(Int(3))
                    io[:].out_string(String("gonna make a Blah\n"))
                    b[:] = _var1 = Blah()
                    _var1
                    io[:].out_string(String("gonna call doThemAll\n"))
                    b[:].doThemAll()
                    return io[:].out_string(String("looks ok!\n"))

                return                 _block1()

            return _let2(Void)

        return _let1(IO())



if __name__ == '__main__':
    bootstrap(Main)
