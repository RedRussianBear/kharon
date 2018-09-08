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


def parameter_types(*types):
    def editor(func):
        func.types = list(types)

    return editor


def returns(return_type):
    def editor(func):
        func.returns = return_type

    return editor
