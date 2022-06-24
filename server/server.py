import os

import psycopg2
from flask import Flask
from psycopg2.extensions import AsIs

DATABASE_HOST = os.environ.get("DB_HOST")
DATABASE_PORT = os.environ.get("DB_PORT")
DATABASE_USER = os.environ.get("DB_USER")
DATABASE_PASSWORD = os.environ.get("DB_PASSWORD")
DATABASE_NAME = os.environ.get("DB_NAME")

TABLE_NAME = "TestTable"


conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    host=DATABASE_HOST,
    password=DATABASE_PASSWORD,
    port=DATABASE_PORT
)

with conn, conn.cursor() as cur:
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (TABLE_NAME,))
    data = cur.fetchone()[0]
    if data is None:
        cur.execute("CREATE TABLE %s (user_name varchar PRIMARY KEY, user_data varchar);", (AsIs(TABLE_NAME),))
    
app = Flask(__name__)

@app.route("/home")
def home():
    return "Hello!"

@app.route("/home/<user_name>")
def get_user(user_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s WHERE user_name = %s;", (AsIs(TABLE_NAME), user_name, ))
    data = cur.fetchone()
    cur.close()
    ret_val = str(data) if data is not None else f'User {user_name} does not exist.'
    return ret_val

@app.route("/home/post/<user_name>/<user_data>")
def post_user(user_name, user_data):
    with conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM %s WHERE user_name = %s;", (AsIs(TABLE_NAME), user_name, ))
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO %s (user_name, user_data) VALUES (%s, %s);", (AsIs(TABLE_NAME), user_name, user_data))
        else:
            cur.execute("UPDATE %s SET user_data = %s WHERE user_name = %s;", (AsIs(TABLE_NAME), user_data, user_name))
    return "Data saved successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    conn.close()
    
