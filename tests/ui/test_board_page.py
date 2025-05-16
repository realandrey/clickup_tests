from pages.board_page import BoardPage

class TestBoardPage:


    def test_task_delete(self, login, create_task_fixture, task_api):
        task_id = create_task_fixture['id']
        task_name = create_task_fixture['name']
        board_page = BoardPage(login)

        board_page.navigate_to_board()
        board_page.wait_for_task_visible(task_name)

        board_page.delete_task(task_name)
        task_link_selector = f'[data-test="board-task__name-link__{task_name}"]'
        board_page.page.locator(task_link_selector).wait_for(state='detached', timeout=5000)
        assert not board_page.page.locator(task_link_selector).is_visible(), f"Задача {task_name} все еще видна через UI"
        response = task_api.get_task(task_id)
        assert response.status_code == 404, "Ожидали 404, задача все еще доступна"