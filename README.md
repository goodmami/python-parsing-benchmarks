# Python Parsing Benchmarks

This repository contains a suite of test cases and implementations for
parsing text using Python. Both speed an memory usage are compared for
each implementation. Each implementation must be:

* **Correct** -- it implements the specification exactly
  - Syntax -- it parses all valid inputs and rejects bad ones
  - Semantics -- it produces the expected data structures
* **Plausible** -- it only uses expected (e.g., documented) parser
  features

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
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install .
```

From here on it's assumed you're in the `(env)` environment.

**Note:** the `pe` library is not yet on PyPI, so you'll need to clone
its repository and install it manually for now.

``` console
$ git clone https://github.com/goodmami/pe.git
...
$ pip install pe/
```


## Run Benchmarks

The benchmarks are implemented using [pytest](https://pytest.org) and
[pytest-benchmark](https://github.com/ionelmc/pytest-benchmark), so to
run all tests you can just run `pytest` itself:

``` console
$ pytest
```

The performance tests can take a while to run, so you may want to
filter out some tests:

``` console
$ pytest --benchmark-skip    # skip performance tests
$ pytest --benchmark-only    # skip validity tests
```

Use `--bench` to select the implementations to test with a
comma-separated list of names:

``` console
$ pytest --bench=pe,stdlib   # only test pe and stdlib
```

Some tests, such as finding the recursion limit in the JSON task, print the result ot stdout even if the test passes, but `pytest` filters stdout by default. To see this output, use the `-rP` option:

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
