from Base_clases import *


class Main(Object):
    @mutable_params
    def main(self, ) -> 'Int':
        def _block1():
            self.abort()
            return Int(0)

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
