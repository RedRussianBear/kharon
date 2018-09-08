class Type:
    def __init__(self, value):
        self.value = value

    def c(self):
        pass

    format_string = ''


class Int(Type):
    def c(self):
        return "int"

    format_string = 'i'


class Float(Type):
    def c(self):
        return "float"

    format_string = 'f'


class Double(Type):
    def c(self):
        return "double"

    format_string = 'd'


class Char(Type):
    def c(self):
        return "char"

    format_string = 'c'


class Void(Type):
    def c(self):
        return "void"

    format_string = 'P'


class Short(Type):
    def c(self):
        return "short"

    format_string = 'h'


class Long(Type):
    def c(self):
        return "long"

    format_string = 'q'


TYPES = [Int, Float, Double, Char, Void, Short, Long]


def parameter_types(func, *types):
    func.types = list(types)


def returns(func, return_type):
    func.returns = return_type
