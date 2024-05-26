from Base_clases import *


class Main(IO):
    @mutable_params
    def print(self, x: Par['Int']) -> 'Object':
        def _block1():
            self.out_int(x[:])
            return self.out_string(String("\n"))

        return _block1()

    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(foo: Par[Int]):
            @mutable_params
            def _let2(foo: Par[Int]):
                @mutable_params
                def _let3(foo: Par[Bool]):
                    @mutable_params
                    def _let4(foo: Par[Int]):
                        return self.print((foo[:] + Int(1)))

                    return (_let4(Int(0)) if (foo[:]).not_() else Int(5))

                return _let3(false)

            return _let2(~(Int(1)))

        return _let1(Int(5))



if __name__ == '__main__':
    bootstrap(Main)
