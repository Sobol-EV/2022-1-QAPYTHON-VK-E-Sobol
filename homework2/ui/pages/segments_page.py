import allure
from selenium.webdriver.support import expected_conditions as EC

from ui.locators.segments_locators import (
    SegmentsPageLocators,
    SegmentsListPageLocators,
    SegmentsListNewPageLocators,
)
from ui.pages.base_page import BasePage


class SegmentsPage(BasePage):
    URL = 'https://target.my.com/segments'
    locators = SegmentsPageLocators()


class SegmentsListPage(SegmentsPage):
    URL = 'https://target.my.com/segments/segments_list'
    locators = SegmentsListPageLocators()

    @allure.step("Clicking on the created segment")
    def click_name_segments(self, name_segments):
        self.click(
            self.locators.segment_entry_name_locator(name_segments)
        )

    @allure.step("Clicking on the delete segment button")
    def click_delete_segment(self, id_segments):
        self.click(
            self.locators.segment_entry_delete_locator(id_segments)
        )

    @allure.step('Clicking on the create segment button')
    def click_create_segments(self):
        if self.visibility_element(
            self.locators.INSCRIPTION_CREATE_SEGMENT, 10
        ):
            self.click(self.locators.INSCRIPTION_CREATE_SEGMENT)
        else:
            self.visibility_element(self.locators.CREATE_SEGMENT_BUTTON)
            self.click(self.locators.CREATE_SEGMENT_BUTTON)

    @allure.step("Deleting a segment by id")
    def delete_segments_by_id(self, id_segments):
        self.is_opened()
        self.click_delete_segment(id_segments)
        self.click(self.locators.DELETE_NOTIFICATION_BUTTON)


class SegmentsListNewPage(SegmentsPage):
    URL = 'https://target.my.com/segments/segments_list/new/'
    locators = SegmentsListNewPageLocators()

    def get_segment_id(self):
        url = str(self.driver.current_url)
        return url.split('/')[-1]

    @allure.step("Comparison of the current segment with the created one")
    def check_current_segment_by_name(self, name_segment):
        self.visibility_element(
            self.locators.FILED_TITLE_SEGMENT
        )
        with allure.step('Comparing values in the field with the name of the segment'):
            assert EC.text_to_be_present_in_element_attribute(
                self.locators.FILED_TITLE_SEGMENT, "value", name_segment
            ), f"Title segment not {name_segment}"
        return self.get_segment_id()

    @allure.step("Create a segment")
    def create_segment(self, name_segment):
        assert self.driver.current_url in self.URL
        self.visibility_element(
            self.locators.MODULE_ADD_SEGMENTS
        )
        self.click(self.locators.APP_GAME_SOCIAL_NETWORK)
        self.click(self.locators.CHECKBOX_PLAYED_AND_PAID)
        self.click(self.locators.ADD_SEGMENT_BUTTON)
        self.fill_field(name_segment, self.locators.FILED_TITLE_SEGMENT)
        self.click(self.locators.CREATE_SEGMENT_BUTTON)
