from textx import metamodel_from_file
from os.path import join, dirname
import collections
from bench import helpers

this_folder = dirname(__file__)


class Member:
    def __init__(self, key, value, parent=None):
        self.pair = (key, value)

    def __repr__(self):
        return str(self.pair)

    def __iter__(self):
        return iter(self.pair)


class Object(collections.UserDict):
    def __init__(self, members, parent=None):
        self.data = {key: value for key, value in members}


# class Array:
#     def __init__(self, values, parent=None):
#         self.value = list(values)
#
#     def __repr__(self):
#         return str(self.value)
class Array(collections.UserList):
    def __init__(self, values, parent=None):
        self.data = list(values)


def compile():
    json_mm = metamodel_from_file(
        join(this_folder, "json.tx"),
        debug=False,
        classes=[Member, Object, Array],
    )

    json_mm.register_obj_processors(
        {
            "NULL": lambda _: None,
            "STRING": lambda x: helpers.json_unescape(x),
            "FLOAT": float,
            "BOOL": lambda x: x == "true",
        }
    )

    return lambda s: json_mm.model_from_str(s)


parse = compile()
if __name__ == "__main__":
    print(parse("null"))
    assert parse("true") is True
    assert parse("null") is None, parse("null").__class__
    assert parse(R'"\"\b\f\n\r\t\/\\"') == '"\b\f\n\r\t/\\'
