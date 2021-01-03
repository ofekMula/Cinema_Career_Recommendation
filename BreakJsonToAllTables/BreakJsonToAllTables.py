import csv
import json
import pandas as pd
import os

# DB tables' names apart from Film
Tables = ["Actors", "Director", "Writer", "Production", "Genre"]
# foreign keys for intermediate tables
id_keys = ["Actor_id", "Director_id", "Writer_id", "Production_id", "Genre_id"]
# attributes for main table apart from Film
Tables_attributes = ["id", "fullName"]

# attributes for Film table
film_table_attributes_list = ["Title", "Year", "Runtime", "imdbRating", "Language", "Country"]

# accessing extra data (rating column) from ratings.csv
ratings_df = pd.read_csv("ratings.csv")
fieldnames_ratings = list(ratings_df.columns)
movie_names_ratings = ratings_df[fieldnames_ratings[0]].to_list()


def create_csv_file(file_name, field_names):
    """
    :param file_name: name of csv file
    :param field_names: name of attributes (column names)
    this function opens the file and writes the given column names
    """
    # Open file in append mode
    with open(file_name, 'w', newline='', encoding="utf-8") as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(field_names)


def init_csvs():
    """
    this function creates all the csv files matching to the DB tables
    """
    # create csv for Film:
    index = film_table_attributes_list.index("imdbRating")
    new_key_list = ["id"] + film_table_attributes_list
    new_key_list[index + 1] = "Rating"
    create_csv_file("Film.csv", new_key_list)

    # create csv for other tables
    for table in Tables:
        create_csv_file(table + ".csv", Tables_attributes)

    # create csv for intermediate tables:
    for i in range(len(Tables)):
        create_csv_file("Film_" + Tables[i] + ".csv", ["Film_id", id_keys[i]])


def SaveNamesToALLTables(jsonName):
    """
    :param jsonName: a json file name.
    this function opens the jsonName.json file and load the data in the correct format
    to a dictionary (movieData). we will use the dictionary to insert the data into the correct csv file.
    """
    with open(jsonName + ".json", encoding="utf-8") as f:
        movieData = json.load(f)

        if not (all([key in movieData for key in Tables]) and
                all([key in movieData for key in film_table_attributes_list])):
            # the json file does not contain all the data required
            print("Not inserted: ", jsonName)
            return  # hence, we do not add it to the DB and exit

#       # add more relevant movies
#        year = int(movieData["Year"])
#
#        if year <= 2008:
#            return

        if movieData["imdbRating"] == "N/A":  # no rating in the json file, so we take it from ratings.csv
            if jsonName in movie_names_ratings:  # searching for the current movie in the csv
                index = movie_names_ratings.index(jsonName)
                rating = ratings_df.loc[index].at[fieldnames_ratings[1]]  # get the matching rating
                movieData["imdbRating"] = str(rating)

        film_key = saveToFilmTable("Film", movieData)

        if film_key is not None:
            for tableName in Tables:
                keyList = saveToMainTable(tableName, movieData)  # get key list
                for key in keyList:
                    linkTable = "Film_" + tableName
                    savetoLinkedTable(linkTable, film_key, key)


def saveToMainTable(TableName, movieData):
    """
    :param TableName: a main table name
    :param movieData: a dictionary containing json file data
    :return: this function returns a list of keys of records inserted into TableName.csv.
    """
    csvName = TableName + ".csv"
    movieNames = movieData[TableName].split(",")

    with open(csvName, 'a', newline='', encoding="utf-8") as outfile:
        df = pd.read_csv(TableName + ".csv")
        fieldnames = list(df.columns)

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        DBNames = df[fieldnames[1]].to_list()
        keyList = []

        n = len(DBNames) + 1

        for i in range(len(movieNames)):
            if "(" in movieNames[i]:
                index_parenthesis = movieNames[i].index("(")
                movieNames[i] = movieNames[i][:index_parenthesis - 1]

            movieNames[i] = movieNames[i].strip()  # remove spaces

        movieNames = list(dict.fromkeys(movieNames))  # remove duplicates created from removing the parentheses

        for name in movieNames:

            if name != "N/A":
                if name not in DBNames:
                    key = str(n)
                    keyList.append(n)
                    print(TableName, ":     ", name, ", Key:", key)
                    n = n + 1
                    writer.writerow({fieldnames[0]: key, fieldnames[1]: name})
                else:
                    # we need to retrieve its id and add it to the list
                    index = DBNames.index(name)
                    key = df.loc[index].at[fieldnames[0]]
                    print("key = ", key)
                    # [fieldnames[0]][index + 1]  # plus 1 because of the row of the field_names
                    keyList.append(key)

    return keyList


def savetoLinkedTable(TableName, film_key, key):
    """
    :param TableName: a main table name
    :param film_key: a key in Film.csv
    :param key: a Key in TableName.csv
     the data in the records key and film_key is from the same json file. this function inserts the tuple
     (film_key, key) to the relevant intermediate csv file (Film_TableName.csv).
    """
    if TableName == "Film_Genre":
        print("in Film_Genre")
    csvName = TableName + ".csv"
    f = open(csvName, 'r')
    reader = csv.reader(f)
    fieldnames = next(reader)

    with open(csvName, 'a', newline='', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        print(TableName, ":     " + str(film_key), "<->", str(key))
        writer.writerow({fieldnames[0]: film_key, fieldnames[1]: key})


def saveToFilmTable(table_name, movie_data):
    """
    :param table_name: the name of the table to insert the record
    :param movie_data: the dictionary retrieved from json file
    :return: the key of the inserted movie a a string if inserted and None if not inserted.
    """
    # film_keys_list = ["Title", "Year", "Runtime", "imdbRating", "Awards"]
    film_data_dict = dict()
    csvName = table_name + ".csv"

    with open(csvName, 'a', newline='', encoding="utf-8") as outfile:
        df = pd.read_csv(csvName)

        fieldnames = list(df.columns)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        DBNames = df[fieldnames[1]].to_list()  # the names of the movies in the DB already

        n = len(DBNames) + 1

        movie_key = str(n)

        name_movie = movie_data["Title"]

        if name_movie not in DBNames:  # insert only if not already in the DB
            # create the record for the movie
            film_data_dict[fieldnames[0]] = movie_key
            for i in range(1, len(fieldnames)):
                key = fieldnames[i]
                if key == "Rating":
                    new_key = "imdb" + key  # the key in the json is imdbRating
                    value = movie_data[new_key]
                else:
                    value = movie_data[key]
                if value == "N/A":
                    value = ""
                film_data_dict[key] = value

            writer.writerow(film_data_dict)

            return movie_key

    return None


def run_over_jsons(path, to_init):
    """
    :param to_init: boolean telling if to init the tables or not.
    :param path: of a directory containing only json files
    This method runs over all jsons and inserts them to the tables.
    """

    if to_init:
        init_csvs()

    for json_file_name in os.listdir(path):
        json_file_name = json_file_name[:len(json_file_name) - len(".json")]  # remove the .json suffix
        SaveNamesToALLTables(path + "\\" + json_file_name)


path = "C:\\Users\\DinPC\\PycharmProjects\\db_project\\BreakJsonToAllTables\\jsons"

run_over_jsons(path, True)

# path_new_movies = "C:\\Users\\DinPC\\PycharmProjects\\db_project\\BreakJsonToAllTables\\jsons3"
# run_over_jsons(path_new_movies, False)




