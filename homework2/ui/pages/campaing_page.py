import allure
from selenium.webdriver.support import expected_conditions as EC

from ui.locators.campaing_locators import CampaingPageLocators
from ui.pages.base_page import BasePage


class CampaingPage(BasePage):

    URL = 'https://target.my.com/campaign/new'
    locators = CampaingPageLocators()

    @allure.step('Сampaign creation process')
    def create_campaing(self, link, campaing_name, file_path):
        with allure.step('URL validation'):
            assert self.is_opened(), \
                f"Redirect to {self.URL}"
        self.click(self.locators.TRAFFIC_BUTTON)
        self.fill_field(link, self.locators.LINK_FIELD)
        self.fill_field(
            campaing_name, self.locators.CAMPAING_NAME_FIELD
        )
        self.click(self.locators.ADVERTISING_FORMAT_BUTTON)
        self.upload_file(
            self.locators.UPLOAD_BANNER_240X400,
            file_path
        )
        self.click(self.locators.CREATE_CAMPAING_BUTTON)

    @allure.step("Comparison of the current campaign with the created one")
    def check_create_campaing_by_name(self, campaing_name):
        self.visibility_element(self.locators.CAMPAING_NAME_FIELD)
        with allure.step('Comparing the value in the field with the name of the campaign'):
            assert EC.text_to_be_present_in_element_attribute(
                    self.locators.CAMPAING_NAME_FIELD, "value", campaing_name
                    ), f"Title campaing not {campaing_name}"
