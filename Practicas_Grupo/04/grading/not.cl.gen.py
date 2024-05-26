from Base_clases import *


class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(x: Par[Int]):
            @mutable_params
            def _let2(b: Par[Bool]):
                def _block1():
                    _loop1 = Void
                    while Bool(x[:] < Int(100)):
                        def _block2():
                            Bool(b[:] == (((((((((((b[:]).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_())
                            Bool(b[:] == (((((((((((b[:]).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_())
                            Bool(b[:] == (((((((((((b[:]).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_())
                            Bool(b[:] == (((((((((((b[:]).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_())
                            Bool(b[:] == (((((((((((b[:]).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_()).not_())
                            x[:] = _var1 = (x[:] + Int(1))
                            return _var1

                        _loop1 = _block2()
                    Void
                    return (self.abort() if b[:] else Int(0))

                return                 _block1()

            return _let2(false)

        return _let1(Int(0))



if __name__ == '__main__':
    bootstrap(Main)
