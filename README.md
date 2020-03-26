# Python Parsing Benchmarks

This repository contains a suite of test cases and implementations for
parsing text using Python. Both speed an memory usage are compared for
each implementation. Each implementation must be:

* **Correct** -- it implements the specification exactly
  - Syntax -- it parses all valid inputs and rejects bad ones
  - Semantics -- it produces the expected data structures
* **Plausible** -- it only uses generally known parser features or
  parsing strategies

Validation tests can ensure the correctness of an implementation, but
its plausibility is harder to pin down. Basically, grammars that
require knowlege of a parser's internals or undocumented features to
increase performance are discouraged. The grammar should be
understandable by someone with access to the parser's documentation
and examples.


## Implementations

This table lists the tasks performed and the libraries benchmarked. An
empty cell indicates that there is no implementation for that library
(yet; contributions welcome!). The stdlib implementation is held as
the baseline and the timing numbers are a ratio to that baseline
(e.g., 19.3 means it is 19.3 times slower than the baseline). Bold
numbers are the fastest non-baseline implementation.

(These numbers are run using CPython)

| Implementation | Algorithm           | [JSON]      | [Arithmetic] |
| -------------- | ------------------- | ----------: | -----------: |
| [stdlib]       | handwritten         | 1.0         | 1.0          |
| [Lark]         | [LALR]              | 53.0        | **19.3**     |
| [parsimonious] | [Recursive Descent] | 116.2       | --           |
| [pe]           | [Recursive Descent] | **30.7**    | 22.2         |
| [pyparsing]    | [Recursive Descent] | 161.9       | --           |

[stdlib]: https://docs.python.org/3/
[Lark]: https://github.com/lark-parser/lark
[parsimonious]: https://github.com/erikrose/parsimonious
[pe]: https://github.com/goodmami/pe
[pyparsing]: https://github.com/pyparsing/pyparsing/

[JSON]: tasks/json.md
[Arithmetic]: tasks/arithmetic.md

[LALR]: https://en.wikipedia.org/wiki/LALR_parser
[Recursive Descent]: https://en.wikipedia.org/wiki/Recursive_descent_parser


## Setup

Python 3.6+ is required.

First create a virtual environment (recommended) and install the
package and requirements:

``` console
$ python3 -m venv cpy
$ source cpy/bin/activate
(cpy) $ pip install -r requirements.txt
```

You can also use PyPy by creating its own virtual environment:

``` console
$ pypy3 -m venv pypy
$ source pypy/bin/activate
(pypy) $ pip install -r requirements.txt
```

From here on it's assumed you're in one of the `(cpy)` or `(pypy)` environments.

## Run Benchmarks

The benchmarks are implemented using [pytest](https://pytest.org) and
[pytest-benchmark](https://github.com/ionelmc/pytest-benchmark), so
you can run the tests with `pytest` if you adjust `PYTHONPATH`:

``` console
$ PYTHONPATH=. pytest
```

But it might be easier to just run the included `validate.py` and
`benchmark.py` scripts, which pass the appropriate options on to
`pytest`:

``` console
$ python validate.py   # skip performance tests (they take a while)
$ python benchmark.py  # skip validity tests
```

You can give specific library names to limit the tests that are run:

``` console
$ python validate.py pe stdlib  # only run validation for pe and stdlib
```

Some tests print to stdout diagnostic information that can be useful,
such as the recursion limit in JSON parsing. Use the following option to see that information:

``` console
$ pytest -rP                 # print stdout for each test
```


## Disclaimer

Performance benchmarks are not the only criterion one should use when
choosing a parsing library, and this repository is not meant to
declare some winner. On the one hand, there are many other valid
criteria (ease of use, stability, security, availability, support,
etc.), but on the other hand we can't discuss relative performance
without numbers, so here we are.
