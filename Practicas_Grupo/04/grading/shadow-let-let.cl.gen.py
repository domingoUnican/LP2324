from Base_clases import *


class Main(IO):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(var: Par[String]):
                @mutable_params
                def _let2(var: Par[String]):
                    return self.out_string(var[:])

                return _let2(String("good"))

            _let1(String("bad"))
            return self.out_string(String("\n"))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
