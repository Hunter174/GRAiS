import requests
import json
import os

class HabiticaAPI:
    def __init__(self):
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.config_file = os.path.join(root_dir, 'credentials.json')
        print(self.config_file)
        self.credentials = self.load_credentials()
        self.base_url = "https://habitica.com/api/v3"
        self.headers = {
            "x-api-user": self.credentials['habitica']['user_id'],
            "x-api-key": self.credentials['habitica']['api_token'],
            "Content-Type": "application/json"
        }

    def load_credentials(self):
        """Load credentials from the credentials.json file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.config_file} not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Couldn't parse credentials.json file.")
            return None

    def get_tasks(self):
        """Get all current open tasks."""
        url = f"{self.base_url}/tasks/user"  # API endpoint for fetching tasks
        params = {"type": "todos"}  # We only want to fetch todos
        try:
            response = requests.get(url, headers=self.headers, params=params)

            # Check if the response status is OK (200)
            if response.status_code == 200:
                tasks = response.json()  # Parse the JSON response
                return tasks.get("data", [])  # Return the list of todos
            else:
                print(f"Error: {response.status_code}, {response.json().get('message', 'No message')}")
                return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_player_summary(self):
        """Get player statis"""
        url = f"{self.base_url}/user"  # API endpoint for fetching tasks
        try:
            response = requests.get(url, headers=self.headers)

            # Check if the response status is OK (200)
            if response.status_code == 200:
                user_info = response.json()  # Parse the JSON response
                return user_info.get("data", [])  # Return the list of todos
            else:
                print(f"Error: {response.status_code}, {response.json().get('message', 'No message')}")
                return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

if __name__ == "__main__":
    api = HabiticaAPI()
    api.get_player_summary()