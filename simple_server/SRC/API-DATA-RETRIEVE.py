import os
import requests
import pathlib


def getDatabyId(id):
    ### Should subsribe to
    # https: // rapidapi.com / rapidapi / api / movie - database - imdb - alternative
    ## to register, even for free acount, a credit card is required

    url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
    querystring = {"i": id, "r": "json"}
    headers = {
        'x-rapidapi-key': "427cbf98cdmsh2eb8ba5a0d9cd7ap1d6ac0jsn6578fd5b7a59",
        'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    ###########################################################################
    pathlib.Path("./jsons" + id + ".json").write_bytes(response.content)  ## SAVE FILE


def loadId():
    pathName = "2021 Movies.txt"  ##set to file with IMDB's IDs
    n = len(open(pathName).readlines())
    print(n)
    with open(pathName) as file_in:

        for i, line in enumerate(file_in):
            if i < 100:  ## above 1000 it COST MONEY
                line = line.strip('\n')
                getDatabyId(line)
                if i % 50 == 0:
                    k = i / n * 100
                    print(format(k, ".2f"), "%")


os.mkdir("./jsons") ## /  signs are for linux
loadId()

with open('BreakJsonToAllTables.py') as infile:
    exec(infile.read())

with open('push_tabel.py') as infile:
    exec(infile.read())
