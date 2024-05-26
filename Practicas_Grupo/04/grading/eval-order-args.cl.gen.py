from Base_clases import *


class Main(IO):
    @mutable_params
    def recite(self, value: Par['Int']) -> 'Object':
        def _block1():
            self.out_int(value[:])
            return self.out_string(String("\n"))

        return _block1()

    @mutable_params
    def disregard(self, a: Par['Object'], b: Par['Object'], c: Par['Object']) -> 'Object':
        return self

    @mutable_params
    def main(self, ) -> 'Object':
        return self.disregard(self.recite(Int(1)), self.recite(Int(2)), self.recite(Int(3)))



if __name__ == '__main__':
    bootstrap(Main)
