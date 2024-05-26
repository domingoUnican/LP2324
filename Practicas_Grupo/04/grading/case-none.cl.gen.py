from Base_clases import *


class Main(IO):
    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(thing: Par[Object]):
            _match1 = check_match(thing[:])
            if isinstance(_match1, Int):
                i = _match1
                _match_result1 = self.out_string(String("int\n"))
            elif isinstance(_match1, Bool):
                b = _match1
                _match_result1 = self.out_string(String("bool\n"))
            else:
                _match_result1 = Void
            return _match_result1

        return _let1(self)



if __name__ == '__main__':
    bootstrap(Main)
