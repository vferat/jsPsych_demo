import requests
import base64
import json

from flask import Flask, request, redirect, g, render_template, url_for
import requests

# Authentication Steps, parameters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


app = Flask(__name__)

#  Client Keys
CLIENT_ID = "afd131ec748441ffb78d52369c99571d"
with open('../client_secret.txt') as f:
    CLIENT_SECRET = f.readline()
    print(CLIENT_SECRET)

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-read-collaborative user-read-recently-played playlist-read-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


def get_access_token_from_code(code):
    url = 'https://accounts.spotify.com/api/token'

    auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'}

    data = {
        'code': code,
        'redirect_uri': auth_query_parameters['redirect_uri'],
        'grant_type': 'authorization_code'}

    x = requests.post(url, headers=headers, data=data)
    response = json.loads(x.text)
    print(response)
    access_token = response['access_token']
    return access_token

@app.route("/")
def index():
    # Auth Step 1: Authorization
    url = 'https://accounts.spotify.com/authorize'
    url += '?response_type='  + auth_query_parameters['response_type']
    url += '&client_id=' + CLIENT_ID
    url += '&scope=' + auth_query_parameters['scope']
    url += '&redirect_uri=' + auth_query_parameters['redirect_uri']
    return redirect(url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    code = request.args['code']
    access_token = get_access_token_from_code(code)
    print(access_token)
    return redirect(url_for('experiment'))


@app.route("/experiment")
def experiment():
    return render_template('experiment.html')


if __name__ == "__main__":
    app.run(port=PORT)