
import pytest

TASK = 'ini'


def test_empty(parse):
    assert parse('') == {}


def test_comments(parse):
    assert parse('''
        ; comments

        ; nothing but comments
    ''') == {}


def test_section(parse):
    assert parse('[section]') == {'section': {}}
    assert parse('[a section]') == {'a section': {}}
    assert parse('[[[[]') == {'[[[': {}}
    assert parse('''
        ; comments
        [section]
        ; more comments = nothing
    ''') == {'section': {}}


def _make(s):
    return '''
        [s]
        {}
    '''.format(s)


def test_key_value(parse):
    assert parse(_make('x=5')) == {'s': {'x': '5'}}


def test_key(parse):
    assert parse(_make('x  =5')) == {'s': {'x': '5'}}
    assert parse(_make(' x =5')) == {'s': {'x': '5'}}
    assert parse(_make('  x=5')) == {'s': {'x': '5'}}
    assert parse(_make('x y=5')) == {'s': {'x y': '5'}}
    assert parse(_make(' x y =5')) == {'s': {'x y': '5'}}
    assert parse(_make('x   y=5')) == {'s': {'x   y': '5'}}
    assert parse(_make('[x=5')) == {'s': {'[x': '5'}}
    assert parse(_make('x]=5')) == {'s': {'x]': '5'}}
    assert parse(_make('x[y]=5')) == {'s': {'x[y]': '5'}}

def test_value(parse):
    assert parse(_make('x=5  ')) == {'s': {'x': '5'}}
    assert parse(_make('x= 5 ')) == {'s': {'x': '5'}}
    assert parse(_make('x=  5')) == {'s': {'x': '5'}}
    assert parse(_make('x=5 6')) == {'s': {'x': '5 6'}}
    assert parse(_make('x= 5 6 ')) == {'s': {'x': '5 6'}}
    assert parse(_make('x=5   6')) == {'s': {'x': '5   6'}}
    assert parse(_make('x=5=6')) == {'s': {'x': '5=6'}}
    assert parse(_make('x= " 5 " ')) == {'s': {'x': '" 5 "'}}
    assert parse(_make('x==')) == {'s': {'x': '='}}
    assert parse(_make('x=[val]')) == {'s': {'x': '[val]'}}


# def test_multiline(parse):
#     assert parse(_make('x=5\ny=6')) == {'s': {'x': '5', 'y': '6'}}
#     assert parse(_make('x=5\n y=6')) == {'s': {'x': '5\n y=6'}}
#     assert parse(_make('x=\n 5\\\n  y=6')) == {'s': {'x': '5  y=6'}}


def test_multisection(parse):
    assert parse('''
      [a section]
      x = 5
      [b section]
      x = 6
    ''') == {'a section': {'x': '5'}, 'b section': {'x': '6'}}


block = '''
x=1
    y  = indented keyval
w x y z = key with spaces
a = value with = character
abc = " something with quotes "
d[e] = not a section
[e = also not a section
f] = and this
g = [neither is this]
h===========
'''

big = '\n\n'.join(f'[section {i}]\n\n{block}' for i in range(1000))


def test_parse_time(parse, benchmark):
    benchmark.group = 'ini'
    result = benchmark(parse, big)
    assert len(result) == 1000


def test_compile_time(compile, benchmark):
    benchmark.group = 'ini-compile'
    parse = benchmark(compile)
    assert parse('''[section name]\n  x=5''') == {'section name': {'x': '5'}}
