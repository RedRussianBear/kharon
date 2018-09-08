from .lexify import RESERVED, INT, ID


class Node:

    def __init__(self, *children):
        self.children = children


class Token(Node):

    def __init__(self, type, value, *children):
        super(Token, self).__init__(children)


class Value(Node):
    pass


class Product(Node):
    pass


class Sums(Node):
    pass


class Expression(Node):
    pass


class Assign(Node):
    pass


class Line(Node):
    pass


class Lines(Node):
    pass


class Block(Node):
    pass


class If(Node):
    pass


class IfElse(Node):
    pass


class Function(Node):
    pass


class Token(Node):

    def __init__(self, type, value, *children):
        super(Token, self).__init__(children)


grammar = [
    (Value, ((Token, INT),)),
    (Product, ((Value,),)),
    (Sums, ((Product,),)),
    (Sums, ((Product,), (Token, RESERVED, '*'), (Value,))),
    (Sums, ((Product,), (Token, RESERVED, '/'), (Value,))),
    (Expression, ((Sums,),)),
    (Sums, ((Sums,), (Token, RESERVED, '+'), (Product,))),
    (Sums, ((Sums,), (Token, RESERVED, '-'), (Product,))),
    (Assign, ((Token, ID), (Token, RESERVED, '='), (Expression,))),
    (Line, ((Expression,), (Token, RESERVED, ';'))),
    (Line, ((Assign,), (Token, RESERVED, ';'))),
    (Lines, ((Lines,), (Token, RESERVED, ';'), (Line,))),
    (Block, ((Token, RESERVED, '?'), (Lines,), (Token, RESERVED, '!'))),
    (Function, ((Block,),)),
    (If, ((Token, RESERVED, 'if'), (Block,),)),
    (IfElse, ((If,), (Token, RESERVED, 'else'), (Block,))),
    (Block, ((If,),)),
    (Block, ((IfElse,),)),

]

grammar.reverse()

sr = {
    (ID, '='): True,
    (Value, '$'): False,
    (Product, '$'): False,
    (Sums, '$'): False,
    (Expression, '$'): False,
    (Assign, '$'): False,
    (Line, '$'): False,
    (Lines, '$'): False,
    (Block, '$'): False,
    (If, '$'): False,
    (IfElse, '$'): False,
    (Function, '$'): False,

}


def match(stack, rule):
    parts = rule[1]
    rlen = len(parts)

    for i in range(rlen):
        if not isinstance(stack[-rlen + i], parts[i][0]):
            return False
        if len(parts[i]) >= 1 and not stack[-rlen + i].type == parts[i][1]:
            return False
        if len(parts[i]) >= 1 and not stack[-rlen + i].value == parts[i][2]:
            return False

    return True


def reduce(stack, rule):
    children = []
    for i in range(len(rule[1])):
        children.append(stack.pop())
    children.reverse()

    stack.append(rule[0](*children))


def parse(tokens):
    stack = []
    unread = [Token(token[1], token[0], []) for token in tokens]

    while not isinstance(stack[0], Function):

        if sr[(stack[-1].type if type(stack[-1]) == Token else type(stack[-1]), unread[0].value)] or \
                sr[(stack[-1].type if type(stack[-1]) == Token else type(stack[-1]), unread[0].type)]:
            keep_reducing = True
            while keep_reducing:
                keep_reducing = False

                for rule in grammar:
                    if match(stack, rule):
                        reduce(stack, rule)
                        keep_reducing = True
                        break

        stack.append(unread.pop(0))

    return stack[0]
