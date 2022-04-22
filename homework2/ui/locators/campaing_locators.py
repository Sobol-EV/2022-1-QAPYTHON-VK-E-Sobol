from selenium.webdriver.common.by import By
from ui.locators.basic_locators import BasePageLocators


class CampaingPageLocators(BasePageLocators):

    TRAFFIC_BUTTON = (By.XPATH, '//div[@class="column-list-item _traffic"]')
    LINK_FIELD = (By.XPATH, '//div[contains(@class, "suggester-module-wrapper")]//input')
    CAMPAING_NAME_FIELD = (By.XPATH, '//div[contains(@class, "input_campaign-name")]//input')
    ADVERTISING_FORMAT_BUTTON = (By.XPATH, '//div[contains(@id, "patterns_banner")]')
    UPLOAD_BANNER_240X400 = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]//input[@type="file"]')
    CREATE_CAMPAING_BUTTON = (By.XPATH, '//div[contains(@class, "footer__button js-save-button-wrap")]//button')
