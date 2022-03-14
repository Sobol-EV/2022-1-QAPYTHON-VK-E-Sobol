import pytest
from base import BaseCase
from ui.locators import basic_locators
import data
from selenium.webdriver.support import expected_conditions as EC


class TestExample(BaseCase):

    @pytest.mark.UI
    @pytest.mark.parametrize("login", [
        data.VALID_LOGIN, data.INVALID_LOGIN
    ])
    def test_login(self, login):
        """Checks authorization"""
        self.authorization(login, data.PASSWORD)
        if login == data.VALID_LOGIN:
            assert EC.url_to_be(data.URL_AUTHORIZED),\
                "Login successful"
        if login == data.INVALID_LOGIN:
            assert data.MESSAGE_INVALID_LOGIN in self.driver.page_source,\
                "Login failed"

    @pytest.mark.skip
    @pytest.mark.UI
    def test_logout(self):
        """Checking for logout"""
        self.authorization(data.VALID_LOGIN, data.PASSWORD)
        self.visibility_element(basic_locators.RIGHT_DROPDOWN_MENU)
        self.click_retry(basic_locators.RIGHT_DROPDOWN_MENU)
        self.find(basic_locators.RIGHT_DROPDOWN_MENU_OPEN)
        self.visibility_element(basic_locators.EXIT)
        self.click(basic_locators.EXIT)
        assert EC.url_to_be(data.URL), "Logout completed successfully"

    @pytest.mark.UI
    def test_edit_profile(self, personal_data):
        """Checks if the profile can be edited"""
        self.authorization(data.VALID_LOGIN, data.PASSWORD)
        self.click_retry(basic_locators.PROFILE_BUTTON)
        assert EC.url_to_be(data.URL_PROFILE), "Successful opening of the page"
        self.fill_field(personal_data['fio'], basic_locators.PROFILE_FIO)
        self.fill_field(personal_data['phone'], basic_locators.PROFILE_MOBILE)
        self.click(basic_locators.PROFILE_SAVE_LOCATOR)
        assert self.visibility_element(
            basic_locators.PROFILE_SAVE_MESSAGE, 3
        ), "Checking for Successful Data Change Notification"
        self.driver.refresh()
        assert EC.text_to_be_present_in_element_value(
            basic_locators.RIGHT_DROPDOWN_MENU_NAME, personal_data['fio']
        ), "The name has changed in the top right menu"
        assert EC.text_to_be_present_in_element_attribute(
            basic_locators.PROFILE_FIO, "value", personal_data['fio']
        ), "Name change saved in the field"
        assert EC.text_to_be_present_in_element_attribute(
            basic_locators.PROFILE_MOBILE, "value", personal_data['phone']
        ), "Phone change saved in the field"

    @pytest.mark.UI
    @pytest.mark.parametrize(("url", "locator"), (
            (data.URL_AUDIENCE, basic_locators.MENU_BUTTON_AUDIENCE),
            (data.URL_BALANCE, basic_locators.MENU_BUTTON_BALANCE)
        )
    )
    def test_menu_tab(self, url, locator):
        """Checks website pages"""
        self.authorization(data.VALID_LOGIN, data.PASSWORD)
        self.click_retry(locator)
        assert EC.url_to_be(url), f"Page {url} is active"
