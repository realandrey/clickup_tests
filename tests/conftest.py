import requests
import pytest

from api_clients.task_api import TaskAPI
from constants import BASE_URL, HEADERS, LIST_ID
from utils.helpers import CLICKUP_API, CLICKUP_API_KEY


@pytest.fixture(scope="session")
def create_and_delete_task():
    create_url = f"{BASE_URL}/list/{LIST_ID}/task"
    payload = {
        "name" : "Autotest task"
    }
    response = requests.post(create_url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json().get("id")

    yield task_id # Передаёт ID задачи в сам тест

    if task_id:
        delete_url = f"{BASE_URL}/task/{task_id}"
        requests.delete(delete_url, headers=HEADERS)

@pytest.fixture(scope="session")
def task_api():
    api = TaskAPI(CLICKUP_API, CLICKUP_API_KEY)
    response = api.get_team()
    if response.status_code != 200:
        pytest.fail(f"Не удалось подключиться к API: {response.status_code} / {response.text}")
    return api

@pytest.fixture
def get_team_fixture(task_api):
    response = task_api.get_team()
    assert response.status_code == 200, f"GET /team вернул {response.status_code}"
    teams = response.json().get("teams")
    assert teams, "Список teams пуст или отсутствует"
    return teams[0]

@pytest.fixture
def get_space_fixture(task_api, get_team_fixture):
    response = task_api.get_space(get_team_fixture["id"])
    assert response.status_code == 200, f"GET /team/{get_team_fixture['id']}/space вернул {response.status_code}"
    spaces = response.json().get("spaces")
    assert spaces, "Список spaces пуст или отсутствует"
    return spaces[0]

@pytest.fixture
def get_folder_fixture(task_api, get_space_fixture):
    response = task_api.get_folder(get_space_fixture["id"])
    assert response.status_code == 200, f"GET /space/{get_space_fixture['id']}/folder вернул {response.status_code}"
    folders = response.json().get("folders")
    assert folders, "Список folders пуст или отсутствует"
    return folders[0]

@pytest.fixture
def get_list_fixture(task_api, get_folder_fixture):
    response = task_api.get_list(get_folder_fixture["id"])
    assert response.status_code == 200, f"GET /folder/{get_folder_fixture['id']}/list вернул {response.status_code}"
    lists = response.json().get("lists")
    assert lists, "Список lists пуст или отсутствует"
    return lists[0]

@pytest.fixture
def create_task_fixture(task_api, get_list_fixture):
    task_data = {"name": "Test Task", "description": "Test"}
    response = task_api.create_task(get_list_fixture["id"], task_data)
    assert response.status_code == 200, f"POST /list/{get_list_fixture['id']}/task вернул {response.status_code}"
    task = response.json()
    yield task
    delete_response = task_api.delete_task(task["id"])
    assert delete_response.status_code in (204, 404), f"DELETE /task/{task['id']} вернул {delete_response.status_code}"