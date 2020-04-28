
import pe
from pe.actions import Constant, Pack, Raw

from bench.helpers import json_unescape


def compile():
    Json = pe.compile(
        r'''
        # Syntactic rules
        Start    <- Spacing Value EOF
        Value    <- Object / Array / String / Number / Constant
        Object   <- LBRACE (Member (COMMA Member)*)? RBRACE
        Member   <- String COLON Value
        Array    <- LBRACK (Value (COMMA Value)*)? RBRACK
        String   <- ["] CHAR* ( ESC CHAR* )* ["]
        Number   <- INTEGER FRACTION? EXPONENT?
        Constant <- TRUE / FALSE / NULL

        # Lexical rules
        CHAR     <- [ !#-\[\]-\U0010ffff]
        ESC      <- '\\' ( ["\\/bfnrt]
                         / 'u' HEX HEX HEX HEX )
        HEX      <- [0-9a-fA-F]
        INTEGER  <- "-"? ("0" / [1-9] [0-9]*)
        FRACTION <- "." [0-9]+
        EXPONENT <- [eE] [-+]? [0-9]+
        TRUE     <- "true"
        FALSE    <- "false"
        NULL     <- "null"
        LBRACE   <- "{" Spacing
        RBRACE   <- Spacing "}"
        LBRACK   <- "[" Spacing
        RBRACK   <- Spacing "]"
        COMMA    <- Spacing "," Spacing
        COLON    <- Spacing ":" Spacing
        Spacing  <- [\t\n\r ]*
        EOF      <- Spacing !.
        ''',
        actions = {
            'Object': Pack(dict),
            'Member': Pack(tuple),
            'Array': Pack(list),
            'String': Raw(json_unescape),
            'Number': Raw(float),
            'TRUE': Constant(True),
            'FALSE': Constant(False),
            'NULL': Constant(None),
        },
        flags=pe.OPTIMIZE)
    return lambda s: Json.match(s, flags=pe.STRICT).value()


parse = compile()
