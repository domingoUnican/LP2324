from Base_clases import *


class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            (self.abort() if Bool(true == false) else Int(0))
            (Int(0) if Bool(true == true) else self.abort())
            (Int(0) if Bool(String("hello") == String("hello").copy()) else self.abort())
            @mutable_params
            def _let1(a: Par[String]):
                return (Int(0) if Bool(a[:] == String("")) else self.abort())

            _let1(String())
            return (self.abort() if Bool(Int(5) == Int(6)) else Int(0))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
