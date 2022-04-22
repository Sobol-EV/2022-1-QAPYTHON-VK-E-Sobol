import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC

from base import BaseCase


class TestWithoutAuthorization(BaseCase):

    authorize = False

    @pytest.mark.UI
    def test_negative_auth_redirect(self, fake_credentials):
        """
        Checking for unsuccessful authorization when
        entering a login in email format
        """
        with allure.step('Authorization:'):
            self.login_page.authorization(
                fake_credentials['login'], fake_credentials['password']
            )
            with allure.step('URL validation:'):
                assert EC.url_contains(self.login_page.FAILED_LOGIN_URL), \
                    f"Redirect {self.login_page.FAILED_LOGIN_URL} on unsuccessful authorization"
            with allure.step('Checking the Error Notification:'):
                assert self.login_page.MESSAGE_INVALID_LOGIN in self.driver.page_source, \
                    "Login failed message"

    @pytest.mark.UI
    def test_negative_auth(self, fake_credentials):
        """
        Checking for unsuccessful authorization when
        entering a login in the username format
        """
        with allure.step('Authorization:'):
            self.login_page.authorization(
                fake_credentials['username'],
                fake_credentials['password'],
            )
            with allure.step('URL validation'):
                assert EC.url_to_be(self.login_page.URL), \
                    f"Stay on the previous login page {self.login_page.URL}"
            with allure.step('Checking the Error Notification'):
                assert self.login_page.visibility_element(
                    self.login_page.locators.AUTH_ERROR_NOTIFICATION
                ), "Login failed message"


class TestWithAuthorization(BaseCase):

    @pytest.mark.UI
    def test_create_campaing(self, data_campaing, file_path):
        """
        Checking the function of creating a campaign and then deleting it
        """
        self.dashboard_page.click(
            self.dashboard_page.locators.CREATE_CAMPAING_BUTTON
        )
        self.campaing_page.create_campaing(
            data_campaing['link'],
            data_campaing['campaing_name'],
            file_path
        )
        with allure.step('URL validation'):
            assert EC.url_contains(self.dashboard_page.URL), \
                    f"Redirect to {self.dashboard_page.URL}"
        self.dashboard_page.view_active_campaing()
        self.dashboard_page.open_new_tab(
            self.dashboard_page.locators.campaing_entry_locator(
                data_campaing['campaing_name']
            )
        )
        with self.switch_to_window(
                current=self.driver.current_window_handle,
                close=True
        ):
            self.campaing_page.check_create_campaing_by_name(
                data_campaing['campaing_name']
            )
        self.dashboard_page.delete_campaing_entry()
        with allure.step('No active campaigns'):
            assert self.dashboard_page.visibility_element(
                    self.dashboard_page.locators.NO_CAMPAING_NOTIFY
            ), "Notification not found"

    @pytest.mark.UI
    def test_create_and_delete_segment(self, data_segments):
        """
        Checking the function of creating a segment with subsequent deletion
        """
        self.segment_id = None

        self.dashboard_page.click(
            self.base_page.locators.SEGMENTS_BUTTON
        )
        assert self.segments_list_page.is_opened(), \
            "URL validation"
        self.segments_list_page.click_create_segments()
        self.segments_list_new_page.create_segment(
            data_segments['segments_name']
        )
        self.segments_list_page.open_new_tab(
            self.segments_list_page.locators.segment_entry_name_locator(
                data_segments['segments_name']
            )
        )
        with self.switch_to_window(
                current=self.driver.current_window_handle,
                close=True
        ):
            self.segment_id = self.segments_list_new_page.check_current_segment_by_name(
                data_segments['segments_name']
            )
        self.segments_list_page.delete_segments_by_id(self.segment_id)
        with allure.step('Checking for the absence of a segment'):
            assert EC.visibility_of_all_elements_located(
                self.segments_list_page.locators.segment_entry_name_locator(
                    data_segments['segments_name']
                )
            )
