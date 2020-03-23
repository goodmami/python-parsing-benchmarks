
# JSON Parsing Task

This task implements the [JSON Specification], which is a format
commonly used to demonstrate the usage of parser libraries. However,
unlike many of those illustrative implementations, this task must
implement the specification exactly. Namely:

- Any JSON value (`true`, `false`, `null`, a number, a string, an
  array, or an object) may be the top-level element
- Whitespace is allowed before or after the top-level element
- No non-whitespace characters are allowed after the top-level element
- Strings must only contain the allowed characters (e.g., no unescaped
  newlines)
- String escapes must be converted appropriately (e.g., `\n` becomes a
  newline, `\u3042` becomes `あ`, etc.)
- Invalid string escapes must not be allowed
- The integer portion of non-zero numbers must not start with `0`
- Numbers like `Infinity` and `NaN` are not allowed

The parser must not only accept valid JSON and reject invalid JSON,
but it must convert a JSON object to the appropriate data structures.
Some details of the specification are intentionally left without a
prescribed behavior:

- Numbers may be cast as any accurate numeric datatype (e.g., `1` may
  be an integer or a float, but `1.2` must always be a float)
- Multi-sequence unicode codepoints with surrogate characters may be
  resolved to the original character or left as a surrogate sequence
  (e.g., `"\ud834\udd1e"` (12 characters in JSON) may be resolved to
  `'𝄞'` (1-character string) or `'\ud834\udd1e'` (2-character
  string)).

[JSON Specification]: https://www.json.org/
