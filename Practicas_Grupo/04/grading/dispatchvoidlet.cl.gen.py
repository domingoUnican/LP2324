from Base_clases import *


class Main(Object):
    @mutable_params
    def foo(self, ) -> 'Int':
        return Int(5)

    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(m: Par[Main]):
            return m[:].foo()

        return _let1(Void)



if __name__ == '__main__':
    bootstrap(Main)
