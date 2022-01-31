from lark import Lark, Transformer, v_args
from lark_cython import lark_cython

def compile():
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

        def number(self, n):
            return int(n.value)

    arithmetic_parser = Lark(arithmetic_grammar,
                             parser='lalr',
                             lexer='basic',
                             propagate_positions=False,
                             maybe_placeholders=False,
                             transformer=TreeToResult(), 
                             _plugins=lark_cython.plugins)

    return lambda s: arithmetic_parser.parse(s + ';')


parse = compile()
