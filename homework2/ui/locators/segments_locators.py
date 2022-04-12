from selenium.webdriver.common.by import By
from ui.locators.basic_locators import BasePageLocators


class SegmentsPageLocators(BasePageLocators):
    pass


class SegmentsListPageLocators(SegmentsPageLocators):

    INSCRIPTION_CREATE_SEGMENT = (By.XPATH, '//a[@href="/segments/segments_list/new/"]')
    CREATE_SEGMENT_BUTTON = (By.XPATH, '//button[contains(@class, "button_submit")]')
    DELETE_NOTIFICATION_BUTTON = (
        By.XPATH, '//button[contains(@class,"button_confirm-remove")]'
    )

    @staticmethod
    def segment_entry_name_locator(name):
        return By.XPATH, f'//a[@title="{name}"]'

    @staticmethod
    def segment_entry_delete_locator(id_segment):
        return By.XPATH, f'//div[@data-test="remove-{id_segment} row-{id_segment}"]'


class SegmentsListNewPageLocators(SegmentsPageLocators):

    MODULE_ADD_SEGMENTS = (By.XPATH, '//div[@class="modal-view__body__content"]')
    APP_GAME_SOCIAL_NETWORK = (By.XPATH, '//div[text()="Приложения и игры в соцсетях"]')
    CHECKBOX_PLAYED_AND_PAID = (
        By.XPATH, '//div[contains(@class, "adding-segments-source__header")]//input'
    )
    ADD_SEGMENT_BUTTON = (
        By.XPATH, '//div[@class="modal-view__body__content"]//button[contains(@class,"button_submit")]'
    )
    FILED_TITLE_SEGMENT = (
        By.XPATH, '//div[contains(@class, "input_create-segment-form")]//input'
    )
    CREATE_SEGMENT_BUTTON = (By.XPATH, '//div[contains(@class, "create-segment-form")]//button')
