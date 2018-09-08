class Type:
    def __init__(self, value):
        self.value = value

    c = ''

    format_string = ''


class Int(Type):
    c = "int"
    format_string = 'i'


class Float(Type):
    c = "float"
    format_string = 'f'


class Double(Type):
    c = "double"
    format_string = 'd'


class Char(Type):
    c = "char"
    format_string = 'c'


class Void(Type):
    c = "void"
    format_string = 'P'


class Short(Type):
    c = "short"
    format_string = 'h'


class Long(Type):
    c = "long"
    format_string = 'q'


TYPES = [Int, Float, Double, Char, Void, Short, Long]


def parameter_types(func, *types):
    func.types = list(types)


def returns(func, return_type):
    func.returns = return_type
