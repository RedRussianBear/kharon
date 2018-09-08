import inspect
import re
from .c_types import TYPES


def count_indent(line):
    counter = re.compile('^\s+')
    return len(counter.match(line).string)


REPLACEMENTS = [
    (r'\s+', r'\s'),
    *[(r'^([a-zA-Z_][a-zA-Z_0-9]*)\s?=\s?(%s)\(\)' % type_class.__name__,
       r'%s \1;' % type_class.c) for type_class in TYPES],
    (r'([a-z]+)\s(.*?):', r'\1\(\2\)'),
    (r' and ', r'&&'),
    (r' or ', r'||'),
    (r' not ', r'!'),
]


def ferry_function(func, device):
    name = '%s_%s' % (device.__name__, func.__name__)
    parameters = ''
    for parameter, p_type in zip([p[0] for p in inspect.signature(func).parameters], func.types):
        parameters += '%s %s' % (p_type.c, parameter)

    header = '%s %s(%s){\n' % (func.returns.c, name, parameters)
    lines = inspect.getsourcelines(func)

    body = ''
    for line, next_line in zip(lines[1:], lines[2:] + ['']):
        ind = count_indent(line)
        next_ind = count_indent(next_line)

        for replacement in REPLACEMENTS:
            line = re.sub(replacement[0], replacement[1], line)

        body += line
        if next_ind > ind:
            body += '{' * int((next_ind - ind) / 4)
        if next_ind < ind:
            body += '}' * int((ind - next_ind) / 4)

    return header + body
