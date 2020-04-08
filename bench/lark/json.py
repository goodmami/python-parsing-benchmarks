
from lark import Lark, Transformer, v_args

from bench.helpers import json_unescape


def compile():
    # NOTE: the ; after value is to detect the end of the input
    json_grammar = r"""
        ?start: _WS? value _WS? ";"

        ?value: object
              | array
              | string
              | NUMBER             -> number
              | "true"             -> true
              | "false"            -> false
              | "null"             -> null

        array  : _BRACK1 [value (_COMMA value)*] _BRACK2
        object : _CURLY1 [pair (_COMMA pair)*] _CURLY2
        pair   : string _COLON value

        _COLON: /\s*:\s*/
        _COMMA: /\s*,\s*/
        _CURLY1: /\s*{\s*/
        _CURLY2: /\s*}\s*/
        _BRACK1: /\s*\[\s*/
        _BRACK2: /\s*\]\s*/

        string : STRING
        STRING: "\"" INNER* "\""
        INNER: /[ !#-\[\]-\U0010ffff]*/
             | /\\(?:["\/\\bfnrt]|u[0-9A-Fa-f]{4})/

        NUMBER : INTEGER FRACTION? EXPONENT?
        INTEGER: ["-"] ("0" | "1".."9" INT?)
        FRACTION: "." INT
        EXPONENT: ("e"|"E") ["+"|"-"] INT

        _WS: /\s+/

        %import common.INT
    """

    class TreeToJson(Transformer):
        @v_args(inline=True)
        def string(self, s):
            return json_unescape(s)

        array = list
        pair = tuple
        object = dict
        number = v_args(inline=True)(float)

        null = lambda self, _: None
        true = lambda self, _: True
        false = lambda self, _: False

    json_parser = Lark(json_grammar,
                       parser='lalr',
                       lexer='standard',
                       propagate_positions=False,
                       maybe_placeholders=False,
                       transformer=TreeToJson())

    # trailing ; is currently necessary to detect end of input
    return lambda s: json_parser.parse(s + ';')


parse = compile()
