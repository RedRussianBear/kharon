import inspect
import copy
import sys
import re

RESERVED = 'RESERVED'
FLOAT = 'FLOAT'
INT = 'INT'
STRING = 'STRING'
ID = 'ID'

TOKENS = [
    (r'(?!^)[\s\t]', None),
    (r'#[^\n]*', None),
    (r'\n', RESERVED),
    (r'^[\s\t]+', RESERVED),
    (r'=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r':', RESERVED),
    (r';', RESERVED),
    (r'?', RESERVED),
    (r'!', RESERVED),
    (r',', RESERVED),
    (r'\.', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'=', RESERVED),
    (r'!=', RESERVED),
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'return', RESERVED),
    (r'def', RESERVED),
    (r'[0-9]*\.[0-9]+', FLOAT),
    (r'[0-9]+', INT),
    (r'".*"', STRING),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', ID)
]


def make_lexer(token_expressions):
    def lex(characters):
        pos = 0
        tokens = []
        while pos < len(characters):
            match = None
            for token_expression in token_expressions:
                pattern, tag = token_expression
                regex = re.compile(pattern)
                match = regex.match(characters, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = (text, tag)
                        tokens.append(token)
                    break
            if not match:
                sys.stderr.write('Illegal character: %s\\n' % characters[pos])
                sys.exit(1)
            else:
                pos = match.end(0)
        return tokens

    return lex


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


def lex_function(func):
    lexer = make_lexer(TOKENS)
    lines = inspect.getsourcelines(func)
    source = ''

    for line in lines[1:]:
        pass

    return lexer(source)
