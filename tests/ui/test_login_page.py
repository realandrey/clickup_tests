from playwright.sync_api import expect

from pages.login_page import LoginPage
from tests.ui.conftest import browser
from utils.helpers import CLICKUP_EMAIL
import pytest

class TestLoginPage:

    def test_login_success(self, login):
        login.wait_for_selector("text=Automate")  # дождаться элемента
        assert "Automate" in login.content()

    def test_login_negative(self, browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.login_with_invalid_password(CLICKUP_EMAIL, 'this_pass_is_wrong_123!')

        error_locator = page.locator('[data-test="form__error"]')
        expect(error_locator).to_be_visible(timeout=15000)

        assert 'Incorrect password for this email.' in error_locator.inner_text()
        assert not page.locator("text=Automate").is_visible(timeout=3000)