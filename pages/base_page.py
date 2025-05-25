import re
import allure

from playwright.sync_api import expect

class BasePage:

    def __init__(self, page, base_url='https://app.clickup.com'):
        self.page = page
        self._endpoint = ''
        self.base_url = base_url

    def _get_full_url(self):
        return f"{self.base_url}/{self._endpoint}"

    @allure.step("Навигация по странице")
    def navigate_to(self):
        full_url = self._get_full_url()
        self.page.goto(full_url)
        self.page.wait_for_load_state('load')
        expect (self.page).to_have_url(full_url)
        expect(self.page).to_have_url(re.compile(f"{full_url}"))

    @allure.step("Клик по селектору: {selector}")
    def wait_for_selector_and_click(self, selector):
        self.page.wait_for_selector(selector)
        self.page.click(selector)

    @allure.step("Заполнение поля: {selector} значением: {value}")
    def wait_for_selector_and_fill(self, selector, value):
        self.page.wait_for_selector(selector)
        self.page.fill(selector, value)

    @allure.step("Ввод текста с задержкой в {selector}")
    def wait_for_selector_and_type(self, selector, value, delay):
        self.page.wait_for_selector(selector)
        self.page.type(selector, value, delay=delay)

    @allure.step("Проверка, что элемент {selector} видим")
    def assert_element_is_visible(self, selector, timeout=60000):
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    @allure.step("Проверка наличия текста '{text}' на странице")
    def assert_text_present_on_page(self, text):
        expect(self.page.locator('body')).to_contain_text(text)

    @allure.step("Проверка, что значение поля {selector} заполнено текстом {text}")
    def assert_text_in_element(self, selector, text):
        expect(self.page.locator(selector)).to_have_text(text)

    @allure.step("Проверка, что значение поля {selector} равно {expected_value}")
    def assert_input_value(self, selector, expected_value):
        expect(self.page.locator(selector)).to_have_value(expected_value)

    @allure.step("Ожидание появления селектора: {selector}")
    def wait_for_selector(self,selector):
        expect(self.page.locator(selector)).to_be_visible(timeout=10000)

    @allure.step("Наведение курсора на элемент: {selector}")
    def wait_for_selector_and_hover(self, selector):
        self.page.wait_for_selector(selector)
        self.page.hover(selector)


