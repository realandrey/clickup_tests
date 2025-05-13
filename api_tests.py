from http.client import responses

import requests

from conftest import create_and_delete_task
from constants import BASE_URL, HEADERS, LIST_ID

def test_create_task():
    url = f"{BASE_URL}/list/{LIST_ID}/task"
    payload = {
        "name": "Test task"
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
    assert "id" in response.json()
    assert response.json()["name"] == "Test task"

    task_id = response.json()["id"]
    requests.delete(f"{BASE_URL}/task/{task_id}", headers=HEADERS)


def test_get_task(create_and_delete_task):
    task_id = create_and_delete_task
    url = f"{BASE_URL}/task/{task_id}"

    response = requests.get(url, headers=HEADERS)

    assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
    data = response.json()
    assert data["id"] == str(task_id), "ID задачи не совпадает"
    assert "name" in data, "Поле 'name' отсутствует в ответе"


def test_update_task(create_and_delete_task):
    task_id = create_and_delete_task
    url = f"{BASE_URL}/task/{task_id}"
    payload = {
            "name": "Updated task from Postman",
        }

    response = requests.put(url, headers=HEADERS, json=payload)

    assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
    assert "id" in response.json()
    assert response.json()["name"] == "Updated task from Postman"


def test_delete_task(create_and_delete_task):
    task_id = create_and_delete_task
    url = f"{BASE_URL}/task/{task_id}"

    response = requests.delete(url, headers=HEADERS)

    assert response.status_code == 204, f"Ожидал 204 статус код, получил {response.status_code}"
    assert response.content == b'', "Ожидал пустое тело ответа"

    response_get = requests.get(f"{BASE_URL}/task/{task_id}", headers=HEADERS)
    assert response_get.status_code == 404, f"Ожидал 404 статус код, задача не была удалена, получил {response_get.status_code}"

