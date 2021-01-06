import requests
import pathlib
import json
from pathlib import Path

def getDatabyId(id):
    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
    querystring = {"i":id,"r":"json"}
    headers = {
        'x-rapidapi-key': "427cbf98cdmsh2eb8ba5a0d9cd7ap1d6ac0jsn6578fd5b7a59",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
