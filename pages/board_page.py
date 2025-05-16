import os

from pages.base_page import BasePage
from constants import TEAM_ID
from playwright.sync_api import expect


class BoardPage(BasePage):
    _endpoint = f"{TEAM_ID}/v/b/t/{TEAM_ID}"

    TEAM_ID = os.getenv("CLICKUP_TEAM_ID", "90131041433")
    BOARD_BUTTON = '[data-test="data-view-item__Board"]'
    BOARD_HEADER = "[data-test='board-header']"
    CREATE_BUTTON = '[data-test="board-group-header__create-task-button__to do"]'
    TASK_INPUT = '[data-test="quick-create-task-panel__panel-board__input"]'
    SAVE_BUTTON = '[data-test="quick-create-task-panel__panel-board__enter-button"]'
    DELETE_MENU_ITEM = ".nav-menu-item__name >> text='Delete'"
    VIRTUAL_SCROLL = 'cdk-virtual-scroll-viewport'
    TASK_LINK_TEMPLATE = '[data-test="board-task__name-link__{name}"]'
    ELLIPSIS_MENU_TEMPLATE = '[data-test="board-actions-menu__ellipsis__{name}"]'

    def open_board(self):
        self.page.goto(f"https://app.clickup.com/{self._endpoint}")
        self.page.wait_for_load_state("load")
        expect(self.page).to_have_url(f"https://app.clickup.com/{self._endpoint}")
        self.wait_for_selector_and_click(self.BOARD_BUTTON)
        viewport = self.page.locator(self.VIRTUAL_SCROLL)
        if viewport.is_visible():
            viewport.scroll_to(0, 1000)

    def wait_for_task_visible(self, task_name: str, timeout: int = 15000):
        self.page.wait_for_selector(f"text={json.dumps(task_name)}", state="visible", timeout=timeout)

# навести курсор на карточку через ховер(добавить в бейз пейдж) затем нажаить на кебаб и удалить.