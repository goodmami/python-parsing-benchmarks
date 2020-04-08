# INI Configuration File Parsing Task

This task parses a specific subset of the [INI] file format. For
example:

    [Colors]
	; colors are 3-digit hex RGB values
	red=#f00
	green=#0f0
	blue=#00f

INI files are notoriously ill-defined, particularly for corner cases,
but generally follow some basic principles:

* Keys are separated from values with some delimiter
* Key-value pairs are grouped in sections
* Sections are indicated with square brackets (e.g., `[Section Name]`)
* Line comments are prefixed with a special character

In order to make this task comparable to (a subset of) the Python
standard library's [configparser] module, the following additional
constraints are added:

* Keys without values or delimiters are allowed (value is `None`)
* Keys with a delimiter but without a value are allowed (value is `''`)
* Sections and keys may be indented
* Whitespace around keys and values is stripped
* Whitespace within keys and values is not normalized
* Only the `=` character is used as a key-value delimiter
* Only the `;` character is used to start comments
* Comments are whole-line only (cannot appear on the same line as a
  section header, key, or value)
* Values may not span multiple lines
* There are no escaped characters
* There is no interpolation of values
* There is no default section
* The parser should return a standard `dict` object.

Here is a illustrative PEG:

```
Start   <- Section* Comment* EOF
Section <- Comment* Header Body
Header  <- Space* Title Space* (EOL / EOF)
Title   <- '[' (![\]=\n\r] .)* ']'
Body    <- (Comment* Pair)*
Pair    <- Space* Key ('=' Value)?
Key     <- !Title (![=\n\r] .)*
Value   <- (!EOL .)*

Comment <- Space* (';' (!EOL .)*)? (EOL / EOF)
Space   <- [\t ]
EOL     <- '\r\n' / [\n\r]
EOF     <- !.
```


### Extras

In future iterations of this task consider the following extensions.


#### Multiline Values

It would be nice to accommodate multi-lined values. Python's
[configparser] uses indentation for this, e.g.:

	[Poems]
	roses are red=
	  These key-value pairs,
	  Grouped into a section,
	  Mathematically speaking,
	  Are like a surjection.

Other parsers may escape newlines or use some other technique. The
indentation one is perhaps more challenging to parse than other
techniques.


### Extra: Simple Validation

* Duplicate keys within a section raise an error
* Duplicate section names raise an error


[INI]: https://en.wikipedia.org/wiki/INI_file
[configparser]: https://docs.python.org/3/library/configparser.html
