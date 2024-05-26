from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.var: String = String()

        self.var: String = String("bad")

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            @mutable_params
            def _let1(var: Par[String]):
                return self.out_string(var[:])

            _let1(String("good"))
            return self.out_string(String("\n"))

        return _block1()

    def copy(self):
        c = Main()
        c.var = self.var
        return c

if __name__ == '__main__':
    bootstrap(Main)
