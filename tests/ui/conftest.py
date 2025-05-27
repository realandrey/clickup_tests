import allure
import pytest
from playwright.sync_api import Browser, Page, sync_playwright

from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD


@pytest.fixture
def browser() -> Browser:
    with allure.step("Запуск Playwright и инициализация браузера Chromium"):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False, slow_mo=1000)
            yield browser
            with allure.step("Закрытие браузера"):
                browser.close()


@pytest.fixture
def login(browser: Browser) -> Page:
    with allure.step("Создание контекста браузера и новой страницы"):
        context = browser.new_context()
        page = context.new_page()
    with allure.step("Вход в ClickUp через UI"):
        LoginPage(page).login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
    yield page
    with allure.step("Закрытие контекста после завершения сессии"):
        page.close()
        context.close()
