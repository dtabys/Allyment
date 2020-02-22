from flask import Flask, request
import sqlite3
import json
from sqlite3 import Error

app = Flask(__name__)

database = sqlite3.connect("data/database.db")
database.row_factory = sqlite3.Row
dbcur = database.cursor()


app = Flask(__name__)

database = sqlite3.connect("data/database.db")
database.row_factory = sqlite3.Row
db_cursor = database.cursor()


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


@app.route("/")
def index():
    response = {"status": "error", "reason": "invalid path"}
    return json.dumps(response)


@app.route("/register", methods=["POST"])
def register():
    response = {}

    if (request.is_json):
        content = request.get_json()
        if(content["username"] and content["password"]):
            # TODO
            pass
        else:
            response["status"] = "error"
            response["reason"] = "missing username or password"
    else:
        response["status"] = "error"
        response["reason"] = "Invalid JSON"

    return json.dumps(response)

@app.route("/login", methods=["POST"])
def login():
    response = {}

    if (request.is_json):
        content = request.get_json()
        if(content["username"] and content["password"]):
            # TODO
            pass
        else:
            response["status"] = "error"
            response["reason"] = "missing username or password"
    else:
        response["status"] = "error"
        response["reason"] = "Invalid JSON"

    return json.dumps(response)


if __name__ == '__main__':
    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            notifications text NOT NULL,
                                            filters text,
                                            posts text,
                                            requests text
                                        ); """

    sql_create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        items text NOT NULL,
                                        location text NOT NULL,
                                        start_time integer NOT NULL,
                                        end_time integer NOT NULL,
                                        contact text NOT NULL,
                                        description text,
                                        logistics text,
                                        tags text,
                                        requests text,
                                        FOREIGN KEY (account_id) REFERENCES accounts (id)
                                    );"""

    sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text,
                                        tags text,
                                        quantity integer NOT NULL,
                                        FOREIGN KEY (posts_id) REFERENCES posts (id),
                                        FOREIGN KEY (account_id) REFERENCES accounts (id)
                                    );"""

    sql_create_requests_table = """CREATE TABLE IF NOT EXISTS requests (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        request_items text NOT NULL,
                                        request_quantity integer NOT NULL,
                                        FOREIGN KEY (posts_id) REFERENCES posts (id),
                                        FOREIGN KEY (account_id) REFERENCES accounts (id)
                                    );"""

    conn = database
    # create tables
    if conn is not None:
        # create tables
        create_table(conn, sql_create_accounts_table)
        create_table(conn, sql_create_posts_table)
        create_table(conn, sql_create_items_table)
        create_table(conn, sql_create_requests_table)
    else:
        print("Error! cannot create the database connection.")

    app.run("127.0.0.1", "8000")
