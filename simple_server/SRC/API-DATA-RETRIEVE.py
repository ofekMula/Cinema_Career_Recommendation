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
    ###########################################################################
    pathlib.Path(id+".json").write_bytes(response.content) ## SAVE FILE





def loadId():
    pathName = "2021 Movies.txt" ##set to file with IMDB's IDs
    n = len(open(pathName).readlines(  ))
    print(n)
    with open(pathName) as file_in:

        for i,line in enumerate(file_in):
            if i>-1: ## used to load in batches
                line = line.strip('\n')
                getDatabyId(line)
                if i%50==0:
                    k =i/n*100
                    print(format(k, ".2f"),"%")




loadId()

