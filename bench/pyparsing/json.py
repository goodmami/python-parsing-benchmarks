
import pyparsing as pp

from bench.helpers import json_unescape


LBRACE, RBRACE, LBRACK, RBRACK, COLON = map(pp.Suppress, '{}[]:')

value    = pp.Forward()

true     = pp.Keyword('true').setParseAction(pp.replaceWith(True))
false    = pp.Keyword('false').setParseAction(pp.replaceWith(False))
null     = pp.Keyword('null').setParseAction(pp.replaceWith(None))
number   = (pp.Regex(r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][-+]?[0-9]+)?')
            .setParseAction(pp.tokenMap(float)))
string   = (pp.Regex(r'"([ !#-\[\]-\U0010ffff]+'
                     r'|\\(?:["\\/bfnrt]|u[0-9A-Fa-f]{4}))*"')
            .setParseAction(pp.tokenMap(json_unescape)))

items    = pp.delimitedList(value)
array    = (pp.Group(LBRACK - pp.Optional(items) + RBRACK)
            .setParseAction(lambda t: t.asList()))

member   = pp.Group(string + COLON + value)
members  = pp.delimitedList(member)
object   = (pp.Dict(LBRACE - pp.Optional(members) + RBRACE)
            .setParseAction(lambda t: t.asDict()))

value   << (object | array | string | number | true | false | null)

json     = value('top') + pp.StringEnd()
json.setDefaultWhitespaceChars(' \t\n\r')
json.parseWithTabs()


def parse(s):
    return json.parseString(s)['top']
