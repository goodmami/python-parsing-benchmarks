
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
@pytest.fixture(scope='session', params=implementations)
def parse_arithmetic(request):
    if request.param not in implementations:
        pytest.skip('not selected')
    mod = pytest.importorskip(
        f'bench.{request.param}.arithmetic',
        reason=f'could not import bench.{request.param}.arithmetic'
    )
    return mod.parse
