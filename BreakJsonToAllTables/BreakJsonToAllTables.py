import csv
import json
import pandas as pd

def SaveNamesToALLTables(jsonName):
    with open(jsonName+'.json') as f:
        movieData = json.load(f)
        Tables = ["Actors","Director","Writer","Production","Genere"]
        ## film_key =   function din and matan
        film_key=4 #DELETE

        for tableName in Tables:

             keyList = saveToMainTable(tableName, movieData) ## get key list
             for key in keyList:
                linkTable = "Film_"+tableName
                savetoLinkedTable(linkTable,film_key,key)
    f.close()


def  saveToMainTable(TableName, movieData):
    csvName = TableName + ".csv"
    movieNames = movieData[TableName].split(",")

    with open(csvName , 'a', newline='') as outfile:
        df = pd.read_csv(TableName + ".csv")
        fieldnames = list(df.columns)

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        DBNames =  df[fieldnames[1]].to_list()
        keyList =[]

        n= len(DBNames)+1

        for name in movieNames:

            if name == "N/A":
                name ="    "
            name= name.strip()  ##remove spaces
            if name not in DBNames:
                key =str(n)
                keyList.append(n)
                print(TableName,":     " , name, ", Key:", key)
                n=n+1
                writer.writerow({fieldnames[0]: key, fieldnames[1]: name})



        outfile.close()
        return keyList

def  savetoLinkedTable(TableName,film_key,key):
    csvName = TableName+".csv"
    f = open(csvName, 'r')
    reader = csv.reader(f)
    fieldnames = next(reader)


    with open(csvName , 'a', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        print(TableName,":     "+str(film_key), "<->", str(key))
        writer.writerow({fieldnames[0]: film_key, fieldnames[1]: key})
        outfile.close()


jsonName = "tt0459113"
SaveNamesToALLTables(jsonName)
