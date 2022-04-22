from selenium.webdriver.common.by import By
from ui.locators.basic_locators import BasePageLocators


class CampaignPageLocators(BasePageLocators):

    TRAFFIC_BUTTON = (By.XPATH, '//div[contains(@class, "_traffic")]')
    LINK_FIELD = (By.XPATH, '//div[contains(@class, "suggester-module-wrapper")]//input')
    CAMPAIGN_NAME_FIELD = (By.XPATH, '//div[contains(@class, "input_campaign-name")]//input')
    ADVERTISING_FORMAT_BUTTON = (By.XPATH, '//div[contains(@id, "patterns_banner")]')
    UPLOAD_BANNER_240X400 = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]//input[@type="file"]')
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//div[contains(@class, "js-save-button-wrap")]//button')
