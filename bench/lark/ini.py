import logging; logging.basicConfig(level=logging.DEBUG)

from lark import Lark, Transformer, v_args

# adapted from https://github.com/lark-parser/lark/blob/master/examples/conf_lalr.py
def compile():

    class TreeToDict(Transformer):
        start = dict

        @v_args(inline=True)
        def section(self, header, *pairs):
            return (header[1:-1], dict(pairs))

        @v_args(inline=True)
        def stripped(self, s=''):
            return str.strip(s)

        value = key = stripped
        header = v_args(inline=True)(str)
        keyval = tuple
        bare_key = v_args(inline=True)(lambda self, key: (key, None))

    parser = Lark(
        r"""
        start: _NL* section*
        section: header _NL+ (keyval _NL+)*
        keyval: key "=" value
              | key                     -> bare_key

        header: /\[[^\n\r\]]+\]/
        key: /[^\n\r=]+/
        value: /[^\n\r]+/
             |

        COMMENT: ";" /[^\n]/* _NL
        %import common.NEWLINE -> _NL
        %import common.WS_INLINE
        %ignore WS_INLINE
        %ignore COMMENT
        """,
        parser="lalr",
        transformer=TreeToDict(),
    )
    return lambda s: parser.parse(s + '\n')


parse = compile()


if __name__ == '__main__':
    print(parse(';comment only'))
    print(parse(';comment\n\n  ; indented comment'))
    print(parse('[section title]'))
    print(parse('''
       [section one]
       x=4
       a b c  =  d e f

       ; comment

       [  section two  ]
         z
           y=123
         w=
    '''))
