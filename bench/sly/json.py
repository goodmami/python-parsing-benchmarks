
from sly import Lexer, Parser

from bench.helpers import json_unescape


def compile():
    class JsonLexer(Lexer):
        tokens = { STRING, NUMBER, TRUE, FALSE, NULL }
        ignore = ' \t\n\r'
        literals = { '{', '}', '[', ']', ':', ',' }

        @_(r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([Ee][+-]?[0-9]+)?')
        def NUMBER(self, t):
            t.value = float(t.value)
            return t

        @_(r'"([ !#-\[\]-\U0010ffff]+|\\(["\/\\bfnrt]|u[0-9A-Fa-f]{4}))*"')
        def STRING(self, t):
            t.value = json_unescape(t.value)
            return t

        @_(r'true')
        def TRUE(self, t):
            t.value = True
            return t

        @_(r'false')
        def FALSE(self, t):
            t.value = False
            return t

        @_(r'null')
        def NULL(self, t):
            t.value = None
            return t


    class JsonParser(Parser):
        tokens = JsonLexer.tokens
        start = 'value'

        @_(r'"{" [ pairs ] "}"')
        def value(self, p):
            if p.pairs:
                return dict(p.pairs)
            else:
                return {}

        @_(r'pair { "," pair }')
        def pairs(self, p):
            return [p.pair0] + p.pair1

        @_(r'STRING ":" value')
        def pair(self, p):
            return (p.STRING, p.value)

        @_(r'"[" [ items ] "]"')
        def value(self, p):
            if p.items:
                return p.items
            else:
                return []

        @_(r'value { "," value }')
        def items(self, p):
            return [p.value0] + p.value1

        @_('STRING',
           'NUMBER',
           'TRUE',
           'FALSE',
           'NULL')
        def value(self, p):
            return p[0]

        def error(self, p):
            raise ValueError(p)

    lexer = JsonLexer()
    parser = JsonParser()

    return lambda s: parser.parse(lexer.tokenize(s))

parse = compile()
