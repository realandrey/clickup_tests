import pytest
import allure

from tests.conftest import create_task_fixture, get_list_fixture, task_api


@allure.feature("Создание задач")
@allure.description("Создание задачи и её удаление")
def test_create_task(create_task_fixture):
    task_id = create_task_fixture["id"]

    with allure.step("Проверка, что задача была успешно создана"):
        assert task_id, "ID задачи пустой"
        allure.attach(str(task_id), name="Created Task ID", attachment_type=allure.attachment_type.TEXT)



@allure.feature("Получение задач")
@allure.description("Получение ранее созданной задачи по ID")
def test_get_task(task_api, create_task_fixture):
    task_id = create_task_fixture["id"]

    with allure.step("Получение задачи через task_api.get_task"):
        response = task_api.get_task(task_id)
        assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"
        data = response.json()
        assert data["id"] == str(task_id)
        assert "name" in data


@allure.feature("Обновление задач")
@allure.description("Обновление задачи по ID")
def test_update_task(task_api, create_task_fixture):
    task_id = create_task_fixture["id"]
    payload = {"name": "Updated task from Postman"}

    with allure.step("Обновление задачи через task_api.update_task"):
        response = task_api.update_task(task_id, payload)
        assert response.status_code == 200, f"Ожидал 200, получил {response.status_code}"
        assert response.json()["name"] == "Updated task from Postman"


@allure.feature("Удаление задач")
@allure.description("Удаление задачи и проверка что она больше не существует")
def test_delete_task(task_api, create_task_fixture):
    task_id = create_task_fixture["id"]

    with allure.step("Удаление задачи через task_api.delete_task"):
        delete_response = task_api.delete_task(task_id)
        assert delete_response.status_code == 204, f"Ожидал 204, получил {delete_response.status_code}"

    with allure.step("Проверка что задача удалена через task_api.get_task"):
        response_get = task_api.get_task(task_id)
        assert response_get.status_code == 404, f"Ожидал 404, получил {response_get.status_code}"


@allure.feature("Негативные тесты создания задачи")
@allure.description("Проверка валидации при создании задачи с некорректными данными")
@pytest.mark.parametrize("payload, expected_status", [
    ({}, 400),
    ({"name": ""}, 400),
    ({"name": None}, 400)
])
def test_create_task_negative(task_api, get_list_fixture, payload, expected_status):
    list_id = get_list_fixture["id"]

    with allure.step("Попытка создать задачу с невалидными данными через task_api.create_task"):
        response = task_api.create_task(list_id, payload)
        assert response.status_code == expected_status, f"Ожидал {expected_status}, получил {response.status_code}"


@allure.feature("Негативные тесты получения задачи")
@allure.description("Проверка получения задачи с некорректным ID")
def test_get_task_negative(task_api):
    fake_task_id = "34534534234"

    with allure.step(f"Попытка получить фейковую задачу через task_api.get_task"):
        response = task_api.get_task(fake_task_id)
        assert response.status_code == 401, f"Ожидал 401, получил {response.status_code}"
        assert "err" in response.json()


@allure.feature("Негативные тесты обновления задачи")
@allure.description("Проверка обновления задачи с несуществующим ID")
def test_update_task_negative(task_api):
    fake_task_id = "sdfasdf34534534234"
    payload = {"name": "Negative name"}

    with allure.step("Попытка обновления фейковой задачи через task_api.update_task"):
        response = task_api.update_task(fake_task_id, payload)
        assert response.status_code == 401, f"Ожидал 401, получил {response.status_code}"
        assert "err" in response.json()


@allure.feature("Негативные тесты удаления задачи")
@allure.description("Проверка удаления задачи с несуществующим ID")
def test_delete_task_negative(task_api):
    fake_task_id = "sdfxx53453423774"

    with allure.step("Попытка удаления фейковой задачи через task_api.delete_task"):
        response = task_api.delete_task(fake_task_id)
        assert response.status_code == 401, f"Ожидал 401, получил {response.status_code}"
        assert "err" in response.json()
