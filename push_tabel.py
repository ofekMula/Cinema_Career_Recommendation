import mysql.connector
import csv
import json
import pandas as pd
import os
"""
using mysql connector we can connect to our mysql server and use queries to fetch data from DB
"""

#when we run server.py locally
def push_csv_to_table(file_name,mysql_conn,cursor):
    df = pd.read_csv(f"./BreakJsonToAllTables/{file_name}" + ".csv")
    rows_n = len(df)
    for i, row in df.iterrows():
        sql = "INSERT INTO Film_Actors VALUES (%s,%s)"
        cur.execute(sql, tuple(row))
        # the connection is not autocommitted by default, so we
        mysql.commit()
        if i % 1000 == 0:
            print(f"commited {i}/{rows_n}")
    print(f"finished +{file_name}")

if __name__ == '__main__':
    mysql = mysql.connector.connect(
        host="localhost",
        user="DbMysql11",
        password="DbMysql11",
        database="DbMysql11",
        port="3305"
    )
    cur = mysql.cursor()
    push_csv_to_table("Actors.csv")
    push_csv_to_table("Director.csv")
    push_csv_to_table("Film.csv")
    push_csv_to_table("Film_Director.csv")
    push_csv_to_table("Film_Genere.csv")
    push_csv_to_table("Film_Production.csv")
    push_csv_to_table("Film_writer.csv")
    push_csv_to_table("Genre.csv")
    push_csv_to_table("Production.csv")
    push_csv_to_table("Writer.csv")


    print("finished pushing all tables")