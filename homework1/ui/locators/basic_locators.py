from selenium.webdriver.common.by import By

# Login page locators
LOGIN_BUTTON = (By.XPATH, '//div[text()="En"]/preceding-sibling::div')
LOGIN_FIELD = (By.XPATH, '//input[@placeholder="Email или номер телефона"]')
PASSWORD_FIELD = (By.XPATH, '//input[@placeholder="Пароль"]')
LOGIN_FORM_BUTTON = (By.XPATH, '//div[text()="Или войдите с помощью соцсетей"]/preceding-sibling::div')

# Profile page locators
PROFILE_BUTTON = (By.XPATH, '//a[@href="/profile"]')
PROFILE_FIO = (By.XPATH, '//div[@data-name="fio"]//input[@type="text"]')
PROFILE_MOBILE = (By.XPATH, '//div[@data-name="phone"]//input[@type="text"]')
PROFILE_SAVE_LOCATOR = (By.XPATH, '//button[@data-class-name="Submit"]')
PROFILE_SAVE_MESSAGE = (By.XPATH, '//div[@data-class-name="SuccessView"]//div')
PROFILE_ADD_EMAIL_BUTTON = (By.XPATH, '//span[@class="clickable-button__text js-text-wrap"]')
PROFILE_ADD_EMAIL_FIELD = (By.XPATH, '//div[@class="js-additional-emails"]//input[@class="input__inp js-form-element"]')
PROFILE_EMAIL_NOTIFICATION_MESSAGE = (By.XPATH, '//div[@class="profile__notification js-before-confirm"]')

# Menu Locators
MENU_BUTTON_AUDIENCE = (By.XPATH, '//a[@href="/segments"]')
MENU_BUTTON_BALANCE = (By.XPATH, '//a[@href="/billing"]')


# Right Dropdown Locators
EXIT_VERSION_2 = (By.XPATH, '//li[./a[@href="/logout"]]')
EXIT_VERSION_3 = (By.XPATH, '//a[@href="/logout"]')
EXIT = (By.XPATH, '//ul[contains(@class, "rightMenu-module-visibleRightMenu")]//a[@href="/logout"]')
RIGHT_DROPDOWN_MENU_OPEN = (By.XPATH, '//ul[contains(@class, "rightMenu-module-visibleRightMenu")]')
RIGHT_DROPDOWN_MENU_NAME = (By.XPATH, '//ul[contains(@class, "right-module-userNameWrap")]')
RIGHT_DROPDOWN_MENU = (By.XPATH, '//div[contains(@class,"right-module-rightButton")]')

