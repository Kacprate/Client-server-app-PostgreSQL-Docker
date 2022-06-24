import os

import psycopg2
from flask import Flask


DATABASE_HOST = os.environ.get("DB_HOST")
DATABASE_PORT = os.environ.get("DB_PORT")
DATABASE_USER = os.environ.get("DB_USER")
DATABASE_PASSWORD = os.environ.get("DB_PASSWORD")
DATABASE_NAME = os.environ.get("DB_NAME")


conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    host=DATABASE_HOST,
    password=DATABASE_PASSWORD,
    port=DATABASE_PORT
)

cur = conn.cursor()
cur.execute("CREATE TABLE test (user_name varchar PRIMARY KEY, user_data varchar);")
cur.close()

app = Flask(__name__)

@app.route("/home")
def home():
    return "Hello!"

@app.route("/home/<user_name>")
def get_user(user_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM test WHERE user_name = %s;", (user_name, ))
    data = cur.fetchone()
    cur.close()
    ret_val = str(data) if data is not None else f'User {user_name} does not exist.'
    return ret_val

@app.route("/home/post/<user_name>/<user_data>")
def post_user(user_name, user_data):
    cur = conn.cursor()
    cur.execute("SELECT * FROM test WHERE user_name = %s;", (user_name, ))
    data = cur.fetchone()
    if data is None:
        cur.execute("INSERT INTO test (user_name, user_data) VALUES (%s, %s);", (user_name, user_data))
    else:
        cur.execute("UPDATE test SET user_data = %s WHERE user_name = %s;", (user_data, user_name))
    cur.close()
    return "Data saved successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    conn.close()
    
