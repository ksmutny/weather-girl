from flask import Flask, redirect, request
import webbrowser

from netatmo_auth_token import AUTHORIZATION_URL, get_netatmo_token, save_netatmo_token


app = Flask(__name__)
app.secret_key = 'super secret'


@app.route('/')
def index():
    return 'Welcome to the Netatmo Authorization App. <a href="/login">Login</a>'

@app.route('/login')
def login():
    return redirect(AUTHORIZATION_URL)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_data = get_netatmo_token(code)
    save_netatmo_token(token_data)
    return 'Token retrieved and saved. You can close this window.'


if __name__ == '__main__':
    webbrowser.open('http://localhost:5000')
    app.run(host='0.0.0.0', port=5000)
