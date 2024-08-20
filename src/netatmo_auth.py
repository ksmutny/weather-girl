from flask import Flask, redirect, request
import webbrowser

from netatmo_auth_token import authorization_url, get_netatmo_token, save_netatmo_token


app = Flask(__name__)
app.secret_key = 'super secret'

AUTH_APP_HOST = 'localhost'
AUTH_APP_PORT = 5000
AUTH_APP_URL = f'http://{AUTH_APP_HOST}:{AUTH_APP_PORT}'
REDIRECT_URI = f'{AUTH_APP_URL}/callback'


@app.route('/')
def index():
    return 'Welcome to the Netatmo Authorization App. <a href="/login">Login</a>'

@app.route('/login')
def login():
    return redirect(authorization_url(REDIRECT_URI))


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_data = get_netatmo_token(code, REDIRECT_URI)
    save_netatmo_token(token_data)
    return 'Token retrieved and saved. You can close this window.'


if __name__ == '__main__':
    webbrowser.open(AUTH_APP_URL)
    app.run(host=AUTH_APP_HOST, port=AUTH_APP_PORT)
