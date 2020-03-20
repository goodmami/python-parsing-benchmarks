#!/bin/bash


object() {
    cat <<EOF
{"n": "$n",
 "true": true,
 "false": false,
 "null": null,
 "integer": -123,
 "float": 123.456e-7,
 "string": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
 "escaped": "this is a quote: \" and this is a slash: \\\\",
 "unicode": "この字は日本語の字だ\n這些字是中文字\nEstas son palabras en español",
 "escaped unicode": "\u3053\u306e\u5b57\u306f\u65e5\u672c\u8a9e\u306e\u5b57\u3060\n\u9019\u4e9b\u5b57\u662f\u4e2d\u6587\u5b57\nEstas son palabras en espa\u00f1ol",
 "object": {"again": {"and again": {"that's": "enough"}}},
 "array": [1,[2,[3,[4,[5,[6,[7,[8,[9,[10]]]]]]]]]]
}
EOF
}

echo '['
for ((n=0;n<10000;n++)); do
    object $n
    echo ','
done
object 5001
echo ']'
