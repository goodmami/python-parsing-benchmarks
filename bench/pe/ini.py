
import pe
from pe.actions import Constant, Pack, Raw


def _normalize_multiline(s):
    lines = s.strip().splitlines()
    # remove \ at end of non-final lines
    return ''.join(line[:-1] for line in lines[:-1]) + lines[-1]


def compile():
    INI = pe.compile(
        r'''
        Start   <- Section* EOF
        Section <- Comment* Header Body
        Header  <- Space* Title Space* (EOL / EOF)
        Title   <- '[' ~(![\]=\n\r] .)* ']'
        Body    <- Comment* (Pair Comment*)*
        Pair    <- Space* Key ('=' val:Value)?
        Key     <- !Title (![=\n\r] .)+
        Value   <- ('\\' EOL / !EOL .)*

        Comment <- Space* (';' (!EOL .)*)? (EOL / EOF)
        Space   <- [\t ]
        EOL     <- '\r\n' / [\n\r]
        EOF     <- !.
        ''',
        actions={
            'Start': Pack(dict),
            'Section': Pack(tuple),
            'Body': Pack(dict),
            'Pair': lambda key, val=None: (key, val),
            'Key': Raw(str.strip),
            'Value': Raw(_normalize_multiline),
        },
        flags=pe.OPTIMIZE
    )
    return lambda s: INI.match(s).value()


parse = compile()
