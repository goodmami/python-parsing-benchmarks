
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from bench.helpers import json_unescape


Json = Grammar(r'''
    Start    = ~"\s*" Value ~"\s*"
    Object   = ~"{\s*" Members? ~"\s*}"
    Members  = Mapping (~"\s*,\s*" Mapping)*
    Mapping  = String ~"\s*:\s*" Value
    Array    = ~"\[\s*" Items? ~"\s*\]"
    Items    = Value (~"\s*,\s*" Value)*
    Value    = Object / Array / String
             / TrueVal / FalseVal / NullVal / Number
    TrueVal  = "true"
    FalseVal = "false"
    NullVal  = "null"
    String   = ~r"\"[ !#-\[\]-\U0010ffff]*(\\.[ !#-\[\]-\U0010ffff]*)*\""
    Number   = ~r"-?(0|[1-9][0-9]*)(\.\d*)?([eE][-+]?\d+)?"
''')

class JsonVisitor(NodeVisitor):
    def generic_visit(self, node, visited_children):
        return visited_children or node

    # helper functions for generic patterns
    def combine_many_or_one(self, node, children):
        """ Usable for following pattern:
            values = value_and_comma* value
        """
        members, member = children
        if isinstance(members, list):
            return members + [member]
        return [member]

    def lift_first_child(self, node, visited_children):
        """ Returns first child from `visited_children`, e.g. for::
            rule = item optional another_optional?
        returns `item`
        """
        return visited_children[0]

    # visitors
    visit_Value = lift_first_child
    visit_Members = visit_Items = combine_many_or_one

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
        print(values)
        if isinstance(values, list):
            values = values[0]
        else:
            values = []
        return values

    def visit_Mapping(self, node, children):
        key, _, value = children
        return key, value

    def visit_String(self, node, visited_children):
        return json_unescape(node.text)

    def visit_Number(self, node, visited_children):
        return float(node.text)

    def visit_TrueVal(self, node, visited_children):
        return True

    def visit_FalseVal(self, node, visited_children):
        return False

    def visit_NullVal(self, node, visited_children):
        return None


jv = JsonVisitor()


def parse(s):
    tree = Json.parse(s)
    return jv.visit(tree)

