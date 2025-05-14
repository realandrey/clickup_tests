from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = '/login'
        self.page.set_default_timeout(15000)

    USERNAME_SELECTOR = '[id="login-email-input"]'
    PASSWORD_SELECTOR = '[id="login-password-input"]'
    LOGIN_BUTTON_SELECTOR = '.login-page-new__main-form-button'
    ERROR_SELECTOR = '.cu-form__error-text'

    def login(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)


    def login_with_invalid_password(self, username, password):
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.wait_for_selector(self.ERROR_SELECTOR)
