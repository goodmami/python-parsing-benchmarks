
import argparse
import pkgutil

import pytest

import bench

implementations = []
for modinfo in pkgutil.iter_modules(bench.__path__):
    if modinfo.ispkg:
        implementations.append(modinfo.name)


def _csvtype(choices):

    def splitarg(arg):
        values = arg.split(',')
        for value in values:
            if value not in choices:
                raise argparse.ArgumentTypeError(
                    'invalid choice: {!r} (choose from {})'
                    .format(value, ', '.join(map(repr, choices))))
        return values

    return splitarg


def pytest_addoption(parser):
    parser.addoption(
        '--bench',
        metavar='NAMES',
        type=_csvtype(implementations),
        help='comma-separated list of implementations to use')


def pytest_configure(config):
    config.addinivalue_line("markers", "bench: mark implementations to run")


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--bench'):
        return  # run all if --bench not given
    imps = config.getoption('--bench')
    implementations[:] = [imp for imp in implementations if imp in imps]


@pytest.fixture(scope='session', params=implementations)
def parse_json(request):
    if request.param not in implementations:
        pytest.skip('not selected')
    mod = pytest.importorskip(
        f'bench.{request.param}.json',
        reason=f'could not import bench.{request.param}.json'
    )
    return mod.parse


@pytest.fixture(scope='session', params=implementations)
def parse_arithmetic(request):
    if request.param not in implementations:
        pytest.skip('not selected')
    mod = pytest.importorskip(
        f'bench.{request.param}.arithmetic',
        reason=f'could not import bench.{request.param}.arithmetic'
    )
    return mod.parse
