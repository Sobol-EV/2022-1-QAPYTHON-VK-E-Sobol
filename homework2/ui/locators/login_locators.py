from selenium.webdriver.common.by import By
from ui.locators.basic_locators import BasePageLocators


class LoginPageLocators(BasePageLocators):

    LOGIN_BUTTON = (By.XPATH, '//div//div[contains(@class, "responseHead-module-button")]')
    LOGIN_FIELD_FORM = (By.XPATH, '//div//input[@name="email"]')
    PASSWORD_FIELD_FORM = (By.XPATH, '//div//input[@name="password"]')
    LOGIN_BUTTON_FORM = (By.XPATH, '//div/div[contains(@class, "authForm-module-button")]')
    AUTH_ERROR_NOTIFICATION = (By.XPATH, '//div/div[contains(@class, "notify-module-error")]')
