import json
from csv import *

# no nominations
film_keys_list = ["Title", "Year", "Runtime", "imdbRating", "Awards"]
genre_keys_list = ["Genre"]
# first and last name
director_keys_list = ["Director"]
language_keys_list = ["Language"]
writer_keys_list = ["Writer"]
actors_keys_list = ["Actors"]

tables_list = [film_keys_list, genre_keys_list, director_keys_list, language_keys_list, writer_keys_list,
               actors_keys_list]
csv_list = [film_keys_list, genre_keys_list, ["First_Name", "Last_Name"],
            language_keys_list, ["First_Name", "Last_Name"], ["First_Name", "Last_Name"]]
dict_list = [dict() for i in range(len(tables_list))]
csv_file_name_list = ["Film.csv", "Genre.csv", "Director.csv", "Language.csv", "Writer.csv", "Actors.csv"]


def create_csv_file(file_name, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(field_names)


def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='', encoding='utf-8') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


def init_csvs():
    for i in range(len(csv_list)):
        create_csv_file(csv_file_name_list[i], csv_list[i])


def read_json():
    # Opening JSON file
    f = open('../BreakJsonToAllTables/tt10137486.json', encoding="utf-8")
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    keys = data.keys()
    for key in keys:
        for i in range(len(tables_list)):
            if key in tables_list[i]:
                # Need to fix
                if data[key] == "N/A":
                    data[key] = ""
                dict_list[i][key] = data[key]

    for i in range(len(dict_list)):
        key = tables_list[i]
        if tables_list[i] in [director_keys_list, writer_keys_list, actors_keys_list]:
            name_lst = dict_list[i][key[0]].split(", ")
            d = dict()
            for name in name_lst:
                d["First_Name"] = ""
                d["Last_Name"] = ""
                lst = name.split()
                if len(lst) > 0:
                    d["First_Name"] = lst[0]
                if len(lst) > 1:
                    d["Last_Name"] = " ".join(lst[1:])
                append_dict_as_row(csv_file_name_list[i], d, csv_list[i])
        else:
            append_dict_as_row(csv_file_name_list[i], dict_list[i], csv_list[i])
    f.close()


init_csvs()
read_json()

