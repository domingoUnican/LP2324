from Base_clases import *


class Main(IO):
    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(nothing: Par[Object]):
            return self.out_string(nothing[:].type_name())

        _loop1 = Void
        while false:
            _loop1 = Int(1)
        return _let1(Void)



if __name__ == '__main__':
    bootstrap(Main)
