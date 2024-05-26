from Base_clases import *


class VarList(IO):
    @mutable_params
    def isNil(self, ) -> 'Bool':
        return true

    @mutable_params
    def head(self, ) -> 'Variable':
        def _block1():
            self.abort()
            return Variable()

        return _block1()

    @mutable_params
    def tail(self, ) -> 'VarList':
        def _block1():
            self.abort()
            return VarList()

        return _block1()

    @mutable_params
    def add(self, x: Par['Variable']) -> 'VarList':
        return (VarListNE()).init(x[:], self)

    @mutable_params
    def print(self, ) -> 'VarList':
        return self.out_string(String("\n"))



class VarListNE(VarList):
    def __init__(self):
        super().__init__()
        self.x: Variable = Void
        self.rest: VarList = Void


    @mutable_params
    def isNil(self, ) -> 'Bool':
        return false

    @mutable_params
    def head(self, ) -> 'Variable':
        return self.x

    @mutable_params
    def tail(self, ) -> 'VarList':
        return self.rest

    @mutable_params
    def init(self, y: Par['Variable'], r: Par['VarList']) -> 'VarListNE':
        def _block1():
            self.x = _var1 = y[:]
            _var1
            self.rest = _var2 = r[:]
            _var2
            return self

        return _block1()

    @mutable_params
    def print(self, ) -> 'VarListNE':
        def _block1():
            self.x.print_self()
            self.out_string(String(" "))
            self.rest.print()
            return self

        return _block1()

    def copy(self):
        c = VarListNE()
        c.x = self.x
        c.rest = self.rest
        return c

class LambdaList(Object):
    @mutable_params
    def isNil(self, ) -> 'Bool':
        return true

    @mutable_params
    def headE(self, ) -> 'VarList':
        def _block1():
            self.abort()
            return VarList()

        return _block1()

    @mutable_params
    def headC(self, ) -> 'Lambda':
        def _block1():
            self.abort()
            return Lambda()

        return _block1()

    @mutable_params
    def headN(self, ) -> 'Int':
        def _block1():
            self.abort()
            return Int(0)

        return _block1()

    @mutable_params
    def tail(self, ) -> 'LambdaList':
        def _block1():
            self.abort()
            return LambdaList()

        return _block1()

    @mutable_params
    def add(self, e: Par['VarList'], x: Par['Lambda'], n: Par['Int']) -> 'LambdaList':
        return (LambdaListNE()).init(e[:], x[:], n[:], self)



class LambdaListNE(LambdaList):
    def __init__(self):
        super().__init__()
        self.lam: Lambda = Void
        self.num: Int = Int(0)
        self.env: VarList = Void
        self.rest: LambdaList = Void


    @mutable_params
    def isNil(self, ) -> 'Bool':
        return false

    @mutable_params
    def headE(self, ) -> 'VarList':
        return self.env

    @mutable_params
    def headC(self, ) -> 'Lambda':
        return self.lam

    @mutable_params
    def headN(self, ) -> 'Int':
        return self.num

    @mutable_params
    def tail(self, ) -> 'LambdaList':
        return self.rest

    @mutable_params
    def init(self, e: Par['VarList'], l: Par['Lambda'], n: Par['Int'], r: Par['LambdaList']) -> 'LambdaListNE':
        def _block1():
            self.env = _var1 = e[:]
            _var1
            self.lam = _var2 = l[:]
            _var2
            self.num = _var3 = n[:]
            _var3
            self.rest = _var4 = r[:]
            _var4
            return self

        return _block1()

    def copy(self):
        c = LambdaListNE()
        c.lam = self.lam
        c.num = self.num
        c.env = self.env
        c.rest = self.rest
        return c

class LambdaListRef(Object):
    def __init__(self):
        super().__init__()
        self.nextNum: Int = Int(0)
        self.l: LambdaList = Void

        self.nextNum: Int = Int(0)

    @mutable_params
    def isNil(self, ) -> 'Bool':
        return self.l.isNil()

    @mutable_params
    def headE(self, ) -> 'VarList':
        return self.l.headE()

    @mutable_params
    def headC(self, ) -> 'Lambda':
        return self.l.headC()

    @mutable_params
    def headN(self, ) -> 'Int':
        return self.l.headN()

    @mutable_params
    def reset(self, ) -> 'LambdaListRef':
        def _block1():
            self.nextNum = _var1 = Int(0)
            _var1
            self.l = _var2 = LambdaList()
            _var2
            return self

        return _block1()

    @mutable_params
    def add(self, env: Par['VarList'], c: Par['Lambda']) -> 'Int':
        def _block1():
            self.l = _var1 = self.l.add(env[:], c[:], self.nextNum)
            _var1
            self.nextNum = _var2 = (self.nextNum + Int(1))
            _var2
            return (self.nextNum - Int(1))

        return _block1()

    @mutable_params
    def removeHead(self, ) -> 'LambdaListRef':
        def _block1():
            self.l = _var1 = self.l.tail()
            _var1
            return self

        return _block1()

    def copy(self):
        c = LambdaListRef()
        c.nextNum = self.nextNum
        c.l = self.l
        return c

