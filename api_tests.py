import requests
from constants import BASE_URL, HEADERS, LIST_ID

def test_create_task():
    url = f"{BASE_URL}/list/{LIST_ID}/task"
    payload = {
        "name": "Test task",
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    assert response.status_code == 200, f"Ожидал 200 статус код, получил {response.status_code}"
    assert "id" in response.json()
    assert response.json()["name"] == "Test task"

    task_id = response.json()["id"]
    requests.delete(f"{BASE_URL}/task/{task_id}", headers=HEADERS)