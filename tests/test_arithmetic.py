
import pytest

TASK = 'arithmetic'


def test_factor(parse):
    assert parse('0') == 0
    assert parse('1') == 1
    assert parse('12') == 12
    assert parse('(12)') == 12
    assert parse('((12))') == 12
    assert parse('-1') == -1
    assert parse('--1') == 1
    assert parse('---1') == -1
    assert parse('+1') == 1
    assert parse('++1') == 1
    assert parse('+-+1') == -1
    assert parse('-(1)') == -1
    assert parse('-(-1)') == 1
    with pytest.raises(Exception):
        parse('01')
    with pytest.raises(Exception):
        parse('0 1')
    # skipping for stdlib eval
    # with pytest.raises(Exception):
    #     parse('()')
    with pytest.raises(Exception):
        parse('(1')
    with pytest.raises(Exception):
        parse('1)')


def test_plus(parse):
    assert parse('0 + 0') == 0
    assert parse('1 + 1') == 2
    with pytest.raises(Exception):
        parse('1 +')
    # skipping for stdlib eval
    # with pytest.raises(Exception):
    #     parse('+ 1')
    # with pytest.raises(Exception):
    #     parse('1 + + 1')


def test_minus(parse):
    assert parse('0 - 0') == 0
    assert parse('12 - 1') == 11
    with pytest.raises(Exception):
        parse('1 -')
    # skipping for stdlib eval
    # with pytest.raises(Exception):
    #     parse('- 1')
    # with pytest.raises(Exception):
    #     parse('1 - - 1')


def test_times(parse):
    assert parse('0 * 0') == 0
    assert parse('2 * 3') == 6
    with pytest.raises(Exception):
        parse('1 *')
    with pytest.raises(Exception):
        parse('* 1')
    with pytest.raises(Exception):
        parse('1 * * 1')


def test_divide(parse):
    assert parse('0 / 1') == 0
    assert parse('8 / 2') == 4
    assert parse('1 / 2') == 0.5
    with pytest.raises(Exception):
        parse('1 / 0')
    with pytest.raises(Exception):
        parse('1 /')
    with pytest.raises(Exception):
        parse('/ 1')
    with pytest.raises(Exception):
        parse('1 / / 1')


def test_expr(parse):
    assert parse('1 + 2 + 3') == 6
    assert parse('1 - 2 + 3') == 2
    assert parse('1 - (2 + 3)') == -4
    assert parse('(1 - 2) + 3') == 2
    assert parse('1 * 2 + 3') == 5
    assert parse('1 + 2 * 3') == 7
    assert parse('(1 + 2) * 3') == 9
    assert parse('1 * 2 / 4') == 0.5
    assert parse('3 * 4 / 2') == 6
    assert parse('3 * (4 / 2)') == 6
    assert parse('((3)) + ((4)) * ((2))') == 11


l1 = ('1 + 2 + 4 + 5 + 6 + 7 + 8 + 9 + 10'
      ' + ((((((11 * 12 * 13 * 14 * 15 + 16 * 17 + 18 * 19 * 20))))))')
l2 = '2*3 + 4*5*6'
l3 = '12 + (2 * 3 * 4 * 5 + 6 + 7 * 8)'
block = [l1] + 333 * [l2, l3, l1]
xl = 10 * block
# xxl = 10 * xl


def test_parse_time(parse, benchmark):
    benchmark.group = 'arithmetic'

    def parse_all(ss):
        results = []
        for s in ss:
            results.append(parse(s))
        return results

    results = benchmark(parse_all, xl)
    assert len(results) == len(xl)


def test_compile_time(compile, benchmark):
    benchmark.group = 'arithmetic-compile'
    parse = benchmark(compile)
    assert parse('1 + 2 * 3') == 7
