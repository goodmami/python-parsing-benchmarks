import re


_json_unesc_re = re.compile(r'\\(["/\\bfnrt]|u[0-9A-Fa-f])')
_json_unesc_map = {
    '"': '"',
    '/': '/',
    '\\': '\\',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
}


def _json_unescape(m):
    c = m.group(1)
    if c[0] == 'u':
        return chr(int(c[1:], 16))
    c2 = _json_unesc_map.get(c)
    if not c2:
        raise ValueError(f'invalid escape sequence: {m.group(0)}')
    return c2


def json_unescape(s):
    return _json_unesc_re.sub(_json_unescape, s[1:-1])


def apply_infix(term, *rest):
    if rest:
        op, rhs = rest
        return op(term, rhs)
    else:
        return term


def reduce_infix(term, *rest):
    total = term
    for i in range(0, len(rest), 2):
        op = rest[i]
        rhs = rest[i+1]
        total = op(total, rhs)
    return total
