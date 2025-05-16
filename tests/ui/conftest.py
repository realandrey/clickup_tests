from http.client import responses

import pytest
import requests
from playwright.sync_api import sync_playwright

from pages.board_page import BoardPage
from utils.helpers import CLICKUP_API_KEY

from constants import LIST_ID
from pages.login_page import LoginPage
from utils.helpers import CLICKUP_EMAIL, CLICKUP_PASSWORD

@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()  # Далее, используя объект playwright, можно запускать браузер и работать с ним
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="session")
def login(browser):
    context = browser.new_context()
    page = context.new_page()
    LoginPage(page).login(CLICKUP_EMAIL, CLICKUP_PASSWORD)

    yield page


@pytest.fixture(scope="session")
def created_card():
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    json = {
        "name": "UI Test Card",
        "status": "to do"
    }

    response = requests.post(url, json=json, headers=headers)
    response.raise_for_status()
    task_id = response.json()["id"]

    yield {
        "id": task_id,
        "name": "UI Test Card"
    }

    requests.delete(f"https://api.clickup.com/api/v2/task/{task_id}", headers=headers) # Очистка после теста

@pytest.fixture
def create_task_fixture(task_api, get_list_fixture):
    task_data = {"name": "Test Task", "description": "Test"}
    response = task_api.create_task(get_list_fixture["id"], task_data)
    assert response.status_code == 200, f"POST /list/{get_list_fixture['id']}/task вернул {response.status_code}"
    task = response.json()
    yield task
    delete_response = task_api.delete_task(task["id"])
    assert delete_response.status_code in (204, 404), f"DELETE /task/{task['id']} вернул {delete_response.status_code}"

@pytest.fixture(scope="session")
def task_api():
    api = TaskAPI(CLICKUP_API, CLICKUP_API_KEY)
    response = api.get_team()
    if response.status_code != 200:
        pytest.fail(f"Не удалось подключиться к API: {response.status_code} / {response.text}")
    return api