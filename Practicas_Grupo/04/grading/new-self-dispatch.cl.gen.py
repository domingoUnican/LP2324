from Base_clases import *


class Base(IO):
    @mutable_params
    def identify(self, ) -> 'Object':
        return self.out_string(String("base\n"))

    @mutable_params
    def duplicate(self, ) -> 'Base':
        return Base()



class Derived(Base):
    @mutable_params
    def identify(self, ) -> 'Object':
        return self.out_string(String("derived\n"))



class Main(Object):
    @mutable_params
    def main(self, ) -> 'Object':
        return (Derived()).duplicate().identify()



if __name__ == '__main__':
    bootstrap(Main)
