import os

from api.fixtures import *
from api.client import ApiClient


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com/')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {
        'url': url,
    }


@pytest.fixture(scope='session')
def credentials():
    user = 'borolax286@siberpay.com'
    password = '789789pP'

    return user, password


@pytest.fixture(scope="function")
def api_client(config, credentials) -> ApiClient:
    api_client = ApiClient(config['url'], *credentials)
    return api_client
