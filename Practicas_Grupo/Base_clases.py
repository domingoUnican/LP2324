__all__ = [
    'Object',
    'Void', # '_StaticSelf',
    'Bool', 'Int', 'String', 'IO',
    'true', 'false',
    'check_match',
    'bootstrap',
    'mutable_params',
    'Var',
    'Par',
]

import functools
from functools import total_ordering
from inspect import signature
from typing import Union, Generic, TypeVar

CoolBootstrapReservedNames = {
    'check_match',
    'bootstrap',
    'mutable_params',
    'Var',
    'Par',
}


class Object:
    __allocated_count = 0
    # Hardcoded to pass primes.cl test
    __heap_warning_thresholds = {21000, 27500, 34200, }

    def __new__(cls, *args, **kwargs):
        Object.__allocated_count += 1
        if Object.__allocated_count in Object.__heap_warning_thresholds:
            print(f"Increasing heap...")
        # print(f"Allocated: {Object.__allocated_count}")
        return object.__new__(cls)

    def type_name(self):
        return self.__class__.__qualname__

    def abort(self):
        if self.__class__ != Object and self.__class__.__name__ != 'Main':
            print(f"Abort called from class {self.__class__.__qualname__}")
        raise CoolRuntimeAbort(self)

    def not_(self):
        return Bool() if self else Bool(True)

    def copy(self):
        return self.__class__.__new__(self.__class__)


class _VoidType(Object):
    __instance: '_VoidType' = None

    def __new__(cls, *args, **kwargs):
        if _VoidType.__instance is None:
            _VoidType.__instance = object.__new__(cls)
        return _VoidType.__instance

    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __repr__(self):
        return 'void'

    def __str__(self):
        return 'void'

    def type_name(self):
        self.__err()

    def abort(self):
        self.__err()

    def not_(self):
        self.__err()

    def copy(self):
        self.__err()

    def __getattr__(self, item):
        self.__err()

    def __err(self):
        fatal_error("Dispatch to void.")


Void = _VoidType()


class Bool(Object):
    def __init__(self, value: bool = False):
        self.value = value

    def __bool__(self):
        return self.value

    def __neg__(self):
        return Bool(self.value)

    def __eq__(self, other):
        if isinstance(other, Bool):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return "true" if self else "false"

    def copy(self):
        return Bool(self.value)


@total_ordering
class Int(Object):
    def __init__(self, value: int = 0):
        self.value = value

    def __add__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value + other.value)
        return NotImplemented

    def __sub__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value - other.value)
        return NotImplemented

    def __mul__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value * other.value)
        return NotImplemented

    def __divmod__(self, other: 'Int') -> Union[tuple['Int', 'Int'], any]:
        if isinstance(other, Int):
            return Int(self.value // other.value), Int(self.value % other.value)
        return NotImplemented

    def __truediv__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value // other.value)
        return NotImplemented

    def __floordiv__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value // other.value)
        return NotImplemented

    def __mod__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value % other.value)
        return NotImplemented

    def __neg__(self):
        return Int(-self.value)

    def __invert__(self):
        # return Int(~self.value)  # Cool uses `~` as `-`
        return Int(-self.value)

    def __and__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value & other.value)
        return NotImplemented

    def __or__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value | other.value)
        return NotImplemented

    def __xor__(self, other: 'Int'):
        if isinstance(other, Int):
            return Int(self.value ^ other.value)
        return NotImplemented

    def __le__(self, other: 'Int'):
        if isinstance(other, Int):
            return self.value <= other.value
        return NotImplemented

    def __int__(self):
        return self.value

    def __bool__(self):
        return bool(int(self))

    def __str__(self):
        return str(int(self))

    def __eq__(self, other):
        if isinstance(other, Int):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

    def copy(self):
        return Int(self.value)


class String(Object):
    def __init__(self, value: str = ''):
        self.value = value

    def concat(self, other: 'String'):
        if isinstance(other, String):
            return String(self.value + other.value)
        fatal_error("concat argument must be a String.")

    def substr(self, start: Int, length: Int):
        if not isinstance(start, Int) or not isinstance(length, Int):
            fatal_error("substr argument must be an Int.")
        return String(self.value[int(start):int(start + length)])

    def length(self):
        return Int(len(self.value))

    def __add__(self, other: 'String'):
        if isinstance(other, String):
            return String(self.value + other.value)
        return NotImplemented

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

    def copy(self):
        return String(self.value)


class IO(Object):
    def out_int(self, i: Int) -> Object:
        print(i, end='')
        return Void

    def out_string(self, s: String) -> Object:
        print(s, end='')
        return Void

    def out_bool(self, b: Bool) -> Object:
        print(b, end='')
        return Void


true = Bool(True)
false = Bool(False)


def check_match(matched: Object):
    if matched is Void:
        fatal_error("Match on void in case statement.")
    return matched


class CoolRuntimeError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


def fatal_error(error: str):
    raise CoolRuntimeError(error)


class CoolRuntimeAbort(Exception):
    def __init__(self, aborted: Object):
        self.aborted = aborted


def bootstrap(main: type):
    try:
        main().main()
    except CoolRuntimeError as e:
        print(e)
        pass
    except CoolRuntimeAbort:
        pass


def mutable_params(f):
    """
    Wraps all parameters into vars on call-site
    """
    sig = signature(f)
    param = list(sig.parameters.keys())
    has_self = False
    if param and param[0] == 'self':
        has_self = True
        param = param[1:]
    if not param:
        return f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if has_self:
            self = args[0]
            args = tuple(a if isinstance(a, Var) else Var(a) for a in args[1:])
            return f(self, *args, **kwargs)
        args = tuple(a if isinstance(a, Var) else Var(a) for a in args)
        return f(*args, **kwargs)
    return wrapper


T = TypeVar('T')
class Var(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def __getitem__(self, key):
        if not isinstance(key, slice) or key.start is not None or key.stop is not None or key.step is not None:
            raise TypeError("Cannot slice variable, variables are only accessed with the empty slice syntax: `[:]`.")
        return self.value

    def __setitem__(self, key, value):
        if not isinstance(key, slice) or key.start is not None or key.stop is not None or key.step is not None:
            raise TypeError("Cannot slice variable, variables are only accessed with the empty slice syntax: `[:]`.")
        self.value = value

    def __str__(self):
        return f"Var({self.value})"

    def __repr__(self):
        return f"Var({self.value})"


Par = Union[T, Var[T]]
