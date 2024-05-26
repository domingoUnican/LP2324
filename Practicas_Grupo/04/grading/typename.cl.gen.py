from Base_clases import *


class Base(IO):
    @mutable_params
    def identify(self, thing: Par['Object']) -> 'Object':
        def _block1():
            self.out_string(thing[:].type_name())
            return self.out_string(String("\n"))

        return _block1()

    @mutable_params
    def test(self, ) -> 'Object':
        def _block1():
            self.identify(Base())
            self.identify(Derived())
            self.identify(Main())
            @mutable_params
            def _let1(poly: Par[Base]):
                return self.identify(poly[:])

            _let1(Derived())
            return self.identify(self)

        return _block1()



class Derived(Base):
    pass


class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        return (Derived()).test()



if __name__ == '__main__':
    bootstrap(Main)
