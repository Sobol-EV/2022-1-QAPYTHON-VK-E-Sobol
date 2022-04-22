import time
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException)
from selenium.webdriver import ActionChains

from ui.locators import basic_locators


class PageNotOpenedExeption(Exception):
    pass


class BasePage(object):

    locators = basic_locators.BasePageLocators()
    URL = None

    def is_opened(self, timeout=15):
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url == self.URL:
                return True
        raise PageNotOpenedExeption(
            f'{self.URL} did not open in {timeout} current url {self.driver.current_url}')

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step('Click')
    def click(self, locator, timeout=None):
        try:
            self.find(locator, timeout=timeout)
            if self.visibility_element(locator):
                elem = self.wait(timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                elem.click()
        except StaleElementReferenceException:
            time.sleep(1)
            self.click(locator)

    @allure.step('Filled the field with a value')
    def fill_field(self, query, locator):
        """Finds an element on the page and enters the desired query"""
        elem = self.find(locator)
        if self.visibility_element(locator):
            elem.send_keys(Keys.CONTROL + "A")
            elem.send_keys(query)

    def visibility_element(self, locator, timeout=None):
        """Displays the visibility of an element"""
        try:
            elem = self.wait(timeout).until(
                    EC.visibility_of_all_elements_located(locator)
            )
            return elem
        except TimeoutException:
            return

    @allure.step('Open new tab')
    def open_new_tab(self, locator):
        element = self.find(locator)
        ActionChains(self.driver).key_down(
            Keys.CONTROL
        ).click(element).key_up(
            Keys.CONTROL
        ).perform()

    @allure.step('Upload file')
    def upload_file(self, locator, file_path):
        self.find(locator).send_keys(file_path)
