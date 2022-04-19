import allure

from ui.locators.login_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.dashboard_page import DashboardPage


class LoginPage(BasePage):

    locators = LoginPageLocators()
    URL = 'https://target.my.com/'
    FAILED_LOGIN_URL = 'https://account.my.com/login/'

    @allure.step("Authorization")
    def authorization(self, login, password):
        self.click(self.locators.LOGIN_BUTTON)
        self.fill_field(login, self.locators.LOGIN_FIELD_FORM)
        self.fill_field(password, self.locators.PASSWORD_FIELD_FORM)
        self.click(self.locators.LOGIN_BUTTON_FORM)

        return DashboardPage(self.driver)
