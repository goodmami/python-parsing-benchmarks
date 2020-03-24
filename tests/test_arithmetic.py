
import pytest


def test_factor(parse_arithmetic):
    assert parse_arithmetic('0') == 0
    assert parse_arithmetic('1') == 1
    assert parse_arithmetic('12') == 12
    assert parse_arithmetic('(12)') == 12
    assert parse_arithmetic('((12))') == 12
    assert parse_arithmetic('-1') == -1
    assert parse_arithmetic('--1') == 1
    assert parse_arithmetic('---1') == -1
    assert parse_arithmetic('+1') == 1
    assert parse_arithmetic('++1') == 1
    assert parse_arithmetic('+-+1') == -1
    assert parse_arithmetic('-(1)') == -1
    assert parse_arithmetic('-(-1)') == 1
    with pytest.raises(Exception):
        parse_arithmetic('01')
    with pytest.raises(Exception):
        parse_arithmetic('0 1')
    # skipping for stdlib eval
    # with pytest.raises(Exception):
    #     parse_arithmetic('()')
    with pytest.raises(Exception):
        parse_arithmetic('(1')
    with pytest.raises(Exception):
        parse_arithmetic('1)')


def test_plus(parse_arithmetic):
    assert parse_arithmetic('0 + 0') == 0
    assert parse_arithmetic('1 + 1') == 2
    with pytest.raises(Exception):
        parse_arithmetic('1 +')
    # skipping for stdlib eval
    # with pytest.raises(Exception):
    #     parse_arithmetic('+ 1')
    # with pytest.raises(Exception):
    #     parse_arithmetic('1 + + 1')


def test_minus(parse_arithmetic):
    assert parse_arithmetic('0 - 0') == 0
    assert parse_arithmetic('12 - 1') == 11
    with pytest.raises(Exception):
        parse_arithmetic('1 -')
    # skipping for stdlib eval
    # with pytest.raises(Exception):
    #     parse_arithmetic('- 1')
    # with pytest.raises(Exception):
    #     parse_arithmetic('1 - - 1')


def test_times(parse_arithmetic):
    assert parse_arithmetic('0 * 0') == 0
    assert parse_arithmetic('2 * 3') == 6
    with pytest.raises(Exception):
        parse_arithmetic('1 *')
    with pytest.raises(Exception):
        parse_arithmetic('* 1')
    with pytest.raises(Exception):
        parse_arithmetic('1 * * 1')


def test_divide(parse_arithmetic):
    assert parse_arithmetic('0 / 1') == 0
    assert parse_arithmetic('8 / 2') == 4
    assert parse_arithmetic('1 / 2') == 0.5
    with pytest.raises(Exception):
        parse_arithmetic('1 / 0')
    with pytest.raises(Exception):
        parse_arithmetic('1 /')
    with pytest.raises(Exception):
        parse_arithmetic('/ 1')
    with pytest.raises(Exception):
        parse_arithmetic('1 / / 1')


def test_expr(parse_arithmetic):
    assert parse_arithmetic('1 + 2 + 3') == 6
    assert parse_arithmetic('1 - 2 + 3') == 2
    assert parse_arithmetic('1 - (2 + 3)') == -4
    assert parse_arithmetic('(1 - 2) + 3') == 2
    assert parse_arithmetic('1 * 2 + 3') == 5
    assert parse_arithmetic('1 + 2 * 3') == 7
    assert parse_arithmetic('(1 + 2) * 3') == 9
    assert parse_arithmetic('1 * 2 / 4') == 0.5
    assert parse_arithmetic('3 * 4 / 2') == 6
    assert parse_arithmetic('3 * (4 / 2)') == 6
    assert parse_arithmetic('((3)) + ((4)) * ((2))') == 11


l1 = ('1 + 2 + 4 + 5 + 6 + 7 + 8 + 9 + 10'
      ' + ((((((11 * 12 * 13 * 14 * 15 + 16 * 17 + 18 * 19 * 20))))))')
l2 = '2*3 + 4*5*6'
l3 = '12 + (2 * 3 * 4 * 5 + 6 + 7 * 8)'
block = [l1] + 333 * [l2, l3, l1]
xl = 10 * block
# xxl = 10 * xl


def test_time(parse_arithmetic, benchmark):
    benchmark.group = 'arithmetic'

    def parse_all(ss):
        results = []
        for s in ss:
            results.append(parse_arithmetic(s))
        return results

    results = benchmark(parse_all, xl)
    assert len(results) == len(xl)
