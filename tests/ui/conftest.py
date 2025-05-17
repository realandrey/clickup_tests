import pytest

from playwright.sync_api import sync_playwright


from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()  # Далее, используя объект playwright, можно запускать браузер и работать с ним
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="session")
def login(browser):
    context = browser.new_context()
    page = context.new_page()
    LoginPage(page).login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    yield page
