from Base_clases import *


class Main(IO):
    @mutable_params
    def method(self, var: Par['String']) -> 'Object':
        _match1 = check_match(String("good"))
        if isinstance(_match1, String):
            var_1 = _match1
            _match_result1 = self.out_string(var_1)
        else:
            _match_result1 = Void
        return _match_result1

    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            self.method(String("bad"))
            return self.out_string(String("\n"))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
