
import pytest

TASK = 'json'


def test_true(parse):
    assert parse('true') is True
    assert parse('  true  ') is True


def test_false(parse):
    assert parse('false') is False
    assert parse('  false  ') is False


def test_null(parse):
    assert parse('null') is None
    assert parse('  null  ') is None


def test_number(parse):
    assert parse('0') == 0
    assert parse('  0  ') == 0
    assert parse('123') == 123
    assert parse('-123') == -123
    assert parse('1.2') == 1.2
    assert parse('-1e2') == -100
    assert parse('1.2e3') == 1200
    assert parse('1.2e-3') == 0.0012
    assert parse('1.2e+3') == 1200
    with pytest.raises(Exception):
        parse('01')
    with pytest.raises(Exception):
        parse('+1')
    with pytest.raises(Exception):
        parse('Infinity')
    with pytest.raises(Exception):
        parse('NaN')


def test_string(parse):
    assert parse('""') == ''
    assert parse('"abc"') == 'abc'
    assert parse('  "abc"  ') == 'abc'
    assert parse('"\\"\\b\\f\\n\\r\\t\\/\\\\"') == '"\b\f\n\r\t/\\'
    assert parse('"字"') == '字'
    assert parse('"\u5b57"') == '字'
    assert parse('"\u5B57"') == '字'
    assert parse('"\u4e2d文\u5b57"') == '中文字'
    # specification does not prescribe how to treat surrogate sequences
    assert parse('"\ud834\udd1e"') in ('𝄞', '\ud834\udd1e')
    with pytest.raises(Exception):
        parse("'abc'")
    with pytest.raises(Exception):
        parse(f'"\b"')
    with pytest.raises(Exception):
        parse(f'"\f"')
    with pytest.raises(Exception):
        parse(f'"\n"')
    with pytest.raises(Exception):
        parse(f'"\r"')
    with pytest.raises(Exception):
        parse(f'"\t"')
    with pytest.raises(Exception):
        parse(f'"\\x"')
    with pytest.raises(Exception):
        parse(f'"\\uDEFG"')


def test_array(parse):
    # assumes parser produces lists and not other iterable types
    assert parse('[]') == []
    assert parse('  [ \t\r\n]  ') == []
    assert parse('[true]') == [True]
    assert parse('[false]') == [False]
    assert parse('[null]') == [None]
    assert parse('[1]') == [1]
    assert parse('["a"]') == ['a']
    assert parse('[[]]') == [[]]
    assert parse('[{}]') == [{}]
    assert parse('[true,false,null]') == [True, False, None]
    assert parse('[true, false, null]') == [True, False, None]
    assert parse('[true ,false ,null]') == [True, False, None]
    assert parse('[\n true,\t false,\r null]') == [True, False, None]
    with pytest.raises(Exception):
        parse('[1 2]')
    with pytest.raises(Exception):
        parse('[1, 2,]')
    with pytest.raises(Exception):
        parse('[,1 ,2]')


def test_object(parse):
    # assumes parser produces dicts and not other mapping types
    assert parse('{}') == {}
    assert parse('  { \t\r\n}  ') == {}
    assert parse('{"name": true}') == {'name': True}
    assert parse('{"name": false}') == {'name': False}
    assert parse('{"name": null}') == {'name': None}
    assert parse('{"name": 1}') == {'name': 1}
    assert parse('{"name": "a"}') == {'name': 'a'}
    assert parse('{"name": []}') == {'name': []}
    assert parse('{"name": {}}') == {'name': {}}

    assert parse(
        '{"name1":true,"name2":false,"name3":null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse(
        '{"name1": true, "name2": false, "name3": null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse(
        '{"name1" :true ,"name2" :false ,"name3" :null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse(
        '{\n "name1": true,\t "name2": false,\r "name3": null}') == {
        'name1': True, 'name2': False, 'name3': None}
    assert parse(
        '{"name with spaces": true}') == {
        'name with spaces': True}
    assert parse('{"": true}') == {'': True}

    # it is undefined which value with a non-unique name is selected
    assert len(parse('{"name": true, "name": false}')) == 1
    with pytest.raises(Exception):
        parse('{"name": true "name": false}')
    with pytest.raises(Exception):
        parse('{"name": true, "name": false,}')
    with pytest.raises(Exception):
        parse('{,"name": true, "name": false}')
    with pytest.raises(Exception):
        parse('{"name": }')


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


def test_parse_time(parse, benchmark):
    benchmark.group = 'json'
    result = benchmark(parse, big)
    assert len(result) == 5000


def test_compile_time(compile, benchmark):
    benchmark.group = 'json-compile'
    parse = benchmark(compile)
    assert parse('{"foo": 1.234e-5}') == {'foo': 1.234e-5}


def _find_recursion_limit(parse, j=1001):
    """Binary search between 1 and *j* to find the recursion limit."""
    i = 1
    while True:
        try:
            parse(('[' * i) + (']' * i))
        # Don't just catch RecursionError in case a library throws
        # something else; if it's not a recursion error, this loop
        # will quickly go to 0
        except Exception:
            j = i
            i = int(i / 2)
            if i <= 1:
                break
        else:
            if j - i <= 1:
                break
            i += int((j - i) / 2)
    return i


def test_recursion(parse):
    limit = _find_recursion_limit(parse, 1001)
    assert limit > 50
    print(f'recursion limit: {"1000+" if limit >= 1000 else limit}')
