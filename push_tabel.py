import mysql.connector
import csv
import json
import pandas as pd
import os

"""
using mysql connector we can connect to our mysql server and use queries to fetch data from DB
"""


# when we run server.py locally
def push_csv_to_table(file_name, mysql_conn, cursor):
    """
    :param file_name: a csv file name
    :param mysql_conn: mysql connector, connected to the server
    :param cursor: cursor, matching to mysql_conn
    :return:
    """
    df = pd.read_csv(f"./BreakJsonToAllTables/{file_name}" + ".csv")
    if file_name == "Film":
        df['Title'].fillna("No Title",inplace =True)
        df['Year'].fillna(-1,inplace=True)
        df['Runtime'].fillna("No Runtime",inplace=True)
        df['Rating'].fillna(df['Rating'].mean(),inplace=True)
        df['Language'].fillna("No Language",inplace=True)
        df['Country'].fillna("No Country",inplace=True)

    rows_n = len(df)
    print(f"starting pushing csv: {file_name}")

    for i, row in df.iterrows():
        if file_name == "Film":
            sql = f"INSERT IGNORE INTO {file_name} VALUES (%s,%s,%s,%s,%s,%s,%s)"
        else:
            sql = f"INSERT IGNORE INTO {file_name} VALUES (%s,%s)"
        cursor.execute(sql, tuple(row))
        # the connection is not autocommitted by default, so we
        mysql_conn.commit()
        if i % 1000 == 0:
            print(f"commited {i}/{rows_n}")
    print(f"finished {file_name} table")


if __name__ == '__main__':
    mysql = mysql.connector.connect(
        host="localhost",
        user="DbMysql11",
        password="DbMysql11",
        database="DbMysql11",
        port="3305"
    )
    cur = mysql.cursor()
    push_csv_to_table("Film", mysql, cur)
    push_csv_to_table("Production",mysql,cur)
    push_csv_to_table("Actors", mysql, cur)
    push_csv_to_table("Director", mysql, cur)
    push_csv_to_table("Film_Director", mysql, cur)
    push_csv_to_table("Genre", mysql, cur)
    push_csv_to_table("Writer", mysql, cur)
    push_csv_to_table("Film_Genre", mysql, cur)
    push_csv_to_table("Film_Production", mysql, cur)
    push_csv_to_table("Film_Writer", mysql, cur)
    push_csv_to_table("Film_Actors", mysql, cur)

    print("finished pushing all tables")
