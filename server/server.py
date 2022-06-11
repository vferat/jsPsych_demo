import json
from flask import Flask, request, redirect, g, render_template, url_for
import requests
from urllib.parse import quote

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.


app = Flask(__name__)

#  Client Keys
CLIENT_ID = "afd131ec748441ffb78d52369c99571d"
CLIENT_SECRET = ""

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
SCOPE = "playlist-modify-public playlist-modify-private"
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


@app.route("/")

def index():
    # Auth Step 1: Authorization
    url = 'https://accounts.spotify.com/authorize'
    url += '?response_type='  + auth_query_parameters['response_type']
    url += '&client_id=' + CLIENT_ID
    url += '&scope=' + auth_query_parameters['scope']
    url += '&redirect_uri=' + auth_query_parameters['redirect_uri']
    print(url)
    return redirect(url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    print(auth_token)
    return redirect(url_for('experiment'))


@app.route("/experiment")
def experiment():
    return render_template('experiment.html')


if __name__ == "__main__":
    app.run(port=PORT)