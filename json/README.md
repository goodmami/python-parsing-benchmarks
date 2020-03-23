
# JSON Parsing Benchmark

The parsers in this benchmark should implement the [JSON
Specification] exactly, including the range of allowed characters in
strings (e.g., unescaped newlines are not allowed). Furthermore, they
should decode escaped unicode characters, such as `\u3042` to `あ`. It
is not specified what datatype numeric values need to be converted to,
so it does not matter what the parser does as long as it converts to
some accurate numeric type.

[JSON Specification]: https://www.json.org/
