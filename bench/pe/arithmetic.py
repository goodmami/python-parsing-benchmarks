
from operator import add, sub, mul, truediv as div, neg

import pe
from pe.actions import Constant

from bench.helpers import reduce_infix


def reduce_prefix(*args):
    term = args[-1]
    for op in args[:-1]:
        term = op(term)
    return term


def compile():
    parser = pe.compile(
        r'''
        Start   <- Spacing Expr EOL? EOF
        Expr    <- Term ((PLUS / MINUS) Term)*
        Term    <- Factor ((TIMES / DIVIDE) Factor)*
        Factor  <- Sign* (LPAR Expr RPAR
                         / INTEGER )
        Sign    <- NEG / POS
        INTEGER <- ~( '0' / [1-9] [0-9]* ) Spacing
        PLUS    <- '+' Spacing
        MINUS   <- '-' Spacing
        TIMES   <- '*' Spacing
        DIVIDE  <- '/' Spacing
        LPAR    <- '(' Spacing
        RPAR    <- ')' Spacing
        NEG     <- '-' Spacing
        POS     <- '+' Spacing
        Spacing <- [ \t\n\f\v\r]*
        EOL     <- '\r\n' / [\n\r]
        EOF     <- !.
        ''',
        actions={
            'Expr': reduce_infix,
            'Term': reduce_infix,
            'Factor': reduce_prefix,
            'INTEGER': int,
            'PLUS': Constant(add),
            'MINUS': Constant(sub),
            'TIMES': Constant(mul),
            'DIVIDE': Constant(div),
            'NEG': Constant(neg),
        },
        flags=pe.OPTIMIZE
    )

    return lambda s: parser.match(s).value()


parse = compile()
