import allure

from playwright.sync_api import expect

from pages.login_page import LoginPage
from tests.ui.conftest import browser
from utils.helpers import CLICKUP_EMAIL
import pytest


@allure.feature("Login functionality")
class TestLoginPage:

    @allure.description("Проверка успешного входа на страницу с валидными данными")
    def test_login_success(self, login):
        with allure.step("Ожидание появления текста 'Automate' на странице"):
            login.wait_for_selector("text=Automate")
        with allure.step("Проверка, что на странице есть текст 'Automate'"):
            assert "Automate" in login.content()

    @allure.description("Проверка ошибки при вводе неправильного пароля")
    def test_login_negative(self, browser):
        page = browser.new_page()
        login_page = LoginPage(page)

        with allure.step(f"Попытка войти с неправильным паролем для {CLICKUP_EMAIL}"):
            login_page.login(CLICKUP_EMAIL, 'this_pass_is_wrong_123!', expect_error=True)

        with allure.step("Проверка, что появилась ошибка 'Incorrect password for this email.'"):
            error_locator = page.locator('[data-test="form__error"]')
            expect(error_locator).to_be_visible(timeout=15000)
            assert 'Incorrect password for this email.' in error_locator.inner_text()

        with allure.step("Проверка, что текст 'Automate' на странице отсутствует"):
            assert not page.locator("text=Automate").is_visible(timeout=3000)