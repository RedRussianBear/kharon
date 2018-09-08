class Type:
    def to_c_string(self):
        pass

class Int(Type):
    def to_c_string(self):
        return "int"

class float(Type):
    def to_c_string(self):
        return "float"

class Double(Type):
    def to_c_string(self):
        return "double"

class Char(Type):
    def to_c_string(self):
        return "char"

class Void(Type):
    def to_c_string(self):
        return "void"

class Short(Type):
    def to_c_string(self):
        return "short"

class Long(Type):
    def to_c_string(self):
        return "long"