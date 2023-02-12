import requests
import json

BASE_URL = "https://api.worldoftanks.eu/wot/"

#### CLIENT ID ####
APPLICATION_ID = "118af1166371d9f116a0716673f1fff0"


def refresh_player_access_token(access_token):
    print(access_token)
    url = BASE_URL + "auth/prolongate/"
    data = {
        "application_id": APPLICATION_ID,
        "access_token": access_token
    }
    response = requests.post(url, data=data)
    return json.loads(response.text)


#### SERVER ID ####
APPLICATION_ID = '15191947d83c11a74271bd856dba7496'


def get_tanks():
    url = BASE_URL + "encyclopedia/vehicles/"
    params = {
        "application_id": APPLICATION_ID,
        "language": "en",
        "fields": ','.join([
            'tank_id',
            'name',
            'description',
            'tier',
            'nation',
            'type',
            'is_premium',
            'is_premium_igr',
            'is_gift',
            'is_wheeled',
            'images',
        ]),

    }
    response = requests.get(url, params=params)
    return response.json()
