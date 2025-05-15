import re
from playwright.sync_api import expect

class BasePage:

    def __init__(self, page, base_url='https://app.clickup.com'):
        self.page = page
        self._endpoint = ''
        self.base_url = base_url

    def _get_full_url(self):
        return f"{self.base_url}/{self._endpoint}"

    def navigate_to(self):
        full_url = self._get_full_url()
        self.page.goto(full_url)
        self.page.wait_for_load_state('load')
        expect (self.page).to_have_url(full_url)
        expect(self.page).to_have_url(re.compile(f"{full_url}"))

    def wait_for_selector_and_click(self, selector):
        self.page.wait_for_selector(selector)
        self.page.click(selector)

    def wait_for_selector_and_fill(self, selector, value):
        self.page.wait_for_selector(selector)
        self.page.fill(selector, value)

    def wait_for_selector_and_type(self, selector, value, delay):
        self.page.wait_for_selector(selector)
        self.page.type(selector, value, delay=delay)

    def assert_element_is_visible(self, selector, timeout=15000):
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def assert_text_present_on_page(self, text):
        expect(self.page.locator('body')).to_contain_text(text)

    def assert_text_in_element(self, selector, text):
        expect(self.page.locator(selector)).to_have_text(text)

    def assert_input_value(self, selector, expected_value):
        expect(self.page.locator(selector)).to_have_value(expected_value)

    def wait_for_selector(self,selector):
        expect(self.page.locator("text=Spaces")).to_be_visible(timeout=15000)

