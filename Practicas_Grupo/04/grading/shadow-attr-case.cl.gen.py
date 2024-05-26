from Base_clases import *


class Main(IO):
    def __init__(self):
        super().__init__()
        self.var: String = String()

        self.var: String = String("bad")

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            _match1 = check_match(String("good"))
            if isinstance(_match1, String):
                var = _match1
                _match_result1 = self.out_string(var)
            else:
                _match_result1 = Void
            _match_result1
            return self.out_string(String("\n"))

        return _block1()

    def copy(self):
        c = Main()
        c.var = self.var
        return c

if __name__ == '__main__':
    bootstrap(Main)
