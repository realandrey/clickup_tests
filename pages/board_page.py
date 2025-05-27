import json

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage


class BoardPage(BasePage):

    def __init__(self, page, team_id):
        super().__init__(page)
        self._endpoint = f"{team_id}/v/b/t/{team_id}"

    BOARD_BUTTON = '[data-test="data-view-item__Board"]'
    BOARD_HEADER = "[data-test='board-header']"
    CREATE_BUTTON = '[data-test="board-group-header__create-task-button__to do"]'
    TASK_INPUT = '[data-test="quick-create-task-panel__panel-board__input"]'
    SAVE_BUTTON = '[data-test="quick-create-task-panel__panel-board__enter-button"]'
    DELETE_MENU_ITEM = ".nav-menu-item__name >> text='Delete'"
    VIRTUAL_SCROLL = "cdk-virtual-scroll-viewport"
    TASK_LINK_TEMPLATE = '[data-test="board-task__name-link__{name}"]'
    ELLIPSIS_MENU_TEMPLATE = '[data-test="board-actions-menu__ellipsis__{name}"]'

    @allure.step("Открываем доску")
    def open_board(self):
        board_url = f"{self.base_url}/{self._endpoint}"
        self.page.goto(board_url)
        self.page.wait_for_load_state("load")
        expect(self.page).to_have_url(board_url)
        viewport = self.page.locator(self.VIRTUAL_SCROLL).nth(1)
        if viewport.is_visible():
            self.page.eval_on_selector(
                self.VIRTUAL_SCROLL, "el => el.scrollTo(0, 1000)"
            )

    @allure.step("Ожидаем появления задачи с именем: {task_name}")
    def wait_for_task_visible(self, task_name: str, timeout: int = 15000):
        self.page.wait_for_selector(
            f"text={json.dumps(task_name)}", state="visible", timeout=timeout
        )

    @allure.step("Проверяем, видна ли задача с именем: {task_name}")
    def is_task_visible(self, task_name: str) -> bool:
        selector = self.TASK_LINK_TEMPLATE.format(name=json.dumps(task_name))
        return self.page.locator(selector).is_visible()

    @allure.step("Создаём задачу с именем: {task_name}")
    def create_task_ui(self, task_name: str):
        with allure.step("Нажимаем кнопку создания задачи"):
            self.wait_for_selector_and_click(self.CREATE_BUTTON)
        with allure.step("Вводим имя задачи"):
            self.wait_for_selector_and_type(self.TASK_INPUT, task_name, delay=100)
        with allure.step("Сохраняем задачу"):
            self.wait_for_selector_and_click(self.SAVE_BUTTON)
        with allure.step("Ожидаем появления задачи в списке"):
            self.page.wait_for_selector(self.TASK_LINK_TEMPLATE.format(name=task_name))

    @allure.step("Удаляем задачу с именем: {task_name}")
    def delete_task(self, task_name: str):
        task_selector = self.TASK_LINK_TEMPLATE.format(name=task_name)
        ellipsis_selector = self.ELLIPSIS_MENU_TEMPLATE.format(name=task_name)

        task = self.page.locator(task_selector)

        with allure.step("Прокручиваем к задаче"):
            task.scroll_into_view_if_needed()
            self.page.wait_for_timeout(300)

        with allure.step("Наводим курсор на задачу"):
            task.hover()

        with allure.step("Открываем контекстное меню задачи"):
            self.wait_for_selector_and_click(ellipsis_selector)

        with allure.step("Нажимаем пункт 'Delete'"):
            self.wait_for_selector_and_click(self.DELETE_MENU_ITEM)

        with allure.step("Ожидаем исчезновения задачи из DOM"):
            self.page.wait_for_selector(task_selector, state="detached", timeout=10000)
