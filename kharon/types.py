class Type:
    def Type(self, value):
        self.value = value

    def to_c_string(self):
        pass

    format_string = ''


class Int(Type):
    def to_c_string(self):
        return "int"

    format_string = 'i'


class float(Type):
    def to_c_string(self):
        return "float"

    format_string = 'f'

class Double(Type):
    def to_c_string(self):
        return "double"

    format_string = 'd'


class Char(Type):
    def to_c_string(self):
        return "char"

    format_string = 'c'


class Void(Type):
    def to_c_string(self):
        return "void"

    format_string = 'P'


class Short(Type):
    def to_c_string(self):
        return "short"

    format_string = 'h'


class Long(Type):
    def to_c_string(self):
        return "long"

    format_string = 'q'


def fun_types(func, *types):
    func.types = list(types)
