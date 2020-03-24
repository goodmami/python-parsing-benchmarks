
# Simple Arithmetic Parsing Task

This task evaluates the value of simple arithmetic expressions, such
as the following:

	1
	-1
	+1
	--1
	-(1)
	-(-1)
    -1 + 2
    1 + - 2 * 3
    -(-1 + --2) * -3
    (((1 + 2) * 3) / (4 * (5 - 6)))

It is adapted from [pegen](https://github.com/gvanrossum/pegen/)'s
[x.gram](https://github.com/gvanrossum/pegen/blob/master/data/x.gram),
which is useful for testing pathological backtracking. I have removed
the need to parse names (e.g., `a + b`) to aid in computing the actual
numerical results of the expressions for validation.

(*Note*: these modifications seem to have made it less pathological
regarding backtracking; the task may therefore change to try and
recreate the difficulty)

Here is a rough description of the task:

- there is one expression per line; except for the newline, whitespace
  is not significant outside of tokens
- an expression is a sequence of operations involving addition (`+`),
  subtraction (`-`), multiplication (`*`), and division (`/`)
  operators and integer atoms
- parentheses (`(` and `)`) may group sub-expressions
- integers and parethesized expressions may be modified with a
  negative or positive sign (`-` or `+`)
- the order of operations puts parenthesized expressions and integers
  at the highest priority, followed by signs, then by multiplication
  and division, then by addition and subtraction
- for sequential operations at the same priority (e.g., `+` and `-`),
  the application is left-associative (e.g., `1 - 2 + 3` equals `2`,
  not `-4`)

And here is a PEG (excluding ignored whitespace):

```
Start   <- Expr EOL? EOF
Expr    <- Term '+' Expr
         / Term '-' Expr
         / Term
Term    <- Factor '*' Term
         / Factor '/' Term
         / Factor
Factor  <- Sign Factor
         / '(' Expr ')'
		 / INTEGER
Sign    <- [-+]
INTEGER <- '0' / [1-9] [0-9]*
EOL     <- '\r\n' / [\n\r]
EOF     <- !.
```

Whitespace is allowed around any grammar terms except for within
`INTEGER`, `EOL`, and `EOF`. Allowed whitespace characters are the
set: ` \t\n\f\v\r`.

Note that the grammar defines the syntax, not the semantics, as
otherwise it would be right-associative. Parsers with left-recursion
support could alter the `Expr` and `Term` rules like this to be more
semantically accurate:

```
Expr    <- Expr '+' Term
         / Expr '-' Term
         / Term
Term    <- Term '*' Factor
         / Term '/' Factor
         / Factor
```

Otherwise you could convert them into repetitions:

```
Expr    <- Term ([-+] Term)*
Term    <- Factor ([*/] Factor)*
```

To help with these two use cases, the `bench.helpers.apply_infix()`
and `bench.helpers.reduce_infix()` functions are provided:

```python
>>> from operator import add, sub
>>> from bench.helpers import apply_infix, reduce_infix
>>> apply_infix(apply_infix(1, sub, 2), add, 3)
2
>>> reduce_infix(1, sub, 2, add, 3)
2
```

Also note that these functions just return the first argument if there
are no operations:

```python
>>> apply_infix(3)
3
>>> reduce_infix(3)
3
```
