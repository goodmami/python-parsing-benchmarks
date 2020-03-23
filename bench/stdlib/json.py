
import json


def invalid_constant(s):
    raise ValueError(s)


def parse(s):
    return json.loads(s, parse_constant=invalid_constant)
