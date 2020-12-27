from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__)

"""
using mysql connector we can connect to our mysql server and use queries to fetch data from DB
"""

#when we run server.py locally

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
    query = request.args.get('query')
    cur = mysql.cursor()
    mysql_query = f"SELECT * FROM avengers WHERE Title LIKE '%{query}%'"
    cur.execute(mysql_query)
    rows_num = len(cur.fetchall())
    return render_template('searchResults.html', count=rows_num, query=query)

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port="40707", debug=True)

