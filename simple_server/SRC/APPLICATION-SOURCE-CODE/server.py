from flask import Flask, render_template, request
import mysql.connector


# import mySqlQueries

def findCountry(input):
    cur = mysql.cursor()
    # mysql_query = f"DESCRIBE Film"
    # cur.execute(mysql_query)
    headers = [f"number of films in {input} is: "]
    result = [headers]
    print(headers)
    mysql_query = f"SELECT  sum(c.count)  as films_in_country FROM" \
                  f"( SELECT Country,COUNT(*) as count FROM Film  WHERE Country LIKE '%{input}%'" \
                  f"GROUP BY Country order by count desc) as c"

    cur.execute(mysql_query)
    ft = cur.fetchall()
    print(ft)
    if ft[0][0] == None:
        ft[0] = (0,)
    result.extend(ft)
    return render_template('searchResults.html', data=result)


def findbestProduction():
    cur = mysql.cursor()
    headers = ["amount", "Production"]

    result = [headers]
    print(headers)
    mysql_query = f"SELECT  count(f.id) as film_amount , p.fullName FROM Film as f, Production as p , Film_Production as fp where (f.id=fp.film_id) and  (fp.Production_id=p.id) and f.rating>=7 GROUP BY  p.fullName ORDER BY film_amount DESC LIMIT 20 "

    cur.execute(mysql_query)
    result.extend(cur.fetchall())
    return render_template('searchResults.html', data=result)


app = Flask(__name__)

"""
using mysql connector we can connect to our mysql server and use queries to fetch data from DB
"""

# when we run server.py locally

mysql = mysql.connector.connect(
    host="localhost",
    user="DbMysql11",
    password="DbMysql11",
    database="DbMysql11",
    port="3305"
)


# when we run server on the nova: delta-tomcat-vm

# mysql = mysql.connector.connect(
#   host="mysqlsrv1.cs.tau.ac.il",
#   user="DbMysql11",
#   password="DbMysql11",
#   database="DbMysql11",
# )
@app.route('/search')
def search_return_html():
    input = request.args.get('query')
    # return findbestProduction()
    return findCountry(input)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/Film_queries.html')
def films():
    return render_template('Film_queries.html')


@app.route('/Actor_queries.html')
def actors():
    return render_template('Actor_queries.html')


@app.route('/Directors_queries.html')
def directors():
    return render_template('Directors_queries.html')


@app.route('/Producer_queries.html')
def producer():
    return render_template('Producer_queries.html')


def run_query_1(input):
    cur = mysql.cursor()
    headers = ["amount", "Production"]

    result = [headers]
    print(headers)
    mysql_query = f"SELECT  count(f.id) as film_amount , p.fullName FROM Film as f, Production as p , Film_Production as fp where (f.id=fp.film_id) and  (fp.Production_id=p.id) and f.rating>=7 GROUP BY  p.fullName ORDER BY film_amount DESC LIMIT 20 "

    cur.execute(mysql_query)
    result.extend(cur.fetchall())
    return render_template('searchResults.html', data=result)


def run_query_2(input):
    pass


def run_query_3(input):
    pass


def run_query_4():
    cur = mysql.cursor()

    mysql_query = f"SELECT  DISTINCT a.fullName as name,count(g.fullName) as count \
FROM Actors as a, Genre as g,Film_Actors as fa, Film_Genre as fg \
Where a.id =fa.Actor_id and g.id = fg.Genre_id and fa.Film_id = fg.Film_id \
Group BY a.fullname \
ORDER BY count DESC \
LIMIT 20"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


# This query returns 100 actors that worked with the required director.
def run_query_5(input):
    cur = mysql.cursor()

    mysql_query = f"SELECT a.fullName as Actors\
                  FROM Director d, Actors a, Film f, Film_Director fd, Film_Actors fa\
                  WHERE MATCH(d.fullName) AGAINST({input}) and\
                  f.id = fa.Film_id and\
                  f.id = fd.Film_id and\
                  d.id = fd.Director_id and\
                  a.id = fa.Actor_id\
                  LIMIT 100;"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


def run_query_6(input):
    cur = mysql.cursor()

    mysql_query = f"SELECT f.Title, f.Rating\
                  FROM Director d, Film f, Film_Director fd\
                  WHERE f.id = fd.Film_id AND\
	              d.id = fd.Director_id AND\
                  MATCH(d.fullName) AGAINST({input})\
                  ORDER BY f.Rating DESC\
                  LIMIT 100;"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


def run_query_7(input):
    cur = mysql.cursor()

    mysql_query = f"CREATE VIEW IF NOT EXISTS Director_And_Num_Films_{input} AS\
                SELECT d2.id, d2.fullName, COUNT(f.id) AS num_of_films\
                FROM Director d2, Film f, Film_Director fd, Genre g, Film_Genre fg\
                WHERE d2.id = fd.Director_id AND\
	            f.id = fd.Film_id AND\
	            f.id = fg.Film_id AND\
	            g.id = fg.Genre_id AND\
	            g.fullName = {input}\
                GROUP BY d2.id, d2.fullName;\
                SELECT Director_And_Num_Films.fullName\
                FROM Director_And_Num_Films\
                WHERE Director_And_Num_Films.num_of_films > 10\
                ORDER BY Director_And_Num_Films.num_of_films DESC\
                LIMIT 100;"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


def run_query_8(input):
    cur = mysql.cursor()

    mysql_query = f"CREATE OR REPLACE VIEW films_rating AS\
                SELECT f.id, f.Rating\
                FROM Film f, Genre g, Film_Genre fg\
                WHERE f.id = fg.Film_id and\
                fg.Genre_id = g.id and\
                g.fullName = {input[0]} and\
                f.Rating > {input[1]}\
                ORDER BY f.Rating DESC;\
                SELECT w.fullName, COUNT(fr.id) AS num_best_films\
                FROM Writer w, films_rating fr, Film_Writer fw\
                WHERE w.id = fw.Writer_id and\
                fr.id = fw.Film_id\
                GROUP BY w.id, w.fullName\
                ORDER BY num_best_films DESC\
                LIMIT 100;"

    cur.execute(mysql_query)
    result = cur.fetchall()

    return render_template('searchResults.html', data=result)


@app.route('/query1')
def query_1():
    input = request.args.get('query')
    return run_query_1(input)


@app.route('/query2')
def query_2():
    input = request.args.get('query')
    return run_query_2(input)


@app.route('/query3')
def query_3():
    input = request.args.get('query')
    return run_query_3(input)


@app.route('/query4')
def query_4():
    return run_query_4()


@app.route('/query5')
def query_5():
    input = request.args.get('query')
    return run_query_5(input)


@app.route('/query6')
def query_6():
    input = request.args.get('query')
    return run_query_6(input)


@app.route('/query7')
def query_7():
    input = request.args.get('query')
    return run_query_7(input)


@app.route('/query8')
def query_8():
    input = request.args.get('query')
    input_arr = input.split(',')
    input_arr = [s.strip() for s in input_arr]
    return run_query_8(input_arr)


if __name__ == '__main__':
    app.run(port="8888", debug=True)
    # app.run(port="40707", debug=True,host='delta-tomcat- - when running on delta tomcat server.
