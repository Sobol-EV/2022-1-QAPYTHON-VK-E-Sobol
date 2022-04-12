import os
import pytest
import allure
from contextlib import contextmanager
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage
from ui.pages.campaign_page import CampaignPage
from ui.pages.segments_page import (
    SegmentsPage,
    SegmentsListPage,
    SegmentsListNewPage,
)


class BaseCase:
    driver = None
    authorize = True

    @allure.step('Switch to an open tab')
    @contextmanager
    def switch_to_window(self, current, close=False):
        for window in self.driver.window_handles:
            if window != current:
                self.driver.switch_to.window(window)
                break
        yield
        if close:
            with allure.step(f'Closing a created tab'):
                self.driver.close()
        with allure.step(f'Switching to the previous tab'):
            self.driver.switch_to.window(current)

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']} - {i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(
                screenshot_path, 'failed.png', allure.attachment_type.PNG
            )
            with open(browser_logs, 'r') as f:
                allure.attach.file(
                    f.read(), 'test.log', allure.attachment_type.TEXT
                )

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()

            self.dashboard_page: DashboardPage = (request.getfixturevalue('dashboard_page'))
            self.base_page:BasePage = (request.getfixturevalue('base_page'))
            self.campaign_page: CampaignPage = (request.getfixturevalue('campaign_page'))
            self.segments_page: SegmentsPage = (request.getfixturevalue('segments_page'))
            self.segments_list_page: SegmentsListPage = (request.getfixturevalue('segments_list_page'))
            self.segments_list_new_page: SegmentsListNewPage = (request.getfixturevalue('segments_list_new_page'))
