from Base_clases import *


class Main(IO):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(x: Par[Bool]):
                @mutable_params
                def _let2(y: Par[Int]):
                    @mutable_params
                    def _let3(z: Par[String]):
                        def _block2():
                            self.out_int((y[:] + Int(1)))
                            return self.out_string(z[:].concat(String("test\n")))

                        return (self.abort() if x[:] else _block2())

                    return _let3(String())

                return _let2(Int(0))

            return _let1(false)

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
