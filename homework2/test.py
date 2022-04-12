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
    def test_create_campaign(self, data_campaign, file_path):
        """
        Checking the function of creating a campaign and then deleting it
        """
        self.dashboard_page.go_to_url(self.campaign_page.URL)
        self.campaign_page.create_campaign(
            data_campaign['link'],
            data_campaign['campaign_name'],
            file_path
        )
        with allure.step('URL validation'):
            assert EC.url_contains(self.dashboard_page.URL), \
                    f"Redirect to {self.dashboard_page.URL}"
        self.dashboard_page.view_active_campaign()
        self.driver.refresh()
        with allure.step('Checking the created campaign'):
            assert self.dashboard_page.visibility_element(
                self.dashboard_page.locators.campaign_entry_locator(
                    data_campaign['campaign_name']
                )
            ), "The created campaign did not appear in the active list"
        self.dashboard_page.delete_campaign_entry()
        with allure.step('No active campaigns'):
            assert self.dashboard_page.visibility_element(
                    self.dashboard_page.locators.NO_CAMPAIGN_NOTIFY
            ), "Notification not found"

    @pytest.mark.UI
    def test_create_segment(self, data_segments):
        """
        Checking the function of creating a segment with subsequent deletion
        """
        self.segment_id = None

        self.segments_list_new_page.create_segment(
            data_segments['segments_name']
        )
        self.segment_id = self.segments_list_page.get_segment_id_by_locator(
            self.segments_list_page.locators.segment_entry_name_locator(
                data_segments['segments_name']
            )
        )
        self.driver.refresh()
        with allure.step('Checking the created segment'):
            assert self.segments_list_page.visibility_element(
                self.segments_list_page.locators.segment_entry_name_locator(
                    data_segments['segments_name']
                )
            ), "The created segment did not appear in list"
        self.segments_list_page.delete_segments_by_id(self.segment_id)

    @pytest.mark.UI
    def test_delete_segment(self, data_segments):
        self.segment_id = None

        self.segments_list_new_page.create_segment(
            data_segments['segments_name']
        )
        self.segment_id = self.segments_list_page.get_segment_id_by_locator(
            self.segments_list_page.locators.segment_entry_name_locator(
                data_segments['segments_name']
            )
        )
        self.segments_list_page.delete_segments_by_id(self.segment_id)
        with allure.step('Checking for the absence of a segment'):
            assert EC.visibility_of_all_elements_located(
                self.segments_list_page.locators.segment_entry_name_locator(
                    data_segments['segments_name']
                )
            )
