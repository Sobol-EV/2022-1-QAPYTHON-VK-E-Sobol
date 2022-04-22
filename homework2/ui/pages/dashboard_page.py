import allure

from ui.locators.dashboard_locators import DashboardPageLocators
from ui.pages.base_page import BasePage


class DashboardPage(BasePage):

    URL = 'https://target.my.com/dashboard'
    locators = DashboardPageLocators()

    @allure.step("Click on the created campaign")
    def click_campaing(self, name_campaing):
        self.click(self.locators.campaing_entry_locator(name_campaing))

    @allure.step("Deleting a сampaign")
    def delete_campaing_entry(self):
        self.click(self.locators.SETTINGS_CAMPAING_ENTRY)
        self.visibility_element(self.locators.OPEN_LIST)
        self.click(self.locators.DELETE_CAMPAING)
        self.driver.refresh()

    @allure.step("Active campaigns shown")
    def view_active_campaing(self):
        self.click(self.locators.TYPE_CAMPAING_LIST)
        self.visibility_element(self.locators.OPEN_LIST)
        self.click(self.locators.TYPE_CAMPAING_ACTIVE)
