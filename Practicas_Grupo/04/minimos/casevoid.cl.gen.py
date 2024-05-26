from Base_clases import *


class Main(Object):
    def __init__(self):
        super().__init__()
        self.x: Main = Void


    @mutable_params
    def main(self, ) -> 'Object':
        def _block1():
            _match1 = check_match(self.x)
            if isinstance(_match1, Main):
                m = _match1
                _match_result1 = Int(0)
            else:
                _match_result1 = Void
            return _match_result1

        return _block1()

    def copy(self):
        c = Main()
        c.x = self.x
        return c

if __name__ == '__main__':
    bootstrap(Main)
