# Python Parsing Benchmarks

This repository contains a suite of test cases and implementations for
parsing text using Python. Both speed an memory usage are compared for
each implementation. Each implementation must be:

* **Correct** -- it implements the specification exactly
  - Syntax -- it parses all valid inputs and rejects bad ones
  - Semantics -- it produces the expected data structures
* **Plausible** -- it only uses expected (e.g., documented) parser
  features

## Tasks Performed

The following tasks are included:

- [JSON](tasks/json.md)
- [Arithmetic](tasks/arithmetic.md)


## Libraries Tested

The following parsing libaries have implementations for the tasks:

- [Lark](https://github.com/lark-parser/lark)
- [pe](https://github.com/goodmami/pe)
- [pyparsing](https://github.com/pyparsing/pyparsing/)
- [stdlib](https://docs.python.org/3/) (Python 3 standard library modules)


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
