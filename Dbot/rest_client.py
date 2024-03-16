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
            with open('audio_file.mp3', 'wb') as f:
                f.write(response.content)
            return 'audio_file.mp3'
        else:
            raise ValueError("Failed to retrieve audio file, response code:" + str(response))

    def get_weather(self, api_key, city):
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = data['current']['condition']['text']
            temperature = data['current']['temp_c']
            humidity = data['current']['humidity']
            wind_speed = data['current']['wind_kph'] / 3.6  # Convert from kph to m/s
            return {
                'weather': weather,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed
            }
        else:
            return response

    def get_forecast(self, api_key, city):
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            forecast_tomorrow = data['forecast']['forecastday'][2]
            date = forecast_tomorrow['date']
            weather = forecast_tomorrow['day']['condition']['text']
            max_temp = forecast_tomorrow['day']['maxtemp_c']
            min_temp = forecast_tomorrow['day']['mintemp_c']
            return {
                'date': date,
                'weather': weather,
                'max_temp': max_temp,
                'min_temp': min_temp
            }
        else:
            return None

if __name__ == "__main__":
    rc = RestClient()
    API_KEY = "b858a49ec6a44b7db57201600241403"
    city = "Białystok, PL"
    x = rc.get_forecast(API_KEY, city)
    print(x)
