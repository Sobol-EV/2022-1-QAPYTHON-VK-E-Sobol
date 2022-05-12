import os
import sys
import time
import shutil
import logging
import requests
from requests.exceptions import ConnectionError

import pytest

import settings
from mock import flask_mock
from socket_client.client import Socket

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='session')
def client():
    return Socket()


@pytest.fixture(scope='function')
def requests_folder(request):
    test_dir = os.path.join(
        request.config.log_temp_dir,
        request._pyfuncitem.nodeid
        .replace('/', '_')
        .replace(':', '_')
    )
    os.makedirs(test_dir)
    return test_dir


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass
    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 5s!')


def pytest_configure(config):
    std_directory = os.path.join(repo_root, 'std_log')
    requests_directory = os.path.join(repo_root, 'requests_log')

    if not hasattr(config, 'workerinput'):

        if os.path.exists(requests_directory):
            shutil.rmtree(requests_directory)
        if os.path.exists(std_directory):
            shutil.rmtree(std_directory)

        os.makedirs(requests_directory)
        os.makedirs(std_directory)

        mock_stdout = open(os.path.join(
            std_directory,
            'mock_stdout.txt'
        ), 'w')
        config.mock_stderr = open(os.path.join(
            std_directory,
            'mock_stderr.txt'
        ), 'w')

        sys.stderr = config.mock_stderr
        flask_mock.run_mock()

        sys.stdout = mock_stdout
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        mock_stdout.close()

    config.log_temp_dir = requests_directory


def pytest_unconfigure(config):

    requests.get(
        f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown'
    )
    sys.stderr.close()
    sys.stderr = sys.__stderr__
    config.mock_stderr.close()


@pytest.fixture(scope='function')
def logger(requests_folder):
    log_formatter = logging.Formatter('%(asctime)s - %(message)s')
    log_file = os.path.join(requests_folder, 'test.log')
    log_level = logging.INFO
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)
    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()




