import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import data
from faker import Faker


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default=data.URL)


@pytest.fixture()
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')
    return {'browser': browser, 'url': url}


@pytest.fixture()
def driver(config):
    browser = config['browser']
    url = config['url']
    if browser == 'chrome':
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install()
        )
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def personal_data():
    faker = Faker()
    fio = faker.name()
    phone = faker.phone_number()
    email = faker.email()
    return {"fio": fio, "phone": phone, "email": email}


@pytest.fixture(scope='session')
def url_site_pages():
    return {
        "URL_BALANCE": data.URL_BALANCE,
        "URL_AUDIENCE": data.URL_AUDIENCE
    }



