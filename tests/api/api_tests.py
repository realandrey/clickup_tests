import requests
import pytest

from tests.conftest import create_and_delete_task
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

    response_get = requests.get(f"{BASE_URL}/task/{task_id}", headers=HEADERS) #Запрос на получение информации о задаче с тем же task_id, чтобы убедиться, что задача больше не существует.
    assert response_get.status_code == 404, f"Ожидал 404 статус код, задача не была удалена, получил {response_get.status_code}"


@pytest.mark.parametrize("payload, expected_status", [
    ({}, 400), # нет обязательного поля name
    ({"name": ""}, 400), # пустое имя
    ({"name": None}, 400) # name = None
])
def test_create_task_negative(payload, expected_status):
    url = f"{BASE_URL}/list/{LIST_ID}/task"
    response = requests.post(url, headers=HEADERS, json=payload)

    assert response.status_code == expected_status, f"Ожидал {expected_status}, получил {response.status_code}. Ответ: {response.text}"


def test_get_task_negative():
    fake_task_id = "34534534234"
    url = f"{BASE_URL}/task/{fake_task_id}"

    response = requests.get(url, headers=HEADERS)

    assert response.status_code == 401, f"Ожидал 401 статус код, получил {response.status_code}"
    assert "err" in response.json(), "Ожидал ошибку в теле ответа"


def test_update_task_negative():
    fake_task_id = "sdfasdf34534534234"
    url = f"{BASE_URL}/task/{fake_task_id}"
    payload = {
        "name": "Negative name",
    }

    response = requests.put(url, headers=HEADERS, json=payload)

    assert response.status_code == 401, f"Ожидал 401 статус код, получил {response.status_code}"
    assert "err" in response.json(), "Ожидал ошибку в теле ответа"


def test_delete_task_negative():
    fake_task_id = "sdfxx53453423774"
    url = f"{BASE_URL}/task/{fake_task_id}"
    response = requests.put(url, headers=HEADERS)

    assert response.status_code == 401, f"Ожидал 401 статус код, получил {response.status_code}"
    assert "err" in response.json(), "Ожидал ошибку в теле ответа"
