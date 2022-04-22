import allure
from selenium.webdriver.support import expected_conditions as EC

from ui.locators.campaign_locators import CampaignPageLocators
from ui.pages.base_page import BasePage


class CampaignPage(BasePage):

    URL = 'https://target.my.com/campaign/new'
    locators = CampaignPageLocators()

    @allure.step('Campaign creation process')
    def create_campaign(self, link, campaign_name, file_path):
        with allure.step('URL validation'):
            assert self.is_opened(), \
                f"Redirect to {self.URL}"
        self.click(self.locators.TRAFFIC_BUTTON)
        self.fill_field(link, self.locators.LINK_FIELD)
        self.fill_field(
            campaign_name, self.locators.CAMPAIGN_NAME_FIELD
        )
        self.click(self.locators.ADVERTISING_FORMAT_BUTTON)
        self.upload_file(
            self.locators.UPLOAD_BANNER_240X400,
            file_path
        )
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON)

    @allure.step("Comparison of the current campaign with the created one")
    def check_create_campaign_by_name(self, campaign_name):
        self.visibility_element(self.locators.CAMPAIGN_NAME_FIELD)
        with allure.step('Comparing the value in the field with the name of the campaign'):
            assert EC.text_to_be_present_in_element_attribute(
                    self.locators.CAMPAIGN_NAME_FIELD, "value", campaign_name
                    ), f"Title campaign not {campaign_name}"
