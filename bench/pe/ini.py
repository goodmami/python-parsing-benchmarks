
import pe
from pe.actions import Constant, Pack, Capture


def _normalize_multiline(s):
    lines = s.strip().splitlines()
    # remove \ at end of non-final lines
    return ''.join(line[:-1] for line in lines[:-1]) + lines[-1]


def compile():
    INI = pe.compile(
        r'''
        Start   <- (Comment* Section)* Comment* EOF
        Section <- Header Body
        Header  <- Space* Title Space* (EOL / EOF)
        Title   <- '[' ~(![\]=\n\r] .)* ']'
        Body    <- (Comment* Pair)*
        Pair    <- Space* Key ('=' val:Value)?
        Key     <- !Title (![=\n\r] .)+
        Value   <- ('\\' EOL / !EOL .)*

        Comment <- (Space* ';' (!EOL .)* / Space+) (EOL / EOF)
                 / EOL
        Space   <- [\t ]
        EOL     <- '\r\n' / [\n\r]
        EOF     <- !.
        ''',
        actions={
            'Start': Pack(dict),
            'Section': Pack(tuple),
            'Body': Pack(dict),
            'Pair': lambda key, val=None: (key, val),
            'Key': Capture(str.strip),
            'Value': Capture(_normalize_multiline),
        },
        parser='machine',
        flags=pe.OPTIMIZE
    )
    return lambda s: INI.match(s).value()


parse = compile()
