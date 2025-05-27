import allure

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "login"
        self.page.set_default_timeout(60000)

    USERNAME_SELECTOR = '[id="login-email-input"]'
    PASSWORD_SELECTOR = '[id="login-password-input"]'
    LOGIN_BUTTON_SELECTOR = '[data-test="login-submit"]'
    ERROR_SELECTOR = '[data-test="form__error"]'

    @allure.step("Вход в систему с пользователем: {username}")
    def login(self, username, password, expect_error: bool = False):
        self.navigate_to()

        with allure.step("Вводим логин и пароль"):
            self.wait_for_selector_and_type(self.USERNAME_SELECTOR, username, 100)
            self.wait_for_selector_and_type(self.PASSWORD_SELECTOR, password, 100)
            self.assert_input_value(self.USERNAME_SELECTOR, username)
            self.assert_input_value(self.PASSWORD_SELECTOR, password)

        with allure.step("Нажимаем кнопку 'Войти'"):
            self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)

        if expect_error:
            with allure.step("Ожидаем появление ошибки"):
                self.wait_for_selector(self.ERROR_SELECTOR)
