from flask import Flask, request, session
import sqlite3
import random
import string
from sqlite3 import Error
import json
from database import init_tables, check_login

app = Flask(__name__)

database = sqlite3.connect("data/database.db")
database.row_factory = sqlite3.Row

SESSION_TYPE = 'memcached'
app.secret_key = "TEST SECRET KEY CHANGE BEFORE DEPLOYMENT"
#session.init_app(app)

@app.route("/")
def index():
    response = {"status": "error", "reason": "invalid path"}
    return json.dumps(response)


@app.route("/register", methods=["POST"])
def register():
    response = {}

    if (request.is_json):
        content = request.get_json()
        if (content["username"] and content["password"]):
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
    with sqlite3.connect("data/database.db") as database:
        response = {}
        cursor = database.cursor()
        session.clear()

        if (request.is_json):
            content = request.get_json()
            if (content["username"] and content["password"]):
                accountId = check_login(cursor, content["username"], content["password"])
                if(accountId is None):
                    response["status"] = "unauthorized"
                    response["reason"] = "username or password incorrect"
                else:
                    session["loggedin"] = True
                    session["accId"] = accountId
                    session["username"] = username
            else:
                response["status"] = "error"
                response["reason"] = "missing username or password"
        else:
            response["status"] = "error"
            response["reason"] = "Invalid JSON"

        database.commit()
        cursor.close()
        return json.dumps(response)


if __name__ == '__main__':
    with sqlite3.connect("data/database.db") as database:
        dbcur = database.cursor()
        init_tables(dbcur)
        database.commit()
        dbcur.close()
        database.close()
        app.run("127.0.0.1", "8000")
