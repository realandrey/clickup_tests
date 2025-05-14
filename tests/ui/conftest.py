import pytest

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()  # Далее, используя объект playwright, можно запускать браузер и работать с ним
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def login_fixture(page):
    login_page = LoginPage(page)
    login_page.login('dolomonddd@gmail.com', 'Test@756990!!')  # Логинимся с правильными данными
    return login_page