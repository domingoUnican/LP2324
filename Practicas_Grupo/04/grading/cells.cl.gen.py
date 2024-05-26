from Base_clases import *


class CellularAutomaton(IO):
    def __init__(self):
        super().__init__()
        self.population_map: String = String()


    @mutable_params
    def init(self, map: Par['String']) -> 'CellularAutomaton':
        def _block1():
            self.population_map = _var1 = map[:]
            _var1
            return self

        return _block1()

    @mutable_params
    def print(self, ) -> 'CellularAutomaton':
        def _block1():
            self.out_string(self.population_map.concat(String("\n")))
            return self

        return _block1()

    @mutable_params
    def num_cells(self, ) -> 'Int':
        return self.population_map.length()

    @mutable_params
    def cell(self, position: Par['Int']) -> 'String':
        return self.population_map.substr(position[:], Int(1))

    @mutable_params
    def cell_left_neighbor(self, position: Par['Int']) -> 'String':
        return (self.cell((self.num_cells() - Int(1))) if Bool(position[:] == Int(0)) else self.cell((position[:] - Int(1))))

    @mutable_params
    def cell_right_neighbor(self, position: Par['Int']) -> 'String':
        return (self.cell(Int(0)) if Bool(position[:] == (self.num_cells() - Int(1))) else self.cell((position[:] + Int(1))))

    @mutable_params
    def cell_at_next_evolution(self, position: Par['Int']) -> 'String':
        return (String("X") if Bool((((Int(1) if Bool(self.cell(position[:]) == String("X")) else Int(0)) + (Int(1) if Bool(self.cell_left_neighbor(position[:]) == String("X")) else Int(0))) + (Int(1) if Bool(self.cell_right_neighbor(position[:]) == String("X")) else Int(0))) == Int(1)) else String("."))

    @mutable_params
    def evolve(self, ) -> 'CellularAutomaton':
        @mutable_params
        def _let1(position: Par[Int]):
            @mutable_params
            def _let2(num: Par[Int]):
                @mutable_params
                def _let3(temp: Par[String]):
                    def _block1():
                        _loop1 = Void
                        while Bool(position[:] < num[:]):
                            def _block2():
                                temp[:] = _var1 = temp[:].concat(self.cell_at_next_evolution(position[:]))
                                _var1
                                position[:] = _var2 = (position[:] + Int(1))
                                return _var2

                            _loop1 = _block2()
                        Void
                        self.population_map = _var3 = temp[:]
                        _var3
                        return self

                    return                     _block1()

                return _let3(String())

            return _let2(self.num_cells())

        return _let1(Int(0))

    def copy(self):
        c = CellularAutomaton()
        c.population_map = self.population_map
        return c

class Main(Object):
    def __init__(self):
        super().__init__()
        self.cells: CellularAutomaton = Void


    @mutable_params
    def main(self, ) -> 'Main':
        def _block1():
            self.cells = _var1 = (CellularAutomaton()).init(String("         X         "))
            _var1
            self.cells.print()
            @mutable_params
            def _let1(countdown: Par[Int]):
                _loop1 = Void
                while Bool(Int(0) < countdown[:]):
                    def _block2():
                        self.cells.evolve()
                        self.cells.print()
                        countdown[:] = _var2 = (countdown[:] - Int(1))
                        return _var2

                    _loop1 = _block2()
                return Void

            _let1(Int(20))
            return self

        return _block1()

    def copy(self):
        c = Main()
        c.cells = self.cells
        return c

if __name__ == '__main__':
    bootstrap(Main)
