
import pkgutil

import pytest

import bench

implementations = []
for modinfo in pkgutil.iter_modules(bench.__path__):
    if modinfo.ispkg:
        implementations.append(modinfo.name)


@pytest.fixture(scope='session', params=implementations)
def parse_json(request):
    print(f'bench.{request.param}.json')
    return pytest.importorskip(f'bench.{request.param}.json').parse
