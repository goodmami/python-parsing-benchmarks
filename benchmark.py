#!/usr/bin/env python3

import sys
import argparse

import pytest

argparser = argparse.ArgumentParser()
argparser.add_argument('lib', nargs='*', help='name of parsing library in bench/')
args, rest = argparser.parse_known_args()

pytest_args = ['--benchmark-only', '--rootdir=tests/'] + rest

if args.lib:
    pytest_args.append(f'--bench={",".join(args.lib)}')

pytest.main(pytest_args)

