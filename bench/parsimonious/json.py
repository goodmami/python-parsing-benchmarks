
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from bench.helpers import json_unescape


def compile():
    g = Grammar(r'''
        Start    = ~r"\s*" Value ~r"\s*"
        Object   = ~r"{\s*" Members? ~r"\s*}"
        Members  = Mapping (~r"\s*,\s*" Mapping)*
        Mapping  = String ~r"\s*:\s*" Value
        Array    = ~r"\[\s*" Items? ~r"\s*\]"
        Items    = Value (~r"\s*,\s*" Value)*
        Value    = Object / Array / String
                 / TrueVal / FalseVal / NullVal / Number
        TrueVal  = "true"
        FalseVal = "false"
        NullVal  = "null"
        String   = ~r"\"[ !#-\[\]-\U0010ffff]*(?:\\(?:[\"\\/bfnrt]|u[0-9A-Fa-f]{4})[ !#-\[\]-\U0010ffff]*)*\""
        Number   = ~r"-?(0|[1-9][0-9]*)(\.\d*)?([eE][-+]?\d+)?"
    ''')

    class JsonVisitor(NodeVisitor):
        def generic_visit(self, node, children):
            return children or node.text

        # helper functions for generic patterns
        def delimited(self, node, children):
            items = [children[0]]
            items.extend(item for _, item in children[1])
            return items

        def atomic(self, node, children):
            return children[0]

        # visitors
        visit_Value = atomic
        visit_Members = visit_Items = delimited

        def visit_Start(self, node, children):
            return children[1]

        def visit_Object(self, node, children):
            _, members, _ = children
            if isinstance(members, list):
                members = members[0]
            else:
                members = []
            return dict(members)

        def visit_Array(self, node, children):
            _, values, _ = children
            if isinstance(values, list):
                values = values[0]
            else:
                values = []
            return values

        def visit_Mapping(self, node, children):
            key, _, value = children
            return key, value

        def visit_String(self, node, children):
            return json_unescape(node.text)

        def visit_Number(self, node, children):
            return float(node.text)

        def visit_TrueVal(self, node, children):
            return True

        def visit_FalseVal(self, node, children):
            return False

        def visit_NullVal(self, node, children):
            return None

    v = JsonVisitor()
    return lambda s: v.visit(g.parse(s))


parse = compile()
