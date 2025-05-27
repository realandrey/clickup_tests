import allure
import pytest

from api_clients.task_api import TaskAPI
from utils.helpers import CLICKUP_API, CLICKUP_API_KEY


@pytest.fixture(scope="session")
def task_api():
    with allure.step("Инициализация TaskAPI и проверка подключения к API"):
        api = TaskAPI(CLICKUP_API, CLICKUP_API_KEY)
        response = api.get_team()
        assert (
            response.status_code == 200
        ), f"Ошибка подключения к API: {response.status_code} / {response.text}"
        return api


@pytest.fixture
def get_team_fixture(task_api):
    with allure.step("Получение команды через /team"):
        response = task_api.get_team()
        assert response.status_code == 200, f"GET /team вернул {response.status_code}"
        teams = response.json().get("teams")
        assert teams, "Список teams пуст или отсутствует"
        return teams[0]


@pytest.fixture
def get_space_fixture(task_api, get_team_fixture):
    with allure.step("Получение пространства по ID команды"):
        response = task_api.get_space(get_team_fixture["id"])
        assert (
            response.status_code == 200
        ), f"GET /team/{get_team_fixture['id']}/space вернул {response.status_code}"
        spaces = response.json().get("spaces")
        assert spaces, "Список spaces пуст или отсутствует"
        return spaces[0]


@pytest.fixture
def get_folder_fixture(task_api, get_space_fixture):
    with allure.step("Получение папки по ID пространства"):
        response = task_api.get_folder(get_space_fixture["id"])
        assert (
            response.status_code == 200
        ), f"GET /space/{get_space_fixture['id']}/folder вернул {response.status_code}"
        folders = response.json().get("folders")
        assert folders, "Список folders пуст или отсутствует"
        return folders[0]


@pytest.fixture
def get_list_fixture(task_api, get_folder_fixture):
    with allure.step("Получение списка по ID папки"):
        response = task_api.get_list(get_folder_fixture["id"])
        assert (
            response.status_code == 200
        ), f"GET /folder/{get_folder_fixture['id']}/list вернул {response.status_code}"
        lists = response.json().get("lists")
        assert lists, "Список lists пуст или отсутствует"
        return lists[0]


@pytest.fixture
def create_task_fixture(task_api, get_list_fixture):
    with allure.step("Создание задачи в списке"):
        task_data = {"name": "Test Task", "description": "Test"}
        response = task_api.create_task(get_list_fixture["id"], task_data)
        result = {
            "status_code": response.status_code,
            "data": response.json()
        }

        yield result

        with allure.step("Удаление задачи после теста"):
            delete_response = task_api.delete_task(result["data"]["id"])
            assert delete_response.status_code == 204, (
                f"Ошибка удаления задачи: {delete_response.status_code} / {delete_response.text}"
            )


@pytest.fixture
def fake_task_id():
    return "nonexistent_task_id_34534534234"
