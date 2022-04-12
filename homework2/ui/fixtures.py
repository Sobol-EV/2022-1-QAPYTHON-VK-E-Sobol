import os.path
import shutil
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from _pytest.fixtures import FixtureRequest

import data
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import (
    SegmentsPage,
    SegmentsListPage,
    SegmentsListNewPage,
)
from generators.value_generator import (
    DataAuth,
    DataCampaign,
    DataSegments,
)


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = r'C:\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture()
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if selenoid:
        capabilities = {
            "browserName": "chrome",
            'version': '98.0',
        }
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities,
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def campaign_page(driver):
    return CampaignPage(driver=driver)


@pytest.fixture
def segments_page(driver):
    return SegmentsPage(driver=driver)


@pytest.fixture
def segments_list_page(driver):
    return SegmentsListPage(driver=driver)


@pytest.fixture
def segments_list_new_page(driver):
    return SegmentsListNewPage(driver=driver)


def get_driver(brower_name):
    if brower_name == 'chrome':
        browser = webdriver.Chrome(executable_path=ChromeDriverManager(
        ).install())
    elif brower_name == 'firefox':
        browser = webdriver.Firefox(executable_path=GeckoDriverManager(
        ).install())
    else:
        raise RuntimeError(f'Unsupported browser: "{brower_name}"')
    browser.maximize_window()

    return browser


@pytest.fixture(scope='session', params=['chrome', 'firefox'])
def all_drivers(config, request):
    url = config['url']
    browser = get_driver(request.param)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture(scope='session')
def credentials():
    user = data.VALID_LOGIN
    password = data.VALID_PASSWORD
    return user, password


@pytest.fixture(scope='function')
def fake_credentials():
    generator = DataAuth()
    data_auth = generator.build()
    return data_auth


@pytest.fixture(scope='session')
def data_campaign():
    generator = DataCampaign()
    return generator.build()


@pytest.fixture(scope='session')
def data_segments():
    generator = DataSegments()
    return generator.build()


@pytest.fixture()
def file_path(repo_root):
    return os.path.join(repo_root, 'files', 'banner.jpg')


@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver(config['browser'])
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.authorization(*credentials)

    cookies = driver.get_cookies()
    driver.quit()

    return cookies


@pytest.fixture(scope='function')
def auth(request: FixtureRequest, driver):
    cookies = request.getfixturevalue('cookies')
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

    return DashboardPage(driver=driver)
