from dotenv import load_dotenv
import os
import requests


class RestClient:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("API_USERNAME")
        self.password = os.getenv("API_PASSWORD")
        self.url = os.getenv("API_URL")

    def get_authenticate_token(self):
        credentials = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(self.url + "authenticate/", data=credentials)
        if response.status_code == 200:
            try:
                return response.json()['token']
            except KeyError:
                print("Error reading token")
                raise

    def get_discord_members(self):
        response = requests.get(self.url + "api/members/", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            return response.json()

    def get_game_roles(self):
        response = requests.get(self.url + "api/members/roles/gameroles", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            return response.json()


if __name__ == "__main__":
    rc = RestClient()
    rc.get_discord_members()
