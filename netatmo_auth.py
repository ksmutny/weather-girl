from flask import Flask, redirect, request, url_for
from dotenv import load_dotenv
import json
import os
import requests
import webbrowser


app = Flask(__name__)
app.secret_key = 'super secret'

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

AUTHORIZATION_BASE_URL = 'https://api.netatmo.com/oauth2/authorize'
REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_URL = 'https://api.netatmo.com/oauth2/token'


@app.route('/')
def index():
    return 'Welcome to the Netatmo Authorization App. <a href="/login">Login</a>'


@app.route('/login')
def login():
    authorization_url = f'{AUTHORIZATION_BASE_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read_station'
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
    )
    token_data = token_response.json()

    # Save token data to a file
    with open('token.json', 'w') as file:
        json.dump(token_data, file)


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(host='0.0.0.0', port=5000)
