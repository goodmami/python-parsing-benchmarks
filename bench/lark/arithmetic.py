
from lark import Lark, Transformer, v_args

from bench.helpers import apply_infix

arithmetic_grammar = r'''
    ?start: expr ";"
    ?expr: term
        | expr "+" term    -> add
        | expr "-" term    -> sub
    ?term: factor
        | term "*" factor  -> mul
        | term "/" factor  -> div
    ?factor: "-" factor    -> neg
        | "+" factor
        | INTEGER          -> number
        | "(" expr ")"
    INTEGER: "0" | "1".."9" INT?

    %import common.INT
    %import common.WS_INLINE
    %ignore WS_INLINE
'''

@v_args(inline=True)
class TreeToResult(Transformer):
    from operator import add, sub, mul, truediv as div, neg
    number = int


arithmetic_parser = Lark(arithmetic_grammar, parser='lalr',
                         lexer='standard',
                         propagate_positions=False,
                         maybe_placeholders=False,
                         transformer=TreeToResult())

def parse(s):
    return arithmetic_parser.parse(s + ';')
