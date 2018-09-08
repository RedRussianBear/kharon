import hashlib
import inspect
import copy


class Symbol:

    def __init__(self, name, symbol_type):
        self.name = name
        self.type = symbol_type


def get_functions(device):
    functions = inspect.getmembers(device, lambda a: (inspect.isroutine(a)))
    functions = [a for a in functions if not (a[0].startswith('__') and a[0].endswith('__'))]
    return functions


def get_members(device):
    members = inspect.getmembers(device, lambda a: not (inspect.isroutine(a)))
    members = [a for a in members if not (a[0].startswith('__') and a[0].endswith('__'))]
    return members


def gen_device_symtable(device):
    table = {}

    for member in get_members(device):
        table[member[0]] = Symbol(member[0], type(member[1]))

    for func in get_functions(device):
        table[func[0]] = Symbol(func[0], type(func[1]))

    return table


def gen_function_symtable(func, device_symtable):
    table = copy.copy(device_symtable)

    for parameter, p_type in zip([p[0] for p in inspect.signature(func).parameters], func.types):
        table[parameter] = Symbol(parameter, p_type)


def make_comm_map(device):
    comm_map = {}

    for func in device.__dict__.values():
        m = hashlib.md5()
        m.update(func.__name__)
        comm_map['%s.%s' % (device.__name__, func.__name__)] = m.hexdigest()
    return comm_map
