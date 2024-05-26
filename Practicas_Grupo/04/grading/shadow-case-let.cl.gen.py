from Base_clases import *


class Main(IO):
    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            _match1 = check_match(String("bad"))
            if isinstance(_match1, String):
                var = _match1
                @mutable_params
                def _let1(var: Par[String]):
                    return self.out_string(var[:])

                _match_result1 = _let1(String("good"))
            else:
                _match_result1 = Void
            _match_result1
            return self.out_string(String("\n"))

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
