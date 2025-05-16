import requests
import pytest
from constants import BASE_URL, HEADERS, LIST_ID


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

