from Base_clases import *


class Base(IO):
    @mutable_params
    def identify(self, ) -> 'Object':
        return self.out_string(String("base\n"))



class Derived(Base):
    @mutable_params
    def identify(self, ) -> 'Object':
        return self.out_string(String("derived\n"))



class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(me: Par[Base]):
                return me[:].identify()

            _let1(Base())
            @mutable_params
            def _let2(me: Par[Base]):
                return me[:].identify()

            _let2(Derived())
            @mutable_params
            def _let3(me: Par[Derived]):
                return me[:].identify()

            return _let3(Derived())

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
