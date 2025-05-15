from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL
import pytest

class TestLoginPage:

    def test_login_success(self, login):
        login.wait_for_selector("text=Automate")  # дождаться элемента
        assert "Automate" in login.content()
