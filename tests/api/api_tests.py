import requests
import pytest
import allure

from tests.conftest import create_and_delete_task, get_list_fixture
from constants import BASE_URL, HEADERS



@allure.feature("Создание задач")
@allure.description("Создание задачи и её удаление")
def test_create_task(get_list_fixture):
    with allure.step("Подготовка данных"):
        list_id = get_list_fixture("id")
        url = f"{BASE_URL}/list/{list_id}/task"
        payload = {
            "name": "Test task"
        }

    with allure.step("Отправка запроса на создание задачи"):
        response = requests.post(url, headers=HEADERS, json=payload)
        assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
        task_id = response.json()["id"]
        assert "id" in response.json()
        assert response.json()["name"] == "Test task"
        allure.attach(str(task_id), name="Created Task ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Удаление задачи"):
        delete_response = requests.delete(f"{BASE_URL}/task/{task_id}", headers=HEADERS)
        assert delete_response.status_code == 204, "Удаление задачи завершилось с ошибкой"


@allure.feature("Получение задач")
@allure.description("Получение ранее созданной задачи по ID")
def test_get_task(create_and_delete_task):
    task_id = create_and_delete_task

    with allure.step("Получение задачи по ID"):
        url = f"{BASE_URL}/task/{task_id}"

        response = requests.get(url, headers=HEADERS)

        assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
        data = response.json()
        assert data["id"] == str(task_id), "ID задачи не совпадает"
        assert "name" in data, "Поле 'name' отсутствует в ответе"


@allure.feature("Обновление задач")
@allure.description("Обновление задачи по ID")
def test_update_task(create_and_delete_task):
    task_id = create_and_delete_task
    url = f"{BASE_URL}/task/{task_id}"
    payload = {
            "name": "Updated task from Postman",
        }

    with allure.step(f"Обновление задачи с ID {task_id}"):
        response = requests.put(url, headers=HEADERS, json=payload)

        assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
        assert "id" in response.json()
        assert response.json()["name"] == "Updated task from Postman"


@allure.feature("Удаление задач")
@allure.description("Удаление задачи и проверка что она больше не существует")
def test_delete_task(create_and_delete_task):
    task_id = create_and_delete_task
    url = f"{BASE_URL}/task/{task_id}"

    with allure.step("Удаление задачи"):
        response = requests.delete(url, headers=HEADERS)

        assert response.status_code == 204, f"Ожидал 204 статус код, получил {response.status_code}"
        assert response.content == b'', "Ожидал пустое тело ответа"

    with allure.step("Проверка: задачи больше не существует"):
        response_get = requests.get(f"{BASE_URL}/task/{task_id}", headers=HEADERS) #Запрос на получение информации о задаче с тем же task_id, чтобы убедиться, что задача больше не существует.
        assert response_get.status_code == 404, f"Ожидал 404 статус код, задача не была удалена, получил {response_get.status_code}"


@allure.feature("Негативные тесты создания задачи")
@allure.description("Проверка валидации при создании задачи с некорректными данными")
@pytest.mark.parametrize("payload, expected_status", [
    ({}, 400), # нет обязательного поля name
    ({"name": ""}, 400), # пустое имя
    ({"name": None}, 400) # name = None
])
def test_create_task_negative(payload, expected_status, get_list_fixture):
    with allure.step("Попытка создания задачи с невалидным телом запроса"):
        list_id = get_list_fixture("id")
        url = f"{BASE_URL}/list/{list_id}/task"
        response = requests.post(url, headers=HEADERS, json=payload)

        assert response.status_code == expected_status, f"Ожидал {expected_status}, получил {response.status_code}. Ответ: {response.text}"


@allure.feature("Негативные тесты получения задачи")
@allure.description("Проверка получения задачи с некорректным ID")
def test_get_task_negative():
    fake_task_id = "34534534234"
    url = f"{BASE_URL}/task/{fake_task_id}"

    with allure.step(f"Получение задачи с фейковым ID {fake_task_id}"):
        response = requests.get(url, headers=HEADERS)

        assert response.status_code == 401, f"Ожидал 401 статус код, получил {response.status_code}"
        assert "err" in response.json(), "Ожидал ошибку в теле ответа"


@allure.feature("Негативные тесты обновления задачи")
@allure.description("Проверка обновления задачи с несуществующим ID")
def test_update_task_negative():
    fake_task_id = "sdfasdf34534534234"
    url = f"{BASE_URL}/task/{fake_task_id}"
    payload = {
        "name": "Negative name",
    }

    with allure.step(f"Попытка обновления фейковой задачи ID {fake_task_id}"):
        response = requests.put(url, headers=HEADERS, json=payload)

        assert response.status_code == 401, f"Ожидал 401 статус код, получил {response.status_code}"
        assert "err" in response.json(), "Ожидал ошибку в теле ответа"


@allure.feature("Негативные тесты удаления задачи")
@allure.description("Проверка удаления задачи с несуществующим ID")
def test_delete_task_negative():
    fake_task_id = "sdfxx53453423774"
    url = f"{BASE_URL}/task/{fake_task_id}"

    with allure.step(f"Попытка удаления фейковой задачи ID {fake_task_id}"):
        response = requests.put(url, headers=HEADERS)

        assert response.status_code == 401, f"Ожидал 401 статус код, получил {response.status_code}"
        assert "err" in response.json(), "Ожидал ошибку в теле ответа"
