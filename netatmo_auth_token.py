from dotenv import load_dotenv
import json
import os
import requests


load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URL = 'https://api.netatmo.com/oauth2/token'
AUTHORIZATION_BASE_URL = 'https://api.netatmo.com/oauth2/authorize'


def authorization_url(redirect_uri):
    return f'{AUTHORIZATION_BASE_URL}?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&scope=read_station'


def read_netatmo_token():
    with open('token.json', 'r') as file:
        return json.load(file)


def save_netatmo_token(token_data):
    with open('token.json', 'w') as file:
        json.dump(token_data, file)


def get_netatmo_token(authorization_code, redirect_uri):
    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': authorization_code,
            'redirect_uri': redirect_uri
        }
    )
    return token_response.json()


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

    return token_response.json()
