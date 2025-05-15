from pages.base_page import BasePage
from constants import TEAM_ID
from playwright.sync_api import expect


class BoardPage(BasePage):





    def __init__(self, page):
        super().__init__(page)
        self._endpoint = f"{TEAM_ID}/v/b/t/{TEAM_ID}"
        self.page.set_default_timeout(30000)

    def open_board(self):
        self.page.goto(f"https://app.clickup.com/{self._endpoint}")