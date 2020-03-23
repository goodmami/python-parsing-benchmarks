
import pytest


def test_true(parse_json):
    assert parse_json('true') is True
    assert parse_json('  true  ') is True


def test_false(parse_json):
    assert parse_json('false') is False
    assert parse_json('  false  ') is False


def test_null(parse_json):
    assert parse_json('null') is None
    assert parse_json('  null  ') is None


def test_number(parse_json):
    assert parse_json('0') == 0
    assert parse_json('  0  ') == 0
    assert parse_json('123') == 123
    assert parse_json('-123') == -123
    assert parse_json('1.2') == 1.2
    assert parse_json('-1e2') == -100
    assert parse_json('1.2e3') == 1200
    assert parse_json('1.2e-3') == 0.0012
    assert parse_json('1.2e+3') == 1200
    with pytest.raises(Exception):
        parse_json('01')
    with pytest.raises(Exception):
        parse_json('+1')
    with pytest.raises(Exception):
        parse_json('Infinity')
    with pytest.raises(Exception):
        parse_json('NaN')


def test_string(parse_json):
    assert parse_json('""') == ''
    assert parse_json('"abc"') == 'abc'
    assert parse_json('  "abc"  ') == 'abc'
    assert parse_json('"\\"\\b\\f\\n\\r\\t\\/\\\\"') == '"\b\f\n\r\t/\\'
    assert parse_json('"字"') == '字'
    assert parse_json('"\u5b57"') == '字'
    assert parse_json('"\u5B57"') == '字'
    assert parse_json('"\u4e2d文\u5b57"') == '中文字'
    # specification does not prescribe how to treat surrogate sequences
    assert parse_json('"\ud834\udd1e"') in ('𝄞', '\ud834\udd1e')
    with pytest.raises(Exception):
        parse_json("'abc'")
    for c in '\b\f\n\r\t':
        with pytest.raises(Exception):
            parse_json(f'"{c}"')


def test_array(parse_json):
    # assumes parser produces lists and not other iterable types
    assert parse_json('[]') == []
    assert parse_json('  [ \t\r\n]  ') == []
    assert parse_json('[true]') == [True]
    assert parse_json('[false]') == [False]
    assert parse_json('[null]') == [None]
    assert parse_json('[1]') == [1]
    assert parse_json('["a"]') == ['a']
    assert parse_json('[[]]') == [[]]
    assert parse_json('[{}]') == [{}]
    assert parse_json('[true,false,null]') == [True, False, None]
    assert parse_json('[true, false, null]') == [True, False, None]
    assert parse_json('[true ,false ,null]') == [True, False, None]
    assert parse_json('[true,\n false,\n null]') == [True, False, None]
    with pytest.raises(Exception):
        parse_json('[1 2]')
    with pytest.raises(Exception):
        parse_json('[1, 2,]')
    with pytest.raises(Exception):
        parse_json('[,1 ,2]')


def test_object(parse_json):
    # assumes parse_jsonr produces dicts and not other mapping types
    assert parse_json('{}') == {}
    assert parse_json('  { \t\r\n}  ') == {}
    assert parse_json('{"name": true}') == {'name': True}
    assert parse_json('{"name": false}') == {'name': False}
    assert parse_json('{"name": null}') == {'name': None}
    assert parse_json('{"name": 1}') == {'name': 1}
    assert parse_json('{"name": "a"}') == {'name': 'a'}
    assert parse_json('{"name": []}') == {'name': []}
    assert parse_json('{"name": {}}') == {'name': {}}

    assert parse_json(
        '{"name1":true,"name2":false,"name3":null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse_json(
        '{"name1": true, "name2": false, "name3": null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse_json(
        '{"name1" :true ,"name2" :false ,"name3" :null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse_json(
        '{\n "name1": true,\n "name2": false,\n "name3": null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse_json(
        '{"name with spaces": true}') == {
        'name with spaces': True}
    assert parse_json('{"": true}') == {'': True}

    # it is undefined which value with a non-unique name is selected
    assert len(parse_json('{"name": true, "name": false}')) == 1
    with pytest.raises(Exception):
        parse_json('{"name": true "name": false}')
    with pytest.raises(Exception):
        parse_json('{"name": true, "name": false,}')
    with pytest.raises(Exception):
        parse_json('{,"name": true, "name": false}')
    with pytest.raises(Exception):
        parse_json('{"name": }')


obj = [r'''
{"true": true,
 "false": false,
 "null": null,
 "integer": -123,
 "float": 123.456e-7,
 "string": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
 "escaped": "this is a quote: \" and this is a slash: \\",
 "unicode": "この字は日本語の字だ\n這些字是中文字\nEstas son palabras en español",
 "escaped unicode": "\u3053\u306e\u5b57\u306f\u65e5\u672c\u8a9e\u306e\u5b57\u3060\u000a\u9019\u4e9b\u5b57\u662f\u4e2d\u6587\u5b57\u000a\u0045\u0073\u0074\u0061\u0073\u0020\u0073\u006f\u006e\u0020\u0070\u0061\u006c\u0061\u0062\u0072\u0061\u0073\u0020\u0065\u006e\u0020\u0065\u0073\u0070\u0061\u00f1\u006f\u006c",
 "mixed unicode": "この\u5b57は\u65e5\u672c\u8a9eの\u5b57だ\n\u9019\u4e9b字\u662f中文字\nEstas son palabras en espa\u00f1ol",
 "object": {"again": {"and again": {"that's": "enough"}}},
 "array": [1,[2,[3,[4,[5,[6,[7,[8,[9,[10]]]]]]]]]]
}''']

big = '[' + ','.join(5000 * obj) + ']'


def test_performance(parse_json, benchmark):
    result = benchmark(parse_json, big)
    assert len(result) == 5000


def test_recursion(parse_json):
    i = 1
    j = 1001
    while True:
        try:
            parse_json(('[' * i) + (']' * i))
        except RecursionError:
            j = i
            i = int(i / 2)
            if i <= 1:
                break
        else:
            if j - i <= 1:
                break
            i += int((j - i) / 2)
    parse_json(('[' * i) + (']' * i))
    print(f'maximum recursion depth: {i}')
    assert i >= 150, f'failed at recursion depth {i}'
