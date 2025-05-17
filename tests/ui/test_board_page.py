from datetime import datetime

import pytest
from pages.board_page import BoardPage
from tests.conftest import create_task_fixture, task_api, get_list_fixture, get_folder_fixture, get_space_fixture, get_team_fixture



class TestBoardPage:


    def test_task_delete(self, login, create_task_fixture, task_api):
        task_id = create_task_fixture['id']
        task_name = create_task_fixture['name']
        board_page = BoardPage(login)

        board_page.open_board()
        board_page.wait_for_task_visible(task_name)

        board_page.delete_task(task_name)
        task_link_selector = f'[data-test="board-task__name-link__{task_name}"]'
        board_page.page.locator(task_link_selector).wait_for(state='detached', timeout=5000)
        assert not board_page.page.locator(task_link_selector).is_visible(), f"Задача {task_name} все еще видна через UI"
        response = task_api.get_task(task_id)
        assert response.status_code == 404, "Ожидали 404, задача все еще доступна"

    def test_create_task_ui(self, login, task_api, get_list_fixture):
        name_for_test = f"Task for delete test {datetime.now().strftime('%H%M%S')}"
        board_page = BoardPage(login)

        board_page.open_board()
        board_page.create_task_ui(name_for_test)

        task_link_selector = f'[data-test="board-task__name-link__{name_for_test}"]'
        board_page.page.locator(task_link_selector).wait_for(state='visible', timeout=5000)
        assert board_page.page.locator(task_link_selector).is_visible(), "Созданная задача не отображается через UI"

        list_id = get_list_fixture['id']
        response = task_api.session.get(f"{task_api.base_url}/list/{list_id}/task")
        assert response.status_code == 200, f"GET /list/{list_id}/task вернул {response.status_code}"
        tasks = response.json().get('tasks', [])

        created = next((t for t in tasks if t['name'] == name_for_test), None)
        assert created, f"Задача '{name_for_test}' не найдена через API"
        task_id = created['id']

        delete_resp = task_api.delete_task(task_id)
        assert delete_resp.status_code == 204, f"DELETE /task/{task_id} вернул {delete_resp.status_code}"

        check_resp = task_api.get_task(task_id)
        assert check_resp.status_code == 404, f"Ожидали 404, получили {check_resp.status_code}"
