from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from os.path import join, dirname

# STRING = _(r'"([ !#-\[\]-\U0010ffff]+|\\(["\/\\bfnrt]|u[0-9A-Fa-f]{4}))*"')
# FLOAT = _(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([Ee][+-]?[0-9]+)?")
# BOOL = _(r"(true|false)\b", rule_name="BOOL", root=True)
this_folder = dirname(__file__)


class Member:
    def __init__(self, key, value, parent=None):
        self.pair = (key, value)

    def __repr__(self):
        return str(self.pair)

    def __iter__(self):
        return iter(self.pair)


class Object:
    def __init__(self, members, parent=None):
        self.value = {key: value for key, value in members}

    def __repr__(self):
        return str(self.value)


json_mm = metamodel_from_file(
    join(this_folder, "json.tx"),
    debug=False,
    builtins={"FLOAT": float, "BOOL": bool, "STRING": str},
    classes=[Member, Object],
)


def parse(s):
    return json_mm.model_from_string(s)
