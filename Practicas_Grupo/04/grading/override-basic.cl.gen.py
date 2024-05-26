from Base_clases import *


class Base(IO):
    @mutable_params
    def identify(self, ) -> 'Object':
        def _block1():
            self.out_string(self.type_name())
            return Base.out_string(self, String("\n"))

        return _block1()



class Derived(Base):
    @mutable_params
    def out_string(self, s: Par['String']) -> 'Derived':
        def _block1():
            Base.out_string(self, String("derived "))
            Base.out_string(self, s[:])
            return Base.out_string(self, String("\n"))

        return _block1()



class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(me: Par[Base]):
                return Base.identify(me[:], )

            _let1(Base())
            @mutable_params
            def _let2(me: Par[Base]):
                return Base.identify(me[:], )

            _let2(Derived())
            @mutable_params
            def _let3(me: Par[Derived]):
                def _block2():
                    Base.identify(me[:], )
                    return Derived.identify(me[:], )

                return                 _block2()

            return _let3(Derived())

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
