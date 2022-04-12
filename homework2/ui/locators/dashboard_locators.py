from selenium.webdriver.common.by import By
from ui.locators.basic_locators import BasePageLocators


class DashboardPageLocators(BasePageLocators):

    CREATE_CAMPAIGN_BUTTON = (By.XPATH, '//div[text()="Создать кампанию"]')
    TYPE_CAMPAIGN_LIST = (By.XPATH, '//div[contains(@class, "statusFilter-module-filterButtonWrapper")]//span')
    TYPE_CAMPAIGN_ACTIVE = (By.XPATH, '//li[@title="Активные кампании"]')
    SETTINGS_CAMPAIGN_ENTRY = (
        By.XPATH, '//div[@data-entity-type="campaign"]//div[contains(@class, "icon-settings")]/parent::div'
    )
    OPEN_LIST = (By.XPATH, '//ul[contains(@class, "optionsList-module-optionsList")]')
    DELETE_CAMPAIGN = (By.XPATH, '//li[@title="Удалить"]')
    NO_CAMPAIGN_NOTIFY = (By.XPATH, '//div[contains(@class, "dashboard-module-notifyBlock")]')

    @staticmethod
    def campaign_entry_locator(name):
        return By.XPATH, f'//a[@title="{name}"]'
