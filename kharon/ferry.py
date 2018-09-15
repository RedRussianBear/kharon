import inspect
import re
from pkg_resources import resource_filename, Requirement
from .vars import TYPES
import json


def count_indent(line):
    counter = re.compile(r'(^\s+)')
    match = counter.match(line)
    return 0 if match is None else len(match.expand(r'\1'))


def name_function(func, device):
    return '%s_%s' % (device.__name__, func.__name__)


def make_function_head(func, device):
    name = name_function(func, device)
    parameters = ''
    for parameter, p_type in zip([p for p in list(inspect.signature(func).parameters)[1:]], func.types):
        parameters += '%s %s, ' % (p_type.c, parameter)
    parameters = parameters[:-2]

    header = '%s %s(%s)' % (func.returns.c, name, parameters)

    return header


def ferry_function(func, device):
    replacements = [
        (r'\s+', r' '),
        (r'self\.', r''),
        (r'time\.sleep\(([0-9]+)\)', r'delay(\1);'),
        *[(r's*([a-zA-Z_][a-zA-Z_0-9]*)\s*=\s*%s\(\)' % type_class.__name__,
           r'%s \1;' % type_class.c) for type_class in TYPES],
        *[(r's*([a-zA-Z_][a-zA-Z_0-9]*)\s*=\s*%s\((.+)\)' % type_class.__name__,
           r'%s \1 = \2;' % type_class.c) for type_class in TYPES],
        (r'(s*[a-zA-Z_][a-zA-Z_0-9]*\s*=\s+.*?)$', r'\1;'),
        (r'(s*return\s*.*?)$', r'\1;'),
        (r'([a-z]+)\s(.*?):', r'\1(\2)'),
        (r's*print\((.*?)\)', r'Serial.println(\1);'),
        (r' and ', r'&&'),
        (r' or ', r'||'),
        (r' not ', r'!'),
        *[(r'\s*%s.%s\((.*?)\)\s*$' % (member[0], funky[0]), r'%s\1);' % funky[1]()) for member in
          get_members(device) for funky in get_functions(member[1])],
        *[(r'%s.%s\((.*?)\)' % (member[0], funky[0]), r'%s\1)' % funky[1]()) for member in
          get_members(device) for funky in get_functions(member[1])],

    ]

    header = make_function_head(func, device)
    lines = inspect.getsourcelines(func)[0]

    body = '{'
    for line, next_line in zip(lines[3:], lines[4:] + ['    ']):
        ind = count_indent(line)
        next_ind = count_indent(next_line)

        for replacement in replacements:
            line = re.sub(replacement[0], replacement[1], line)

        body += line
        if next_ind > ind:
            body += '{' * int((next_ind - ind) / 4)
        if next_ind < ind:
            body += '}' * int((ind - next_ind) / 4)

        body += '\n\n'
    return header + body


def get_functions(c):
    functions = inspect.getmembers(c, lambda a: (inspect.isroutine(a)))
    functions = [a for a in functions if not (a[0].startswith('__') and a[0].endswith('__'))]
    return functions


def get_members(c):
    members = inspect.getmembers(c, lambda a: not (inspect.isroutine(a)))
    members = [a for a in members if not (a[0].startswith('__') and a[0].endswith('__'))]
    for member in members:
        member[1].name = member[0]
    return members


def make_soul_map(device):
    soul_map = {}

    c = 1
    for func in get_functions(device):
        soul_map[name_function(func[1], device)] = c
        c += 1
    return soul_map


def make_param_struct(func, device):
    name = name_function(func, device)
    parameters = ''
    for parameter, p_type in zip([p for p in list(inspect.signature(func).parameters)[1:]], func.types):
        parameters += '%s %s;\n' % (p_type.c, parameter)

    return 'struct Struct_%s { %s } %s_struct;\n\n' % (name, parameters, name)


def make_comm_case(func, device, channel):
    name = name_function(func, device)
    parameters = ''
    for parameter in [p for p in list(inspect.signature(func).parameters)[1:]]:
        parameters += '%s_struct.%s, ' % (name, parameter)
    parameters = parameters[:-2]

    return 'case %d:\n memcpy((void*) &%s_struct,(void*) message, messageLen);\n Serial.flush();\n Serial.println(%s(' \
           '%s));\n   \n break;\n\n' % (channel, name, name, parameters)


def assemble(device):
    template = open(resource_filename(Requirement.parse("kharon"), "kharon/template.ino")).read()

    dev_ino = template + '\n'
    members = [x for x in get_members(device)]
    functions = [x[1] for x in get_functions(device)]

    declarations = ''
    setup = ''
    requires = {''}
    for member in members:
        declarations += member[1].declaration() + '\n'
        setup += member[1].setup() + '\n'
        requires.add(member[1].requires)
    setup += '\n__init__();\n'
    imports = ''
    for require in requires:
        imports += require + '\n'
    dev_ino = re.sub('//GLOBALS', declarations, dev_ino)
    dev_ino = re.sub('//SETUP', setup, dev_ino)
    dev_ino = re.sub('//IMPORTS', imports, dev_ino)

    soul_map = make_soul_map(device)

    with open("soul_map.json", 'w+') as f:
        f.write(json.dumps(soul_map))

    statement = ''
    implementation = ''
    structs = ''
    cases = ''
    for func in functions:
        statement += make_function_head(func, device) + ';\n'
        implementation += ferry_function(func, device) + '\n'
        structs += make_param_struct(func, device)
        cases += make_comm_case(func, device, soul_map[name_function(func, device)])
    dev_ino = re.sub('//FUNCTIONS', statement + '\n' + implementation + '\n' + structs, dev_ino)
    dev_ino = re.sub('//CASES', cases, dev_ino)

    with open('souls.ino', 'w+') as f:
        f.write(dev_ino)
