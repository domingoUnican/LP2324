from Base_clases import *


class Main(IO):
    @mutable_params
    def complain(self, ) -> 'Object':
        return self.out_string(String("bad\n"))

    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(nothing: Par[Main]):
            return Main.complain(nothing[:], )

        return _let1(Void)



if __name__ == '__main__':
    bootstrap(Main)
