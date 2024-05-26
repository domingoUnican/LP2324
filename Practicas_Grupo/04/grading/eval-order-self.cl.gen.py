from Base_clases import *


class Main(IO):
    @mutable_params
    def recite(self, value: Par['Int']) -> 'Main':
        def _block1():
            self.out_int(value[:])
            self.out_string(String("\n"))
            return self

        return _block1()

    @mutable_params
    def disregard(self, a: Par['Object']) -> 'Object':
        return self

    @mutable_params
    def main(self, ) -> 'Object':
        return self.recite(Int(2)).disregard(self.recite(Int(1)))



if __name__ == '__main__':
    bootstrap(Main)
