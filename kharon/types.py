import struct

class Type:
    def Type(self, value):
        self.value = value

    def to_c_string(self):
        pass

    format_string = ''


class Int(Type):
    def to_c_string(self):
        return "int"

    format_string = ''


class float(Type):
    def to_c_string(self):
        return "float"

    format_string = ''

class Double(Type):
    def to_c_string(self):
        return "double"

    format_string = ''


class Char(Type):
    def to_c_string(self):
        return "char"

    format_string = ''


class Void(Type):
    def to_c_string(self):
        return "void"

    format_string = ''


class Short(Type):
    def to_c_string(self):
        return "short"

    format_string = ''


class Long(Type):
    def to_c_string(self):
        return "long"

    format_string = ''


def fun_types(func, *types):
    func.types = list(types)