class Expr(IO):
    @mutable_params
    def print_self(self, ) -> 'Expr':
        def _block1():
            self.out_string(String("\nError: Expr is pure virtual; can't print self\n"))
            self.abort()
            return self

        return _block1()

    @mutable_params
    def beta(self, ) -> 'Expr':
        def _block1():
            self.out_string(String("\nError: Expr is pure virtual; can't beta-reduce\n"))
            self.abort()
            return self

        return _block1()

    @mutable_params
    def substitute(self, x: Par['Variable'], e: Par['Expr']) -> 'Expr':
        def _block1():
            self.out_string(String("\nError: Expr is pure virtual; can't substitute\n"))
            self.abort()
            return self

        return _block1()

    @mutable_params
    def gen_code(self, env: Par['VarList'], closures: Par['LambdaListRef']) -> 'Expr':
        def _block1():
            self.out_string(String("\nError: Expr is pure virtual; can't gen_code\n"))
            self.abort()
            return self

        return _block1()



class Variable(Expr):
    def __init__(self):
        super().__init__()
        self.name: String = String()


    @mutable_params
    def init(self, n: Par['String']) -> 'Variable':
        def _block1():
            self.name = _var1 = n[:]
            _var1
            return self

        return _block1()

    @mutable_params
    def print_self(self, ) -> 'Variable':
        return self.out_string(self.name)

    @mutable_params
    def beta(self, ) -> 'Expr':
        return self

    @mutable_params
    def substitute(self, x: Par['Variable'], e: Par['Expr']) -> 'Expr':
        return (e[:] if Bool(x[:] == self) else self)

    @mutable_params
    def gen_code(self, env: Par['VarList'], closures: Par['LambdaListRef']) -> 'Variable':
        @mutable_params
        def _let1(cur_env: Par[VarList]):
            def _block1():
                _loop1 = Void
                while (false if cur_env[:].isNil() else (Bool(cur_env[:].head() == self)).not_()):
                    def _block2():
                        self.out_string(String("get_parent()."))
                        cur_env[:] = _var1 = cur_env[:].tail()
                        return _var1

                    _loop1 = _block2()
                Void
                def _block3():
                    self.out_string(String("Error:  free occurrence of "))
                    self.print_self()
                    self.out_string(String("\n"))
                    self.abort()
                    return self

                return (                _block3() if cur_env[:].isNil() else self.out_string(String("get_x()")))

            return             _block1()

        return _let1(env[:])

    def copy(self):
        c = Variable()
        c.name = self.name
        return c

class Lambda(Expr):
    def __init__(self):
        super().__init__()
        self.arg: Variable = Void
        self.body: Expr = Void


    @mutable_params
    def init(self, a: Par['Variable'], b: Par['Expr']) -> 'Lambda':
        def _block1():
            self.arg = _var1 = a[:]
            _var1
            self.body = _var2 = b[:]
            _var2
            return self

        return _block1()

    @mutable_params
    def print_self(self, ) -> 'Lambda':
        def _block1():
            self.out_string(String("\\"))
            self.arg.print_self()
            self.out_string(String("."))
            self.body.print_self()
            return self

        return _block1()

    @mutable_params
    def beta(self, ) -> 'Expr':
        return self

    @mutable_params
    def apply(self, actual: Par['Expr']) -> 'Expr':
        return self.body.substitute(self.arg, actual[:])

    @mutable_params
    def substitute(self, x: Par['Variable'], e: Par['Expr']) -> 'Expr':
        @mutable_params
        def _let1(new_body: Par[Expr]):
            @mutable_params
            def _let2(new_lam: Par[Lambda]):
                return new_lam[:].init(self.arg, new_body[:])

            return _let2(Lambda())

        return (self if Bool(x[:] == self.arg) else _let1(self.body.substitute(x[:], e[:])))

    @mutable_params
    def gen_code(self, env: Par['VarList'], closures: Par['LambdaListRef']) -> 'Lambda':
        def _block1():
            self.out_string(String("((new Closure"))
            self.out_int(closures[:].add(env[:], self))
            self.out_string(String(").init("))
            (self.out_string(String("new Closure))")) if env[:].isNil() else self.out_string(String("self))")))
            return self

        return _block1()

    @mutable_params
    def gen_closure_code(self, n: Par['Int'], env: Par['VarList'], closures: Par['LambdaListRef']) -> 'Lambda':
        def _block1():
            self.out_string(String("class Closure"))
            self.out_int(n[:])
            self.out_string(String(" inherits Closure {\n"))
            self.out_string(String("  apply(y : EvalObject) : EvalObject {\n"))
            self.out_string(String("    { out_string(\"Applying closure "))
            self.out_int(n[:])
            self.out_string(String("\\n\");\n"))
            self.out_string(String("      x <- y;\n"))
            self.body.gen_code(env[:].add(self.arg), closures[:])
            self.out_string(String(";}};\n"))
            return self.out_string(String("};\n"))

        return _block1()

    def copy(self):
        c = Lambda()
        c.arg = self.arg
        c.body = self.body
        return c

