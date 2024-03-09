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
        response = requests.get(self.url + "api/members/roles/gameroles/", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            return response.json()

    def get_game_role(self, game_role_detection):
        response = requests.get(self.url + "api/members/roles/gameroles/" + game_role_detection + "/", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Value not found")

    def set_new_minutes_spent(self, member_name, minutes_spent):
        response = requests.post(f"{self.url}api/members/minutes_spent/{member_name}/{minutes_spent}/", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Something went wrong while putting data into the server")

    def get_time_ranking(self):
        pass


if __name__ == "__main__":
    rc = RestClient()
    rc.set_new_minutes_spent("testerbotow2137", 20)

