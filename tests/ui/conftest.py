from http.client import responses

import pytest
import requests
from playwright.sync_api import sync_playwright
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


@pytest.fixture
def login(browser):
    context = browser.new_context()
    page = context.new_page()
    LoginPage(page).login(CLICKUP_EMAIL, CLICKUP_PASSWORD)
    yield page
    context.close()


@pytest.fixture
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