class App(Expr):
    def __init__(self):
        super().__init__()
        self.fun: Expr = Void
        self.arg: Expr = Void


    @mutable_params
    def init(self, f: Par['Expr'], a: Par['Expr']) -> 'App':
        def _block1():
            self.fun = _var1 = f[:]
            _var1
            self.arg = _var2 = a[:]
            _var2
            return self

        return _block1()

    @mutable_params
    def print_self(self, ) -> 'App':
        def _block1():
            self.out_string(String("(("))
            self.fun.print_self()
            self.out_string(String(")@("))
            self.arg.print_self()
            self.out_string(String("))"))
            return self

        return _block1()

    @mutable_params
    def beta(self, ) -> 'Expr':
        _match1 = check_match(self.fun)
        if isinstance(_match1, Lambda):
            l = _match1
            _match_result1 = l.apply(self.arg)
        elif isinstance(_match1, Expr):
            e = _match1
            @mutable_params
            def _let1(new_fun: Par[Expr]):
                @mutable_params
                def _let2(new_app: Par[App]):
                    return new_app[:].init(new_fun[:], self.arg)

                return _let2(App())

            _match_result1 = _let1(self.fun.beta())
        else:
            _match_result1 = Void
        return _match_result1

    @mutable_params
    def substitute(self, x: Par['Variable'], e: Par['Expr']) -> 'Expr':
        @mutable_params
        def _let1(new_fun: Par[Expr]):
            @mutable_params
            def _let2(new_arg: Par[Expr]):
                @mutable_params
                def _let3(new_app: Par[App]):
                    return new_app[:].init(new_fun[:], new_arg[:])

                return _let3(App())

            return _let2(self.arg.substitute(x[:], e[:]))

        return _let1(self.fun.substitute(x[:], e[:]))

    @mutable_params
    def gen_code(self, env: Par['VarList'], closures: Par['LambdaListRef']) -> 'App':
        def _block1():
            self.out_string(String("(let x : EvalObject <- "))
            self.fun.gen_code(env[:], closures[:])
            self.out_string(String(",\n"))
            self.out_string(String("     y : EvalObject <- "))
            self.arg.gen_code(env[:], closures[:])
            self.out_string(String(" in\n"))
            self.out_string(String("  case x of\n"))
            self.out_string(String("    c : Closure => c.apply(y);\n"))
            self.out_string(String("    o : Object => { abort(); new EvalObject; };\n"))
            return self.out_string(String("  esac)"))

        return _block1()

    def copy(self):
        c = App()
        c.fun = self.fun
        c.arg = self.arg
        return c

class Term(IO):
    @mutable_params
    def var(self, x: Par['String']) -> 'Variable':
        @mutable_params
        def _let1(v: Par[Variable]):
            return v[:].init(x[:])

        return _let1(Variable())

    @mutable_params
    def lam(self, x: Par['Variable'], e: Par['Expr']) -> 'Lambda':
        @mutable_params
        def _let1(l: Par[Lambda]):
            return l[:].init(x[:], e[:])

        return _let1(Lambda())

    @mutable_params
    def app(self, e1: Par['Expr'], e2: Par['Expr']) -> 'App':
        @mutable_params
        def _let1(a: Par[App]):
            return a[:].init(e1[:], e2[:])

        return _let1(App())

    @mutable_params
    def i(self, ) -> 'Expr':
        @mutable_params
        def _let1(x: Par[Variable]):
            return self.lam(x[:], x[:])

        return _let1(self.var(String("x")))

    @mutable_params
    def k(self, ) -> 'Expr':
        @mutable_params
        def _let1(x: Par[Variable]):
            @mutable_params
            def _let2(y: Par[Variable]):
                return self.lam(x[:], self.lam(y[:], x[:]))

            return _let2(self.var(String("y")))

        return _let1(self.var(String("x")))

    @mutable_params
    def s(self, ) -> 'Expr':
        @mutable_params
        def _let1(x: Par[Variable]):
            @mutable_params
            def _let2(y: Par[Variable]):
                @mutable_params
                def _let3(z: Par[Variable]):
                    return self.lam(x[:], self.lam(y[:], self.lam(z[:], self.app(self.app(x[:], z[:]), self.app(y[:], z[:])))))

                return _let3(self.var(String("z")))

            return _let2(self.var(String("y")))

        return _let1(self.var(String("x")))



