from flask import Flask, render_template, request
import mysql.connector
#import mySqlQueries

def findCountry(input):
    cur = mysql.cursor()
    mysql_query = f"DESCRIBE Film"
    cur.execute(mysql_query)
    h = cur.fetchall()
    headers = []
    for col in h:
        headers.append(col[0])
    result = [headers]
    print(headers)
    mysql_query = f"SELECT * FROM Film  WHERE Title LIKE '%{input}%' LIMIT 20 "

    cur.execute(mysql_query)
    result.extend(cur.fetchall())
    return render_template('searchResults.html', data=result)

def findbestProduction():
    cur = mysql.cursor()
    headers = ["amount","Production"]

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

#when we run server_temp.py locally

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
    return findbestProduction()


@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port="40707", debug=True)






