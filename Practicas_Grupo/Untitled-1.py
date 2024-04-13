from Base_clases import *
class Main(IO):
    def main(self):
        nothing = None
        while False:
            nothing = 1  # Loop nunca se ejecuta
        self.out_string(nothing.type_name())
Main().main()
