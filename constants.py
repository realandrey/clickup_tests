from utils.helpers import CLICKUP_API_KEY

BASE_URL = "https://api.clickup.com/api/v2"

HEADERS = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}

# ID твоего Workspace, Space и List надо найти вручную в ClickUp
TEAM_ID = "90151159924"
SPACE_ID = "90154583437"
LIST_ID = "901511028330"
