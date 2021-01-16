import csv
import json
import pandas as pd
import os

# DB tables' names apart from Film
Tables = ["Actor", "Director", "Writer", "Production", "Genre"]
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


def init_csvs(film_file_name, csvs_names):
    """
    :param csvs_names: names of files to build
    :param film_file_name: name of the file related to film table
    this function creates all the csv files matching to the DB tables
    """
    # create csv for Film:
    index = film_table_attributes_list.index("imdbRating")
    new_key_list = ["id"] + film_table_attributes_list
    new_key_list[index + 1] = "Rating"
    create_csv_file(film_file_name + ".csv", new_key_list)

    # create csv for other tables
    for file in csvs_names:
        create_csv_file(file + ".csv", Tables_attributes)

    # create csv for intermediate tables:
    for i in range(len(csvs_names)):
        create_csv_file("Film_" + csvs_names[i] + ".csv", ["Film_id", id_keys[i]])


def SaveNamesToALLTables(jsonName, year_to_screen, is_over_year, film_file_name,
                         csvs_names, curr_last_key, number_insertion):
    """
    :param number_insertion: the sequence number of the current insertion
    :param curr_last_key: a dictionary containing mapping between
    csvs_names and film_file_name to the last key in the table.
    :param csvs_names: names of files to build
    :param film_file_name: name of the file related to film table
    :param is_over_year: boolean telling us if to screen according to year.
    :param year_to_screen: the year to screen.
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

        if is_over_year:
            # add more relevant movies
            year = int(movieData["Year"])

            if year <= year_to_screen:
                return

        if movieData["imdbRating"] == "N/A":  # no rating in the json file, so we take it from ratings.csv
            if jsonName in movie_names_ratings:  # searching for the current movie in the csv
                index = movie_names_ratings.index(jsonName)
                rating = ratings_df.loc[index].at[fieldnames_ratings[1]]  # get the matching rating
                movieData["imdbRating"] = str(rating)

        film_key = saveToFilmTable(film_file_name, movieData, curr_last_key[film_file_name], number_insertion)

        if film_key is not None:
            for tableName in csvs_names:
                keyList = saveToMainTable(tableName, movieData, curr_last_key[tableName], number_insertion)  # get key list
                for key in keyList:
                    linkTable = "Film_" + tableName
                    savetoLinkedTable(linkTable, film_key, key)


def saveToMainTable(TableName, movieData, last_key, number_insertion):
    """
    :param number_insertion: the sequence number of the current insertion
    :param last_key: the last key inserted
    :param TableName: a main table name
    :param movieData: a dictionary containing json file data
    :return: this function returns a list of keys of records inserted into TableName.csv.
    """
    origin_table = TableName[:len(TableName) - len(number_insertion)]
    csvName = TableName + ".csv"
    movieNames = movieData[origin_table].split(",")

    with open(csvName, 'a', newline='', encoding="utf-8") as outfile:
        df = pd.read_csv(TableName + ".csv")
        fieldnames = list(df.columns)

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        DBNames = df[fieldnames[1]].to_list()
        keyList = []

        n = len(DBNames) + 1 + last_key

        for i in range(len(movieNames)):
            if "(" in movieNames[i]:
                index_parenthesis = movieNames[i].index("(")
                movieNames[i] = movieNames[i][:index_parenthesis - 1]

            movieNames[i] = movieNames[i].strip()  # remove spaces

        movieNames = list(dict.fromkeys(movieNames))  # remove duplicates created from removing the parentheses

        if number_insertion == "":
            number_insertion = "0"

        for name in movieNames:

            if name != "N/A":
                in_previous = False
                for k in range(int(number_insertion) + 1):
                    if k == 0:
                        csvName_previous = origin_table + ".csv"
                    else:
                        csvName_previous = origin_table + str(k) + ".csv"
                    df_previous = pd.read_csv(csvName_previous)
                    fieldnames_previous = list(df.columns)
                    DBNames_previous = df_previous[fieldnames_previous[1]].to_list()
                    # the names of the movies in the DB already
                    if name in DBNames_previous:
                        # we need to retrieve its id and add it to the list
                        index = DBNames_previous.index(name)
                        key = df_previous.loc[index].at[fieldnames[0]]
                        print("key = ", key)
                        # [fieldnames[0]][index + 1]  # plus 1 because of the row of the field_names
                        keyList.append(key)
                        in_previous = True
                        break

                if not in_previous:
                    key = str(n)
                    keyList.append(n)
                    print(TableName, ":     ", name, ", Key:", key)
                    n = n + 1
                    writer.writerow({fieldnames[0]: key, fieldnames[1]: name})

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


def saveToFilmTable(table_name, movie_data, last_key, number_insertion):
    """
    :param number_insertion: the sequence number of the current insertion
    :param last_key: the last key inserted
    :param table_name: the name of the table to insert the record
    :param movie_data: the dictionary retrieved from json file
    :return: the key of the inserted movie a a string if inserted and None if not inserted.
    """

    film_data_dict = dict()
    csvName = table_name + ".csv"

    with open(csvName, 'a', newline='', encoding="utf-8") as outfile:
        df = pd.read_csv(csvName)

        fieldnames = list(df.columns)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        DBNames = df[fieldnames[1]].to_list()  # the names of the movies in the DB already

        n = len(DBNames) + 1 + last_key

        movie_key = str(n)

        name_movie = movie_data["Title"]

        if number_insertion == "":
            number_insertion = "0"

        for k in range(int(number_insertion) + 1):
            if k == 0:
                csvName_previous = "Film.csv"
            else:
                csvName_previous = "Film" + str(k) + ".csv"
            df_previous = pd.read_csv(csvName_previous)
            fieldnames_previous = list(df.columns)
            DBNames_previous = df_previous[fieldnames_previous[1]].to_list()
            # the names of the movies in the DB already
            if name_movie in DBNames_previous:
                return None

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


def run_over_jsons(path, to_init, film_file_name, csvs_names,
                   year_to_screen, is_over_year, curr_last_key, number_insertion):
    """
    :param number_insertion: the sequence number of the current insertion
    :param curr_last_key: a dictionary containing mapping between
    csvs_names and film_file_name to the last key in the table.
    :param is_over_year: boolean telling us if to screen according to year.
    :param year_to_screen: the year to screen.
    :param csvs_names: names of files to build
    :param film_file_name: name of the file related to film table
    :param to_init: boolean telling if to init the tables or not.
    :param path: of a directory containing only json files
    This method runs over all jsons and inserts them to the tables.
    """

    if to_init:
        init_csvs(film_file_name, csvs_names)

    for json_file_name in os.listdir(path):
        json_file_name = json_file_name[:len(json_file_name) - len(".json")]  # remove the .json suffix
        SaveNamesToALLTables(path + "\\" + json_file_name, year_to_screen, is_over_year,
                             film_file_name, csvs_names, curr_last_key, number_insertion)


curr_last_key_tables = dict()
for table in Tables:
    curr_last_key_tables[table] = 0
curr_last_key_tables["Film"] = 0

path = "./jsons"

run_over_jsons(path, True, "Film", Tables, None, False, curr_last_key_tables, number_insertion="")

# path_new_movies = "C:\\Users\\DinPC\\PycharmProjects\\db_project\\BreakJsonToAllTables\\jsons3"
# run_over_jsons(path_new_movies, False, "Film", Tables, 2008, True, curr_last_key_tables, number_insertion="")
#
# path = "C:\\Users\\DinPC\\PycharmProjects\\db_project\\BreakJsonToAllTables\\jsons4"
#
# new_Tables = [table + "1" for table in Tables]
#
# curr_last_key_tables = dict()
# for i in range(len(Tables)):
#     csv_name = Tables[i] + ".csv"
#     df = pd.read_csv(csv_name)
#     fieldnames = list(df.columns)
#     DBNames = df[fieldnames[1]].to_list()  # the names of the movies in the DB already
#     curr_last_key_tables[new_Tables[i]] = len(DBNames)
#
# csv_name = "Film.csv"
# df = pd.read_csv(csv_name)
# fieldnames = list(df.columns)
# DBNames = df[fieldnames[1]].to_list()  # the names of the movies in the DB already
# curr_last_key_tables["Film1"] = len(DBNames)
#
# run_over_jsons(path, to_init=True, film_file_name="Film1", csvs_names=new_Tables,
#                year_to_screen=2004, is_over_year=True, curr_last_key=curr_last_key_tables, number_insertion="1")





