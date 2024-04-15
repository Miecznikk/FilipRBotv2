from dotenv import load_dotenv
import os
import requests


class RestController:
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
        response = requests.get(f"{self.url}api/members/minutes_spent/ranking/", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            return response.json()

    def get_random_connect_audio(self):
        response = requests.get(f"{self.url}api/utils/audio/random_connect/get_random", headers={
            "Authorization": f"Token {self.get_authenticate_token()}"
        })
        if response.status_code == 200:
            with open('../audio_file.mp3', 'wb') as f:
                f.write(response.content)
            return 'audio_file.mp3'
        else:
            raise ValueError("Failed to retrieve audio file, response code:" + str(response))

    def get_default_message(self, user_name, message_content):
        response = requests.get(f"{self.url}/api/messages/get/default_message/{user_name}/{message_content}",
                                headers={"Authorization": f"Token {self.get_authenticate_token()}"})

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Something went wrong while retrieving default message" + str(response))

    def get_questions(self, number_of_questions):
        response = requests.get(f"{self.url}/api/quiz/questions/{number_of_questions}",
                                headers={"Authorization": f"Token {self.get_authenticate_token()}"})
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Something went wrong while retrieving questions" + str(response))

    def add_points_to_member(self, member, points):
        response = requests.post(f"{self.url}/api/members/points/add/{member}/{points}/",
                                 headers={"Authorization": f"Token {self.get_authenticate_token()}"})
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Something went wrong while adding points to member {member}" + str(response))

    def get_points_ranking(self):
        response = requests.get(f"{self.url}/api/members/points/ranking/",
                                headers={"Authorization": f"Token {self.get_authenticate_token()}"})
        if response.status_code == 200:
            return response.json()


if __name__ == "__main__":
    rc = RestClient()
    print(rc.get_points_ranking())
