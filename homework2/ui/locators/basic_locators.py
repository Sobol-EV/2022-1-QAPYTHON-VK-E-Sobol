from selenium.webdriver.common.by import By


class BasePageLocators:

    SEGMENTS_BUTTON = (By.XPATH, '//a[@href="/segments"]')
    DASHBOARD_BUTTON = (By.XPATH, 'href="/dashboard"')
