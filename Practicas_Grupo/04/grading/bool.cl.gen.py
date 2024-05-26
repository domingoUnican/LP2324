from Base_clases import *


class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(t: Par[Bool]):
            @mutable_params
            def _let2(f: Par[Bool]):
                @mutable_params
                def _let3(t1: Par[Object]):
                    @mutable_params
                    def _let4(t2: Par[Object]):
                        @mutable_params
                        def _let5(f1: Par[Object]):
                            @mutable_params
                            def _let6(f2: Par[Object]):
                                @mutable_params
                                def _let7(b1: Par[Bool]):
                                    @mutable_params
                                    def _let8(b2: Par[Object]):
                                        @mutable_params
                                        def _let9(io: Par[IO]):
                                            def _block1():
                                                io[:].out_string(String("t: "))
                                                io[:].out_string(t[:].type_name())
                                                io[:].out_string(String("\n"))
                                                b1[:] = _var1 = t[:]
                                                _var1
                                                io[:].out_string(String("b1: "))
                                                io[:].out_string(b1[:].type_name())
                                                io[:].out_string(String("\n"))
                                                b2[:] = _var2 = t1[:]
                                                _var2
                                                io[:].out_string(String("b2: "))
                                                io[:].out_string(b2[:].type_name())
                                                io[:].out_string(String("\n"))
                                                b1[:] = _var3 = f[:].copy()
                                                _var3
                                                io[:].out_string(String("b1: "))
                                                io[:].out_string(b1[:].type_name())
                                                io[:].out_string(String("\n"))
                                                b2[:] = _var4 = f2[:].copy()
                                                _var4
                                                io[:].out_string(String("b2: "))
                                                io[:].out_string(b2[:].type_name())
                                                return io[:].out_string(String("\n"))

                                            return                                             _block1()

                                        return _let9(IO())

                                    return _let8(Void)

                                return _let7(false)

                            return _let6(false)

                        return _let5(f[:])

                    return _let4(true)

                return _let3(t[:])

            return _let2(false)

        return _let1(true)



if __name__ == '__main__':
    bootstrap(Main)