class Main(Term):
    @mutable_params
    def beta_reduce(self, e: Par['Expr']) -> 'Expr':
        def _block1():
            self.out_string(String("beta-reduce: "))
            e[:].print_self()
            @mutable_params
            def _let1(done: Par[Bool]):
                @mutable_params
                def _let2(new_expr: Par[Expr]):
                    def _block2():
                        _loop1 = Void
                        while (done[:]).not_():
                            def _block3():
                                new_expr[:] = _var1 = e[:].beta()
                                _var1
                                done[:] = _var2 = true
                                def _block4():
                                    e[:] = _var3 = new_expr[:]
                                    _var3
                                    self.out_string(String(" =>\n"))
                                    return e[:].print_self()

                                return (_var2 if Bool(new_expr[:] == e[:]) else _block4())

                            _loop1 = _block3()
                        Void
                        self.out_string(String("\n"))
                        return e[:]

                    return                     _block2()

                return _let2(Void)

            return _let1(false)

        return _block1()

    @mutable_params
    def eval_class(self, ) -> 'Main':
        def _block1():
            self.out_string(String("class EvalObject inherits IO {\n"))
            self.out_string(String("  eval() : EvalObject { { abort(); self; } };\n"))
            return self.out_string(String("};\n"))

        return _block1()

    @mutable_params
    def closure_class(self, ) -> 'Main':
        def _block1():
            self.out_string(String("class Closure inherits EvalObject {\n"))
            self.out_string(String("  parent : Closure;\n"))
            self.out_string(String("  x : EvalObject;\n"))
            self.out_string(String("  get_parent() : Closure { parent };\n"))
            self.out_string(String("  get_x() : EvalObject { x };\n"))
            self.out_string(String("  init(p : Closure) : Closure {{ parent <- p; self; }};\n"))
            self.out_string(String("  apply(y : EvalObject) : EvalObject { { abort(); self; } };\n"))
            return self.out_string(String("};\n"))

        return _block1()

    @mutable_params
    def gen_code(self, e: Par['Expr']) -> 'Main':
        @mutable_params
        def _let1(cl: Par[LambdaListRef]):
            def _block1():
                self.out_string(String("Generating code for "))
                e[:].print_self()
                self.out_string(String("\n------------------cut here------------------\n"))
                self.out_string(String("(*Generated by lam.cl (Jeff Foster, March 2000)*)\n"))
                self.eval_class()
                self.closure_class()
                self.out_string(String("class Main {\n"))
                self.out_string(String("  main() : EvalObject {\n"))
                e[:].gen_code(VarList(), cl[:])
                self.out_string(String("\n};\n};\n"))
                _loop1 = Void
                while (cl[:].isNil()).not_():
                    @mutable_params
                    def _let2(e: Par[VarList]):
                        @mutable_params
                        def _let3(c: Par[Lambda]):
                            @mutable_params
                            def _let4(n: Par[Int]):
                                def _block2():
                                    cl[:].removeHead()
                                    return c[:].gen_closure_code(n[:], e[:], cl[:])

                                return                                 _block2()

                            return _let4(cl[:].headN())

                        return _let3(cl[:].headC())

                    _loop1 = _let2(cl[:].headE())
                Void
                return self.out_string(String("\n------------------cut here------------------\n"))

            return             _block1()

        return _let1((LambdaListRef()).reset())

    @mutable_params
    def main(self, ) -> 'Int':
        def _block1():
            self.i().print_self()
            self.out_string(String("\n"))
            self.k().print_self()
            self.out_string(String("\n"))
            self.s().print_self()
            self.out_string(String("\n"))
            self.beta_reduce(self.app(self.app(self.app(self.s(), self.k()), self.i()), self.i()))
            self.beta_reduce(self.app(self.app(self.k(), self.i()), self.i()))
            self.gen_code(self.app(self.i(), self.i()))
            self.gen_code(self.app(self.app(self.app(self.s(), self.k()), self.i()), self.i()))
            self.gen_code(self.app(self.app(self.app(self.app(self.app(self.app(self.app(self.app(self.i(), self.k()), self.s()), self.s()), self.k()), self.s()), self.i()), self.k()), self.i()))
            self.gen_code(self.app(self.app(self.i(), self.app(self.k(), self.s())), self.app(self.k(), self.app(self.s(), self.s()))))
            return Int(0)

        return _block1()



if __name__ == '__main__':
    bootstrap(Main)
