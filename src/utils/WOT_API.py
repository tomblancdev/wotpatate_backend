import requests
import json

APPLICATION_ID = "118af1166371d9f116a0716673f1fff0"
BASE_URL = "https://api.worldoftanks.eu/wot/"


def refresh_player_access_token(access_token):
    print(access_token)
    url = BASE_URL + "auth/prolongate/"
    data = {
        "application_id": APPLICATION_ID,
        "access_token": access_token
    }
    response = requests.post(url, data=data)
    return json.loads(response.text)
