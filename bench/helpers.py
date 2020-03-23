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
    else:
        return _json_unesc_map[c]


def json_unescape(s):
    return _json_unesc_re.sub(_json_unescape, s[1:-1])
