
import configparser


def parse(s):
    cp = configparser.ConfigParser(
        defaults=None,
        dict_type=dict,
        allow_no_value=True,
        delimiters='=',
        comment_prefixes=';',
        inline_comment_prefixes=None,
        strict=True,
        empty_lines_in_values=False,
        interpolation=None,
    )
    cp.read_string(s)
    d = {}
    for section_name in cp.sections():
        d[section_name] = inner = {}
        section = cp[section_name]
        for key in section:
            inner[key] = section[key]
    return d
