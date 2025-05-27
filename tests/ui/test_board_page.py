from datetime import datetime

import pytest
import allure

from pages.board_page import BoardPage


@allure.suite("UI: Board")
@allure.feature("Работа с задачами на доске")
class TestBoardPage:

    @allure.title("Удаление задачи через UI и проверка через API")
    @allure.description("""
        Проверка удаления задачи с доски через UI.
        Подтверждаем, что:
        - Задача исчезла с доски
        - API возвращает 404 по её ID
        """)
    def test_task_delete(self, login, create_task_fixture, task_api, get_team_fixture):
        task_id = create_task_fixture['id']
        task_name = create_task_fixture['name']
        board_page = BoardPage(login, get_team_fixture["id"])

        with allure.step("Открываем доску"):
            board_page.open_board()

        with allure.step(f"Ожидаем отображение задачи '{task_name}'"):
            board_page.wait_for_task_visible(task_name)

        with allure.step(f"Удаляем задачу '{task_name}'"):
            board_page.delete_task(task_name)

        task_link_selector = f'[data-test="board-task__name-link__{task_name}"]'

        with allure.step("Проверяем, что задача исчезла из DOM"):
            board_page.page.locator(task_link_selector).wait_for(state='detached', timeout=5000)
            assert not board_page.page.locator(task_link_selector).is_visible(), f"Задача {task_name} все еще видна через UI"

        with allure.step("Проверяем, что API возвращает 404 по ID задачи"):
            response = task_api.get_task(task_id)
            assert response.status_code == 404, "Ожидали 404, задача все еще доступна"

    @allure.title("Создание задачи через UI и валидация через API")
    @allure.description("""
        Тест на создание новой задачи через UI:
        - Проверка отображения на доске
        - Проверка наличия через API
        - Удаление задачи через API
        """)
    def test_create_task_ui(self, login, task_api, get_list_fixture, get_team_fixture):
        name_for_test = f"Task for delete test {datetime.now().strftime('%H%M%S')}"
        board_page = BoardPage(login, get_team_fixture["id"])

        with allure.step("Открываем доску"):
            board_page.open_board()

        with allure.step(f"Создаём задачу '{name_for_test}'"):
            board_page.create_task_ui(name_for_test)

        task_link_selector = f'[data-test="board-task__name-link__{name_for_test}"]'

        with allure.step("Проверяем, что задача отображается в UI"):
            board_page.page.locator(task_link_selector).wait_for(state='visible', timeout=5000)
            assert board_page.page.locator(task_link_selector).is_visible(), "Созданная задача не отображается через UI"

        list_id = get_list_fixture['id']
        response = task_api.get_tasks_from_list(list_id)
        assert response.status_code == 200, f"GET /list/{list_id}/task вернул {response.status_code}"
        tasks = response.json().get('tasks', [])

        with allure.step("Получаем ID созданной задачи через API"):
            created = next((t for t in tasks if t['name'] == name_for_test), None)
            assert created, f"Задача '{name_for_test}' не найдена через API"
            task_id = created['id']

        with allure.step("Удаляем задачу через API"):
            delete_resp = task_api.delete_task(task_id)
            assert delete_resp.status_code == 204, f"DELETE /task/{task_id} вернул {delete_resp.status_code}"

        with allure.step("Проверяем, что API возвращает 404 на удалённую задачу"):
            check_resp = task_api.get_task(task_id)
            assert check_resp.status_code == 404, f"Ожидали 404, получили {check_resp.status_code}"
