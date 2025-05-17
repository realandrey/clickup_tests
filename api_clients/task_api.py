import requests


class TaskAPI:
    def __init__(self, base_url, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": api_key,
            "Content-Type": "application/json"
        })
        self.base_url = base_url


    def get_team(self):
        return self.session.get(f"{self.base_url}/team")


    def get_space(self, team_id):
        return self.session.get(f"{self.base_url}/team/{team_id}/space")


    def get_folder(self, space_id):
        return self.session.get(f"{self.base_url}/space/{space_id}/folder")


    def get_list(self, folder_id):
        return self.session.get(f"{self.base_url}/folder/{folder_id}/list")


    def create_task(self, list_id, task_data):
        return self.session.post(f"{self.base_url}/list/{list_id}/task", json=task_data)


    def get_task(self, task_id):
        return self.session.get(f"{self.base_url}/task/{task_id}")


    def update_task(self, task_id, task_update):
        return self.session.put(f"{self.base_url}/task/{task_id}", json=task_update)


    def delete_task(self, task_id):
        return self.session.delete(f"{self.base_url}/task/{task_id}")