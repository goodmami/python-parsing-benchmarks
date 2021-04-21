from os.path import dirname, join

from bench import helpers
from textx import metamodel_from_str


def compile():
    class Object(dict):
        def __init__(self, members, parent=None):
            self.update((m.key, m.value) for m in members)

    class Array(list):
        def __init__(self, values, parent=None):
            self.extend(values)

    json_mm = metamodel_from_str(
        """/*
            A grammar for JSON data-interchange format.
            See: http://www.json.org/
        */
        File:
            Value
        ;

        Array:
            "[" values*=Value[','] "]"
        ;

        Value:
            STRING | FLOAT | BOOL | Object | Array | NULL
        ;


        STRING:
            /"([ !#-\[\]-\U0010ffff]+|\\(["\/\\bfnrt]|u[0-9A-Fa-f]{4}))*"/
        ;

        FLOAT:
            /-?(0|[1-9][0-9]*)(\.[0-9]+)?([Ee][+-]?[0-9]+)?/
        ;

        BOOL:
            /\b(true|false)\b/
        ;

        NULL:
            /\bnull\b/
        ;

        Object:
            "{" members*=Member[','] "}"
        ;

        Member:
            key=STRING ':' value=Value
        ;
""",
        debug=False,
        classes=[Object, Array],
    )

    json_mm.register_obj_processors(
        {
            "NULL": lambda _: None,
            "STRING": helpers.json_unescape,
            "FLOAT": float,
            "BOOL": lambda x: x == "true",
        }
    )

    return lambda s: json_mm.model_from_str(s)


parse = compile()
# if __name__ == "__main__":
#     print(parse("null"))
#     assert parse("true") is True
#     assert parse("null") is None, parse("null").__class__
#     assert parse(R'"\"\b\f\n\r\t\/\\"') == '"\b\f\n\r\t/\\'
