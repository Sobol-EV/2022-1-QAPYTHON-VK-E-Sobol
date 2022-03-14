import pytest
from ui.locators import basic_locators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException)


class BaseCase:
    driver = None
    CLICK_RETRY = 39

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None):
        """Locates an element on a page"""
        return self.wait(timeout).until(
            EC.presence_of_element_located(locator)
        )

    def fill_field(self, query, locator):
        """Finds an element on the page and enters the desired query"""
        elem = self.find(locator)
        elem.send_keys(Keys.CONTROL + "A")
        elem.send_keys(query)

    def click(self, locator, timeout=None):
        """Checks if an element is clickable and clickable"""
        elem = self.wait(timeout).until(
            EC.element_to_be_clickable(locator)
        )
        elem.click()

    def click_retry(self, locator):
        """Repeats clicks until a successful click"""
        for i in range(self.CLICK_RETRY):
            try:
                elem = self.find(locator)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == self.CLICK_RETRY - 1:
                    raise

    def authorization(self, email, password):
        """Authorization from the main page"""
        self.click(basic_locators.LOGIN_BUTTON)
        self.fill_field(email, basic_locators.LOGIN_FIELD)
        self.fill_field(password, basic_locators.PASSWORD_FIELD)
        self.click(basic_locators.LOGIN_FORM_BUTTON)

    def visibility_element(self, locator, timeout=None):
        """Displays the visibility of an element"""
        try:
            elem = self.wait(timeout).until(
                    EC.visibility_of_all_elements_located(locator)
            )
            return elem
        except TimeoutException:
            return























