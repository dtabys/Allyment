from flask import Flask, request, session
import sqlite3
from sqlite3 import Error
import json
from database import init_tables
from flask_session import Session

app = Flask(__name__)

database = sqlite3.connect("data/database.db")
database.row_factory = sqlite3.Row

SESSION_TYPE = 'memcached'
Session(app)

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


if __name__ == '__main__':
    dbcur = database.cursor()
    init_tables(dbcur)
    database.commit()
    dbcur.close()
    app.run("127.0.0.1", "8000")
