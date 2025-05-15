from pages.base_page import BasePage


class BoardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._endpoint = 'login'
        self.page.set_default_timeout(30000)