import allure

from ui.locators.dashboard_locators import DashboardPageLocators
from ui.pages.base_page import BasePage


class DashboardPage(BasePage):

    URL = 'https://target.my.com/dashboard'
    locators = DashboardPageLocators()

    @allure.step("Click on the created campaign")
    def click_campaign(self, name_campaign):
        self.click(self.locators.campaign_entry_locator(name_campaign))

    @allure.step("Deleting a Campaign")
    def delete_campaign_entry(self):
        self.click(self.locators.SETTINGS_CAMPAIGN_ENTRY)
        self.visibility_element(self.locators.OPEN_LIST)
        self.click(self.locators.DELETE_CAMPAIGN)
        self.driver.refresh()

    @allure.step("Active campaigns shown")
    def view_active_campaign(self):
        self.click(self.locators.TYPE_CAMPAIGN_LIST)
        self.visibility_element(self.locators.OPEN_LIST)
        self.click(self.locators.TYPE_CAMPAIGN_ACTIVE)
