import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URL = 'https://api.netatmo.com/oauth2/token'


def read_netatmo_token():
    with open('token.json', 'r') as file:
        token_data = json.load(file)

    return token_data


def refresh_netatmo_token(token_data):
    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': token_data['refresh_token']
        }
    )

    token_data = token_response.json()

    with open('token.json', 'w') as file:
        json.dump(token_data, file)

    return token_data


def get_station_data():

    def get_data(token_data):
        headers = {
            'Authorization': f"Bearer {token_data['access_token']}"
        }
        return requests.get('https://api.netatmo.com/api/getstationsdata', headers = headers)

    token_data = read_netatmo_token()
    response = get_data(token_data)

    # if token expired refresh token
    if response.status_code == 401:
        token_data = refresh_netatmo_token(token_data)
        response = get_data(token_data)

    devices = response.json()['body']['devices']

    dashboard_data = []

    for device in devices:
        dashboard_data.append(extract_module_data(device))

        for module in device['modules']:
            dashboard_data.append(extract_module_data(module))

    return dashboard_data


def extract_module_data(module_data):
    return {
        'module_name': module_data['module_name'],
        'temperature': module_data['dashboard_data']['Temperature'],
        'humidity': module_data['dashboard_data']['Humidity'],
        'co2': module_data['dashboard_data'].get('CO2', None),
        'pressure': module_data['dashboard_data'].get('Pressure', None),
        'temp_trend': module_data['dashboard_data']['temp_trend'],
        'pressure_trend': module_data['dashboard_data'].get('pressure_trend', None),
        'battery_percent': module_data.get('battery_percent', None),
    }


with open('data_netatmo.json', 'w') as file:
    json.dump(get_station_data(), file)
