from flask import Flask, Response, jsonify, render_template
from base64 import b64encode

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import requests
import json
import os
import random

# Importação correta do escape
from markupsafe import escape

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

# Definição das URLs da API do Spotify
SPOTIFY_URL_REFRESH_TOKEN = "https://accounts.spotify.com/api/token"
SPOTIFY_URL_NOW_PLAYING = "https://api.spotify.com/v1/me/player/currently-playing"
SPOTIFY_URL_RECENTLY_PLAY = "https://api.spotify.com/v1/me/player/recently-played?limit=10"

# Inicializando o app Flask
app = Flask(__name__)

# Função para criar a autenticação básica
def getAuth():
    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode("ascii")

# Função para renovar o token
def refreshToken():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }

    headers = {"Authorization": f"Basic {getAuth()}"}

    response = requests.post(SPOTIFY_URL_REFRESH_TOKEN, data=data, headers=headers)
    return response.json()["access_token"]

# Função para obter músicas recentemente tocadas
def recentlyPlayed():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(SPOTIFY_URL_RECENTLY_PLAY, headers=headers)

    if response.status_code == 204:
        return {}

    return response.json()

# Função para obter a música que está tocando agora
def nowPlaying():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(SPOTIFY_URL_NOW_PLAYING, headers=headers)

    if response.status_code == 204:
        return {}

    return response.json()

# Função para gerar as barras de progressão
def barGen(barCount):
    barCSS = ""
    left = 1
    for i in range(1, barCount + 1):
        anim = random.randint(1000, 1350)
        barCSS += ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(i, left, anim)
        left += 4

    return barCSS

# Função para carregar a imagem base64 a partir de uma URL
def loadImageB64(url):
    response = requests.get(url)
    return b64encode(response.content).decode("ascii")

# Função para gerar o SVG com as informações da música
def makeSVG(data):
    barCount = 85
    contentBar = "".join(["<div class='bar'></div>" for i in range(barCount)])
    barCSS = barGen(barCount)

    if data == {}:
        content_bar = ""
        recent_plays = recentlyPlayed()
        size_recent_play = len(recent_plays["items"])
        idx = random.randint(0, size_recent_play - 1)
        item = recent_plays["items"][idx]["track"]
    else:
        item = data["item"]

    img = loadImageB64(item["album"]["images"][1]["url"])
    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    songName = item["name"].replace("&", "&amp;")

    dataDict = {
        "content_bar": contentBar,
        "css_bar": barCSS,
        "artist_name": artistName,
        "song_name": songName,
        "img": img,
    }

    return render_template("spotify.html.j2", **dataDict)

# Rota principal do Flask
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    data = nowPlaying()
    svg = makeSVG(data)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp

# Inicializa o app Flask
if __name__ == "__main__":
    app.run(debug=True)
